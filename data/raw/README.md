---
language:
- en
license: cc-by-4.0
tags:
- legal
- immigration
- question-answering
- retrieval-augmented-generation
- united-states
- fine-tuning
size_categories:
- 10K<n<100K
task_categories:
- question-answering
- text-generation
pretty_name: USA Immigration Law Q&A Dataset
---

# USA Immigration Law Q&A Dataset

A large-scale, source-grounded Q&A dataset covering U.S. immigration law and policy,
built entirely from official government sources, open legal datasets, and curated
community materials. Complete pipeline available at https://github.com/nshportun/usa-immigration and pre-print https://arxiv.org/abs/2605.30589

## Dataset Contents

| Split | Records | Description |
|-------|---------|-------------|
| `train` | 16,065 | Training Q&A pairs |
| `eval` | 993 | Stratified held-out evaluation set |
| `corpus` | 10,056 | Canonical source documents |

## Coverage (Q&A pairs by subdomain)

| Subdomain | Train | Eval |
|-----------|-------|------|
| Family-based immigration | ~3,754 | 233 |
| Naturalization | ~2,514 | 156 |
| Asylum | ~1,972 | 122 |
| General immigration | ~1,964 | 122 |
| Adjustment of status | ~1,626 | 101 |
| Removal | ~1,203 | 74 |
| Humanitarian | ~842 | 52 |
| Employment authorization | ~784 | 48 |
| Admissibility | ~521 | 32 |
| Nonimmigrant visas | ~516 | 32 |
| Statistics | ~133 | 8 |
| Travel documents | ~103 | 6 |
| Employment-based (EB) | ~70 | 4 |
| Appeals | ~63 | 3 |

## Data Sources

- **USCIS Policy Manual** (primary_official) — official adjudication policy
- **USCIS Forms & Instructions** (primary_official) — I-130, I-485, I-765, N-400, I-589, etc.
- **8 CFR / INA** (primary_official) — federal regulations and statute text
- **BIA Precedent Decisions** (primary_official) — Board of Immigration Appeals
- **DHS/CBP Statistics** (primary_official) — yearbook tables, enforcement data
- **harshitha008/US-immigration-laws** (secondary_reputable) — 8,897 QA pairs, Apache 2.0
- **Law StackExchange** (community) — immigration-tagged expert Q&A

## Q&A Pair Schema

```python
{
    "qa_id": "qa-000001",
    "question": "Who may file Form I-130?",
    "answer": "A U.S. citizen or lawful permanent resident...",
    "answer_type": "factual",              # factual | procedural | definition | statistics
    "extraction_type": "rule_derived",     # direct | rule_derived | case_derived
    "source_doc_id": "uscis-form-i130",
    "source_url": "https://www.uscis.gov/i-130",
    "source_span": "Who May File...",
    "authority_level": "primary_official", # primary_official | secondary_reputable | community_non_authoritative
    "topic_tags": ["family-based", "I-130"],
    "immigration_subtopic": "family-based immigration",
    "generation_mode": "rule",             # faq | rule | form | precedent | statistics
    "review_status": "draft",
    "time_sensitive": false
}
```

## Intended Use

- **RAG** — retrieval-augmented generation for immigration legal assistants
- **Fine-tuning** — domain adaptation of small LLMs (Llama 3.2 3B/8B recommended)
- **Benchmarking** — evaluating LLM performance on U.S. immigration law

## ⚠️ Disclaimer

This dataset is for research and educational purposes only. It does not constitute
legal advice. Immigration law is complex and changes frequently — always consult a
licensed immigration attorney for your specific situation.

## License

- Government source text: public domain (U.S. government works)
- HF-sourced data (`harshitha008/US-immigration-laws`): Apache 2.0
- Community data: CC BY-SA 4.0
- Dataset compilation: **CC BY 4.0**

## Citation

```bibtex
@dataset{nshportun2026usaimmigration,
  author = {nshportun},
  title  = {USA Immigration Law Q\&A Dataset},
  year   = {2026},
  url    = {https://huggingface.co/datasets/nshportun/usa-immigration-law-qa}
}
```
