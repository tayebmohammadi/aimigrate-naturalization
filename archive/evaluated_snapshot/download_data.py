"""Download the three public data files at a fixed revision; verify hashes."""
import hashlib
import json
import ssl
import certifi
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
REVISION = "f25cc4476b6e45b20e3d0d3f6f7aeb50efb8dc6f"
BASE = f"https://huggingface.co/datasets/nshportun/usa-immigration-law-qa/resolve/{REVISION}"


def main():
    raw = ROOT / "data/raw"
    raw.mkdir(parents=True, exist_ok=True)
    tree = json.loads((raw / "repository-tree.json").read_text())
    for entry in tree:
        name = entry["path"]
        if not (name.endswith(".parquet") or name == "README.md"):
            continue
        target = raw / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            print(f"Downloading {name}: {entry['size']:,} bytes", flush=True)
            with urlopen(f"{BASE}/{name}", timeout=120,
                         context=ssl.create_default_context(cafile=certifi.where())) as response:
                content = response.read()
            target.write_bytes(content)
        content = target.read_bytes()
        assert len(content) == entry["size"], f"Size mismatch: {name}"
        if "lfs" in entry:
            assert hashlib.sha256(content).hexdigest() == entry["lfs"]["oid"], name
        print(f"Verified {name}")


if __name__ == "__main__":
    main()
