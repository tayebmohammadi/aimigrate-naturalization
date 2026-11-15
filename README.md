# AImigrate

AImigrate is a local prototype for English naturalization questions. We search official USCIS passages with BM25 or MiniLM, then use a local Qwen model to draft a short answer with links to its evidence. It gives general information, not legal advice or an eligibility decision.

## How it works

Enter a question and choose BM25 or MiniLM. The app ranks source passages, keeps the best passage from each of the top three distinct documents, and sends those passages with the question to Qwen. It shows the answer, evidence, and USCIS links. Retrieval scores and valid citations do not prove an answer is correct.

## Install and run

Python 3.11 must already be installed. From the project folder, run:

```sh
bash setup.sh
bash run.sh
```

First-time setup needs internet. It creates `.venv`, installs the pinned dependencies, downloads and checks the dataset, builds the index, and downloads MiniLM and Qwen. Later runs reuse valid data, index files, and the normal Hugging Face model cache. The setup and launch scripts use Bash. We tested them on an Intel Mac; Linux and Windows are untested.

The app opens at <http://127.0.0.1:8502>. If that port is already in use, choose another with `AIMIGRATE_PORT=8503 bash run.sh`.

The current cache uses about 87 MB for MiniLM and 2.9 GB for Qwen; the environment used about 1.4 GB on the test Mac. The 1.5B Qwen model ran on a 16 GB Intel Mac, but swap was already in use. CPU generations took about 65–73 seconds. Allow several GB of disk space and a minute or more per answer.

## Data and results

We use revision `f25cc4476b6e45b20e3d0d3f6f7aeb50efb8dc6f` of the [USA Immigration Law Q&A dataset](https://huggingface.co/datasets/nshportun/usa-immigration-law-qa). Its card declares CC BY 4.0 for the compilation and separate terms for incorporated materials. Citation: nshportun (2026), *USA Immigration Law Q&A*, DOI [10.57967/hf/8824](https://doi.org/10.57967/hf/8824). Raw Parquet files are downloaded by setup and excluded from Git. The prepared subset has 57 USCIS documents and the index has 1,696 source-only passages. Dataset answers are generated, not manually verified. See the model cards for [MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) and [Qwen](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct).

Fixed retrieval results are in [results/stage2](results/stage2/RESULTS.md). The 50-response assessment is in [docs/EVALUATION.md](docs/EVALUATION.md), with evidence and raw outputs in `results/stage5/`. Source/model citations and the required assistance disclosure are in [docs/ASSISTANCE_DISCLOSURE.md](docs/ASSISTANCE_DISCLOSURE.md); setup and reproduction details are in [docs/REPRODUCE.md](docs/REPRODUCE.md). USCIS pages are a downloaded snapshot and may be out of date. The model can omit conditions, abstain, or fail validation.
