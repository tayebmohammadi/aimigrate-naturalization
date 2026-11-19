# Evaluation

## Retrieval

We preserved the dataset’s original splits and evaluated both methods on 31 held-out naturalization questions. The expected source was each dataset row’s linked USCIS document ID. Both methods ranked that source in the top three on 29/31 questions. Mean reciprocal rank was 0.860 for BM25 and 0.822 for MiniLM. Another relevant page can answer a question without earning credit under this metric. [Retrieval results and examples](../results/retrieval/RESULTS.md) · [Per-question ranks](../results/retrieval/per_question.csv)

## Draft answers

We sampled 20 of the held-out questions and added five out-of-scope questions. Each question went through both retrieval methods with the same Qwen generator and instructions, producing 50 saved responses. We read all 50 in a manual review and did not record individual scores or notes. We separately checked the 20 selected dataset reference answers against their linked USCIS pages. The final Codex source verification found 18 supported as written and two with scope clarifications. [Reference verification](../results/source-verification/FINAL_VERIFICATION.md)

The table summarizes the separate assisted assessment by OpenAI Codex. The supported useful answers are a subset of the drafts accepted by the app. The app checks format, citation IDs, and quote presence. The assisted assessment checks support for the displayed claims.

| Selected outcomes | BM25 + Qwen | MiniLM + Qwen |
|---|---:|---:|
| Naturalization drafts accepted by the app | 8/20 | 5/20 |
| Naturalization drafts rated supported and useful | 7/20 | 3/20 |
| Naturalization questions declined | 6/20 | 3/20 |
| Naturalization outputs that failed validation | 6/20 | 12/20 |
| Out-of-scope questions appropriately declined | 5/5 | 5/5 |

One BM25 decline on a naturalization question was appropriate. Both methods declined the same five out-of-scope questions. This small set gives limited evidence about questions near the boundary of the collection. [Assessment protocol](../results/answers/ASSESSMENT_PROTOCOL.md) · [Ratings and reasons](../results/answers/assessment/ratings.csv) · [Reviewer metadata](../results/answers/assessment/assessment_metadata.json)

The [paired examples](../results/answers/responses/) include unsuccessful outputs. For the motion-to-reopen deadline, BM25 retrieved the 15-day rule, but the app rejected Qwen’s changed quote. MiniLM retrieved a passage without the rule, produced a raw 30-day answer, and hit the token limit. The app accepted neither draft. For the civics-test question, both methods retrieved the cutoff and Qwen still declined both times.
