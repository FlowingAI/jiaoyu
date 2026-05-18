# jiaoyu

教育类 Codex Skills 与教学辅助资产仓库。默认说明语言为中文，必要时附英文说明，方便中文教学场景直接使用。

## Skills

### `skills/middle-school-composition-review/`

**中文说明**

初中作文三阶批改 Skill，用于把一篇初中语文作文整理成三个教学版本：

1. **阅卷评分版**：根据评分标准给出分项分、原始分、折算分、等级判断、优点、失分点和提分建议。
2. **逐段修改示范版**：保留学生原意，逐段指出问题，给出修改示范，并说明这样修改的原因和好处。
3. **完整修改成文版**：在学生原文基础上润色成完整示范作文，并可生成 A4 作文纸 PNG/PDF；左侧为作文正文，右侧为红笔方法批注。

默认评分口径：如果评分表为内容 20 分、表达 20 分、特征/发展 10 分，则先按 **50 分原始分** 评分；用户要求满分 60 分时，再按 `原始50分 × 1.2` 折算，并同时展示两个分数。

默认输出风格：中文优先，语气像语文老师，评价中肯具体，既指出问题，也保留鼓励。

**English Summary**

A Codex Skill for middle-school Chinese composition review. It produces three teaching-oriented outputs: rubric-based scoring, paragraph-by-paragraph revision guidance, and a polished complete essay rendered on printable A4 composition paper with red teacher comments. Chinese is the default language for all teaching output.

## Files

- `SKILL.md`: Skill instructions and workflow.
- `agents/openai.yaml`: Agent configuration.
- `scripts/render_composition_pages.py`: Deterministic A4 composition-paper renderer for Chinese text, red comments, and printable PDF output.
