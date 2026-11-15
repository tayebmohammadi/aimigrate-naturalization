"""Compare both retrievers on held-out questions. Run `python -m scripts.check_retrieval` first."""
import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from retrieval import INDEX, ROOT, Retriever, read_jsonl, sha256, source_metrics


def main():
    """Score both frozen methods on the held-out questions and save document-rank results."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "results/stage2-reproduction")
    parser.add_argument("--checks", type=Path, default=ROOT / "results/stage2-reproduction/training_checks.json")
    args = parser.parse_args()
    out = args.output
    checks_path = args.checks
    checks = json.loads(checks_path.read_text())
    protocol_hash = sha256(ROOT / "docs/STAGE2_PROTOCOL.md")
    assert checks['passed'] and checks['protocol_sha256'] == protocol_hash
    assert checks['index_manifest_sha256'] == sha256(INDEX / "manifest.json"), "Rerun training checks for this index"
    retriever = Retriever()
    qa_path = ROOT / "data/processed/official_qa_eval.jsonl"
    questions = read_jsonl(qa_path)
    assert len(questions) == 31 and all(q['split'] == 'eval' for q in questions)
    rows, details = [], []
    for qa in questions:
        # Access question and source identity only, never answer or source_span.
        row = {"qa_id": qa['qa_id'], "question": qa['question'], "source_doc_id": qa['source_doc_id']}
        for method in ("bm25", "minilm"):
            ranked = retriever.search(qa['question'], method, top_k=None, distinct_documents=True)
            assert len(ranked) == len({r['doc_id'] for r in ranked}) == 57
            metrics = source_metrics([r['doc_id'] for r in ranked], qa['source_doc_id'])
            row.update({f"{method}_{k}": v for k, v in metrics.items()})
            row[f"{method}_top3_doc_ids"] = '|'.join(r['doc_id'] for r in ranked[:3])
            details.append({"qa_id": qa['qa_id'], "question": qa['question'], "method": method,
                            "source_doc_id": qa['source_doc_id'], **metrics,
                            "top_sources": ranked[:3],
                            "complete_document_ranking": [
                                {"rank": i, **{key: r[key] for key in ('doc_id', 'passage_id', 'score')}}
                                for i, r in enumerate(ranked, 1)]})
        rows.append(row)
    summary = []
    for method in ("bm25", "minilm"):
        summary.append({"method": method, "questions": len(rows),
                        "hits_at_3": sum(r[f'{method}_recall_at_3'] for r in rows),
                        "recall_at_3": sum(r[f'{method}_recall_at_3'] for r in rows) / len(rows),
                        "mrr": sum(r[f'{method}_reciprocal_rank'] for r in rows) / len(rows)})
    out.mkdir(parents=True, exist_ok=True)
    for name, records in (("comparison.csv", summary), ("per_question.csv", rows)):
        with (out / name).open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    (out / "evaluation_details.jsonl").write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in details))
    report = {"executed_at_utc": datetime.now(timezone.utc).isoformat(),
              "settings": retriever.settings, "index_summary": retriever.manifest['summary'],
              "index_manifest_sha256": sha256(INDEX / "manifest.json"),
              "protocol_sha256": protocol_hash, "eval_file_sha256": sha256(qa_path),
              "training_checks_sha256": sha256(checks_path),
              "evaluation_code_sha256": sha256(ROOT / "scripts/evaluate_retrieval.py"),
              "comparison": summary}
    (out / "evaluation_summary.json").write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
