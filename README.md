# Research Podcast

**Turn research into audio without turning evidence into vibes.**

Research Podcast is an agent skill for Codex-compatible skill workflows. It converts papers, PDFs, reports, lecture notes, or multiple research sources into natural AI podcast conversations while preserving a source-to-claim trail.

## Why it is different
Most “document to podcast” workflows optimize for fluency. This project adds a verification layer:

`source -> source map -> cited dialogue turn -> validated script -> TTS`

That makes it useful for research papers, exam revision, literature comparison, and defense rehearsal where an engaging hallucination is still a bad result.

## Modes
- **deep-dive** — explain problem, method, evidence, meaning, limitations
- **exam-review** — teach concepts, traps, recall questions, recap
- **defense** — presentation plus skeptical committee-style questioning
- **briefing** — multi-source, decision-oriented synthesis

## Repository structure
```text
research-podcast/
├── SKILL.md
├── PROMPT.md
├── QUALITY_RULES.md
├── AGENTS.md
├── config/
│   └── config.example.yaml
├── schemas/
│   └── podcast-script.schema.json
├── scripts/
│   ├── requirements.txt
│   ├── utils.py
│   ├── validate_script.py
│   └── speak.py
└── examples/
    ├── source.md
    ├── source_map.json
    └── script.json
```

## Quick test
```bash
python -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/validate_script.py \
  --script examples/script.json \
  --sources examples/source_map.json
```

Expected output:
```text
Validation passed.
```

## Audio setup
Copy the example config into your local data directory and keep the API key in `.env`, never in the repository.

```bash
mkdir -p ~/.research-podcast
cp config/config.example.yaml ~/.research-podcast/config.yaml
printf 'FISH_API_KEY=replace_me\n' > ~/.research-podcast/.env
```

Then set `host_a_voice_id` and `host_b_voice_id` in the local config. Fish Audio TTS is intentionally isolated in `scripts/speak.py`, so another provider can be added later without rewriting the skill workflow.

## Example prompts
```text
把这篇论文做成 10 分钟中文播客，deep-dive，重点讲研究设计和限制。

把这三篇论文做成 briefing，找出真正有证据支持的分歧。

把这一章做成 exam-review，主持人要不断问我容易混淆的点。

把我的建模论文做成 defense，一个主持人汇报，一个像评委追问。
```

## Design philosophy
The agent writes the research-aware script; deterministic code validates its structure and generates audio. This keeps reasoning in the agent and repeatable mechanics in scripts.

## Security
- Never commit API keys.
- Never ask users to paste secrets into chat.
- Keep user runs under `~/.research-podcast` rather than the skill repository.
