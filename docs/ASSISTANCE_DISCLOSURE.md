# Coding and review assistance disclosure

OpenAI Codex assisted with planning, implementation, data preparation, testing, and
writing across Stages 1–6. It created or edited the project scripts, app, configuration
and documentation; downloaded and inspected the pinned public dataset; prepared the
fixed retrieval and answer collections; and created preliminary review materials.

Current status is summarized in `PROJECT_STATUS.md`; result folders keep the
underlying records. Older stage notes are in the local
`archive/development-history/` folder and are excluded from publication. Checks
include data/schema and hash checks, model smoke checks, retrieval checks,
Streamlit AppTest/server checks, the fixed answer collection, and validation of
the 50 saved records.
Stage 6 included one separately saved real app-generation smoke run
(`results/stage6/app_flow_smoke.json`), absolute-path checks, and preservation
hash checks. This single smoke run is not an additional evaluation case or a factual
quality rating.

During cleanup, coding assistance was used for file organization, documentation,
and verification. One additional AppTest used the same ceremony development question
and made one real Qwen request (65.3 seconds); its separate output is
`results/cleanup_verification_2026-11-15/app_generation_smoke.json`. It is a smoke
check, not another evaluation case or a factual-quality rating.

The 31-question retrieval metrics and 50 generated answers are machine-produced
results. On November 14, 2026, OpenAI Codex (coding assistant) reviewed the 20 fixed
Stage 5A references against their linked USCIS text and context. It saved separate
verdicts, excerpts, qualifications, and seven fresh direct-page captures under
`results/stage5/assisted_reference_verification/`; the web reader had returned 403
and the direct requests returned HTTP 200. Fourteen references were supported as
written and six with scope/context qualifications. This was an assisted review, not
independent student evaluation. On November 14, 2026, the student explicitly
reported reviewing all 20 reference rows and finding them reasonable. The dated
addendum `results/stage5/assisted_reference_verification/STUDENT_REVIEW_ADDENDUM_2026-11-14.md`
records that statement without claiming the student independently visited every
USCIS page or wrote assistant comments. It keeps the assistant's source verification
separate from additional assistant-authored comments; the separate web-reader
checks for those comments returned HTTP 403. The earlier assistant verification
packet records seven direct-curl page captures that returned HTTP 200 and archived
sources for the other reviewed pages. The student's report does not establish
student ratings of generated answers, which remain pending. No Qwen answers were
generated or graded during the reference review.

Final reference verification: On November 15, 2026, OpenAI Codex (coding assistant)
made fresh direct-curl captures for all 16 unique USCIS URLs linked by the selected
20 questions. All returned HTTP 200; the relevant paragraphs and neighboring
context were inspected. The final adjudication counts are 18 supported as written,
two supported with a material scope clarification, and none needing correction or
unverifiable. This narrows the earlier assistant review’s broader six qualifications;
that earlier packet remains preserved. The student reports personally reviewing all
20 question-answer pairs against USCIS and finding them accurate at the level checked.
This is recorded as a student report, without attributing assistant comments or
claiming separate student visits to every page. The final record is
`results/stage5/final_reference_verification_2026-11-15/FINAL_VERIFICATION.md`.
No Qwen generation or review of the 50 generated responses occurred in this step;
answer-quality ratings remain pending.

Saved-response assessment: On November 15, 2026, OpenAI Codex (coding assistant)
reviewed all 50 frozen response records against the exact supplied passages and the
verified reference material. It created `results/stage5/answer_evaluation/ratings.csv`,
metadata, and the summary in `docs/EVALUATION.md`. The assessments are assistant
ratings, not ratings assigned by the student. The original response files and blank
`student_ratings.csv` were preserved. No model was run during this assessment.

Repository organization and documentation were updated with coding assistance.
Before cleanup, retrieval outputs and hashes for frozen questions, settings,
scripts, and results were saved in `results/cleanup_baseline_2026-11-15.json`.
The exact earlier evaluated source snapshot remains in `archive/evaluated_snapshot/`;
current source files are not represented as byte-identical to that snapshot.
Cleanup checks are saved separately under `results/cleanup_verification_2026-11-15/`.

On November 15, 2026, coding assistance also revised reader-facing project prose
and the source/answer review generators to use the project’s voice. The paired HTML
packet’s explanatory text and pending-rating labels were updated; its evidence,
response records, saved ratings, and machine-readable reviewer fields were not
rewritten. The retrieval code and working index fingerprint were not changed.
Pre-edit hashes are in `results/writing_cleanup_baseline_2026-11-15.json`.
