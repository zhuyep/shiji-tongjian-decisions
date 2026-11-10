---
title: 第二源也能 exact——不是单句把戏
date: 2026-11-10
status: discovery-demo
source_scope: sample-corpus 已登记片段 shiji-041（《史记》卷四十一《越王勾践世家》）与 shiji-055（《史记》卷五十五《留侯世家》）
validation_boundary: 只复现离线核验行为；不编造新史源；演示非用户处境；exact 只证明文本一致，不证明历史真实性或古今适用
---

# 第二源也能 exact

**一句话**：核源不是只对上某一句——同一份 sample-corpus 里，换一个已登记来源，也能一键得到 `status: exact`。

这不是人生抉择推演，只是把「别把核源当成单句把戏」跑成可分享对照。两条命令都用仓库现成语料与公开接口，不新增引文 ID，不编造出处。与[核源翻车→exact](verify-flip.zh-CN.md)、[normalized_only 不是 exact](verify-normalized.zh-CN.md)、[错绑 ID 不是 exact](verify-wrong-id.zh-CN.md)互补：那三页分别演示改字、只改标点、出处绑错；本页演示**另一个真实来源也能核到 exact**。错绑演示里作为反例出现的 `shiji-055`，在这里用它自己的已登记引文核过。

## ① 来源一：`shiji-041`（《史记》卷四十一《越王勾践世家》）→ 应得 `status: exact`

克隆仓库后，在仓库根目录运行（与根 README「30 秒核源 / 离线核验」同一条）：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令，臣行意。'
```

预期：返回 JSON，`status` 为 `exact`，`source.id` 为 `shiji-041`，并带来源、偏移与上下文。本演示实测进程退出码为 `0`。`exact` 只表示引文与本地缓存文本一致，不证明历史事件真实、也不证明可迁移到你的现实抉择。

## ② 来源二：`shiji-055`（《史记》卷五十五《留侯世家》）→ 同样应得 `status: exact`

换一个已登记 ID 和一句属于该片段的引文（与仓库自带测试相同）：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-055 --quote '留侯行少傅事。'
```

预期：同样返回 `status: exact`，`source.id` 为 `shiji-055`，书卷为《史记》卷五十五《留侯世家》。本演示实测退出码为 `0`。两条命令对得上，只能说明语料里至少有两个可核来源，不能外推成「全书已核」或「任意口头出处都可信」。

## ③ 边界（诚实）

- **演示非用户处境**：这里没有虚构跳槽/晋升/合伙剧情，只核两句已登记引文。
- **不编造新史源**：只用 sample-corpus 已有的 `shiji-041` 与 `shiji-055`，不新增引文 ID。
- **只复现离线核验**：本地脚本不联网；结果是文本一致性，不是史学结论。
- **和另外三页的分工**：[改一字](verify-flip.zh-CN.md)会翻车，[只改标点](verify-normalized.zh-CN.md)最多得到 `normalized_only`，[出处绑错](verify-wrong-id.zh-CN.md)得到 `not_found`；本页则证明第二个已登记来源本身也能 `exact`。
- **覆盖范围**：sample-corpus 是指定段落节选，不是完整卷，更不是两书全文。

## ④ 接着读完整示例与反馈

- [核源翻车→exact](verify-flip.zh-CN.md)（改一字 → 非 exact）
- [normalized_only 不是 exact](verify-normalized.zh-CN.md)（只改标点仍不能当逐字核验）
- [错绑 ID 不是 exact](verify-wrong-id.zh-CN.md)（原文对了、出处 ID 绑错也不能冒充已核）
- [跳槽完整示例](job-switch-decision.zh-CN.md)
- [晋升完整示例](promotion-decision.zh-CN.md)
- [合伙/长期承诺示例](partner-commitment-decision.zh-CN.md)
- [示例索引](README.md)
- 读完留下一条具体判断：[体验反馈表](https://github.com/zhuyep/shiji-tongjian-decisions/issues/new?template=experience.yml)（可选「只看公开示例」；提交公开可见，无需私人经历）
