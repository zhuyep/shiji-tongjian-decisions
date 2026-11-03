---
title: 核源翻车→exact——离线核验前后对比演示
date: 2026-11-02
status: discovery-demo
source_scope: sample-corpus 已登记片段 shiji-041（《史记》卷四十一）
validation_boundary: 只复现离线核验行为；不编造新史源；演示非用户处境；exact 只证明文本一致，不证明历史真实性或古今适用
---

# 核源翻车 → exact

**一句话**：类比可以假，引文不能假——改一个字就该翻车；对上语料才配叫 `exact`。

这不是人生抉择推演，只是把 README 里那条「30 秒核源」命令跑成可分享的前后对照。演示用现成 sample-corpus 与公开命令，不新增引文 ID，不编造出处。

## ① 正确引文 → 应得 `status: exact`

克隆仓库后，在仓库根目录运行（与根 README「30 秒核源 / 离线核验」同一条）：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令，臣行意。'
```

预期：返回 JSON，`status` 为 `exact`，并带来源、偏移与上下文。`exact` 只表示引文与本地缓存文本一致，不证明历史事件真实、也不证明可迁移到你的现实抉择。

## ② 故意改一字 → 应得非 exact / 缺口说明

把末字「意」改成「义」，其余参数不变：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令，臣行义。'
```

预期：不再是 `exact`（本演示实测为 `not_found`：语料里没有这句改字版）。缺字、错字、口头近似都不该被当成已核出处；语料没有就明说缺口，不补造引文。

## ③ 边界（诚实）

- **演示非用户处境**：这里没有虚构跳槽/晋升剧情，只核一句已登记引文。
- **不编造新史源**：只用 `shiji-041` 与仓库自带 sample-corpus。
- **只复现离线核验**：本地脚本不联网；结果是文本一致性，不是史学结论。

## ④ 接着读完整示例与反馈

- [normalized_only 不是 exact](verify-normalized.zh-CN.md)（只改标点仍不能当逐字核验）
- [跳槽完整示例](job-switch-decision.zh-CN.md)（含本句「君行令，臣行意。」所在案例簇）
- [晋升完整示例](promotion-decision.zh-CN.md)
- [合伙/长期承诺示例](partner-commitment-decision.zh-CN.md)
- [示例索引](README.md)
- 读完留下一条具体判断：[体验反馈表](https://github.com/zhuyep/shiji-tongjian-decisions/issues/new?template=experience.yml)（可选「只看公开示例」；提交公开可见，无需私人经历）