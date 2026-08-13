# Under-a-minute audio demo

This case includes a **zero-key, reproducible two-host audio demo** built from the evidence-grounded Transformer script.

The demo selects six turns from `script.json` covering the paper's central architecture claim (`S01`), the scaled-attention explanation (`S02`), and the reported 28.4 BLEU result (`S07`).

Reference run: **54.3 seconds**.

From the repository root:

```bash
python scripts/validate_script.py \
  --script examples/attention-is-all-you-need/script.json \
  --sources examples/attention-is-all-you-need/source_map.json

python examples/attention-is-all-you-need/generate_demo.py
```

The second command requires local `espeak`, `ffmpeg`, and the repository Python requirements. It writes:

```text
examples/attention-is-all-you-need/transformer-demo.mp3
```

This local eSpeak version exists so the demo is reproducible without an API key. For production-quality voices, use `scripts/speak.py` with the configured TTS provider.
