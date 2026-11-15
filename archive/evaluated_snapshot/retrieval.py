"""Shared passage/document retrieval, also usable from a future app."""
import argparse
import hashlib
import json
import re
from importlib.metadata import version
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "data/index"
SOURCES = ROOT / "data/processed/sources.jsonl"
SETTINGS = ROOT / "retrieval_settings.json"


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_settings():
    return json.loads(SETTINGS.read_text())


def fingerprint():
    """Inputs that must match for index/embedding reuse."""
    return {
        "sources_sha256": sha256(SOURCES), "settings_sha256": sha256(SETTINGS),
        "code_sha256": {name: sha256(ROOT / name) for name in ("build_index.py", "retrieval.py")},
        "versions": {name: version(name) for name in (
            "sentence-transformers", "transformers", "tokenizers", "torch", "numpy", "rank-bm25")},
    }


def load_model(settings):
    # Uses the existing normal Hugging Face cache. No separate cache or new model.
    from sentence_transformers import SentenceTransformer
    import torch
    torch.set_num_threads(4)
    return SentenceTransformer(settings["model"], revision=settings["model_revision"],
                               device=settings["device"], local_files_only=True)


def tokenize(text):
    # N-400 and 5-year stay single tokens; keep numbers and negation words.
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())


def check_lengths(model, texts):
    lengths = [len(ids) for ids in model.tokenizer(
        texts, add_special_tokens=True, truncation=False)["input_ids"]]
    if any(n > model.max_seq_length for n in lengths):
        raise ValueError(f"Input exceeds model limit {model.max_seq_length}; lengths={lengths}")
    return lengths


def rank_documents(passage_results):
    """Use each document's best passage; passage order also resolves exact ties."""
    best = {}
    for row in sorted(passage_results, key=lambda r: (-r["score"], r["doc_id"], r["passage_id"])):
        best.setdefault(row["doc_id"], row)
    return list(best.values())


def source_metrics(ranked_doc_ids, source_doc_id):
    rank = ranked_doc_ids.index(source_doc_id) + 1 if source_doc_id in ranked_doc_ids else None
    return {"source_rank": rank, "recall_at_3": int(rank is not None and rank <= 3),
            "reciprocal_rank": 1.0 / rank if rank else 0.0}


class Retriever:
    def __init__(self):
        self.settings = load_settings()
        self.manifest = json.loads((INDEX / "manifest.json").read_text())
        if self.manifest["fingerprint"] != fingerprint():
            raise ValueError("Index inputs changed; run build_index.py before searching.")
        for name, expected in self.manifest["artifact_sha256"].items():
            if sha256(INDEX / name) != expected:
                raise ValueError(f"Index artifact changed: {name}; rebuild the index.")
        self.passages = read_jsonl(INDEX / "passages.jsonl")
        self.embeddings = np.load(INDEX / "embeddings.npy", allow_pickle=False)
        if self.embeddings.shape != (len(self.passages), 384):
            raise ValueError("Embedding shape does not match passages.")
        if not np.isfinite(self.embeddings).all() or not np.allclose(
                np.linalg.norm(self.embeddings, axis=1), 1, atol=1e-5):
            raise ValueError("Embeddings must be finite unit vectors.")
        self.bm25 = BM25Okapi([tokenize(p["text"]) for p in self.passages], **self.settings["bm25"])
        self.model = None

    def score(self, question, method):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question must be a nonempty string.")
        if method == "bm25":
            return self.bm25.get_scores(tokenize(question))
        if method != "minilm":
            raise ValueError("Method must be bm25 or minilm.")
        if self.model is None:
            self.model = load_model(self.settings)
        check_lengths(self.model, [question])
        vector = self.model.encode([question], normalize_embeddings=True,
                                   convert_to_numpy=True, show_progress_bar=False)[0]
        scores = self.embeddings @ vector
        if not np.isfinite(scores).all():
            raise ValueError("Nonfinite retrieval scores.")
        return scores

    def search(self, question, method="bm25", top_k=3, distinct_documents=False):
        """Return best passages, or best passage per distinct document; None returns all."""
        scores = self.score(question, method)
        rows = [{**p, "score": float(score), "method": method}
                for p, score in zip(self.passages, scores)]
        rows.sort(key=lambda r: (-r["score"], r["doc_id"], r["passage_id"]))
        if distinct_documents:
            rows = rank_documents(rows)
        return rows if top_k is None else rows[:top_k]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    parser.add_argument("--method", choices=["bm25", "minilm"], default="bm25")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--documents", action="store_true", help="Rank distinct source documents")
    args = parser.parse_args()
    print(json.dumps(Retriever().search(args.question, args.method, args.top_k, args.documents),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
