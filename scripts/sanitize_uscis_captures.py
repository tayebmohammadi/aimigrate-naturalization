"""Save safe public derivatives of USCIS HTML captures.

Original bytes are kept in a private home-directory archive. Run this file
with capture paths, or without arguments to scan the Stage 5 HTML archives.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_ROOT = Path.home() / ".local/share/aimigrate-private/uscis-html-captures"
FIELD = "apiKey_aao_pm_search"
MARKER = b"<!-- Sanitized USCIS derivative: upstream client-side configuration values removed where present. -->\n"
SETTINGS_SCRIPT = re.compile(
    rb"<script[^>]*data-drupal-selector=[\"']drupal-settings-json[\"'][^>]*>(.*?)</script>",
    re.DOTALL,
)
FIELD_VALUE = re.compile(rb'("apiKey_aao_pm_search"\s*:\s*")[^"\\]*(")')
GOOGLE_KEY = re.compile(rb"AIza[0-9A-Za-z_-]{35}")
OTHER_CREDENTIALS = {
    "AWS access key": re.compile(rb"(?:AKIA|ASIA)[A-Z0-9]{16}"),
    "GitHub token": re.compile(rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})"),
    "OpenAI-style key": re.compile(rb"sk-[A-Za-z0-9]{20,}"),
    "Slack token": re.compile(rb"xox[baprs]-[A-Za-z0-9-]{20,}"),
    "Private key block": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def has_public_marker(raw):
    """Tell whether a page is already a labeled sanitized derivative."""
    return MARKER in raw


def sha256(data):
    """Return the SHA-256 digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def sanitize_capture(raw):
    """Redact the named USCIS page setting and label the public derivative."""
    if has_public_marker(raw):
        if GOOGLE_KEY.search(raw) or any(pattern.search(raw) for pattern in OTHER_CREDENTIALS.values()):
            raise ValueError("A credential-like pattern remains in an already labeled capture.")
        return raw, False
    if any(pattern.search(raw) for pattern in OTHER_CREDENTIALS.values()):
        raise ValueError("A credential-like value needs manual review before publication.")

    matches = list(SETTINGS_SCRIPT.finditer(raw))
    redacted = False
    if len(matches) > 1:
        raise ValueError("More than one Drupal settings block; inspect this capture manually.")
    if matches:
        match = matches[0]
        settings_bytes = match.group(1)
        try:
            settings = json.loads(settings_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("The Drupal settings block could not be parsed safely.") from error

        config = settings.get("uscis_design", {})
        if FIELD in config:
            value = config[FIELD]
            if not isinstance(value, str):
                raise ValueError("The USCIS setting is not a string; inspect this capture manually.")
            fields = list(FIELD_VALUE.finditer(settings_bytes))
            if len(fields) != 1:
                raise ValueError("The USCIS setting could not be isolated safely.")
            value_bytes = value.encode("utf-8")
            key_matches = list(GOOGLE_KEY.finditer(raw))
            if key_matches and (len(key_matches) != 1 or key_matches[0].group(0) != value_bytes):
                raise ValueError("An additional Google-key pattern needs manual review.")

            safe_settings = FIELD_VALUE.sub(
                rb'\1[redacted upstream page configuration]\2', settings_bytes, count=1
            )
            try:
                safe_config = json.loads(safe_settings.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ValueError("The redacted settings block did not remain valid JSON.") from error
            if safe_config.get("uscis_design", {}).get(FIELD) != "[redacted upstream page configuration]":
                raise ValueError("The redacted setting did not pass its structure check.")
            raw = raw[:match.start(1)] + safe_settings + raw[match.end(1):]
            redacted = True

    if GOOGLE_KEY.search(raw):
        raise ValueError("A Google-key pattern remains outside the targeted page setting.")
    if FIELD.encode() in raw and not matches:
        raise ValueError("The named setting is outside a recognized Drupal block; inspect manually.")

    doctype = re.search(rb"<!doctype[^>]*>", raw, re.IGNORECASE)
    if doctype:
        raw = raw[:doctype.end()] + b"\n" + MARKER + raw[doctype.end():]
    else:
        raw = MARKER + raw
    return raw, redacted


def private_original_path(project_path, private_dir):
    """Map a project HTML path to its matching private archive path."""
    try:
        relative = project_path.resolve().relative_to(ROOT)
    except ValueError as error:
        raise ValueError("Only files inside this project can be sanitized.") from error
    return private_dir / relative


def preserve_original(project_path, raw, private_dir):
    """Keep exact original bytes outside Git before changing the public copy."""
    target = private_original_path(project_path, private_dir)
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(target.parent, 0o700)
    if target.exists():
        if target.read_bytes() == raw:
            return target
        target = target.with_name(f"{target.stem}-{sha256(raw)[:12]}{target.suffix}")
    target.write_bytes(raw)
    os.chmod(target, 0o600)
    return target


def update_access_records(changes):
    """Keep capture logs clear about original and sanitized HTML hashes."""
    logs = [
        ROOT / "results/stage5/current_page_access.jsonl",
        ROOT / "results/stage5/assisted_reference_verification/live_pages/access_records.jsonl",
        ROOT / "results/stage5/final_reference_verification_2026-11-15/access_records.jsonl",
    ]
    by_path = {item["path"]: item for item in changes}
    for log in logs:
        if not log.exists():
            continue
        updated = []
        changed = False
        for line in log.read_text().splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            recorded = record.get("html_file")
            candidates = set()
            if recorded:
                relative = Path(recorded)
                candidates.add(relative.as_posix())
                candidates.add((Path("results/stage5") / relative).as_posix())
            item = next((by_path[candidate] for candidate in candidates if candidate in by_path), None)
            if item:
                previous_hash = record.get("original_html_sha256") or record.get("html_sha256")
                if previous_hash != item["original_sha256"] or record.get("html_sha256") not in (
                    item["original_sha256"], item["sanitized_sha256"]
                ):
                    raise ValueError(f"Capture log hash did not match its original: {recorded}")
                record["original_html_sha256"] = item["original_sha256"]
                record["html_sha256"] = item["sanitized_sha256"]
                record["html_sanitized_derivative"] = True
                record["redacted_config_fields"] = [f"uscis_design.{FIELD}"]
                changed = True
            updated.append(json.dumps(record, ensure_ascii=False))
        if changed:
            log.write_text("\n".join(updated) + "\n")


def update_public_manifest(changes):
    """Add sanitized derivatives without dropping earlier hash records."""
    report = ROOT / "results/stage5/public_html_redaction"
    report.mkdir(parents=True, exist_ok=True)
    path = report / "redaction_manifest.json"
    if path.exists():
        manifest = json.loads(path.read_text())
    else:
        manifest = {
            "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "reviewer": "OpenAI Codex (coding assistant)",
            "description": "Public derivative hash crosswalk; exact pre-redaction files are preserved outside the repository.",
            "redacted_setting": f"uscis_design.{FIELD}",
            "files": [],
        }
    known = {(item["path"], item["sanitized_sha256"]) for item in manifest["files"]}
    for item in changes:
        key = (item["path"], item["sanitized_sha256"])
        if key not in known:
            manifest["files"].append(item)
            known.add(key)
    manifest["capture_count"] = len(manifest["files"])
    manifest["updated_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    path.write_text(json.dumps(manifest, indent=2) + "\n")


def sanitize_file(path, private_dir):
    """Preserve, sanitize, and hash one tracked HTML capture."""
    path = Path(path).resolve()
    if path.suffix.lower() != ".html" or not path.is_file():
        raise ValueError("Provide an existing HTML capture file.")
    raw = path.read_bytes()
    safe, redacted = sanitize_capture(raw)
    if not redacted:
        return None
    preserve_original(path, raw, private_dir)
    path.write_bytes(safe)
    return {
        "path": str(path.relative_to(ROOT)),
        "original_sha256": sha256(raw),
        "sanitized_sha256": sha256(safe),
        "redacted_config_fields": [f"uscis_design.{FIELD}"],
        "original_preserved_privately": True,
    }


def main():
    """Sanitize selected captures and write a hash crosswalk for review."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="HTML captures; default scans the Stage 5 page archives")
    parser.add_argument("--private-dir", type=Path, default=None)
    args = parser.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    private_dir = args.private_dir or (PRIVATE_ROOT / stamp)
    private_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(private_dir, 0o700)
    paths = [Path(value) if Path(value).is_absolute() else ROOT / value for value in args.paths]
    if not paths:
        folders = [
            ROOT / "results/stage5/current_pages",
            ROOT / "results/stage5/assisted_reference_verification/live_pages",
            ROOT / "results/stage5/final_reference_verification_2026-11-15/live_pages",
        ]
        paths = sorted(path for folder in folders for path in folder.rglob("*.html"))
    changes = [item for path in paths if (item := sanitize_file(path, private_dir))]
    update_public_manifest(changes)
    saved_manifest = json.loads((ROOT / "results/stage5/public_html_redaction/redaction_manifest.json").read_text())
    update_access_records(saved_manifest["files"])
    print(f"Sanitized {len(changes)} new USCIS HTML captures; original files were preserved privately.")


if __name__ == "__main__":
    main()
