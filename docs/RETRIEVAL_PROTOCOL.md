# Retrieval protocol

We built passages from the 57 filtered USCIS documents. We kept the dataset answers and labeled source excerpts out of passage creation. We used training questions for development checks and kept the settings fixed for the 31 held-out questions.

We used `sentence-transformers/all-MiniLM-L6-v2` at revision
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. It accepts up to 256 tokens including two special tokens. Passages have up to 180 WordPiece content tokens, with about 40 tokens of overlap. The index builder adjusts boundaries to keep words intact and checks token lengths again. MiniLM rejects questions above its limit. Titles are stored as metadata. A title already in the source text stays in that text.

The index builder removes the “Was this page helpful?” footer and navigation blocks of three or more USCIS Policy Manual volume links. It normalizes whitespace and keeps line and paragraph boundaries. It preserves policy notes, footnotes, citations, and short answers that may carry a condition. It removes exact duplicate passages within a document. Matching passages in different documents keep their separate IDs. The index builder records what it removes.

Both methods search the identical saved passage collection:

- BM25Okapi: k1=1.5, b=0.75, epsilon=0.25 (installed rank-bm25). BM25 lowercases words and keeps ASCII letters, digits, and internal hyphens. It keeps numbers, form IDs, and words like “not.” It uses the tokens as written, without adding synonyms.
- MiniLM: MiniLM runs on CPU with float32 values. It normalizes passage and question vectors so their dot product gives cosine similarity. Passage embeddings are built once and reused when
  source bytes, settings, pipeline code, and relevant package versions match.
  The retriever checks hashes so it reads the matching passage and embedding files.

The retriever sorts passages by score, highest first. It breaks exact ties by document ID and passage ID. Each document takes the score of its best passage, which also serves as its evidence. The score orders results. We set no score cutoff for rejecting a result.

Recall@3 is the share of questions where the linked source document is among the top three distinct results. For each question, reciprocal rank is one divided by the linked document’s rank among all 57 documents. It is zero if the document is absent. Mean reciprocal rank (MRR) averages these values across questions. The dataset links one source per question. Other sources may also be relevant.

We checked both methods on three training questions about the purpose of the administrative ceremony, filing N-600 after age 18, and enlistment under INA 329. The checks cover source links, token lengths, normalized vectors, rank calculations, and ties. We then scored the 31 held-out questions without changing the settings. The saved results include full document rankings, top passages, and per-question scores. We found no exact question–answer duplicates between the filtered splits. Both splits could link to the same documents.
