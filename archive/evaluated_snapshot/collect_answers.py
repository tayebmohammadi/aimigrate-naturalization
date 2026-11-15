"""Sequential, checkpointed collection of the fixed Stage 5 answer outputs.

Run again to resume. Completed failures are retained, never automatically retried.
This script deliberately does not read the source-review notes or reference answers.
"""
import datetime
import faulthandler
import fcntl
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import resource
import sys
import tempfile
from threading import Event, Lock, Thread
import time

from answer import AnswerGenerator, MODEL_ID, REVISION, SETTINGS, SYSTEM_PROMPT
from retrieval import INDEX, ROOT, Retriever, read_jsonl, sha256

PACKET = ROOT / 'results/stage5'
OUT = PACKET / 'collection'
RECORDS = OUT / 'records'
REQUESTS = OUT / 'requests'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def save_new(path, value):
    """Durable atomic publication that refuses to overwrite an existing file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)  # FileExistsError protects earlier records.
    finally:
        Path(temporary).unlink(missing_ok=True)


def inputs():
    frozen = json.loads((PACKET / 'frozen_configuration.json').read_text())
    selection = json.loads((PACKET / 'selection_manifest.json').read_text())
    assert MODEL_ID == frozen['model'] and REVISION == frozen['revision']
    assert SETTINGS == frozen['settings']
    assert hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest() == frozen['system_prompt_sha256']
    for name, key in [('answer.py','answer_code_sha256'), ('retrieval.py','retrieval_code_sha256'),
                      ('retrieval_settings.json','retrieval_settings_sha256'),
                      ('data/index/manifest.json','index_manifest_sha256')]:
        assert sha256(ROOT/name) == frozen[key], f'Frozen input changed: {name}'
    assert sha256(PACKET/'selection.jsonl') == selection['selection_sha256']
    assert sha256(PACKET/'out_of_scope.jsonl') == selection['out_of_scope_sha256']
    # Keep only question identity/text. Do not carry expected_behavior/references into inference.
    questions = []
    for filename, kind, count in [('selection.jsonl','in_scope',20), ('out_of_scope.jsonl','out_of_scope',5)]:
        rows = read_jsonl(PACKET/filename)
        assert len(rows) == count
        questions.extend({'qa_id':r['qa_id'], 'question':r['question'], 'question_type':kind} for r in rows)
    cases = [{**q, 'method':m, 'pair_id':q['qa_id']+'__'+m} for q in questions for m in ('bm25','minilm')]
    assert len(cases) == len({c['pair_id'] for c in cases}) == 50
    cached = Path.home()/'.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots'/REVISION
    tokenizer_config = json.loads((cached/'tokenizer_config.json').read_text())
    assert hashlib.sha256(tokenizer_config['chat_template'].encode()).hexdigest() == frozen['chat_template_sha256']
    packages = {n:version(n) for n in ('torch','transformers','tokenizers','sentence-transformers','numpy','rank-bm25')}
    fingerprint_inputs = {
        'frozen_configuration_sha256':sha256(PACKET/'frozen_configuration.json'),
        'selection_sha256':sha256(PACKET/'selection.jsonl'),
        'out_of_scope_sha256':sha256(PACKET/'out_of_scope.jsonl'),
        'collector_code_sha256':sha256(ROOT/'collect_answers.py'),
        'requirements_sha256':sha256(ROOT/'requirements.txt'),
        'index_manifest_sha256':sha256(INDEX/'manifest.json'),
        'python':sys.version, 'packages':packages}
    return frozen, cases, fingerprint_inputs, digest(fingerprint_inputs)


class Progress:
    """Heartbeat/resource inspection only; never alters generation or restarts a call."""
    def __init__(self):
        self.start = time.perf_counter()
        self.state = {'phase':'setup', 'case':'none', 'started':self.start}
        self.completed = 0
        self.stop = Event()
        self.lock = Lock()
        self.thread = Thread(target=self.watch, daemon=True)

    def event(self, kind, **fields):
        row = {'time_utc':now(), 'event':kind, 'pid':os.getpid(), **fields}
        with self.lock, (OUT/'events.jsonl').open('a') as handle:
            handle.write(json.dumps(row, ensure_ascii=False)+'\n')
            handle.flush()
            os.fsync(handle.fileno())

    def phase(self, name, pair):
        self.state = {'phase':name, 'case':pair, 'started':time.perf_counter()}

    def watch(self):
        inspected = set()
        while not self.stop.wait(30):
            state = self.state.copy()
            elapsed = time.perf_counter()-state['started']
            print(f"HEARTBEAT {self.completed}/50 total={time.perf_counter()-self.start:.1f}s "
                  f"{state['case']} {state['phase']}={elapsed:.1f}s", flush=True)
            key = (state['case'], state['phase'])
            if elapsed > 150 and key not in inspected:
                usage = resource.getrusage(resource.RUSAGE_SELF)
                self.event('slow_call_inspected', **state, phase_seconds=elapsed,
                           process_cpu_seconds=usage.ru_utime+usage.ru_stime,
                           max_rss_bytes_macos=usage.ru_maxrss)
                with (OUT/'slow_call_stacks.txt').open('a') as handle:
                    handle.write(f"\n{now()} {state} elapsed={elapsed:.1f}s\n")
                    faulthandler.dump_traceback(file=handle, all_threads=True)
                print('SLOW CALL: resource/stack inspection saved; continuing unchanged.', flush=True)
                inspected.add(key)


def parse_raw(raw):
    if not isinstance(raw, str):
        return None
    text = raw.strip()
    fence = re.fullmatch(r'```(?:json)?\s*(.*?)\s*```', text, flags=re.S | re.I)
    try:
        return json.loads(fence.group(1) if fence else text)
    except json.JSONDecodeError:
        return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    RECORDS.mkdir(exist_ok=True)
    REQUESTS.mkdir(exist_ok=True)
    with (OUT/'batch.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        frozen, cases, fingerprint_inputs, fingerprint = inputs()
        manifest_path = OUT/'batch_manifest.json'
        if not manifest_path.exists():
            save_new(manifest_path, {'created_at_utc':now(), 'configuration_fingerprint':fingerprint,
                                    'fingerprint_inputs':fingerprint_inputs, 'frozen_configuration':frozen,
                                    'expected_cases':cases, 'order':'selection order, BM25 then MiniLM; then five OOS pairs'})
        manifest = json.loads(manifest_path.read_text())
        assert manifest['configuration_fingerprint'] == fingerprint, 'Configuration changed; do not mix collections.'
        assert manifest['expected_cases'] == cases
        expected = {c['pair_id']:c for c in cases}
        completed = {}
        for path in RECORDS.glob('*.json'):
            row = json.loads(path.read_text())
            pair = row['pair_id']
            assert pair in expected and path.name == pair+'.json' and pair not in completed
            assert row['configuration_fingerprint'] == fingerprint, f'Mismatched checkpoint: {pair}'
            assert all(row[k] == expected[pair][k] for k in ('qa_id','question','question_type','method'))
            completed[pair] = row
        print(f'Checkpoint audit: {len(completed)}/50 matching records; {50-len(completed)} pending.', flush=True)
        if len(completed) == 50:
            print('All 50 matching pairs skipped; no generator loaded and no outputs overwritten.', flush=True)
            return
        progress = Progress()
        progress.completed = len(completed)
        progress.event('session_started', resumed_completed=len(completed), fingerprint=fingerprint)
        progress.thread.start()
        try:
            progress.phase('retriever_load', 'startup')
            retriever = Retriever()
            progress.phase('generator_load', 'startup')
            generator = AnswerGenerator()  # Exactly one Qwen constructor for this process/batch.
            assert generator.context_limit == frozen['model_context_limit']
            progress.event('model_loaded', model=MODEL_ID, revision=REVISION, load_seconds=generator.load_seconds)
            for case in cases:
                pair = case['pair_id']
                if pair in completed:
                    progress.event('matching_checkpoint_skipped', pair_id=pair)
                    continue
                request_path = REQUESTS/(pair+'.json')
                base = {**case, 'configuration_fingerprint':fingerprint, 'primary_attempt':True,
                        'started_at_utc':now(), 'raw_response':None, 'displayed_answer':'',
                        'citations':[], 'evidence':[], 'messages':[], 'prompt':None,
                        'generation_time_seconds':None, 'retrieval_time_seconds':None}
                if request_path.exists():
                    previous = json.loads(request_path.read_text())
                    assert previous['configuration_fingerprint'] == fingerprint
                    # A durable start without a result must not be silently generated twice.
                    base.update(previous, status='execution_failure', error_stage='interrupted',
                                error='Previous process ended after a durable start; no completed response available. Not auto-retried.')
                else:
                    stage = 'retrieval'
                    generation_start = None
                    try:
                        progress.phase(stage, pair)
                        started = time.perf_counter()
                        passages = retriever.search(case['question'], case['method'], 3, True)
                        base['retrieval_time_seconds'] = time.perf_counter()-started
                        base['retrieved_passages'] = passages
                        stage = 'prepare'
                        progress.phase(stage, pair)
                        evidence, messages, prompt, prepared = generator.prepare(case['question'], passages)
                        base.update(evidence=evidence, messages=messages, prompt=prompt,
                                    prompt_tokens=prepared['input_ids'].shape[1])
                        del prepared
                        save_new(request_path, base)
                        stage = 'generation'
                        progress.phase(stage, pair)
                        progress.event('generation_started', pair_id=pair)
                        generation_start = time.perf_counter()
                        result = generator.answer(case['question'], passages)
                        base.update(result)
                        base['generation_time_seconds'] = result['runtime_seconds']
                        assert result['evidence'] == evidence and result['prompt'] == prompt
                    except Exception as error:
                        if generation_start is not None:
                            base['generation_time_seconds'] = time.perf_counter()-generation_start
                        base.update(status='execution_failure', error_stage=stage,
                                    error=f'{type(error).__name__}: {error}')
                base.update(finished_at_utc=now(), parsed_output=parse_raw(base['raw_response']),
                            validation_outcome={'status':base['status'], 'error':base.get('validation_error',base.get('error',''))},
                            student_review_status='pending')
                save_new(RECORDS/(pair+'.json'), base)
                completed[pair] = base
                progress.completed = len(completed)
                progress.event('case_saved', pair_id=pair, completed=len(completed),
                               status=base['status'], generation_seconds=base['generation_time_seconds'])
                print(f"SAVED {len(completed)}/50 elapsed={time.perf_counter()-progress.start:.1f}s "
                      f"{pair} {base['status']} generation={base['generation_time_seconds']}", flush=True)
            progress.event('session_completed', completed=len(completed),
                           elapsed_seconds=time.perf_counter()-progress.start,
                           max_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            print('COMPLETE: 50 immutable pair records; factual ratings remain pending.', flush=True)
        except BaseException as error:
            progress.event('session_interrupted_or_failed', error=f'{type(error).__name__}: {error}',
                           completed=len(completed), phase=progress.state)
            raise
        finally:
            progress.stop.set()
            progress.thread.join(timeout=2)


if __name__ == '__main__':
    main()
