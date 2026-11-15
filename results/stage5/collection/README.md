# Fixed answer collection

This folder holds all 50 saved responses, the exact evidence supplied to the model,
and the raw model outputs. `records/` contains individual cases; `responses.jsonl` is
the combined export. The questions, model, prompt, retrieval, and generation settings
are fixed. Do not run the answer collector again.

Open `REVIEW.html` to inspect paired evidence and answers. The fields in
`student_ratings.csv` are blank and ready for review. Application checks are
mechanical; they do not establish factual support.

To rebuild only the mechanical summary and review packet, run from the project root:

```sh
.venv/bin/python -m scripts.prepare_answer_review
```

This command does not load a model or generate responses and will not overwrite
existing review entries. Reference answers and review notes were not included in
the model inputs.
