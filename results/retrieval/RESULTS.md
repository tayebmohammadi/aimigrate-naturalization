# Retrieval results

Both methods searched the same 1,696 source-only passages from 57 documents.
Settings and distinct-document metrics were fixed in the [retrieval protocol](../../docs/RETRIEVAL_PROTOCOL.md) before
scoring. The initial 31-question evaluation was executed once, after three training
examples and direct implementation checks; no settings were changed afterward.

| Method | Recall@3 | MRR (all 57 documents) | Source ranked first |
|---|---:|---:|---:|
| BM25 | 29/31 = 0.935484 | 0.859946 | 24/31 |
| MiniLM cosine | 29/31 = 0.935484 | 0.822349 | 22/31 |

BM25 source-rank distribution: 1:24, 2:4, 3:1, 5:1, 8:1.
MiniLM source-rank distribution: 1:22, 2:6, 3:1, 8:1, 29:1.
Both have the same top-three hit count but miss different questions. These results
favor BM25's ordering on this small collection; they do not establish general
superiority or evaluate answer quality.

Failures inspected from saved results:

- Both methods rank the linked source eighth for `qa-9db9beac80a9`, about factors
  an officer should consider concerning an interviewee's understanding. Retrieved
  alternatives cover interview procedures, accommodations, disability exceptions,
  or oath modifications. Broad question wording and overlapping policy topics are
  plausible contributors; generated labels/reference answers need manual review.
- BM25 ranks the linked source fifth for `qa-0b8ea678b7b1`, “To whom does USCIS
  generally issue Certificates of Citizenship?” Its top documents concern closely
  related citizenship/certificate provisions. The source metric counts only the
  one labeled document even if another passage is useful.
- MiniLM ranks the linked source 29th for `qa-830bb1328c81`, “What happens at a
  naturalization ceremony?” It returns Administrative Naturalization Ceremonies,
  General Considerations for All Oath Ceremonies, and Oath Purpose and Background.
  These are topically relevant alternatives; missing the exact linked page should
  not be interpreted as proof that the retrieved evidence is useless.

Training inspection also showed why document metrics are insufficient: for the
military enlistment question, MiniLM finds the right document first but its best
passage ends before the specific physical-presence conditions. Source selection
can succeed while the evidence needed for an answer lies in an adjacent passage.
No settings were adjusted to these findings.

Checks executed: source-only regeneration matched every saved passage; title/URL
and cleaned-text offsets matched all 57 source records; all model inputs fit;
embeddings are finite unit vectors; hand-calculated metrics and exact-tie ordering
passed; long MiniLM input was rejected; a second build reused cached embeddings.
Independent arithmetic from all 62 saved question/method rankings reproduced the
aggregate metrics and verified every top result's provenance. This arithmetic check
did not rerun retrieval or tune settings.

Limitations: 31 generated evaluation questions, one labeled source per question,
known/shared source documents, conservative cleaning with remaining repeated notes,
fixed windows that can cut sentences or separate conditions, and no current-page
or answer correctness validation yet. The frozen initial comparison is retained in
this directory; future reproductions can use a separate output directory.
