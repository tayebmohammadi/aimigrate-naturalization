"""Build the mechanical summary and paired review packet from saved responses. Run with `python -m scripts.prepare_answer_review`; it does not generate answers."""
import csv
import html
import json
from pathlib import Path
import statistics

from answer import validate_response
from retrieval import ROOT, read_jsonl, sha256

PACKET = ROOT/'results/stage5'
OUT = PACKET/'collection'
VALIDATION_FAILURES = {'malformed_output','invalid_citation','invalid_evidence_quote'}


def summary_row(rows, method, kind='all'):
    """Count one method’s saved outcomes and summarize generation times."""
    times = [r['generation_time_seconds'] for r in rows if r['generation_time_seconds'] is not None]
    return {'method':method, 'question_type':kind, 'completed':len(rows),
            'in_scope':sum(r['question_type']=='in_scope' for r in rows),
            'out_of_scope':sum(r['question_type']=='out_of_scope' for r in rows),
            'parsed_answers':sum(r['status']=='answered' for r in rows),
            'model_abstentions':sum(r['status']=='abstained' for r in rows),
            'validation_failures':sum(r['status'] in VALIDATION_FAILURES for r in rows),
            'execution_failures':sum(r['status']=='execution_failure' for r in rows),
            'mean_generation_seconds':statistics.mean(times) if times else None,
            'median_generation_seconds':statistics.median(times) if times else None,
            'timing_n':len(times)}


def card(row):
    """Render one method’s evidence, response, raw output, and blank review fields as escaped HTML."""
    escape = html.escape
    pieces = [f"<section class='method'><h3>{escape(row['method'])}</h3>",
              f"<p>Automatic outcome: <strong>{escape(row['status'])}</strong>. "
              f"Generation time: {row['generation_time_seconds']} s.</p>"]
    if row['status']=='execution_failure':
        pieces.append('<p class="notice">Execution failure, not an abstention: '+escape(row.get('error',''))+'</p>')
    elif row['status'] in VALIDATION_FAILURES:
        pieces.append('<p class="notice">Rejected output, not an evidence-based abstention: '+escape(row.get('validation_error',''))+'</p>')
    elif row['status']=='abstained':
        pieces.append('<p>Model-declared abstention; appropriateness still needs review.</p>')
    pieces.append('<h4>Displayed response</h4><pre>'+escape(row.get('displayed_answer') or '(No accepted displayed answer)')+'</pre>')
    pieces.append('<h4>Citation mapping</h4><ul>')
    for c in row.get('citations',[]):
        pieces.append(f"<li>{escape(c['citation_id'])}: <a href='{escape(c['url'],quote=True)}'>{escape(c['title'])}</a> "
                      f"({escape(c['doc_id'])}, {escape(c['passage_id'])})</li>")
    pieces.append('</ul><h4>Exact evidence supplied</h4>')
    for e in row.get('evidence',[]):
        pieces.append(f"<h5>{escape(e['citation_id'])} {escape(e['title'])}</h5>"
                      f"<p><a href='{escape(e['url'],quote=True)}'>{escape(e['url'])}</a><br>"
                      f"Document: {escape(e['doc_id'])}<br>Passage: {escape(e['passage_id'])}</p>"
                      f"<pre>{escape(e['text'])}</pre>")
    pieces.append('<details open><summary>Raw response (including rejected output)</summary><pre>'+escape(
        row.get('raw_response') if row.get('raw_response') is not None else '(No raw response available)')+'</pre></details>')
    pieces.append('<details><summary>Parsed output / validation</summary><pre>'+escape(
        json.dumps({'parsed_output':row.get('parsed_output'),'validation_outcome':row['validation_outcome']},indent=2,ensure_ascii=False))+'</pre></details>')
    pieces.append('<details><summary>Exact prompt</summary><pre>'+escape(row.get('prompt') or '(Prompt unavailable)')+'</pre></details>')
    pieces.append('<h4>Student ratings — pending</h4><table class="ratings">')
    for label in ['Evidence answerable?','Factual support','Missing conditions/exceptions','Citation relevance',
                  'Readability','Usefulness / addresses question','Outcome / notes','Reviewer / date']:
        pieces.append('<tr><td>'+escape(label)+'</td><td>&nbsp;________________________</td></tr>')
    pieces.append('</table></section>')
    return '\n'.join(pieces)


