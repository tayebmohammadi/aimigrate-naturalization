# AImigrate Naturalization Information Assistant

**Tayeb Mohammadi · CS 72/272**

AImigrate helps immigrants and families read official U.S. naturalization information in plain English. Search a local collection of USCIS passages with BM25 keyword matching or MiniLM semantic search. The app shows three distinct sources, with a passage and a link for each. You can then ask local Qwen for a short cited draft. The collection is a saved snapshot, and drafts can make mistakes or omit conditions. Use the source links to check the current guidance.

## Run locally

Install Python 3.11 and Bash. First-time setup needs internet and several GB of free space. From the repository folder, run:

```sh
bash setup.sh
bash run.sh
```

Open <http://127.0.0.1:8502>. Try the administrative naturalization ceremony example with either search method. Select **Generate answer from this evidence** to request a draft. On the tested Intel Mac, local generation took roughly a minute. See the [setup and reproduction guide](docs/REPRODUCE.md) for prerequisites, the recorded setup check, and retrieval commands.

## Data and methods

We used the pinned [USA Immigration Law Q&A dataset](https://huggingface.co/datasets/nshportun/usa-immigration-law-qa) and indexed only source text from 57 USCIS documents, split into 1,696 passages. Setup downloads and verifies the raw dataset and builds the index. The [pinned dataset card](data/raw/README.md) documents the compilation license and the separate terms for incorporated materials. See the [retrieval protocol](docs/RETRIEVAL_PROTOCOL.md) and [answer assessment protocol](results/answers/ASSESSMENT_PROTOCOL.md) for the methods and settings.

## Results and evidence

| Measure | BM25 | MiniLM |
|---|---:|---:|
| Linked source in the top three | 29/31 | 29/31 |
| Mean reciprocal rank | 0.860 | 0.822 |
| Supported, useful naturalization drafts with Qwen | 7/20 | 3/20 |
| Appropriate declines on out-of-scope questions | 5/5 | 5/5 |

The answer counts come from a separate assisted assessment of the saved outputs. See the [evaluation summary](docs/EVALUATION.md), [per-question retrieval ranks](results/retrieval/per_question.csv), [answer ratings and reasons](results/answers/assessment/ratings.csv), [saved answers and paired examples](results/answers/responses/), and [USCIS reference verification](results/source-verification/FINAL_VERIFICATION.md). The [assistance disclosure](docs/ASSISTANCE_DISCLOSURE.md) records the work performed with coding and review assistance.
