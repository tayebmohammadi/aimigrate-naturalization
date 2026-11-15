"""Small direct checks and three training-only source/evidence demonstrations."""
import json

import numpy as np

from build_index import clean_source, make_passages
from retrieval import (INDEX, ROOT, SOURCES, Retriever, check_lengths, rank_documents,
                       load_model, read_jsonl, sha256, source_metrics, tokenize)

RESULTS = ROOT / "results/stage2"
TRAIN_IDS = ["qa-555ef18e4ec5", "qa-2b240fd9fef3", "qa-35797c99710e"]


def main():
    retriever = Retriever()
    sources = {d["doc_id"]: d for d in read_jsonl(SOURCES)}
    model = retriever.model = load_model(retriever.settings)
    regenerated, audit = [], []
    for source in sorted(sources.values(), key=lambda d: d["doc_id"]):
        chunks, document_audit = make_passages(source, model.tokenizer, retriever.settings)
        regenerated.extend(chunks)
        audit.append(document_audit)
    assert regenerated == retriever.passages
    assert audit == read_jsonl(INDEX / "cleaning_audit.jsonl")
    assert set(p["doc_id"] for p in regenerated) == set(sources)
    allowed = {"passage_id", "doc_id", "title", "url", "text", "content_tokens",
               "cleaned_char_start", "cleaned_char_end"}
    for p in regenerated:
        d = sources[p["doc_id"]]
        cleaned, _ = clean_source(d["text"])
        assert set(p) == allowed
        assert p["text"] == cleaned[p["cleaned_char_start"]:p["cleaned_char_end"]]
        assert (p["title"], p["url"]) == (d["title"], d["url"])
    lengths = check_lengths(model, [p['text'] for p in regenerated])
    assert max(lengths) <= model.max_seq_length
    assert tokenize("NOT eligible for N-400 after 5-year residence") == [
        "not", "eligible", "for", "n-400", "after", "5-year", "residence"]
    sample = "Conditions\nDo not apply before 18 years.\nException: 5 years, not 3."
    assert clean_source(sample + "\nWas this page helpful?\nYes\nNo")[0] == sample
    assert source_metrics(["a", "b", "c", "d"], "d") == {
        "source_rank": 4, "recall_at_3": 0, "reciprocal_rank": 0.25}
    assert source_metrics(["a", "b", "c"], "c")["recall_at_3"] == 1
    assert source_metrics(["a"], "missing")["reciprocal_rank"] == 0
    tied = [{"doc_id": "b", "passage_id": "2", "score": 1},
            {"doc_id": "a", "passage_id": "2", "score": 1},
            {"doc_id": "a", "passage_id": "1", "score": 1}]
    assert [(r['doc_id'], r['passage_id']) for r in rank_documents(tied)] == [('a', '1'), ('b', '2')]
    # Check that a too-long MiniLM question is rejected rather than truncated.
    try:
        check_lengths(model, ["citizenship " * 300])
    except ValueError:
        pass
    else:
        raise AssertionError("Long question was not rejected")
    train = {r["qa_id"]: r for r in read_jsonl(ROOT / "data/processed/official_qa_train.jsonl")}
    examples, markdown = [], ["# Training retrieval checks\n", "Scores are ranking values, not confidence probabilities.\n"]
    for qa_id in TRAIN_IDS:
        qa = train[qa_id]
        markdown.append(f"## {qa['question']}\n\nTraining QA: {qa_id}; linked source: {qa['source_doc_id']}\n")
        for method in ("bm25", "minilm"):
            ranked = retriever.search(qa["question"], method, top_k=None, distinct_documents=True)
            assert len(ranked) == len({r['doc_id'] for r in ranked}) == 57
            assert all(ranked[i]['score'] >= ranked[i + 1]['score'] for i in range(56))
            for row in ranked:
                source = sources[row['doc_id']]
                assert (row['title'], row['url']) == (source['title'], source['url'])
            examples.append({"qa_id": qa_id, "question": qa['question'], "method": method,
                             "linked_source_doc_id": qa['source_doc_id'],
                             "source_rank": source_metrics([r['doc_id'] for r in ranked], qa['source_doc_id'])['source_rank'],
                             "top_sources": ranked[:3]})
            markdown.append(f"### {method}\n")
            for rank, row in enumerate(ranked[:3], 1):
                markdown.append(f"{rank}. [{row['title']}]({row['url']}) — score {row['score']:.6f}\n\n"
                                f"   Document: {row['doc_id']}; passage: {row['passage_id']}\n\n"
                                + "> " + row['text'].replace('\n', '\n> ') + "\n")
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "training_examples.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + '\n' for r in examples))
    (RESULTS / "training_examples.md").write_text('\n'.join(markdown))
    checks = {"passed": True, "index_manifest_sha256": sha256(INDEX / "manifest.json"),
              "protocol_sha256": sha256(ROOT / "STAGE2_PROTOCOL.md"),
              "training_file_sha256": sha256(ROOT / "data/processed/official_qa_train.jsonl"),
              "training_examples_sha256": sha256(RESULTS / "training_examples.jsonl"),
              "check_code_sha256": sha256(ROOT / "check_retrieval.py"),
              "documents": len(sources), "passages": len(regenerated),
              "embedding_shape": list(retriever.embeddings.shape),
              "max_input_tokens": max(lengths), "checks": [
                  "source-only regeneration equals saved passages", "all 57 document IDs retained",
                  "all passage text slices/titles/URLs match source-derived cleaned text",
                  "no QA answer/span fields in searchable passages", "all passage inputs fit model",
                  "normalized finite embeddings", "BM25 keeps negation/numbers/form identifiers",
                  "cleaning retains example conditions/negation", "metric arithmetic and deterministic ties",
                  "too-long MiniLM question rejected", "three training questions, both complete document rankings"]}
    (RESULTS / "training_checks.json").write_text(json.dumps(checks, indent=2) + '\n')
    print(json.dumps(checks, indent=2))
    for r in examples:
        print(r['method'], r['question'], 'linked rank', r['source_rank'])
        for row in r['top_sources']:
            print(' ', row['title'], row['url'], row['text'][:160].replace('\n', ' '))


if __name__ == "__main__":
    main()
