from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PUNCT_RE = re.compile(r"[，。！？、；：,.!?;:\s]+")
HIGH_RISK_RE = re.compile(
    r"\d|不|没|无|未|不能|可以|必须|只|除外|之前|之后|以上|以下|"
    r"mg|kg|mm|cm|ml|%|％|型号|剂量|金额|日期|截止|负责",
    re.IGNORECASE,
)
HALLUCINATION_RE = re.compile(
    r"字幕由|感谢观看|请点赞|欢迎订阅|下期再见|本视频|版权所有",
    re.IGNORECASE,
)


def normalized(text: str) -> str:
    return PUNCT_RE.sub("", text).lower()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_segments(document: dict[str, Any]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for section in document.get("sections", []):
        for segment in section.get("segments", []):
            item = dict(segment)
            item["_section"] = section.get("title", "")
            segments.append(item)
    return segments


def audit(document: dict[str, Any], quality: dict[str, Any] | None) -> dict[str, Any]:
    segments = flatten_segments(document)
    structural_issues: list[str] = []
    review_warnings: list[str] = []
    unresolved_ids: list[Any] = []
    duplicate_pairs: list[list[Any]] = []
    high_risk: list[dict[str, Any]] = []
    hallucination_candidates: list[Any] = []

    if not segments:
        structural_issues.append("No dialogue segments were found under sections[].segments[].")

    ids: list[Any] = []
    previous_start = -1.0
    previous_normalized = ""
    previous_id: Any = None
    normalized_values: list[str] = []

    for index, segment in enumerate(segments):
        segment_id = segment.get("id", index)
        ids.append(segment_id)
        text = str(segment.get("text", "")).strip()
        speaker = str(segment.get("speaker", "")).strip()
        try:
            start = float(segment.get("start", -1))
        except (TypeError, ValueError):
            start = -1
            structural_issues.append(f"Segment {segment_id} has an invalid start time.")

        if not text:
            structural_issues.append(f"Segment {segment_id} has empty text.")
        if not speaker:
            structural_issues.append(f"Segment {segment_id} has no speaker label.")
        if start < previous_start:
            structural_issues.append(f"Segment {segment_id} is out of chronological order.")
        previous_start = max(previous_start, start)

        compact = normalized(text)
        normalized_values.append(compact)
        if compact and compact == previous_normalized:
            duplicate_pairs.append([previous_id, segment_id])
        previous_normalized = compact
        previous_id = segment_id

        if speaker in {"待确认", "说话人待确认", "未知", "unknown"} or "待确认" in text:
            unresolved_ids.append(segment_id)
        if "�" in text:
            structural_issues.append(f"Segment {segment_id} contains a Unicode replacement character.")
        if HALLUCINATION_RE.search(text):
            hallucination_candidates.append(segment_id)
        if HIGH_RISK_RE.search(text) and len(high_risk) < 40:
            high_risk.append(
                {
                    "id": segment_id,
                    "start": start,
                    "speaker": speaker,
                    "text": text,
                }
            )

    duplicate_ids = [value for value, count in Counter(ids).items() if count > 1]
    if duplicate_ids:
        structural_issues.append(f"Duplicate segment IDs: {duplicate_ids[:20]}")

    text_counts = Counter(value for value in normalized_values if value)
    repeated = sum(count - 1 for count in text_counts.values() if count > 1)
    repeated_ratio = repeated / max(len(normalized_values), 1)
    if duplicate_pairs:
        review_warnings.append(f"Found {len(duplicate_pairs)} consecutive duplicate pairs.")
    if repeated_ratio >= 0.10:
        review_warnings.append(f"Global repeated-segment ratio is {repeated_ratio:.1%}.")
    if unresolved_ids:
        review_warnings.append(f"Found {len(unresolved_ids)} unresolved speaker/text markers.")
    if hallucination_candidates:
        review_warnings.append("Found phrases commonly associated with ASR hallucination; listen again.")

    quality_suspicious = bool(quality and quality.get("suspicious"))
    if quality_suspicious:
        reasons = quality.get("reasons") or []
        review_warnings.append("Raw-transcript quality gate was suspicious: " + "; ".join(map(str, reasons)))

    structural_valid = not structural_issues
    ready_for_handoff = bool(
        structural_valid
        and not unresolved_ids
        and not duplicate_pairs
        and not hallucination_candidates
        and not quality_suspicious
    )
    return {
        "structural_valid": structural_valid,
        "ready_for_handoff": ready_for_handoff,
        "segment_count": len(segments),
        "structural_issues": structural_issues,
        "review_warnings": review_warnings,
        "unresolved_segment_ids": unresolved_ids[:200],
        "consecutive_duplicate_pairs": duplicate_pairs[:100],
        "repeated_segment_ratio": round(repeated_ratio, 4),
        "hallucination_candidate_ids": hallucination_candidates[:100],
        "high_risk_listening_checklist": high_risk,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a structured cleaned transcript before handoff.")
    parser.add_argument("transcript", type=Path, help="Path to cleaned_transcript.json")
    parser.add_argument("--quality-report", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    document = read_json(args.transcript)
    quality = read_json(args.quality_report) if args.quality_report else None
    report = audit(document, quality)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report["structural_valid"] else 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())

