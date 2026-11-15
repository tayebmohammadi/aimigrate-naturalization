# Exact evaluated implementation snapshot

This folder preserves the source bytes and index artifacts used for the original
Stage 2 retrieval evaluation and Stage 5 fixed answer collection, copied before
Stage 6 documentation edits. `../evaluated_snapshot_manifest.json` records SHA-256
for each copied file and the original evaluation fingerprints. The root result files
remain in `../../results/` and were not rewritten by Stage 6.

The index in this snapshot is the original evaluated index. The working root index
was explicitly rebuilt after documentation edits changed source hashes. Do not copy
the snapshot index over the working index or regenerate fixed answer outputs as part
of ordinary setup.

From this directory, the preserved app can be started against the snapshot index with
`../../.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501`.
Its code/config/index hashes match the saved Stage 5 configuration. The full original
batch inputs/records are under the project root `results/stage5/`. Do **not** run the
archived `collect_answers.py`: its relative output path here does not contain those
records and would start a separate generation batch. The fixed collection is already
complete. This snapshot is for provenance and the original Stage 2/app implementation.
