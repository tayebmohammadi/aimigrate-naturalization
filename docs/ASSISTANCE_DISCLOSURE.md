# Generative AI and coding assistance disclosure

Tayeb Mohammadi is the project author. OpenAI Codex assisted with planning, implementation, data preparation, testing, repository organization, documentation, and drafting. Its work included project scripts and configuration, the Streamlit app, data and index checks, retrieval tests, model smoke tests, and preparing the fixed answer collection. The saved artifacts document the methods, exact inputs, and results.

The two retrieval methods used pretrained MiniLM for semantic search and BM25 for keyword search. Local Qwen generated the 50 fixed responses from the passages supplied by the selected retriever. The saved app generation check is separate from the fixed evaluation. [Saved responses](../results/answers/responses/) · [App check](../results/app-checks/app_flow_smoke.json)

We reviewed the 20 dataset reference answers against the linked USCIS pages. OpenAI Codex separately verified the relevant passages and surrounding conditions in fresh captures of 16 unique official USCIS pages. Its final verification found 18 references supported as written and two requiring scope clarifications. [Source verification](../results/source-verification/FINAL_VERIFICATION.md)

We manually reviewed all 50 saved model responses without recording individual scores or notes. OpenAI Codex separately assessed all 50 saved records against the supplied evidence and verified source material on November 15, 2026. The numerical ratings and recorded case judgments are from that assisted assessment. No model responses were regenerated during the assessment. [Ratings](../results/answers/assessment/ratings.csv) · [Reviewer metadata](../results/answers/assessment/assessment_metadata.json)

Codex also helped trace and redact a client-side configuration value in downloaded USCIS HTML. The published captures are sanitized copies. The extracted policy text and links were checked for preservation, and the exact original captures are kept privately.
