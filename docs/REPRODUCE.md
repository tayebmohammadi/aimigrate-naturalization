# Setup and reproduction

Install Python 3.11 before setup; we tested Python 3.11.9 on an Intel Mac. The root scripts `setup.sh` and `run.sh` are the short first-time setup and launch commands in the README. They locate the project from their own file paths. The detailed commands below are also useful for reproducing individual steps; run them from the repository root.

## First-time setup

The repository includes prepared QA/source records and passage text. The raw dataset files are excluded from Git. The pinned downloader fetches about 15.3 MB from Hugging Face revision `f25cc4476b6e45b20e3d0d3f6f7aeb50efb8dc6f`, then verifies the files against recorded sizes and hashes.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m scripts.download_data
.venv/bin/python -m scripts.prepare_data
.venv/bin/python -m scripts.smoke_check
.venv/bin/python build_index.py
.venv/bin/python answer.py --download
```

The smoke check and index build use `sentence-transformers/all-MiniLM-L6-v2`. The first run downloads it if it is not in the normal Hugging Face cache. The index build saves 1,696 passages and normalized embeddings in `data/index/`. While splitting long source documents, the tokenizer may warn that the full document exceeds its 256-token model limit; it only tokenizes for chunk boundaries. The saved passages are at most 182 tokens including special tokens, so the model does not receive those full documents. The Qwen download command saves the pinned `Qwen/Qwen2.5-1.5B-Instruct` revision in that cache. Setup reuses valid files and cached models. It does not install Python for you. The current local cache uses about 87 MB for MiniLM and 2.9 GB for Qwen. Keep several GB free for packages and model files; the project environment itself used about 1.4 GB on the test Mac. Model cache sizes vary by platform and cache contents.

## Launch the app

```sh
HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false .venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502 --server.headless true --server.fileWatcherType none --browser.gatherUsageStats false
```

Use `bash run.sh` to launch with the documented settings, or run the command below directly. Open <http://127.0.0.1:8502>. The offline setting works after both models are cached. Generation uses CPU and full-precision Qwen. On the recorded 16 GB Intel Mac, one app generation took 65–73 seconds; the machine already had swap in use. Leave time for a minute or more per answer, and close other memory-heavy apps if needed. We have not tested a clean model download on every platform.

## Reproduce retrieval

The index contains only USCIS source passages, not QA reference answers. BM25 tokenizes lowercase words and numbers; MiniLM ranks by cosine similarity. Both methods score a document by its highest-scoring passage. Run a quick search with either method:

```sh
HF_HUB_OFFLINE=1 .venv/bin/python retrieval.py "What happens at a naturalization ceremony?" --method bm25 --documents
HF_HUB_OFFLINE=1 .venv/bin/python retrieval.py "What happens at a naturalization ceremony?" --method minilm --documents
```

Recreate the training checks and held-out retrieval comparison with:

```sh
.venv/bin/python -m scripts.check_retrieval
.venv/bin/python -m scripts.evaluate_retrieval
```

These scripts write to `results/retrieval-reproduction/`; they do not replace the fixed files in `results/retrieval/`. The fixed comparison used 31 held-out questions. We do not provide a command to rerun the 50-answer collection as part of setup; those responses are frozen evidence, not a setup check.

## Data, models, and saved results

The upstream [dataset card](https://huggingface.co/datasets/nshportun/usa-immigration-law-qa) declares CC BY 4.0 for the dataset compilation and lists different terms for incorporated materials, including Apache 2.0 and CC BY-SA 4.0. Cite it as nshportun (2026), *USA Immigration Law Q&A*, DOI [10.57967/hf/8824](https://doi.org/10.57967/hf/8824). The prepared official subset is included with attribution. The card identifies government source text as public domain. The raw Parquet files remain local and can be downloaded with the pinned script. The [MiniLM model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) and [Qwen model card](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) list Apache 2.0.

The [retrieval ranks](../results/retrieval/per_question.csv), [answer ratings](../results/answers/assessment/ratings.csv), and [saved answers](../results/answers/responses/) support the reported tables. The [reference verification](../results/source-verification/FINAL_VERIFICATION.md) provides the separate source checks. Frozen files retain their original hashes and path strings. Use the current directory layout to locate them: retrieval evidence is under `results/retrieval/`, response records under `results/answers/responses/`, and the final USCIS captures under `results/source-verification/live_pages/`. The active scripts reproduce retrieval. The original evaluated implementation and the exact original USCIS captures are kept privately.

## Recorded setup check

The publication setup was tested with a fresh Python 3.11.9 environment on an Intel Mac, in a temporary path containing spaces. Dependency installation and the verified data download succeeded. Data preparation produced 469 training records, 31 held-out records, 57 documents, and 1,696 passages. Setup reused cached MiniLM and Qwen files. Both searches, Streamlit AppTest, and an isolated launch check passed. A [separate app check](../results/app-checks/app_flow_smoke.json) generated one real draft. Linux and Windows were not tested.
