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

The publication setup was verified in a temporary copy with spaces in its path. A fresh Python 3.11.9 environment installed the pinned requirements and downloaded the verified dataset; preparation reproduced 469 training and 31 evaluation QA records and a 57-document, 1,696-passage index. Cached MiniLM and Qwen files were reused; Qwen was not loaded. BM25 and MiniLM searches passed, as did Streamlit AppTest and an isolated `run.sh` health/page check. No answer generation ran. Frozen retrieval settings, results, references, responses, and ratings still match their saved hashes.

GitHub flagged 39 copies of a Google key-shaped value in captured USCIS HTML. We confirmed it came from the publicly served `uscis_design.apiKey_aao_pm_search` setting, found no app/setup use, preserved original captures privately, and published narrowly redacted derivatives. Main-page text and links are unchanged. See `results/stage5/public_html_redaction/REDACTION.md`; ownership and status are unconfirmed, so the alert remains open. The capture script now sanitizes future public copies.
