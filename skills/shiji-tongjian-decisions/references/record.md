# 结构化记录与输出

## 最低证据单元

每项关键历史主张由一个或多个 evidence_id 支持。证据保留：书名、卷次、篇名/纪名、原文内的纪年或段落锚点、版本/资料库、原文短摘、URL（尽量固定 revision）、获取日期；本地文本另记路径、行号/字符范围、SHA-256。无法确认公历年份时用原纪年，不自行换算。

引文核验状态为 `exact`（逐字命中）、`normalized_only`（只在空白/标点归一后命中，交付时改回原文）、`not_found`、`source_unavailable`。引用结论要求 exact；OCR 与异体字改写不得悄悄算 exact。

“文本一致性”“历史可信度”“古今迁移适用度”是三个不同维度，分别解释依据，不合成一个高置信度标签。

## JSON 结构

以下是字段定义示意。正式记录删去说明文字，未知用 null 或空列表并附缺口，不能用空字符串假装已完成。

```json
{
  "decision": {
    "question": "现实问题",
    "known_facts": [],
    "values_and_red_lines": [],
    "real_options": [],
    "deadline": null,
    "unknowns": [],
    "assumptions": [],
    "kernel": {"tension": "", "agency": "", "dependency": "", "information": "", "timing": "", "exit_and_reversibility": "", "stakeholders": [], "institutions": ""}
  },
  "retrieval": {"library": "", "scope": [], "queries": [], "coverage_limit": "", "candidates": []},
  "cases": [{
    "case_id": "C1",
    "event_cluster": "同一事件只计一次",
    "title": "人物在某节点的某项选择",
    "decision_point": "",
    "match": {"structural_matches": [], "critical_differences": [], "transfer_limits": []},
    "then_known": [{"claim": "", "kind": "史料记载", "evidence_ids": []}],
    "then_unknown": [],
    "options": [{"id": "A", "action": "", "origin": "史料明载/分析重建/反事实假设", "feasibility": "", "chosen": true, "reasoning": [{"claim": "", "kind": "史料记载", "speaker": "", "evidence_ids": []}], "expected_outcomes": []}],
    "observed_outcomes": [{"claim": "", "horizon": "", "kind": "史料记载", "evidence_ids": []}],
    "costs": [{"cost": "", "visibility": "显性/隐性", "epistemic_status": "史料记载/分析推断/待核实", "timing": "当时预期/后来发生/情景风险", "bearer": "", "horizon": "", "reversibility": "", "evidence_ids": [], "inference_basis": null}],
    "counterfactuals": [{"if": "", "plausible_effect": "", "assumptions": [], "status": "反事实假设"}],
    "source_critique": "叙事立场、来源依赖与缺口",
    "evidence": [{"evidence_id": "E1", "book": "史记/资治通鉴", "volume": "", "chapter": "", "chronology_or_anchor": "", "library_and_edition": "", "quote": "", "url": "", "revision": null, "retrieved_at": "", "local_path": null, "sha256": null, "lines": null, "quote_check": "exact", "voice": "叙述者/人物自述/史家评论"}]
  }],
  "modern_branches": [{"option": "", "conditions": [], "scenarios": [], "gains": [], "explicit_costs": [], "hidden_costs": [], "third_party_effects": [], "reversible_step": "", "signals": [], "stop_or_review_conditions": []}],
  "conditional_insights": [{"claim": "当条件C成立，机制M可能导致R", "supporting_cases": [], "countercases": [], "failure_conditions": [], "evidence_limit": ""}],
  "risk_reminders": [],
  "next_step": "",
  "provisional_view": null,
  "what_would_change_view": [],
  "unresolved": []
}
```

## 人类可读版本

1. 先说现实选择真正卡在哪里、暂定判断和关键未知。
2. 历史案例表按“当时信息—可选项—所选及判断—结果—显性/隐性代价”展开，每案附原文证据。
3. 用一个现代选项比较表说明分支、成本、可逆性和需补的信息。
4. 条件性启发、反例/失效条件、风险提醒、最小下一步。
5. 列原文出处及本次检索范围；出处放在对应主张附近，也可以给证据编号。

输出不需冒用“太史公曰”“臣光曰”替 AI 推断背书；真要引用史评，标明是原书评论。不要用长段古文挤占分析；足以核验的短摘加上下文入口即可。
