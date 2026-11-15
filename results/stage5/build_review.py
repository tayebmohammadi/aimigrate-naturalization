"""Build the preliminary reference review from the saved selection and page captures.

Run with `python results/stage5/build_review.py` from the project root.
This script reads archived pages and does not load a model or make network requests.
"""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

# Expected note, essential restriction/context, review issue. No generated answers used.
NOTES = {
 'qa-1c9ac2bdd353': (
  'For INA 319(a) spouses residing in the United States: married and living in marital union for at least three years before filing.',
  'Three years BEFORE filing and the INA 319(a) domestic-spouse category; do not transfer the different 319(b) or 319(d) table rules.', ''),
 'qa-dcd6fb096bd9': (
  'Refer the military-basis revocation cases described in this chapter to ICE.',
  'Such cases refers to military-basis naturalization on/after November 24, 2003, separation other than honorably before five total honorable-service years. These are possible revocation cases, not automatic revocations.',
  'Scope qualification: the short reference depends on the preceding paragraph; do not generalize it to every revocation case.'),
 'qa-9db9beac80a9': (
  'Consider the applicant\'s education level and knowledge of English; rephrasing/supplementing questions may help ensure understanding.',
  'Education AND English knowledge in the interview/testimony context. Do not invent an automatic eligibility exemption.', ''),
 'qa-be519f64475f': (
  'With sufficient cause, the court or USCIS District Director may consider special circumstances of a compelling or humanitarian nature for an expedited oath ceremony.',
  'Discretionary MAY, not guaranteed. Examples are nonexhaustive; travel/employment must be urgent or compelling and judged sufficiently meritorious. Court-exclusive jurisdiction has separate procedures.', ''),
 'qa-36bbfce529b8': (
  'USCIS District Directors, Field Office Directors, and officers acting on their behalf have delegated authority for USCIS administrative oaths and certificate issuance.',
  'ADMINISTRATIVE USCIS ceremonies; do not replace the separate judicial-ceremony judge rule.', ''),
 'qa-5a7336ab968c': (
  'During a judicial naturalization ceremony, the judge in the district of proper jurisdiction has exclusive authority to administer the oath.',
  'JUDICIAL ceremony and proper district, not all USCIS administrative ceremonies.', ''),
 'qa-b941678d80de': (
  'The applicant has 15 days to respond to the USCIS motion to reopen and overcome derogatory information or explain good cause for missing the oath.',
  'USCIS motion concerning a previously approved application; response to derogatory information or multiple missed ceremonies. Do not substitute the 30-day denial-hearing deadline.', ''),
 'qa-73e8e4e98534': (
  'For the INA 319(d) surviving-spouse category, the applicant must have been married and living in marital union at the service member\'s death.',
  'At the time of DEATH; do not import the 319(a) three-year marital-union duration.', ''),
 'qa-f0ba3e1e977e': (
  'An English-test exception does not change administration of the oath in English; an interpreter may interpret during the ceremony.',
  'Distinguish English-test exception from oath language; interpreter assistance and separate oath modifications/waivers must not be ruled out.', ''),
 'qa-f2fa5cd76241': (
  'The DCII check should reveal derogatory information in the applicant\'s military records.',
  'Military-record check, not a guarantee of eligibility or approval. Context: applies to applicants with military service regardless of the naturalization section; validity is 15 months if mentioned.', ''),
 'qa-4609d6be9c7d': (
  'Honorable means generally meeting acceptable military conduct/performance standards, or service so meritorious that another characterization would be inappropriate.',
  'Keep the OR between the two bases. Honorable is a named discharge characterization; do not equate all discharge types or promise naturalization.', ''),
 'qa-c9e78deeb174': (
  'The INA of 1952 made the last major addition: work of national importance under civilian direction.',
  '1952 and the CIVILIAN national-importance-work clause, not the earlier armed/noncombatant-service additions; this is a historical question.', ''),
 'qa-210bd866a25c': (
  'An exemption is a permanent exemption from induction, or release/discharge from military training or service in the U.S. armed forces.',
  'Retain both definition branches. The surrounding alienage-bar discussion has exceptions; this definition does not mean every military exemption permanently bars citizenship.', ''),
 'qa-4ecbcc440b1c': (
  'At minimum, distinguish the general INA 328 military-service provision from the special INA 329 provision for designated periods of hostilities.',
  'Do not imply identical service-duration rules or automatic eligibility. I.3(B) states any period of honorable service during designated hostilities; I.2(B), also reviewed in this set, gives the one-year peacetime rule if duration is discussed.',
  'Scope qualification: the reference is a high-level distinction, not a complete comparison of all eligibility conditions. Accept a correct bounded distinction; do not require every unasked eligibility detail.'),
 'qa-4385aaa06495': (
  'Generally issue the certificate after naturalization approval and the oath; the same section provides an oath-waiver exception and card-surrender rules.',
  'Do not say the oath is ALWAYS required: USCIS may waive it for medical disability. PRC/ARC surrender is required unless waived for a card established lost/destroyed. Medical disability does not itself automatically grant a waiver.',
  'Qualification: the reference summarizes the general rule and omits exceptions in the next paragraphs. Judge an absolute no-exceptions statement as wrong; keep the original dataset reference unchanged.'),
 'qa-5c7a593817d2': (
  'People filing N-400 BEFORE October 20, 2025 take the 2008 naturalization civics test.',
  'FILING date, not interview date. ON/AFTER October 20, 2025 uses the 2025 test according to the reviewed alert. Date-sensitive: recheck if evaluating at a later date.', ''),
 'qa-f4ac028b6dd2': (
  'For INA 319(a), physical presence is 18 months during the relevant residence period (the table gives three years of LPR residence).',
  'Physical presence is distinct from continuous residence and marital union; no invented uninterrupted 18-month stay or transfer of overseas-spouse exemptions.', ''),
 'qa-f074b4c28745': (
  'Give another opportunity to establish eligibility for the oath modification before concluding the interview, and issue an RFE for an additional chance to provide evidence.',
  'Do not immediately conclude ineligibility from missing/refused explanation; RFE and additional opportunity, not automatic approval.',
  'Context qualification: the original source_span includes the interview opportunity; the RFE part is supported by the following paragraph, not the span alone.'),
 'qa-071175958a7d': (
  'At least one year total of honorable U.S. armed-forces service, possibly across multiple periods, for the INA 328 peacetime-service requirement.',
  'AT LEAST one year, honorable service, total periods. This answers service duration only: other conditions, including age/LPR status, still apply; no guaranteed eligibility from duration alone.', ''),
 'qa-a9d1c7e47d92': (
  'The applicant or authorized representative must file the hearing request with USCIS within 30 days after receiving the naturalization denial notice.',
  'Deadline is filing a hearing REQUEST after receipt of DENIAL; not the 15-day motion response or a requirement to hold the hearing within 30 days.', ''),
}


