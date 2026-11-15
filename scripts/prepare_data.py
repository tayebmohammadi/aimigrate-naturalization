"""Filter the pinned QA splits and link official USCIS records. Run with `python -m scripts.prepare_data` from the project root."""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent


def official_url(value):
    """Return whether a URL has the exact official USCIS hostname."""
    if not isinstance(value, str):
        return False
    try:
        return urlsplit(value).hostname == "www.uscis.gov"
    except ValueError:
        return False


def write_jsonl(path, rows):
    """Write records as UTF-8 JSON Lines."""
    with path.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def duplicates(train, evaluation, fields):
    # Exact string comparison: no deduplication or split changes.
    """Count exact duplicate keys without removing or moving rows."""
    keys = lambda rows: Counter(tuple(r[f] for f in fields) for r in rows)
    a, b = keys(train), keys(evaluation)
    shared = a.keys() & b.keys()
    return {"shared_unique_keys": len(shared),
            "train_rows_with_shared_keys": sum(a[k] for k in shared),
            "eval_rows_with_shared_keys": sum(b[k] for k in shared),
            "within_train_extra_rows": sum(n - 1 for n in a.values()),
            "within_eval_extra_rows": sum(n - 1 for n in b.values())}


def main():
    """Apply the documented naturalization and official-source filters to both saved splits."""
    raw, out = ROOT / "data/raw", ROOT / "data/processed"
    out.mkdir(parents=True, exist_ok=True)
    corpus_file = raw / "corpus/corpus-00000-of-00001.parquet"
    corpus = pq.read_table(corpus_file).to_pylist()
    docs = {d["doc_id"]: d for d in corpus}
    assert len(docs) == len(corpus), "Duplicate source document IDs"
    report = {"corpus_documents": len(corpus), "schemas": {
        "corpus": str(pq.read_schema(corpus_file))}, "splits": {}}
    all_qa, selected, natural_splits = {}, {}, {}
    associated = {}
    for split in ("train", "eval"):
        file = raw / f"qa/{split}-00000-of-00001.parquet"
        rows = pq.read_table(file).to_pylist()
        report["schemas"][split] = str(pq.read_schema(file))
        all_qa[split] = rows
        for row in rows:
            row["split"] = split
        natural = [r for r in rows if r["immigration_subtopic"] == "naturalization"]
        natural_splits[split] = natural
        tag_count = sum("naturalization" in (r.get("topic_tags") or []) for r in rows)
        kept, audit = [], []
        counts = Counter()
        for r in natural:
            doc = docs.get(r["source_doc_id"])
            span = r.get("source_span")
            checks = {
                "qa_authority": r.get("authority_level") == "primary_official",
                "qa_hostname": official_url(r.get("source_url")),
                "linked_document": doc is not None,
                "document_authority": bool(doc and doc.get("authority_level") == "primary_official"),
                "document_hostname": bool(doc and official_url(doc.get("url"))),
                "url_agreement": bool(doc and r.get("source_url") == doc.get("url")),
                "exact_span": bool(doc and isinstance(span, str) and span.strip()
                                   and isinstance(doc.get("text"), str) and span in doc["text"]),
            }
            for key, passed in checks.items():
                counts[key] += int(passed)
            audit.append({"qa_id": r["qa_id"], "split": split, **checks})
            if all(checks.values()):
                kept.append(r)
                associated.setdefault(doc["doc_id"], {**doc, "qa_splits": []})
                if split not in associated[doc["doc_id"]]["qa_splits"]:
                    associated[doc["doc_id"]]["qa_splits"].append(split)
        selected[split] = kept
        write_jsonl(out / f"naturalization_{split}.jsonl", natural)
        write_jsonl(out / f"official_qa_{split}.jsonl", kept)
        write_jsonl(out / f"filter_audit_{split}.jsonl", audit)
        report["splits"][split] = {
            "all_qa": len(rows), "unique_qa_ids": len({r['qa_id'] for r in rows}),
            "missing_source_ids_all_qa": sum(r['source_doc_id'] not in docs for r in rows),
            "naturalization_subtopic": len(natural), "naturalization_topic_tag": tag_count,
            "individual_checks_on_naturalization": dict(counts), "official_matching_span": len(kept),
            "review_status_selected": dict(Counter(r['review_status'] for r in kept)),
            "null_counts": {k: sum(r[k] is None for r in rows) for k in rows[0]},
        }
    write_jsonl(out / "sources.jsonl", associated.values())
    report["associated_source_documents"] = len(associated)
    report["cross_split_duplicates"] = {}
    for label, splits in (("all_qa", all_qa), ("naturalization", natural_splits), ("official_subset", selected)):
        report["cross_split_duplicates"][label] = {
            name: duplicates(splits['train'], splits['eval'], fields)
            for name, fields in (("question", ["question"]),
                                 ("qa_pair", ["question", "answer"]), ("qa_id", ["qa_id"]))}
    shared_questions = {r['question'] for r in all_qa['train']} & {r['question'] for r in all_qa['eval']}
    write_jsonl(out / "cross_split_duplicate_records.jsonl",
                [r for rows in all_qa.values() for r in rows if r['question'] in shared_questions])
    report['corpus_null_counts'] = {k: sum(d[k] is None for d in corpus) for k in corpus[0]}
    report["examples"] = [{"qa_id": r['qa_id'], "question": r['question'],
                           "title": docs[r['source_doc_id']]['title'], "url": r['source_url']}
                          for r in selected['train'][:3]]
    (out / "inspection.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != 'schemas'}, indent=2))


if __name__ == "__main__":
    main()
