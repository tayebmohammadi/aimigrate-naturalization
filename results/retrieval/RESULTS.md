# Retrieval results

Both methods searched 1,696 passages from the same 57 USCIS documents. We checked three training examples, then scored the 31 held-out questions. We kept the [retrieval settings](../../docs/RETRIEVAL_PROTOCOL.md) fixed.

| Method | Recall@3 | MRR (all 57 documents) | Source ranked first |
|---|---:|---:|---:|
| BM25 | 29/31 = 0.935484 | 0.859946 | 24/31 |
| MiniLM cosine | 29/31 = 0.935484 | 0.822349 | 22/31 |

BM25 source-rank distribution: 1:24, 2:4, 3:1, 5:1, 8:1.
MiniLM source-rank distribution: 1:22, 2:6, 3:1, 8:1, 29:1.
Both methods had the same top-three hit count. They shared one miss and each had one other miss. BM25 had higher MRR on this set. That metric gives more weight to ranks near the top.

## What we found in the rankings

- Both methods rank the linked source eighth for `qa-9db9beac80a9`, about factors
  an officer should consider concerning an interviewee's understanding. Retrieved
  alternatives cover interview procedures, accommodations, disability exceptions,
  or oath modifications. Broad question wording and overlapping policy topics are
  plausible contributors.
- BM25 ranks the linked source fifth for `qa-0b8ea678b7b1`, “To whom does USCIS
  generally issue Certificates of Citizenship?” Its top documents concern closely
  related citizenship/certificate provisions. The source metric counts only the
  one labeled document even if another passage is useful.
- MiniLM ranks the linked source 29th for `qa-830bb1328c81`, “What happens at a
  naturalization ceremony?” It returns Administrative Naturalization Ceremonies,
  General Considerations for All Oath Ceremonies, and Oath Purpose and Background.
  These cover the right topic. The scoring rule gives credit only for the linked page.

In a training example about military enlistment, MiniLM ranked the linked document first. Its best passage ended before the physical-presence conditions the question asked about. Finding the document and finding the sentence that answers the question are separate steps.

We verified that rebuilding the source passages matched the saved text and source links. The checks also confirmed that the passages fit MiniLM, the embeddings are finite unit vectors, and the retriever handles ties and rejects overlong MiniLM questions. We recalculated the metrics from all 62 saved question–method rankings.

The 31 questions came from a generated dataset with one linked source per question. The fixed passage windows can cut off conditions, and the cleaned text still contains some repeated notes. This test measures document ranking on a saved copy of the sources. See the [answer evaluation](../../docs/EVALUATION.md) and [reference verification](../source-verification/FINAL_VERIFICATION.md) for the checks of draft quality and source content.
