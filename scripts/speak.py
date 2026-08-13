from __future__ import annotations

import argparse
import getpass
import json
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import httpx
from pydub import AudioSegment

from utils import data_dir, ensure_output_dirs, load_config

TTS_URL = "https://api.fish.audio/v1/tts"


def require_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg was not found on PATH")
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg could not be executed")


def read_script(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, list) or not value:
        raise ValueError("script must be a non-empty JSON array")
    return value


def voice_for(segment: dict, cfg: dict) -> str:
    tts = cfg.get("tts", {})
    key = "host_a_voice_id" if segment.get("speaker") == "A" else "host_b_voice_id"
    voice_id = str(tts.get(key, "")).strip()
    if not voice_id:
        raise RuntimeError(f"Missing tts.{key} in config.yaml")
    return voice_id


def synthesize(text: str, voice_id: str, cfg: dict, client: httpx.Client, api_key: str) -> bytes:
    tts = cfg.get("tts", {})
    response = client.post(
        TTS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "text": text,
            "reference_id": voice_id,
            "format": "mp3",
            "mp3_bitrate": int(tts.get("bitrate_kbps", 128)),
            "temperature": float(tts.get("temperature", 0.7)),
            "top_p": float(tts.get("top_p", 0.7)),
            "normalize": True,
        },
    )
    if response.status_code != 200:
        raise RuntimeError(f"TTS request failed with status {response.status_code}")
    return response.content


def generate(script_path: Path) -> Path:
    cfg = load_config()
    ensure_output_dirs()
    require_ffmpeg()
    script = read_script(script_path)
    api_key = getpass.getpass("Fish Audio API key: ").strip()
    if not api_key:
        raise RuntimeError("API key is required")

    pause_ms = int(cfg.get("tts", {}).get("pause_ms", 260))
    combined = AudioSegment.empty()
    gap = AudioSegment.silent(duration=pause_ms)

    with tempfile.TemporaryDirectory(prefix="research-podcast-") as tmp, httpx.Client(timeout=120) as client:
        for index, segment in enumerate(script):
            text = str(segment.get("text", "")).strip()
            if not text:
                raise ValueError(f"Empty text at script index {index}")
            audio = synthesize(text, voice_for(segment, cfg), cfg, client, api_key)
            part = Path(tmp) / f"part-{index:04d}.mp3"
            part.write_bytes(audio)
            if index:
                combined += gap
            combined += AudioSegment.from_file(part, format="mp3")

    combined = combined.fade_in(350).fade_out(700)
    out = data_dir() / "episodes" / f"episode-{datetime.now():%Y%m%d-%H%M%S}.mp3"
    combined.export(out, format="mp3", bitrate=f"{int(cfg.get('tts', {}).get('bitrate_kbps', 128))}k")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate podcast audio from a validated script")
    parser.add_argument("--script", required=True, type=Path)
    args = parser.parse_args()
    print(generate(args.script))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
