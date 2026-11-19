# Saved answer responses

The [combined export](responses.jsonl) contains all 50 fixed responses in evaluation order. Each [individual record](records/) includes the question, exact evidence and prompt, raw model text, displayed result, and validation status. The [request records](requests/) preserve the corresponding inputs.

For paired examples, compare the two records with the same question ID.

| Example | BM25 + Qwen | MiniLM + Qwen |
|---|---|---|
| Motion to reopen deadline | [Record](records/qa-b941678d80de__bm25.json) | [Record](records/qa-b941678d80de__minilm.json) |
| Military-service exemption | [Record](records/qa-210bd866a25c__bm25.json) | [Record](records/qa-210bd866a25c__minilm.json) |
| Civics test cutoff | [Record](records/qa-5c7a593817d2__bm25.json) | [Record](records/qa-5c7a593817d2__minilm.json) |
| Oath history | [Record](records/qa-c9e78deeb174__bm25.json) | [Record](records/qa-c9e78deeb174__minilm.json) |

The [assessment ratings](../assessment/ratings.csv) distinguish factual support from application acceptance. The saved records keep their original fields, paths, and fingerprints for provenance.
