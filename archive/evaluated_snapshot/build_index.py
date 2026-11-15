"""Build the fixed source-only passage collection and normalized MiniLM embeddings."""
import hashlib
import json
import re

import numpy as np

from retrieval import (INDEX, SOURCES, check_lengths, fingerprint, load_model,
                       load_settings, read_jsonl, sha256)


def clean_source(text):
    """Remove only recognized UI boilerplate, not repeated policy statements."""
    audit = {"feedback_footer_removed": False, "navigation_blocks_removed": 0}
    marker = "\nWas this page helpful?"
    if marker in text:
        text = text.split(marker, 1)[0]
        audit["feedback_footer_removed"] = True
    # A contiguous list of >=3 Policy Manual volume links is navigation. Never
    # remove isolated USCIS-PM citations, substantive appendices, or update notes.
    pattern = r"(?:\d+ USCIS-PM\s*\n\s*-\s*\n\s*Volume \d+ - [^\n]+\n?){3,}"
    text, audit["navigation_blocks_removed"] = re.subn(pattern, "\n", text)
    # Normalize whitespace, keeping paragraph/line boundaries in the cleaned view.
    lines = [re.sub(r"[^\S\n]+", " ", line).strip() for line in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip(), audit


def make_passages(source, tokenizer, settings):
    text, audit = clean_source(source["text"])
    offsets = tokenizer(text, add_special_tokens=False, truncation=False,
                        return_offsets_mapping=True)["offset_mapping"]
    budget, overlap = settings["chunk_tokens"], settings["overlap_tokens"]
    passages, seen = [], set()
    start = 0
    while start < len(offsets):
        end = min(start + budget, len(offsets))
        # Avoid splitting a whitespace-delimited word or a form number at a boundary.
        while end < len(offsets) and end > start and offsets[end][0] == offsets[end - 1][1]:
            end -= 1
        if end == start:
            raise ValueError(f"A word exceeds chunk budget in {source['doc_id']}")
        begin_char, end_char = offsets[start][0], offsets[end - 1][1]
        passage_text = text[begin_char:end_char]
        length = len(tokenizer(passage_text, add_special_tokens=False, truncation=False)["input_ids"])
        if length > budget:
            raise ValueError("Retokenized passage exceeds content budget.")
        if passage_text not in seen:
            digest = hashlib.sha256(passage_text.encode()).hexdigest()[:20]
            passages.append({"passage_id": f"{source['doc_id']}-p-{digest}",
                             "doc_id": source["doc_id"], "title": source["title"],
                             "url": source["url"], "text": passage_text,
                             "content_tokens": length, "cleaned_char_start": begin_char,
                             "cleaned_char_end": end_char})
            seen.add(passage_text)
        else:
            audit["duplicate_passages_removed"] = audit.get("duplicate_passages_removed", 0) + 1
        if end == len(offsets):
            break
        next_start = max(start + 1, end - overlap)
        while next_start > start + 1 and offsets[next_start][0] == offsets[next_start - 1][1]:
            next_start -= 1
        start = next_start
    audit.update({"doc_id": source["doc_id"], "raw_characters": len(source["text"]),
                  "cleaned_characters": len(text), "passages": len(passages),
                  "cleaned_sha256": hashlib.sha256(text.encode()).hexdigest()})
    return passages, audit


def main():
    settings = load_settings()
    inputs = fingerprint()
    INDEX.mkdir(parents=True, exist_ok=True)
    manifest_path = INDEX / "manifest.json"
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text())
        if previous["fingerprint"] == inputs and all(
                (INDEX / name).exists() and sha256(INDEX / name) == digest
                for name, digest in previous["artifact_sha256"].items()):
            print("Reusing matching passages and cached embeddings.")
            print(json.dumps(previous["summary"], indent=2))
            return
    sources = sorted(read_jsonl(SOURCES), key=lambda d: d["doc_id"])
    assert len(sources) == len({d["doc_id"] for d in sources}) == 57
    model = load_model(settings)
    special = model.tokenizer.num_special_tokens_to_add(pair=False)
    assert 0 <= settings["overlap_tokens"] < settings["chunk_tokens"]
    assert settings["chunk_tokens"] + special <= model.max_seq_length
    passages, audits = [], []
    for source in sources:
        chunks, audit = make_passages(source, model.tokenizer, settings)
        assert chunks, f"No passages: {source['doc_id']}"
        passages.extend(chunks)
        audits.append(audit)
    assert len({p["passage_id"] for p in passages}) == len(passages)
    texts = [p["text"] for p in passages]
    lengths = check_lengths(model, texts)
    print(f"Encoding {len(passages)} passages on CPU; maximum input {max(lengths)} tokens.", flush=True)
    embeddings = model.encode(texts, batch_size=32, normalize_embeddings=True,
                              convert_to_numpy=True, show_progress_bar=True).astype("float32")
    assert embeddings.shape == (len(passages), 384) and np.isfinite(embeddings).all()
    assert np.allclose(np.linalg.norm(embeddings, axis=1), 1, atol=1e-5)
    for name, rows in (("passages.jsonl", passages), ("cleaning_audit.jsonl", audits)):
        (INDEX / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    np.save(INDEX / "embeddings.npy", embeddings, allow_pickle=False)
    summary = {"documents": len(sources), "passages": len(passages),
               "model_max_seq_length": model.max_seq_length, "special_tokens": special,
               "chunk_content_tokens": settings["chunk_tokens"],
               "target_overlap_tokens": settings["overlap_tokens"],
               "maximum_actual_input_tokens": max(lengths), "embedding_shape": list(embeddings.shape),
               "feedback_footers_removed": sum(a['feedback_footer_removed'] for a in audits),
               "navigation_blocks_removed": sum(a['navigation_blocks_removed'] for a in audits),
               "within_document_duplicate_passages_removed": sum(a.get('duplicate_passages_removed', 0) for a in audits)}
    manifest = {"fingerprint": inputs, "settings": settings, "summary": summary,
                "artifact_sha256": {name: sha256(INDEX / name) for name in (
                    "passages.jsonl", "embeddings.npy", "cleaning_audit.jsonl")}}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
