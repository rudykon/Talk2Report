[English](README.md) · **简体中文**

<p align="center">
  <img src="docs/brand-mark.svg" width="520" alt="Talk2Report 品牌标识">
</p>

# Talk2Report

**以事实为准的音频转报告流程：保守校对、质量门控、全程可追溯**

一个公开的 Codex Skill，用于将访谈、会议、产品调研、临床讨论、可用性测试、播客等音频或视频录制整理成专业、可复核、带时间戳的对话文档。

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-412991?logo=openai&logoColor=white)](talk2report/SKILL.md)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](talk2report/scripts/audit_transcript.py)
[![PowerShell Pipeline](https://img.shields.io/badge/PowerShell-Local%20Pipeline-5391FE?logo=powershell&logoColor=white)](talk2report/scripts/run_local_pipeline.ps1)
[![输出格式](https://img.shields.io/badge/Outputs-DOCX%20%7C%20PDF%20%7C%20JSON-2E7D32)](#输出文件)

[项目概览](#项目概览) · [处理流程](#处理流程) · [流程图](#流程图) · [快速开始](#快速开始) · [质量验证](#质量验证) · [校对原则](#校对原则) · [仓库结构](#仓库结构)

---

## 项目概览

本仓库提供 [`Talk2Report`](talk2report/SKILL.md) Codex Skill，负责协调录音检查、转写、质量审核、保守校对、说话人标注、主题整理、高风险片段复听和最终文档检查。

> [!IMPORTANT]
> Talk2Report 是转写编排与编辑校对 Skill。它会使用当前工作环境中可用的最佳转写能力，但不自带语音识别模型，也不会在未经授权的情况下把录音上传到外部服务。

| 目标 | 实现方式 | 公开依据 |
|---|---|---|
| 生成易读、可追溯的对话报告 | 时间戳、稳定说话人标签、主题分节、结论与明确待办 | [`SKILL.md`](talk2report/SKILL.md) |
| 忠实保留原始表达 | 原始转写不可变、保守校对规则、显式不确定性标记 | [`editorial-policy.md`](talk2report/references/editorial-policy.md) |
| 让交付质量可审计 | 重复检测、时间顺序检查、幻觉提示和高风险复听清单 | [`audit_transcript.py`](talk2report/scripts/audit_transcript.py) |
| 交付专业文档 | 明确的 DOCX/PDF/JSON 结构和视觉检查要求 | [`output-specification.md`](talk2report/references/output-specification.md) |

## 处理流程

Skill 始终把录音作为事实来源，并通过明确的质量门控逐步处理：

| 阶段 | 作用 |
|---|---|
| `检查` | 探测时长、编码、采样率、声道和声道能量，不改写源文件 |
| `转写` | 创建具有稳定 ID、时间戳和可用置信度信息的原始片段 |
| `审计` | 检测重复、异常复述、长时间空白、语言突变和常见 ASR 幻觉 |
| `校对` | 保守修正标点、断句、明显识别错误和术语一致性 |
| `标注` | 使用稳定姓名或角色标签，并明确保留身份不确定性 |
| `整理` | 按真实话题变化组织对话，同时保持时间顺序，区分结论和待办 |
| `复核` | 复听姓名、数字、日期、单位、型号、否定词和低置信度片段 |
| `交付` | 构建目标文档并检查版式、时间戳、标题、分页和待确认事项 |

## 流程图

[![Talk2Report 功能流程：音频视频输入、时间戳转写、质量审计、保守校对、说话人与主题整理、高风险信息复核及文档输出](docs/images/talk2report-overview.png)](docs/images/talk2report-overview.pdf)

[查看高清 PNG](docs/images/talk2report-overview.png) · [下载 PDF 原稿](docs/images/talk2report-overview.pdf)

原始转写和质量证据始终与整理后的交付文档分开保存，避免编辑结果覆盖原始记录。

## 输出文件

在工具条件允许时，默认交付以下文件：

| 文件 | 用途 |
|---|---|
| `<源文件名>_整理校对对话稿.docx` | 面向用户的专业对话文档 |
| `<源文件名>_cleaned_transcript.json` | 带时间戳和来源信息的结构化校对对话 |
| `<源文件名>_transcript_audit.json` | 结构检查、风险提示、待确认片段和复听清单 |
| `<源文件名>_整理校对对话稿.pdf` | 用户要求时生成的固定版式版本 |

主文档包含录音元数据、按话题分节的时间戳对话、已确认结论、明确待办事项，以及存在不确定性时的待复核清单。

## 快速开始

克隆仓库：

```bash
git clone https://github.com/rudykon/Talk2Report.git
cd Talk2Report
```

在 macOS 或 Linux 中安装 Skill：

```bash
mkdir -p ~/.codex/skills
cp -R talk2report ~/.codex/skills/
```

在 Windows PowerShell 中安装：

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\talk2report" "$HOME\.codex\skills\"
```

在 Codex 中调用：

```text
使用 $talk2report，把这个音频整理成带时间戳、说话人、
关键结论和待办事项的校对对话文档。
```

如果本地存在兼容的 `audio_transcript_agent` 项目，可以使用随附脚本自动发现并调用可续跑流水线：

```powershell
.\talk2report\scripts\run_local_pipeline.ps1 `
  -AudioPath ".\recording.mp3" `
  -ProbeOnly
```

如果没有本地流水线，Skill 会使用环境中其他可用的转写能力；当不存在转写引擎时，会明确报告缺失能力。

## 质量验证

交付前审计结构化校对转写：

```bash
python talk2report/scripts/audit_transcript.py \
  cleaned_transcript.json \
  --output transcript_audit.json
```

审计项目包括：

- 文本缺失、说话人缺失、ID 重复和时间顺序错误；
- 连续重复片段和全局重复比例；
- 待确认说话人或术语标记；
- Unicode 替换字符和常见转写幻觉用语；
- 包含数字、日期、单位、否定、截止时间或责任分配的高风险片段。

审计结果只用于辅助复核，不能代替重新听取原始录音。

## 校对原则

| Skill 会保留 | Skill 绝不会编造 |
|---|---|
| 事实、不确定性、强调、否定、限制、分歧和人际语气 | 仅为了让句子流畅而补入的缺失内容 |
| 有录音或用户上下文支持的人名与术语 | 仅凭合理猜测确定的人名、产品名、诊断、数量、日期、负责人或截止时间 |
| 说话人的自我修正和有意义的犹豫 | 录音没有支持的决定、承诺或因果解释 |
| `〔听不清，00:12:34〕` 等明确标记 | 在音频、术语或说话人身份不确定时制造虚假确定性 |

完整的事实来源优先级、允许修改、禁止修改、不确定性标记、说话人规则和高风险复核要求，参见 [`editorial-policy.md`](talk2report/references/editorial-policy.md)。

## 仓库结构

| 路径 | 用途 |
|---|---|
| [`talk2report/SKILL.md`](talk2report/SKILL.md) | 核心编排流程与完成标准 |
| [`talk2report/agents/openai.yaml`](talk2report/agents/openai.yaml) | Codex Skill 展示信息和默认调用提示 |
| [`talk2report/references/editorial-policy.md`](talk2report/references/editorial-policy.md) | 忠实校对和不确定性处理规则 |
| [`talk2report/references/output-specification.md`](talk2report/references/output-specification.md) | 交付文件名、文档结构、JSON 结构和交付说明 |
| [`talk2report/scripts/audit_transcript.py`](talk2report/scripts/audit_transcript.py) | 对校对转写 JSON 执行确定性结构和风险审计 |
| [`talk2report/scripts/run_local_pipeline.ps1`](talk2report/scripts/run_local_pipeline.ps1) | 发现并调用兼容的本地可续跑转写流水线 |

