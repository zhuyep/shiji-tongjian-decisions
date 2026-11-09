---
title: normalized_only 不是 exact——标点近似核源演示
date: 2026-11-03
status: discovery-demo
source_scope: sample-corpus 已登记片段 shiji-041（《史记》卷四十一）
validation_boundary: 只复现离线核验行为；不编造新史源；演示非用户处境；normalized_only 与 exact 都只证明文本一致性，不证明历史真实性或古今适用
---

# normalized_only 不是 exact

**一句话**：标点改了、字还在，也不能冒充逐字一致——`--normalize` 命中时状态是 `normalized_only`，退出码非 0，不能当成 `exact`。

这不是人生抉择推演，只是把 README 里「忽略标点才命中 → `normalized_only`」跑成可分享对照。演示用现成 sample-corpus 与公开命令，不新增引文 ID，不编造出处。与[核源翻车→exact](verify-flip.zh-CN.md)互补：那边演示**改字**翻车，这边演示**只动标点**仍不能当 exact。

## ① 逐字一致 → 应得 `status: exact`

克隆仓库后，在仓库根目录运行（与根 README「30 秒核源 / 离线核验」同一条）：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令，臣行意。'
```

预期：返回 JSON，`status` 为 `exact`。`exact` 只表示引文与本地缓存文本一致，不证明历史事件真实、也不证明可迁移到你的现实抉择。

## ② 只改标点、不加 `--normalize` → 应得 `not_found`

把逗号「，」改成顿号「、」，并去掉句末「。」，其余参数不变：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令、臣行意'
```

预期：`status: not_found`（默认按字面匹配；标点不同就不算命中）。

## ③ 同一近似引文加上 `--normalize` → 应得 `normalized_only`（不是 exact）

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令、臣行意' --normalize
```

或与仓库自带测试相同的无标点写法：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令臣行意' --normalize
```

预期：`status: normalized_only`；进程退出码为 `1`（与 `not_found` 一样非成功）。工具会告诉你「去标点后能对上」，但**不能**把它写成 `exact` 或口头说成「已经逐字核过」。错字即使用 `--normalize` 也仍是 `not_found`——见[核源翻车→exact](verify-flip.zh-CN.md)。

## ④ 边界（诚实）

- **演示非用户处境**：这里没有虚构跳槽/晋升/合伙剧情，只核一句已登记引文。
- **不编造新史源**：只用 `shiji-041` 与仓库自带 sample-corpus。
- **只复现离线核验**：本地脚本不联网；`normalized_only` ≠ 历史结论，也不等于可以对外宣称「原文如此」。
- **和 exact 的分工**：对外展示或绑定证据时，以逐字 `exact` 为准；`normalized_only` 最多说明「去掉标点后像这句话」，不能顶替逐字核验。

## ⑤ 接着读完整示例与反馈

- [核源翻车→exact](verify-flip.zh-CN.md)（改一字 → 非 exact）
- [错绑 ID 不是 exact](verify-wrong-id.zh-CN.md)（原文对了、出处 ID 绑错也不能冒充已核）
- [跳槽完整示例](job-switch-decision.zh-CN.md)
- [晋升完整示例](promotion-decision.zh-CN.md)
- [合伙/长期承诺示例](partner-commitment-decision.zh-CN.md)
- [示例索引](README.md)
- 读完留下一条具体判断：[体验反馈表](https://github.com/zhuyep/shiji-tongjian-decisions/issues/new?template=experience.yml)（可选「只看公开示例」；提交公开可见，无需私人经历）