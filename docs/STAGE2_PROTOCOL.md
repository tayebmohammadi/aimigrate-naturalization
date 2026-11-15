# Stage 2 retrieval protocol — fixed before held-out scoring

Collection: the 57 source records already verified in Stage 1. Neither QA answers
nor QA source spans are inputs to passage creation. All 31 official evaluation
questions are held out; use only selected training questions for implementation
checks. Do not change these settings after observing held-out results.

The cached model `sentence-transformers/all-MiniLM-L6-v2`, revision
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, reports max_seq_length=256 and two
special tokens. Use up to 180 content WordPiece tokens and approximately 40 tokens
of overlap, adjusting boundaries to avoid splitting whitespace-delimited words.
Check the token count of each actual substring again including special tokens;
raise an error instead of silently truncating passages or long MiniLM questions.
Titles remain metadata, not extra text prepended to embeddings. The source title
already present in a document's original text remains part of that text.

Cleaning removes the recognized “Was this page helpful?” feedback footer and
contiguous blocks of at least three numbered USCIS Policy Manual volume-navigation
links. Normalize whitespace but retain line/paragraph boundaries. Do not delete
policy notes, appendices, footnotes, isolated citations, or short “Yes”/“No” lines
that might be part of substantive conditions or tables. Exact duplicate passage
text is removed only within a document. Identical passages in different documents
keep their separate document IDs and provenance. Save an audit for each document.
Remaining boilerplate and historical notes are an acknowledged conservative choice.

Both methods search the identical saved passage collection:

- BM25Okapi: k1=1.5, b=0.75, epsilon=0.25 (installed rank-bm25). Lowercase and
  extract ASCII letter/digit tokens with internal hyphens; no stopword removal,
  stemming, or synonym expansion. Keep numbers, form identifiers, and negation.
- MiniLM: CPU, float32, normalized passage and question embeddings; dot products
  are cosine similarities. Passage embeddings are built once and reused when
  source bytes, settings, pipeline code, and relevant package versions match.
  Artifact hashes check passage/embedding alignment. Use the existing model cache.

Passages sort by descending score, then ascending document ID and passage ID for
exact ties. A document's score is its maximum passage score. Rank distinct document
IDs using the same order; retain the best passage as evidence. Scores are ranking
values, not answer-confidence probabilities. No rejection threshold is fitted.

Recall@3 = fraction of questions whose linked source_doc_id is among the top three
distinct documents. Full-collection MRR = mean of 1/rank of that linked source among
all 57 distinct documents (zero if absent). There is one labeled relevant source
per QA; other sources could still be relevant. Passage-level support is inspected
separately; these source metrics do not verify an answer.

Development checks use the selected training questions about the overall purpose
of the administrative ceremony, filing N-600 after age 18, and enlistment conditions
under INA 329. The proposal's exact “What happens at a naturalization ceremony?”
example is not in the selected training subset; use an actual ceremony QA instead.
Save each method's top three distinct sources and full best passages, plus direct
checks of provenance, token lengths, unit embeddings, metric arithmetic, and ties.
Record this protocol and the successful training-check fingerprint before scoring.

Then score the same 31 evaluation questions once for the initial comparison, with
no tuning afterward. Save full document ranks, top evidence passages, per-question
scores, summary metrics, and hashes of settings, protocol, code, index, and QA file.
Later reruns reproduce the fixed experiment rather than selecting better settings.
Training QA duplicates remain unchanged; there are no exact train/eval QA duplicates
in this subset. Shared source documents are expected for this fixed-corpus task.
Manual current-page checking, answer evaluation, five out-of-scope refusal tests,
answer generation, and Streamlit remain future work.
