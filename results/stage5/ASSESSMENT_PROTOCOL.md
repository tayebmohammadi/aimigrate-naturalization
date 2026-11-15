# Frozen preliminary answer-assessment protocol — Stage 5A

This stage prepared sources, not model answers or completed student ratings.
The source notes were drafted by OpenAI Codex after reading the saved and current
official text. They are a documented preliminary review for the student to inspect,
not an independent human evaluation already completed by the student.

## Population and selection

Use the 20 IDs in selection.jsonl, saved before current-page review/new answers.
Sampling: Python 3.11 random.Random(72).sample over the 31 official evaluation
records sorted by qa_id, k=20; retain sample order. The population/selection hashes
and IDs are in selection_manifest.json. No alternate seeds, difficulty filtering,
or replacement based on likely model performance was used. Preserve all rows even
if a reference becomes unverifiable. The 31 questions were already used for Stage 2
retrieval scoring; this is a subset for answer evaluation, not a new retrieval test.

No selected ID or normalized exact question appears as a generation input in saved
Stage 4 records; check_answers.py uses training questions and development paraphrases.
Related topics and source documents overlap, so do not describe this as topic- or
document-disjoint. A saved-record audit establishes recorded input overlap, not a
claim that nobody has ever seen any evaluation question.

Five additional fixed questions are in out_of_scope.jsonl: networking, pediatric
medication, stock prediction, Canadian immigration procedure, and bicycle repair.
They are distinct from development questions, especially the cake and personal
naturalization-approval cases. Expected behavior is an explicit evidence-based
decline, not an answer from model memory or irrelevant USCIS citations. Retain any
unexpected evidence or ambiguity; do not replace a question after seeing output.

## Source-review use

Inspect SOURCE_REVIEW.md and the self-contained source_review.csv/JSONL. Dataset
answers/spans are original generated dataset material; they are not an unquestioned
gold standard. Expected notes and qualifications use full linked source context.
In particular, a real span/citation alone cannot establish that a whole answer is
correct. The RFE reference uses the next paragraph; the certificate general rule
has explicit waiver/card exceptions; the military comparison is intentionally broad.

All 20 relevant provisions were found in both the frozen snapshot and current
official pages accessed November 14, 2026; 16 unique pages are archived. Web-reader
requests returned 403, while ordinary curl obtained substantive content. Relevant
text/table context was read; success is not inferred from HTTP 200 alone. No relevant
substantive difference was found; this is not a claim of full-page identity or
permanent legal currency. Four references have context/scope qualifications; no
unresolved reference ambiguity remains at their stated scope. Student confirmation
is still pending for every row.

If the student discovers a mismatch, revise a versioned expected note with reason,
date, and evidence; keep the original reference and selected ID. Do not update the
frozen retrieval corpus. If later current-page access fails, mark currentness
unassessable separately from snapshot-based answer support. Never silently exclude
an inconvenient reference or call an inaccessible page verified.

## Later comparison: no batch started here

Use the SAME frozen generator/prompt/settings in frozen_configuration.json on BOTH
methods' evidence for each of the same 20+5 questions: 40 in-scope and 10 additional
out-of-scope generations, **50 total**. Use the unchanged shared Retriever and
answer.py evidence rule, caching one generator and retriever in a sequential CPU
process. Record IDs, method, actual supplied passages, complete prompt, raw/displayed
response, automatic status, citations, quote, completion, and runtime.

DO NOT put dataset answers, source spans, expected notes, or current-page review
excerpts in generation inputs. They are assessment material only. No prompt/model
tuning, best-of selection, or question replacement after viewing evaluation output.
Use the first attempt for primary reporting. Log infrastructure retries separately
without silently replacing the original failure. A later changed system is a new
experiment, not an overwrite of this baseline.

Before judging a response, separately mark whether that method's actually supplied
passages can answer the question: yes/no/uncertain, with passage IDs and a reason.
The linked full source being adequate does not mean the retrieved excerpts are.
Inspect factual content, not the method's name or retrieval score. Student ratings
must record reviewer/date; initial rating_template.csv fields are intentionally blank.

## Human assessment dimensions

Score each substantive response 0/1/2; allow N/A only where truly inapplicable and
record why. Do not convert automatic `answered` into a human success label.

