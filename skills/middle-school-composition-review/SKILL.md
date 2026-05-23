---
name: middle-school-composition-review
description: Use when the user wants to grade, annotate, revise, or generate teaching versions of a middle-school Chinese composition, especially when they ask for three versions: scoring by rubric, paragraph-by-paragraph revision guidance, and a complete polished essay on printable A4 composition paper with red teacher comments.
metadata:
  short-description: 初中作文三阶批改
---

# 初中作文三阶批改

Use this skill for 初中作文批改、阅卷评分、逐段修改、作文润色、红笔批注图、A4 作文纸打印版, or when the user asks to repeat the 三阶作文批改 workflow.

## Core Goal

Produce three teaching-oriented outputs:

1. **阅卷评分版**: tell the student/parent the current score and why.
2. **逐段修改示范版**: show how each paragraph can be improved without discarding the student's original intent.
3. **完整修改成文版**: provide a polished complete essay on A4 composition paper, with black body text and red method comments.

The goal is teaching revision, not ghostwriting. Preserve the student's topic, core material, people, events, and authentic emotion whenever possible.

## Inputs To Gather

Use provided files/images first. Ask only if a necessary item is missing.

- 作文题目和写作要求
- 学生原文, either OCR from images or pasted text
- 评分标准, if provided
- Desired outputs: text-only, annotated images, printable PNG/PDF, or all three
- Destination folder, if the user names one

If the image text is unclear, transcribe only the readable parts and state uncertainty before scoring or revising.

## Default Rubric

If the user provides a rubric image, follow it first. For the common rubric used in this 三阶作文批改 workflow, treat the table as a **50-point raw rubric**:

- **内容 20分**: 是否符合题意、中心是否突出、内容是否充实、思想感情是否健康真实。
- **表达 20分**: 是否符合文体要求、结构是否完整、语言是否通顺、字迹是否工整。
- **特征/发展 10分**: 是否有见解、内容是否丰富、是否有文采。
- **扣分项**:
  - 错别字每 3 个扣 1 分, 重复不计, 最多扣 3 分, 不足 3 个不扣。
  - 字数不足时, 每少 50 字扣 1 分。
  - 无标题扣 2 分。

When the user asks for a 60-point score but the rubric totals 50, output both:

- `原始50分 = 内容分 + 表达分 + 特征分 - 扣分`
- `折算60分 = 原始50分 × 1.2`
- Example: `原始分：37/50；折算分：44/60`

Do not call `内容20 + 表达20 + 特征10` a direct 60-point rubric. When scoring, include 原始分、折算分、分项分、等级判断、主要优点、主要失分点、提分建议. Be 中肯, specific, and encouraging.

## Workflow

### 1. 阅卷评分版

Output as a teacher:

- 分数: if using the 50-point rubric and the user wants 60 points, write both, e.g. `原始分：37/50；折算分：44/60`
- 分项分: 内容、表达、特征/发展、扣分项
- 等级判断, e.g. `二类中等偏上`
- Short explanation of why the score is fair
- 2-4 concrete improvement priorities

For a typical middle-school narrative that has sincere emotion but thin events, uneven expression, and limited detail, a fair audit under the 50-point table might be: 内容 `16/20`, 表达 `14-15/20`, 特征 `7/10`, 扣分 `0-1`; 原始分约 `37-38/50`, 折算分约 `44-46/60`.

If the user requests images, make red-pen scoring/comment pages or annotate the original images. For original-text annotation pages, match the original page count exactly: 原作文几张纸，原文批注图就用几张纸，不要把多页原文缩成一张图. Add one extra scoring-summary page for 分项分、总分、等级、总评、提分建议、鼓励语. For long Chinese text, avoid relying on AI image generation for exact text.

### 2. 逐段修改示范版

For each paragraph or logical section:

- Quote or summarize the original paragraph briefly.
- Identify the main strength and main problem.
- Give a revised paragraph/fragment that keeps the student's intent.
- Explain the benefit, e.g. `开头更快点题`, `动作、语言、神态一起写`, `由具体画面自然升华`.

Prioritize:

- 开头点题 and 景中含情
- Clear event line
- Specific action/language/expression details
- Natural transitions
- Ending that echoes the title and theme

For red-pen images, keep comments short. Do not overcrowd the page.

For paragraph-revision images, annotate the original pages one-to-one first, then add one extra 逐段修改示范页. The extra page should contain 原文问题、修改示范、修改好处, because long teaching explanations should not be squeezed onto the original作文纸.

### 3. 完整修改成文版

Create a complete polished essay based on the original.

Rules:

- Do not invent a completely unrelated story.
- Keep the original emotional core.
- Make the narrative complete: 起因、经过、关键细节、感悟/点题.
- Meet the assignment's word count and genre.
- Label it as a 示范稿 when appropriate.

When the user wants printable images/PDF, prefer deterministic programmatic layout over AI image generation so Chinese text remains accurate.

## Printable A4 Layout Standard

For printable pages:

- A4 portrait, 300 DPI.
- Left side: wide composition grid.
- Right side: narrow red comment column.
- Body text: black Chinese font, preferably 楷体.
- Teacher comments: red, large enough to be close to body text size.
- Grid line color: light ink-green/gray-green; default `RGB(135,160,145)`.
- Keep page bright and print-ready.
- Avoid overlap between body text, red circles/arrows, and comments.
- Use the student's supplied composition paper as the visual reference. Match its grid count and approximate grid size/color; for common `20×20=400` paper, keep 20 columns and 20 rows rather than inventing a wider grid.
- Page-count rule:
  - 阅卷评分版 = 原文页数 + 1 scoring-summary page.
  - 逐段修改示范版 = 原文页数 + 1 paragraph-revision demonstration page.
  - 完整修改成文版 = use the student's paper grid capacity. Start from the original page count, but add pages if the polished essay cannot fit at readable size. State the reason, e.g. `修改稿约810字，20×20作文纸两页容量不足，因此完整成文版为3页`.

Use `scripts/render_composition_pages.py` when a printable complete-essay PNG/PDF is needed.

Example command:

```powershell
cd "path\to\middle-school-composition-review"

python ".\scripts\render_composition_pages.py" `
  --title "作文题目示例" `
  --text-file ".\examples\student_essay.txt" `
  --out-dir ".\output\composition_review" `
  --basename "作文修改示范_宽版批注" `
  --comments "开头景中含情，快速点题。|把时间、地点、人物连成一条线，叙事更清楚。|细节写人物，情感更自然。|结尾照应题目，中心明确。"
```

## Output Naming

When writing files, use clear names:

- `阅卷评分版.*`
- `逐段修改示范版.*`
- `完整作文_宽版批注_page1.png`
- `完整作文_宽版批注_page2.png`
- `完整作文_宽版批注_打印版.pdf`

If a file is open and cannot be overwritten, save a new version with a suffix such as `_新版`, `_大字批注`, or `_墨绿格线`.

## Quality Checklist

Before final response:

- Score matches the rubric and gives reasons.
- If the rubric totals 50 but the user asks for 60, both raw 50-point score and converted 60-point score are shown.
- The sum of item scores is arithmetically consistent with the raw score.
- Paragraph revisions preserve the student's material.
- Complete essay meets the prompt and word-count requirement.
- Original annotation pages match the original composition's page count one-to-one.
- Scoring and paragraph-revision outputs include their required extra summary/demonstration page.
- Complete polished essay uses the student's paper grid count/size as the reference and adds pages when the revised text cannot fit.
- Printable images/PDF are bright, clear, and not crowded.
- Red comments teach methods, not just corrections.
- Final answer lists saved paths and notes any files that could not be overwritten.