def main():
    """Build the mechanical summary and paired review packet without loading a model."""
    manifest = json.loads((OUT/'batch_manifest.json').read_text())
    cases = manifest['expected_cases']
    rows = []
    for case in cases:
        path = OUT/'records'/(case['pair_id']+'.json')
        if not path.exists():
            raise ValueError(f'Collection incomplete: missing {case["pair_id"]}')
        row = json.loads(path.read_text())
        assert row['configuration_fingerprint']==manifest['configuration_fingerprint']
        assert all(row[k]==case[k] for k in ('pair_id','qa_id','method','question','question_type'))
        assert row['student_review_status']=='pending'
        if row['status']!='execution_failure':
            check = validate_response(row['raw_response'],row['evidence'],row['completed'])
            assert check['status']==row['status'] and check['displayed_answer']==row['displayed_answer']
        rows.append(row)
    assert len(rows)==len({r['pair_id'] for r in rows})==50
    assert len(list((OUT/'records').glob('*.json')))==50
    (OUT/'responses.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    methods = [summary_row([r for r in rows if r['method']==m],m) for m in ('bm25','minilm')]
    breakdown = [summary_row([r for r in rows if r['method']==m and r['question_type']==k],m,k)
                 for m in ('bm25','minilm') for k in ('in_scope','out_of_scope')]
    for filename, data in [('mechanical_summary.csv',methods), ('mechanical_by_type.csv',breakdown)]:
        with (OUT/filename).open('w',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    events=read_jsonl(OUT/'events.jsonl')
    report={'configuration_fingerprint':manifest['configuration_fingerprint'],
            'expected_pairs':50,'saved_pairs':len(rows),'all_expected_pairs_saved':True,
            'nonempty_raw_responses':sum(bool(r.get('raw_response')) for r in rows),
            'methods':methods,'by_question_type':breakdown,
            'validation_failure_breakdown':{m:{s:sum(r['method']==m and r['status']==s for r in rows)
                                               for s in sorted(VALIDATION_FAILURES)} for m in ('bm25','minilm')},
            'model_load_events':sum(e['event']=='model_loaded' for e in events),
            'generation_started_events':sum(e['event']=='generation_started' for e in events),
            'slow_call_inspections':[e for e in events if e['event']=='slow_call_inspected'],
            'interruptions':[e for e in events if e['event']=='session_interrupted_or_failed'],
            'checkpoint_skips_during_generation':sum(e['event']=='matching_checkpoint_skipped' for e in events),
            'collection_session_seconds':sum(e['elapsed_seconds'] for e in events if e['event']=='session_completed'),
            'timing_definition':'AnswerGenerator.answer wall time includes preparation/tokenization plus generation; excludes model load and retrieval. Raised calls use elapsed attempted call time; pre-generation failures have null timing.',
            'quality_ratings':'pending; answered denotes application-check success only',
            'responses_sha256':sha256(OUT/'responses.jsonl')}
    (OUT/'mechanical_summary.json').write_text(json.dumps(report,indent=2)+'\n')

    # Review material is loaded ONLY after collection, never used by the collector.
    notes={r['qa_id']:r for r in read_jsonl(PACKET/'source_review.jsonl')}
    questions=[]
    for case in cases:
        if case['qa_id'] not in [q['qa_id'] for q in questions]:
            questions.append(case)
    by_pair={r['pair_id']:r for r in rows}
    parts=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Fixed answer evaluation — pending review</title>',
           '<style>body{font:16px/1.5 system-ui,sans-serif;margin:2rem;color:#17212b}article{margin:2rem 0;padding:1rem;border:1px solid #bbc6cf;break-before:page}.pair{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}.method{min-width:0;background:#f6f8fa;padding:1rem}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 system-ui}h5{font-size:1rem;margin-bottom:.4rem}.notice{background:#fff0cf;padding:.8rem}.ratings{border-collapse:collapse;width:100%}.ratings td{border:1px solid #bbb;padding:.5rem}a{color:#085ba7}@media(max-width:900px){.pair{grid-template-columns:1fr}}@media print{details{display:block}body{margin:0}}</style>',
           '<h1>Fixed answer-evaluation review packet</h1>',
           '<p class="notice">Student ratings remain pending. We separately assessed all 50 saved responses; see <a href="../answer_evaluation/ratings.csv">the assisted ratings</a>. An accepted output is not automatically correct. The Stage 5A reference check is separate from this system-answer review.</p>',
           '<p>Use ASSESSMENT_PROTOCOL.md. Review fields are in student_ratings.csv; browser spaces below are for inspection/printing and do not save edits.</p>',
           '<p>Configuration fingerprint: <code>'+html.escape(manifest['configuration_fingerprint'])+'</code></p>']
    for kind,heading in [('in_scope','Twenty in-scope questions'),('out_of_scope','Five additional out-of-scope questions')]:
        parts.append('<h2>'+heading+'</h2>')
        for i,case in enumerate([q for q in questions if q['question_type']==kind],1):
            parts.append(f"<article id='{html.escape(case['qa_id'])}'><h2>{i}. {html.escape(case['qa_id'])}</h2><p><strong>{html.escape(case['question'])}</strong></p>")
            if kind=='in_scope':
                n=notes[case['qa_id']]
                parts.append('<h3>Checked-source note (preliminary Stage 5A)</h3><p>'+html.escape(n['expected_answer_note'])+'</p>')
                parts.append('<p><strong>Essential qualifications:</strong> '+html.escape(n['essential_conditions_or_context'])+'</p>')
                parts.append('<p><strong>Scope/context note:</strong> '+html.escape(n['ambiguity_or_qualification'] or 'No unresolved ambiguity identified at this scope.')+'</p>')
                parts.append(f"<p>Linked document {html.escape(n['source_doc_id'])}: <a href='{html.escape(n['source_url'],quote=True)}'>{html.escape(n['source_title'])}</a>. Relevant current content checked {html.escape(n['current_access_date'])}.</p>")
                parts.append('<details><summary>Original generated dataset reference/span — not an unquestioned gold answer</summary><pre>'+html.escape(n['dataset_reference_answer']+'\n\n'+n['dataset_source_span'])+'</pre></details>')
            else:
                parts.append('<p>Unsupported topic: judge whether the model declines rather than answers from memory. Do not count invalid output/execution failure as an appropriate abstention.</p>')
            parts.append('<div class="pair">'+card(by_pair[case['qa_id']+'__bm25'])+card(by_pair[case['qa_id']+'__minilm'])+'</div></article>')
    parts.append('</html>')
    (OUT/'REVIEW.html').write_text('\n'.join(parts)+'\n')
    # Create the blank template once; keep any later review entries intact.
    ratings=OUT/'student_ratings.csv'
    if not ratings.exists():
        with ratings.open('x') as handle:
            handle.write((PACKET/'rating_template.csv').read_text())
    (OUT/'README.md').write_text('''# Fixed answer collection

This folder holds all 50 saved responses, the exact evidence supplied to the model,
and the raw model outputs. `records/` contains the individual cases;
`responses.jsonl` is the combined export. The collection and its settings are fixed.
Do not run the answer collector again.

Open `REVIEW.html` to inspect the paired evidence and answers. The fields in
`student_ratings.csv` are blank and ready for review. Application checks are
mechanical; they do not establish factual support.

To regenerate only the mechanical summary and review packet, run this from the
project root:

```sh
.venv/bin/python -m scripts.prepare_answer_review
```

This command does not load a model, generate responses, or overwrite existing
review entries. The prompt received only each question and its retrieved source
passages. Reference answers and review notes stayed out of generation.
''')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
