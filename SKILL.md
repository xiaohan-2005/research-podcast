---
name: research-podcast
description: Turn papers, PDFs, reports, lecture notes, datasets, or research material into an evidence-aware AI podcast for deep dives, exam review, defense rehearsal, or multi-source briefings.
---

# Research Podcast

Turn research into a listenable conversation while preserving a traceable chain from source evidence to spoken claims.

## Paths
- `SKILL_DIR`: directory containing this file.
- `DATA_DIR`: `${RESEARCH_PODCAST_HOME:-~/.research-podcast}`.

Read `QUALITY_RULES.md` before drafting and `PROMPT.md` for dialogue style.

## Workflow

### 1. Read the material
Accept pasted text, local research files, accessible URLs, or multiple sources. If material is already supplied, do not ask for it again.

### 2. Build a source map
Create `DATA_DIR/runs/<run-id>/source_map.json` with stable IDs such as `S01`. Each entry should include the source label, location when known, a factual summary, and minimal supporting evidence. Never invent page numbers or locations.

### 3. Choose a mode
Use the user's requested mode; otherwise default to `deep-dive`.
Supported modes: `deep-dive`, `exam-review`, `defense`, `briefing`.

### 4. Write the script
Follow `PROMPT.md` and save valid JSON to `DATA_DIR/runs/<run-id>/script.json`.
Every factual or interpretive turn must carry supporting `source_ids`.

### 5. Validate
Run:
```bash
python SKILL_DIR/scripts/validate_script.py \
  --script DATA_DIR/runs/<run-id>/script.json \
  --sources DATA_DIR/runs/<run-id>/source_map.json
```
Fix all validation errors before audio generation.

### 6. Generate audio when requested
Use the local configuration in `DATA_DIR/config.yaml` and secrets in `DATA_DIR/.env`. Never place secrets in the repository or ask users to paste them into chat.

Run:
```bash
DATA_DIR/venv/bin/python SKILL_DIR/scripts/speak.py \
  --script DATA_DIR/runs/<run-id>/script.json
```

The audio generator writes an MP3 under `DATA_DIR/episodes/`.

## Completion checks
Before finishing, confirm that:
1. the source map exists;
2. the script validates;
3. factual claims are traceable;
4. no secret appears in tracked outputs;
5. requested audio exists and is non-empty.

## Example requests
- “把这篇论文做成 8 分钟中文 deep-dive，重点讲方法和局限。”
- “把这一章做成 exam-review，多问几个易错点。”
- “把我的建模论文做成 defense，一个主持人汇报，一个像评委追问。”
- “比较这三篇论文，只讨论真正有证据支持的分歧。”
