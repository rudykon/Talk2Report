# Editorial policy

## Source-of-truth order

Use this priority when evidence conflicts:

1. Audible recording
2. User-provided names, terminology, and context
3. Raw timestamped ASR segments
4. Edited transcript
5. Summary and action items

Never use a summary to “correct” the dialogue. A plausible sentence is not evidence that it was spoken.

## Allowed edits

- Add Chinese punctuation and sentence boundaries.
- Normalize full-width/half-width punctuation, spaces, capitalization, and common abbreviations.
- Correct an obvious recognition error when sound and context both support one reading.
- Join fragments from the same speaker when they express one continuous thought.
- Remove empty fillers and exact repetitions when they carry no meaning.
- Replace irrelevant operational noise with a short neutral marker when it matters to the flow, such as `〔现场操作〕`.

## Edits requiring caution

- Keep hedges such as “可能”, “大概”, “我觉得”, and “不一定” when they affect certainty.
- Keep negations and restrictions exactly: “不”, “没”, “未”, “只能”, “不能”, “不需要”.
- Keep corrections made by the speaker when the correction itself matters.
- Preserve meaningful hesitation, disagreement, politeness, or emphasis in interviews and research sessions.
- Do not silently expand acronyms unless the expansion is known from the recording or user context.
- Do not standardize a product or person name solely because a familiar name looks similar.

## Forbidden edits

- Do not fabricate missing words to make a sentence fluent.
- Do not change an opinion into a decision or a suggestion into a commitment.
- Do not infer an owner, deadline, diagnosis, dosage, amount, model number, or metric.
- Do not merge turns across different speakers.
- Do not hide uncertainty by choosing the most likely speaker or term.
- Do not delete off-topic passages without disclosing the omission when the user requested a complete transcript.

## Uncertainty notation

Use concise, searchable markers:

- `〔听不清，00:12:34〕`
- `〔多人重叠〕`
- `〔说话人待确认〕`
- `〔术语待确认：原音近似为“Holo-D”〕`
- `〔数字待复核：原音可能为 15 或 50〕`

Do not use an uncertainty marker as a substitute for listening again when the audio is available.

## Speaker policy

- Prefer real names only when introduced, user-supplied, or repeatedly confirmed by context.
- Prefer functional roles when identity is unnecessary.
- Keep one label per person throughout the document.
- When diarization and textual inference disagree, review the audio before choosing.
- Mark short acknowledgements such as “嗯”, “对”, and “好” as ambiguous unless turn-taking is clear.

## Summary and action-item policy

Separate these categories:

- **Confirmed conclusion:** directly agreed or stated as the result.
- **Explicit action item:** a clear commitment or request to do something.
- **Theme or suggestion:** an editorial synthesis; label it as a summary, not a decision.

For each action item, include only fields supported by speech. Omit owner and due date when absent. Keep a timestamp or section reference when practical.

## High-risk review

Always re-listen to passages containing:

- names, brands, products, places, and abbreviations;
- medical, legal, financial, scientific, or engineering terminology;
- numbers, dates, times, units, percentages, prices, doses, and model identifiers;
- negation, comparison, exceptions, and causal claims;
- decisions, approvals, promises, deadlines, and responsibility assignments.

