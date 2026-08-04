# Output specification

## Default package

Create these artifacts when the available tooling supports them:

- `<source>_整理校对对话稿.docx` — polished, user-facing document
- `<source>_cleaned_transcript.json` — structured edited dialogue and provenance
- `<source>_transcript_audit.json` — structural and review audit
- Optional `<source>_整理校对对话稿.pdf` — fixed-layout copy when requested

Keep raw ASR output and prepared audio inside a run/work directory rather than mixing them with final deliverables.

## Document structure

1. Title: `<source>｜整理校对对话稿`
2. Descriptive subtitle when the subject is clear
3. Metadata:
   - source recording
   - duration
   - participants/roles
   - processing date
   - scope and editorial note
4. `整理后的对话`
5. Topic sections in chronological order
6. Timecoded dialogue turns: `[HH:MM:SS]  角色：文本`
7. `关键结论与待办`
8. `待复核事项`, when any uncertainty remains

## Formatting guidance

- Use a clean professional Chinese font and restrained color accents.
- Make topic headings visually distinct without turning every turn into a heading.
- Keep timestamps visually quiet but readable.
- Distinguish speakers consistently with label color or bold text; do not rely on color alone.
- Avoid dense tables for the main dialogue. Tables are acceptable for a compact action-item register.
- Prevent headings from being orphaned at the bottom of a page.
- Include page numbers for documents longer than two pages.

## Structured JSON shape

Prefer this conceptual schema while retaining any richer fields from the transcription engine:

```json
{
  "source_name": "recording.mp3",
  "duration_seconds": 1847.2,
  "editorial_note": "...",
  "sections": [
    {
      "title": "主题",
      "segments": [
        {
          "id": 1,
          "start": 14.2,
          "end": 31.8,
          "speaker": "产品人员",
          "text": "校对后的文本。",
          "confidence": null,
          "review_status": "verified"
        }
      ]
    }
  ],
  "conclusions": [],
  "actions": [],
  "unresolved": []
}
```

## Handoff note

State:

- what portion of the recording was processed;
- whether speaker labels came from diarization, context inference, or user input;
- whether low-confidence/high-risk passages were listened to;
- which terms or passages remain unresolved;
- which deliverables were visually inspected.

