"""Run selected development cases and save raw model outputs. Run with `python -m scripts.check_answers` from the project root."""
import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

from answer import AnswerGenerator, MODEL_ID, REVISION, SETTINGS, SYSTEM_PROMPT, validate_response
from retrieval import INDEX, ROOT, Retriever, read_jsonl, sha256


def main():
    """Run selected development questions and save raw model responses for later review."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'results/stage4-reproduction')
    parser.add_argument('--cases', nargs='+', help='Optional case labels; omit to run all development cases')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    train = {r['qa_id']: r['question'] for r in read_jsonl(ROOT/'data/processed/official_qa_train.jsonl')}
    supported = train['qa-2b240fd9fef3']
    cases = [
        ('supported_bm25', supported, 'bm25'),
        ('supported_minilm', supported, 'minilm'),
        ('paraphrase', 'Can an Application for Certificate of Citizenship (Form N-600) be filed after age 18?', 'bm25'),
        ('condition', train['qa-ee7c9ee8a613'], 'bm25'),
        ('unrelated', 'How do I bake a chocolate cake?', 'bm25'),
        ('unestablished_conclusion', 'Will my naturalization application definitely be approved?', 'bm25'),
        ('ceremony_bm25', train['qa-555ef18e4ec5'], 'bm25'),
        ('ceremony_minilm', train['qa-555ef18e4ec5'], 'minilm'),
        ('ceremony_paraphrase', 'Why does USCIS hold administrative naturalization ceremonies?', 'bm25'),
    ]
    if args.cases:
        unknown = set(args.cases) - {c[0] for c in cases}
        if unknown:
            parser.error(f'Unknown case labels: {sorted(unknown)}')
        cases = [c for c in cases if c[0] in args.cases]
    # Direct protocol checks: bad references and malformed output are not abstentions.
    dummy = [{'citation_id': '[S1]', 'url': 'https://www.uscis.gov/', 'text': 'Example fact.'}]
    response = lambda ids, quote='Example fact.': json.dumps({
        'status': 'answer', 'answer': 'Example fact.', 'citations': ids, 'quote': quote})
    assert validate_response(response(['[S9]']), dummy)['status'] == 'invalid_citation'
    assert validate_response(response(['[Sfoo]']), dummy)['status'] == 'invalid_citation'
    assert validate_response(response([]), dummy)['status'] == 'invalid_citation'
    assert validate_response(response(['[S1]'], 'Invented quote'), dummy)['status'] == 'invalid_evidence_quote'
    assert validate_response('Unstructured response', dummy)['status'] == 'malformed_output'
    assert validate_response(response(['[S1]']), dummy, False)['status'] == 'malformed_output'
    assert validate_response(json.dumps({'status':'abstain', 'answer':'I cannot verify this from the evidence.',
                                        'citations':[], 'quote':''}), dummy)['status'] == 'abstained'
    retriever = Retriever()
    generator = AnswerGenerator()
    rows = []
    with (args.output/'development.jsonl').open('w') as handle:
        for label, question, method in cases:
            started = time.perf_counter()
            passages = retriever.search(question, method, 3, True)
            retrieval_seconds = time.perf_counter() - started
            try:
                result = generator.answer(question, passages)
            except Exception as error:
                result = {'status': 'generation_error', 'raw_response': None,
                          'displayed_answer': '', 'citations': [], 'error': f'{type(error).__name__}: {error}'}
            row = {'case': label, 'question': question, 'method': method,
                   'retrieval_seconds': retrieval_seconds, 'retrieved_passages': passages, **result,
                   'assessment': 'Pending manual inspection; a valid citation is not proof of support.'}
            handle.write(json.dumps(row, ensure_ascii=False)+'\n')
            handle.flush()
            rows.append(row)
            print(label, result['status'], round(result.get('runtime_seconds',0),2),
                  repr(result['raw_response']), flush=True)
    summary = {'model': MODEL_ID, 'revision': REVISION, 'settings': SETTINGS,
               'system_prompt': SYSTEM_PROMPT, 'model_load_seconds': generator.load_seconds,
               'max_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'index_manifest_sha256': sha256(INDEX/'manifest.json'),
               'answer_code_sha256': sha256(ROOT/'answer.py'),
               'check_code_sha256': sha256(ROOT/'scripts/check_answers.py'),
               'prompt_sha256': hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
               'protocol_checks_passed': True, 'development_runs': len(rows),
               'note': 'Development only; not the later 20-question answer or five-question out-of-scope evaluation.'}
    (args.output/'development_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
