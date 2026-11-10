---
title: 错绑 ID 不是 exact——原文对、出处错的核源演示
date: 2026-11-09
status: discovery-demo
source_scope: sample-corpus 已登记片段 shiji-041（《史记》卷四十一，正确出处）与 shiji-055（《史记》卷五十五，错绑对照；该片段不含本句）
validation_boundary: 只复现离线核验行为；不编造新史源；演示非用户处境；exact 只证明文本一致，不证明历史真实性或古今适用
---

# 错绑 ID 不是 exact

**一句话**：原文对了、出处 ID 绑错，也不能冒充已核——同一句真引文配上错误的 `--id`，状态不是 `exact`，退出码非 0。

这不是人生抉择推演，只是把「别信口头出处」跑成可分享对照。演示用现成 sample-corpus 与公开命令，不新增引文 ID，不编造出处。与[核源翻车→exact](verify-flip.zh-CN.md)、[normalized_only 不是 exact](verify-normalized.zh-CN.md)形成三角互补：那边分别演示**改字**、**只动标点**，这边演示**引文对、ID 错**。

## ① 正确引文 + 正确 ID → 应得 `status: exact`

克隆仓库后，在仓库根目录运行（与根 README「30 秒核源 / 离线核验」同一条）：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令，臣行意。'
```

预期：返回 JSON，`status` 为 `exact`，并带来源、偏移与上下文。`exact` 只表示引文与本地缓存文本一致，不证明历史事件真实、也不证明可迁移到你的现实抉择。

## ② 同一句真引文 + 错误 `--id` → 应得非 exact

引文一字不改，只把 `--id` 换成 sample-corpus 里另一个已登记、但不含这句的片段 `shiji-055`（《史记》卷五十五《留侯世家》）：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-055 --quote '君行令，臣行意。'
```

预期：不再是 `exact`（本演示实测为 `not_found`，进程退出码为 `1`：`shiji-055` 已登记，但这句不在该片段里）。工具返回的 `source.id` 是你传入的 `shiji-055`，`source_quote` 为 `null`。原文是真的、ID 也是登记过的，两者对不上就不能写成「已经核过」。未登记的 ID 会走另一条错误路径（`status: error` / `unknown_source`），本页不演示那种情况。

## ③ 边界（诚实）

- **演示非用户处境**：这里没有虚构跳槽/晋升/合伙剧情，只核一句已登记引文。
- **不编造新史源**：只用 sample-corpus 已有的 `shiji-041` 与 `shiji-055`，不新增引文 ID。
- **只复现离线核验**：本地脚本不联网；结果是文本一致性，不是史学结论。
- **和 exact 的分工**：`exact` 只证明「这句在你指定的那条来源里逐字一致」；引文本身成立、出处绑错，仍然不能对外宣称已核。
- **和另外两页的分工**：[改一字](verify-flip.zh-CN.md)会翻车，[只改标点](verify-normalized.zh-CN.md)最多得到 `normalized_only`，本页则是出处绑错——三类都不是 `exact`。

## ④ 接着读完整示例与反馈

- [核源翻车→exact](verify-flip.zh-CN.md)（改一字 → 非 exact）
- [normalized_only 不是 exact](verify-normalized.zh-CN.md)（只改标点仍不能当逐字核验）
- [第二源也能 exact](verify-second-source.zh-CN.md)（`shiji-055` 本身也有可核引文，不是只能当反例）
- [跳槽完整示例](job-switch-decision.zh-CN.md)（含本句「君行令，臣行意。」所在案例簇）
- [晋升完整示例](promotion-decision.zh-CN.md)
- [合伙/长期承诺示例](partner-commitment-decision.zh-CN.md)
- [示例索引](README.md)
- 读完留下一条具体判断：[体验反馈表](https://github.com/zhuyep/shiji-tongjian-decisions/issues/new?template=experience.yml)（可选「只看公开示例」；提交公开可见，无需私人经历）