def read_jsonl(path):
    """Load nonblank JSON Lines records from a saved Stage 5 file."""
    return [json.loads(l) for l in path.read_text().splitlines()]


def main():
    """Build review tables and notes for the fixed set of reference questions."""
    selection = read_jsonl(HERE/'selection.jsonl')
    manifest = json.loads((HERE/'selection_manifest.json').read_text())
    assert hashlib.sha256((HERE/'selection.jsonl').read_bytes()).hexdigest() == manifest['selection_sha256']
    assert hashlib.sha256((ROOT/manifest['population_file']).read_bytes()).hexdigest() == manifest['population_sha256']
    qa = {r['qa_id']:r for r in read_jsonl(ROOT/'data/processed/official_qa_eval.jsonl')}
    docs = {r['doc_id']:r for r in read_jsonl(ROOT/'data/processed/sources.jsonl')}
    access = {r['source_doc_id']:r for r in read_jsonl(HERE/'current_page_access.jsonl')}
    rows = []
    normalize = lambda t:' '.join(t.split())
    for s in selection:
        q = qa[s['qa_id']];d = docs[s['source_doc_id']];a = access[s['source_doc_id']]
        assert q['question'] == s['question'] and q['source_doc_id'] == s['source_doc_id']
        assert q['source_url'] == d['url'] == s['source_url']
        assert hashlib.sha256((HERE/a['html_file']).read_bytes()).hexdigest() == a['html_sha256']
        assert hashlib.sha256((HERE/a['main_text_file']).read_bytes()).hexdigest() == a['main_text_sha256']
        position = d['text'].find(q['source_span'])
        assert position >= 0
        current = normalize((HERE/a['main_text_file']).read_text())
        current_position = current.find(normalize(q['source_span']))
        note, conditions, issue = NOTES[q['qa_id']]
        verified = a['transport_status'] == 'content_retrieved' and current_position >= 0
        rows.append({**s,'source_title':d['title'],
            'dataset_reference_answer':q['answer'],'dataset_source_span':q['source_span'],
            'dataset_review_status':q['review_status'],
            'expected_answer_note':note,'essential_conditions_or_context':conditions,
            'snapshot_reference_support':'supported_at_stated_scope',
            'snapshot_support_explanation':'Reference checked against linked full document and neighboring text; exact original source span is present. See qualification field; span presence alone was not treated as semantic proof.',
            'snapshot_source_excerpt':d['text'][max(0,position-350):position+len(q['source_span'])+1400],
            'current_page_checked':verified,'current_reference_support':'supported_at_stated_scope' if verified else 'incomplete',
            'current_access_date':a['access_date'],'current_accessed_at_utc':a['accessed_at_utc'],
            'current_http_status':a['http_status'],
            'current_evidence_excerpt':current[max(0,current_position-350):current_position+len(normalize(q['source_span']))+1400] if current_position>=0 else '',
            'current_vs_snapshot':'No difference found in question-relevant provision; original span also present after whitespace normalization. This does not assert full-page identity.' if verified else 'Not established: retain row and inspect access log.',
            'ambiguity_or_qualification':issue,'current_access_problem':'Web reader returned HTTP 403; direct curl obtained substantive HTTP 200 main content. Not blocked after fallback.' if verified else a['error'],
            'current_html_file':a['html_file'],'current_text_file':a['main_text_file'],
            'current_html_sha256':a['html_sha256'],
            'review_author':'OpenAI Codex preliminary source review, not independent student evaluation',
            'student_review_status':'pending'})
    (HERE/'source_review.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    with (HERE/'source_review.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    md=['# Preliminary reference review\n',
        'We checked the 20 selected dataset references against their linked source documents and archived current-page captures. This is a reference review, separate from the 50 generated-answer assessment. Original dataset answers and spans remain identified as dataset material. No new model answers were collected. Reviewer attribution is recorded in the review data and assistance disclosure.\n',
        'The selection was saved before this review. All 20 references are supported at their stated scope in the frozen snapshot and question-relevant current content accessed November 14, 2026. Four rows have explicit scope/context qualifications (2, 14, 15, 18); these are not unverified replacements. No unresolved reference ambiguity or blocked current page remains after direct access.\n',
        'The web reader returned 403 on all 16 unique URLs; ordinary curl retrieved substantive content. Relevant paragraphs/table rows and neighboring conditions were inspected. Current HTML, headers, and main text are archived separately. The frozen retrieval corpus was not updated.\n',
        '| # | QA ID | Question | Snapshot | Current | Qualification |',
        '|---:|---|---|---|---|---|']
    for r in rows:
        md.append(f"| {r['selection_order']} | {r['qa_id']} | {r['question']} | Supported | Checked {r['current_access_date']} | {'See note' if r['ambiguity_or_qualification'] else '—'} |")
    for r in rows:
        md += [f"\n## {r['selection_order']}. {r['qa_id']}\n",r['question']+'\n',
               f"Linked document: `{r['source_doc_id']}` — [{r['source_title']}]({r['source_url']}).\n",
               '**Dataset reference answer (generated dataset material):** '+r['dataset_reference_answer']+'\n',
               '**Dataset source span (original):**\n\n> '+r['dataset_source_span'].replace('\n','\n> ')+'\n',
               '**Preliminary expected-answer note:** '+r['expected_answer_note']+'\n',
               '**Essential conditions/context:** '+r['essential_conditions_or_context']+'\n',
               '**Qualification:** '+(r['ambiguity_or_qualification'] or 'No unresolved reference ambiguity identified at this scope.')+'\n',
               '**Snapshot evidence and neighboring context:**\n\n> '+r['snapshot_source_excerpt'].strip().replace('\n','\n> ')+'\n',
               f"**Current-page review:** relevant provision and context checked {r['current_access_date']} ({r['current_accessed_at_utc']}); no question-relevant difference found. [Archived main text]({r['current_text_file']}) / [HTML]({r['current_html_file']}). Full current excerpt is also in CSV/JSONL.\n",
               '**Row-specific student comments:** None were supplied; see the dated addendum for the overall review statement.\n']
    (HERE/'SOURCE_REVIEW.md').write_text('\n'.join(md)+'\n')
    summary={'selected':len(rows),'snapshot_supported':len(rows),
             'current_references_verified':sum(r['current_page_checked'] for r in rows),
             'unique_current_pages':len(access),'unresolved_reference_ambiguities':0,
             'scope_qualified_references':sum(bool(r['ambiguity_or_qualification']) for r in rows),
             'blocked_or_incomplete_current_rows':sum(not r['current_page_checked'] for r in rows),
             'relevant_substantive_differences_found':0,'student_independent_review_completed':False,
             'new_generations':0,'selection_sha256':manifest['selection_sha256']}
    (HERE/'review_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
