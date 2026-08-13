# Polished showcase

For a public-facing sample, use the production TTS path with the two conversational voice references stored in `showcase_voices.yaml`.

- Host A: Youthful Conversationalist — lively, educational male delivery.
- Host B: Friendly English Host — warm, professional female delivery for podcast and educational material.

These are optional showcase defaults. Replace either voice freely and review the provider usage terms before publishing externally.

Use the standard Transformer case script and the existing production audio workflow in `scripts/speak.py`. The zero-key `generate_demo.py` remains the reproducibility fallback; the production path is intended for presentation-quality audio.