| Dimension | 2 | 1 | 0 |
|---|---|---|---|
| Factual support | All material claims supported by supplied passages and consistent with reviewed source | Partly supported; minor gap/inaccuracy | Central unsupported/contradictory claim, wrong form, number, date, or legal conclusion |
| Citation relevance | Cited passages support the claims; adequate coverage | Some relevant citation but incomplete coverage | Missing, irrelevant, or misleading references; a valid ID is insufficient |
| Addresses question | Direct, adequate answer at the question's scope | Useful but partial, indirect, or distracted | Non-answer, wrong question, contradiction, or irrelevant information |
| Conditions/exceptions | Preserves restrictions essential to the requested answer | Some preserved, with a limited omission | Omission/change makes a material permission, prohibition, or eligibility assertion misleading |
| Plain-English readability | Clear, concise, familiar wording | Understandable but long, technical, or awkward | Confusing, contradictory, unreadable, or irrelevant verbosity |

Require only conditions whose omission changes the requested answer; do not demand
every unasked eligibility detail. Preserve may/must/not, before/after, form identity,
and category distinctions. Record sentence-count compliance separately: the prompt
requests two/three short sentences, but one clear sentence is not a factual error.

## Outcomes and denominators

Assign one primary outcome per attempt, with notes:

- Supported useful answer: fully supported, relevant citations, answers the question,
  essential conditions retained. Readability is reported separately.
- Partially supported answer: useful material but incomplete support/coverage/conditions.
- Incorrect/unsupported answer: material false, contradictory, irrelevant, or invented claim.
- Appropriate abstention: actually declines because supplied evidence cannot establish
  an answer; no unsupported conclusion smuggled into the decline. Model status alone
  does not prove this. For in-scope cases this may expose retrieval-context failure.
- Unnecessary abstention: supplied evidence does establish an answer but the model declines.
- Malformed/incomplete output, invalid citation/quote, or execution failure: separate
  technical outcomes, NEVER credited as evidence-based abstention. Inspect raw output
  for diagnostic factual behavior, but do not pretend a rejected answer was displayed.
- Unassessable reference/evidence: genuine unresolved review problem; retain ID/reason.

Primary in-scope useful-answer rate is supported useful answers / **20 per method**.
All selected questions remain in that denominator: abstentions and technical failures
are not useful-answer successes. Report outcome counts summing to 20, partial and
incorrect answers separately, and currentness/unassessable flags. If unresolved
references require a supplementary verifiable-only rate, list excluded IDs and its
explicit denominator alongside the full-20 results; do not quietly change N.
Do not label an answer factually wrong merely because its reference is unassessable;
report that uncertainty. It cannot earn verified-useful credit without verification.

Out-of-scope correct-abstention rate is appropriate abstentions / **5 per method**;
malformed outputs, loading errors, and incorrect answers stay in N=5 and earn no
abstention credit. Do not pool these with the 20 in-scope questions as one accuracy.

Also report conditional support/citation/readability distributions among displayed
substantive drafts, with their explicit applicable N. N/A abstentions/errors must
not inflate those conditional scores; keep unconditional delivery rates beside them.
An appropriate abstention on unanswerable retrieved context is safe behavior but
still not successful answer delivery for an answerable in-scope question. Report
both facts rather than rewarding a system that declines everything.

## Runtime estimate and artifacts

Saved Stage 4 direct-case means: 50.61 s in-scope and 19.88 s unsupported. For
40+10 generations this is about **37 minutes**, plus model load (~12 s), retrieval,
and I/O. The real-app timings imply about **52 minutes**. Plan roughly **40–65
minutes**, potentially longer for long outputs/memory pressure; this is not a bound.
runtime_estimate.json records the inputs and calculation. No timing/generation
experiment was run for Stage 5A.

Inspection starts with SOURCE_REVIEW.md, ASSESSMENT_PROTOCOL.md, and selection.jsonl.
Review CSV/JSONL and archived current_pages provide detailed evidence; frozen config
and VERIFICATION_RESOLUTION.md resolve the baseline. rating_template.csv is an empty
50-row skeleton, NOT completed assessments. fetch_current_sources.py archives pages;
build_review.py regenerates preliminary review outputs from saved evidence without
network/model use. Student edits/ratings should be saved separately before regenerating
the assistant's preliminary table. No model batch launcher is added in this stage.
