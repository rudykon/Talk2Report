---
name: talk2report
description: Turn audio or video recordings into polished, fact-preserving dialogue reports with timestamps, speaker labels, corrected Chinese text, topic sections, key conclusions, explicit action items, and a review trail. Use Talk2Report for interviews, meetings, product research, clinical discussions, usability sessions, podcasts, requests such as “把这个音频整理成校对好的对话文档”, or any task to transcribe, organize, proofread, and deliver a recording as DOCX, PDF, Markdown, text, or structured JSON.
---

# Talk2Report

Produce a readable document without hiding uncertainty or inventing facts. Keep the raw transcription and quality evidence separate from the edited deliverable.

## Start the job

1. Identify the source recording and requested output. If the user only says “这个音频”, use the single obvious audio/video file in scope; ask only when multiple plausible files remain.
2. Default to the recording's dominant language, a Word document, and the filename `<source>_整理校对对话稿.docx` when the user gives no format preference.
3. Preserve existing artifacts. Reuse raw segments or resumable pipeline output when they clearly belong to the same source recording.
4. Record the source filename, duration, processing date, known participants, and any terminology supplied by the user.

## Choose the transcription path

- Prefer an existing local, resumable pipeline when the workspace contains `audio_transcript_agent/scripts/run.ps1`. Run `scripts/run_local_pipeline.ps1` from this skill to discover and invoke it.
- Otherwise use the best available transcription capability. Prefer timestamped segments and confidence data. Do not download large models, upload confidential audio, or call a paid service without authorization.
- Treat text-based speaker assignment as inference, not voiceprint diarization. Use actual diarization output only when a diarization engine was run.
- If no transcription engine is available, report the exact missing capability and leave any already-created artifacts intact.

## Execute the workflow

### 1. Inspect and prepare the recording

- Probe duration, codec, sample rate, channel count, and channel energy before transcription.
- For split-channel recordings, select or mix channels deliberately. Never assume stereo means two speakers.
- Convert to a transcription-friendly working file without overwriting the source.

### 2. Create an immutable raw transcript

- Transcribe into segments with stable IDs, start/end times, raw text, and confidence fields when available.
- Disable context carryover or use VAD when repeated hallucinations appear around silence, music, or noise.
- Save raw segments before any editorial changes.

### 3. Apply a quality gate

- Check consecutive duplicates, global duplicate ratio, repeated character n-grams, low-confidence regions, long gaps, and unexpected language changes.
- Retry only when the expected quality gain justifies the time and cost. Keep both passes and select the better one using recorded criteria.
- Run `scripts/audit_transcript.py` on structured output. Treat its high-risk excerpts as a listening checklist, not proof of an error.

### 4. Edit conservatively

- Read [references/editorial-policy.md](references/editorial-policy.md) before substantial cleanup.
- Correct punctuation, sentence boundaries, obvious homophone errors, spacing, capitalization, abbreviations, and consistent terminology.
- Merge adjacent fragments from the same speaker when they form one thought; keep the earliest timestamp.
- Remove filler, repeated starts, and operational noise only when meaning, emphasis, uncertainty, and interpersonal intent remain unchanged.
- Never add facts, reasons, owners, dates, quantities, diagnoses, decisions, or commitments not supported by the recording.
- Mark unresolved audio explicitly, for example `〔听不清，00:12:34〕` or `〔术语待确认：原音近似为…〕`.

### 5. Assign speakers carefully

- Use names or roles supplied by the user, stated in the recording, or strongly supported by context.
- Use stable functional labels such as `访谈者`, `受访者`, `医生`, or `产品人员` when names are unknown.
- Use `待确认` when evidence is insufficient. Do not alternate labels merely to make a dialogue look tidy.
- Flag overlapping speech and short ambiguous replies for review.

### 6. Organize the document

- Group the conversation by real topic changes rather than fixed time windows when making the final document.
- Format each turn as `[HH:MM:SS]  角色：文本`.
- Add `关键结论与待办` only after the dialogue. Separate confirmed decisions, explicit action items, and editorially inferred themes.
- Do not invent an owner or deadline. Write `负责人待确认` or omit the field when the recording does not provide it.
- Follow [references/output-specification.md](references/output-specification.md) for document structure and filenames.

### 7. Verify against the audio

- Listen again to low-confidence segments and all passages containing names, product terms, medical/legal/financial terminology, numbers, dates, units, model numbers, and negation words.
- Spot-check the beginning, middle, and end even when confidence is high.
- Reconcile timestamps after merging segments and confirm that chronological order is preserved.
- Keep an unresolved-items list instead of silently guessing.

### 8. Build and inspect the deliverable

- For DOCX output, use the available document-creation workflow and render the file to page images for visual inspection.
- Check title hierarchy, line wrapping, page breaks, timestamp alignment, speaker-label consistency, headers/footers, table of contents, and the final page.
- For PDF output, verify page count, extractable text, expected title/source terms, and absence of replacement characters.
- Deliver the polished document together with a concise note about unresolved items and the degree of speaker certainty.

## Completion standard

Call the transcript “整理校对完成” only when:

- the full recording is covered or omissions are disclosed;
- raw and edited text are separately preserved;
- suspicious and low-confidence regions were reviewed or listed;
- speaker uncertainty is visible;
- high-risk terms, numbers, and negations were checked;
- summaries and action items are traceable to the dialogue;
- the final document was opened or rendered and visually inspected.
