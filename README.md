# Talk2Report

Turn audio or video recordings into polished, fact-preserving dialogue reports.

`Talk2Report` contains the Codex skill `audio-to-polished-dialogue`. It is designed for interviews, meetings, product research, clinical discussions, usability sessions, podcasts, and other recordings that need to become readable, reviewable documents.

## What it does

- Transcribes recordings into timestamped segments.
- Preserves raw transcription separately from editorial changes.
- Corrects punctuation, sentence boundaries, obvious recognition errors, and terminology consistently.
- Assigns stable speaker labels without pretending uncertain identities are known.
- Organizes dialogue by topic while preserving chronological order.
- Extracts confirmed conclusions and explicit action items without inventing owners or deadlines.
- Flags unclear audio, risky terms, numbers, dates, negations, and suspected ASR hallucinations for review.
- Supports polished DOCX, PDF, Markdown, text, and structured JSON deliverables.

## Repository layout

```text
audio-to-polished-dialogue/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── editorial-policy.md
│   └── output-specification.md
└── scripts/
    ├── audit_transcript.py
    └── run_local_pipeline.ps1
```

## Install as a Codex skill

Copy the `audio-to-polished-dialogue` directory into your Codex skills directory:

```text
~/.codex/skills/audio-to-polished-dialogue
```

Then invoke it with a request such as:

```text
Use $audio-to-polished-dialogue to turn this recording into a polished, timestamped dialogue document.
```

中文示例：

```text
使用 $audio-to-polished-dialogue，把这个音频整理成带时间戳、说话人、关键结论和待办事项的校对对话文档。
```

## Editorial principle

The recording remains the source of truth. The skill improves readability while preserving facts, uncertainty, emphasis, negation, and interpersonal intent. It never fills gaps merely to make the conversation sound smoother.

