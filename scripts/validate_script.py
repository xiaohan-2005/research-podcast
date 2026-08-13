from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_SPEAKERS = {"A", "B"}
ALLOWED_TYPES = {"fact", "interpretation", "question", "transition"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate(script_path: Path, sources_path: Path) -> list[str]:
    errors: list[str] = []
    script = load_json(script_path)
    sources = load_json(sources_path)

    if not isinstance(script, list) or len(script) < 2:
        return ["script must be a JSON array with at least two turns"]
    if not isinstance(sources, list):
        return ["sources must be a JSON array"]

    source_ids = {
        item.get("id") for item in sources
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    for i, item in enumerate(script):
        if not isinstance(item, dict):
            errors.append(f"script[{i}] must be an object")
            continue

        speaker = item.get("speaker")
        text = item.get("text")
        refs = item.get("source_ids")
        claim_type = item.get("claim_type")

        if speaker not in ALLOWED_SPEAKERS:
            errors.append(f"script[{i}]: invalid speaker")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"script[{i}]: text must be non-empty")
        if claim_type not in ALLOWED_TYPES:
            errors.append(f"script[{i}]: invalid claim_type")
        if not isinstance(refs, list) or not all(isinstance(x, str) for x in refs):
            errors.append(f"script[{i}]: source_ids must be a string array")
            continue

        missing = [ref for ref in refs if ref not in source_ids]
        if missing:
            errors.append(f"script[{i}]: unknown source_ids {missing}")
        if claim_type in {"fact", "interpretation"} and not refs:
            errors.append(f"script[{i}]: {claim_type} requires source_ids")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an evidence-aware podcast script")
    parser.add_argument("--script", required=True, type=Path)
    parser.add_argument("--sources", required=True, type=Path)
    args = parser.parse_args()

    errors = validate(args.script, args.sources)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
