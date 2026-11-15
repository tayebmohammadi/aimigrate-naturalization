# Stage 4 verification exit status and frozen configuration

The final Stage 4 shell command ran a Python fingerprint/assertion block, which
printed `Final protected-file and model/prompt/code fingerprints match.`, followed by:

```sh
rg -n 'after execution|remains for the next stage|before answer generation' README.md PROJECT_STATUS.md
```

That final text audit found no obsolete phrases. `rg` uses exit **1 for no matches**,
0 for matches, and 2+ for an error. The shell reported the last command's status,
so the combined call exited 1 even though the Python assertions passed. It was
not a model, implementation, protected-file, or fingerprint failure.

Stage 5A repeated only the relevant static checks and the text audit: configuration,
system-prompt hash and answer-code hash matched both final Stage 4 summaries; the
same text search again returned 1 with no output. No generation was run. For future
audits, interpret a no-match result explicitly rather than treating it as a failed
implementation test. Do not hide exit 2+ with a blanket `|| true`.

The authoritative baseline is `frozen_configuration.json`, read from the actual
answer.py AST and pinned cached model/tokenizer configs without loading a model:

- Qwen/Qwen2.5-1.5B-Instruct, revision
  `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`.
- SYSTEM_PROMPT SHA-256:
  `fe998488c016559b170ae6b7f70840aeb0c3031e7cb2a31eb550e95f75c6b62a`.
- CPU float32, four threads, seed 0, eager attention; greedy do_sample=False,
  num_beams=1, repetition_penalty=1.0, use_cache=True. temperature/top_p/top_k=None.
- **Final answer max_new_tokens=160.** The smoke CLI explicitly uses 40. The
  archived formatting-example trial used 128; that is not the final configuration.
- Operational input budget 2,048 tokens, model context 32,768. Select the best
  passage of each of the first three distinct ranked documents; assign [S1]–[S3].
  If necessary, drop whole lowest-ranked sources until input fits. Retain IDs,
  titles, URLs and complete included text. No QA answer/span or review note is
  supplied to the generator. Reserve 160 output tokens; never silently truncate.
- The downloaded generation_config.json has sampling defaults, but `_generate`
  overrides them: False instead of do_sample=True; repetition penalty 1.0 rather
  than 1.1; no temperature/top-p/top-k sampling. Code pads with tokenizer EOS 151645,
  not the repository's pad default 151643. Pinned stop IDs are [151645, 151643].
  Use the project module, not the model card's generic generation defaults.

The system-string fingerprint is not a hash of every question-dependent prompt.
The frozen record also includes code, index/settings, and chat-template fingerprints.
Later generation records must save their own complete rendered prompt and supplied
evidence, as Stage 4 did. No package or application change was needed to resolve
the status ambiguity. Stage 4's reports already state the correct final 160 limit;
only the archived 128 trial and 40-token smoke differ.
