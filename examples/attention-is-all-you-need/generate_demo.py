#!/usr/bin/env python3
"""Generate the under-a-minute Transformer demo without an API key.

Requires `espeak`, `ffmpeg`, and `pydub`. This is a reproducible fallback
for the repository demo; production audio uses the configured TTS provider.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from pydub import AudioSegment

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "script.json"
SELECTED = [0, 1, 4, 5, 14, 15]


def require(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Missing required command: {name}")


def main() -> int:
    require("espeak")
    require("ffmpeg")
    turns = json.loads(SCRIPT.read_text(encoding="utf-8"))
    demo = [turns[i] for i in SELECTED]

    with tempfile.TemporaryDirectory(prefix="research-podcast-demo-") as td:
        td = Path(td)
        parts: list[Path] = []
        for i, turn in enumerate(demo):
            voice = "en-us+m3" if turn["speaker"] == "A" else "en-us+f3"
            speed = "166" if turn["speaker"] == "A" else "160"
            out = td / f"{i:02d}.wav"
            subprocess.run(
                ["espeak", "-v", voice, "-s", speed, "-p", "48", "-a", "165", "-w", str(out), turn["text"]],
                check=True,
            )
            parts.append(out)

        audio = AudioSegment.empty()
        for i, part in enumerate(parts):
            segment = AudioSegment.from_wav(part).high_pass_filter(90).low_pass_filter(7600)
            if i:
                audio += AudioSegment.silent(170 if i % 2 else 220)
            audio += segment.fade_in(15).fade_out(30)

        audio = audio.fade_in(80).fade_out(400)
        out = HERE / "transformer-demo.mp3"
        audio.export(out, format="mp3", bitrate="96k")
        print(f"{out} ({len(audio) / 1000:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
