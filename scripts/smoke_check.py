"""Check required imports and the cached MiniLM model. Run with `python -m scripts.smoke_check` from the project root."""
import json
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas
import pyarrow
import rank_bm25
import streamlit
from sentence_transformers import SentenceTransformer


def main():
    """Import required packages and encode two short sentences with MiniLM on CPU."""
    revision = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu",
                                revision=revision)
    embeddings = model.encode(["How do I apply for naturalization?",
                               "What is the citizenship interview?"], convert_to_numpy=True)
    assert embeddings.shape == (2, 384)
    assert np.isfinite(embeddings).all()
    result = {"model": "sentence-transformers/all-MiniLM-L6-v2", "device": str(model.device),
              "revision": revision,
              "shape": list(embeddings.shape), "all_finite": bool(np.isfinite(embeddings).all()),
              "versions": {p: version(p) for p in ["pandas", "pyarrow", "rank-bm25",
                  "sentence-transformers", "streamlit", "torch", "numpy", "transformers"]}}
    path = Path(__file__).resolve().parent.parent / "data/processed/smoke_check.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
