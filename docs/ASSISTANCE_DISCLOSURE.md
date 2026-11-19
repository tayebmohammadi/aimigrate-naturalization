# Generative AI and coding assistance disclosure

**Project author: Tayeb Mohammadi.** We used OpenAI Codex to help plan, implement, prepare data, test, organize the repository, and write the documentation and drafts. Its work included project scripts and configuration, the Streamlit app, data and index checks, retrieval tests, model smoke tests, and preparing the fixed answer collection. The saved artifacts document the methods, exact inputs, and results.

The two retrieval methods used pretrained MiniLM for semantic search and BM25 for keyword search. Local Qwen generated the 50 fixed responses from the passages supplied by the selected retriever. The saved app generation check is separate from the fixed evaluation. [Saved responses](../results/answers/responses/) · [App check](../results/app-checks/app_flow_smoke.json)

We reviewed the 20 dataset reference answers against the linked USCIS pages. OpenAI Codex separately verified the relevant passages and surrounding conditions in fresh captures of 16 unique official USCIS pages. Its final verification found 18 references supported as written and two requiring scope clarifications. [Source verification](../results/source-verification/FINAL_VERIFICATION.md)

We read all 50 saved responses. We did not record individual scores or notes during that review. OpenAI Codex separately assessed all 50 saved records against the supplied evidence and verified source material on November 15, 2026. The numerical ratings and recorded case judgments are from that assisted assessment. No model responses were regenerated during the assessment. [Ratings](../results/answers/assessment/ratings.csv) · [Reviewer metadata](../results/answers/assessment/assessment_metadata.json)

Codex also helped trace and redact a client-side configuration value in downloaded USCIS HTML. The published captures are sanitized copies. We checked that the policy text and links stayed the same and kept the exact original captures private.
