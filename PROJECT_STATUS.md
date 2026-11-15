# Project status

The local prototype searches official USCIS naturalization sources with BM25 or MiniLM and drafts a cited answer with local Qwen. See [README.md](README.md) to install and launch it, and [docs/REPRODUCE.md](docs/REPRODUCE.md) for data and evaluation commands.

## Saved results

- Retrieval index: 57 documents and 1,696 source-only passages. Both methods reached Recall@3 of 29/31; MRR was 0.859946 for BM25 and 0.822349 for MiniLM. See `results/stage2/`.
- Answer assessment: 50 fixed outputs are preserved in `results/stage5/collection/`; assisted ratings are summarized in [docs/EVALUATION.md](docs/EVALUATION.md). Student ratings remain pending.
- Dataset reference check: all 20 selected references were checked separately against linked USCIS pages; the final verification is in `results/stage5/final_reference_verification_2026-11-15/`.
- App smoke check: one saved generation completed with MiniLM and returned `answered`; see `results/stage6/app_flow_smoke.json`. This checks app flow, not answer quality.

## Limits and next steps

The app uses a downloaded USCIS snapshot, which may be out of date. Local CPU generation took about 65–73 seconds on the tested 16 GB Intel Mac, with swap already in use. Valid citations and retrieval scores do not prove answer correctness. Student ratings, demo/video, slides, and the final report remain to be completed. Assistance and reviewer attribution are in [docs/ASSISTANCE_DISCLOSURE.md](docs/ASSISTANCE_DISCLOSURE.md).

The exact evaluated implementation is preserved in `archive/evaluated_snapshot/` with `archive/evaluated_snapshot_manifest.json`. The Git repository is initialized on `main`; no commit or remote has been created yet.

## Publication setup check

The publication set is 342 files (about 25.7 MiB). A temporary copy with spaces in its path installed the pinned requirements in a fresh Python 3.11.9 environment and downloaded and verified the pinned dataset. Preparation reproduced 469 training and 31 evaluation QA records plus the 57-document, 1,696-passage index. MiniLM and Qwen files came from the existing Hugging Face cache; Qwen's pinned snapshot was checked but the model was not loaded. BM25 and MiniLM CLI searches passed, and Streamlit AppTest passed a BM25 search. `run.sh` launched the temporary app on port 18502; its health endpoint and page responded. No answer generation ran in this setup check. Frozen retrieval settings, results, references, responses, and ratings still match their saved hashes.
