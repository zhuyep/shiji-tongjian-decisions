# 史鉴人生抉择

**把现实中的进退两难，放回《史记》《资治通鉴》的决策现场。**

一个有出处、有反例、有适用边界的 Agent Skill。围绕去留、转型、合作与承诺，比较当时可选的路径、后来发生的结果，以及由谁承担代价。

[English](README.en.md) · [完整示例](examples/promotion-decision.zh-CN.md) · [技能入口](skills/shiji-tongjian-decisions/SKILL.md) · [首版发布](https://github.com/zhuyep/shiji-tongjian-decisions/releases/tag/v0.1.0)

## 先看一次推演

> 晋升会加薪，但职责、资源和工时都没有说清。我更看重家庭时间与收入稳定。接受、协商边界，还是准备离开？

| 历史对照 | 原文纠正的直觉 | 回到今天需要核实的事 |
| --- | --- | --- |
| 范蠡辞越 | 辞越时携轻宝与随从；散财是后来在齐辞相的另一节点 | 离开的理由之外，是否已有现金流、可迁移能力和退出条件？ |
| 张良退居 | 少求封赏、闭门养病之后，仍被要求出谋、行少傅事 | 减少收益或降低头衔，能否实际减少责任？ |
| 吴起迁楚 | 换到支持自己的环境，仍面对支持者去世后的政治风险 | 新机会的支持来自制度和资源，还是某一位个人？ |

这些对照提出需要验证的问题，不能由古代君臣关系推断现代上司的动机。完整示例包含原文、出处、反事实标签和三条现代路径；现实困境为虚构，未使用个人私密经历。

## 安装与使用

需要支持 Agent Skills 的 AI 助手；在线查找新案例需要该助手有搜索或浏览能力。安装工具需要 Node.js，离线原文核验工具需要 Python 3.10+，仅使用标准库。

```bash
npx skills add zhuyep/shiji-tongjian-decisions --skill shiji-tongjian-decisions
```

安装到 Codex：

```bash
npx skills add zhuyep/shiji-tongjian-decisions --skill shiji-tongjian-decisions --agent codex
```

在助手中输入：

```text
请用 $shiji-tongjian-decisions 分析我的选择：……
我最看重……；目前的选项是……；不能接受的代价是……。
请从《史记》《资治通鉴》找结构相近的案例，核对原文，
比较收益、隐性代价、反例和不适用之处，最后给出最小下一步。
```

也可以下载 [Release](https://github.com/zhuyep/shiji-tongjian-decisions/releases/latest)，把 `skills/shiji-tongjian-decisions/` 放到宿主支持的技能目录。技能不需要单独 API Key；模型及联网能力由宿主提供。

## 它具体做什么

1. 提取现实约束、价值排序、可选路径与关键未知。
2. 按选择结构检索两书原文，比较相似点与决定性差异。
3. 先还原决策时的信息，再查看结局，避免倒推“早就注定”。
4. 分开史料记载、史家评论、分析推断和反事实假设。
5. 比较即时与长期代价、承担者、可逆性和失效条件。

同一事件被两书记载，不算两个独立证据。检索分数与案例数量不能转成人生成功率。没有可访问原文时明确交付证据缺口。

## 离线核验一分钟上手

克隆仓库后运行：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令，臣行意。'
```

返回 `status: exact`，并给出来源、原文偏移、行号和上下文。替换过的字不会被当作原句；忽略标点才命中时返回 `normalized_only`，不能冒充逐字一致。详见[来源与检索](skills/shiji-tongjian-decisions/references/sources.md)。

## 当前完成度

- 三卷的选段缓存、三个结构化演示案例、十三条原文短引。
- 十二项原有工具行为测试，加一项公开示例的证据一致性测试。
- 一条虚构困境的制作代理走读；尚无独立真人评价与真实决策效果验证。
- 没有完成两书全文精读、全书案例抽取或全书检索召回率评测。

本地脚本不联网。使用在线 AI 助手时，输入由该助手处理；请自行脱敏现实处境。历史类比只支持思考，不替代当代事实核验或专业判断。

## 反馈与贡献

欢迎提交[问题或使用反馈](https://github.com/zhuyep/shiji-tongjian-decisions/issues)：提供脱敏问题、引用出处、观察到的错误或遗漏，以及怎样才算改进。新增案例请同时说明不适用之处。请勿提交真实同事姓名、家庭信息或未授权材料。

```bash
python3 -m unittest discover -s tests -v
```

如果它确实帮你看清了一个此前忽略的选择或代价，欢迎 Star；更有价值的是一条具体的使用或失败反馈。

## 来源与许可

原创代码与技能说明采用 [MIT](LICENSE)。维基文库电子文本选段及其引文另见 [NOTICE](NOTICE.md) 与[文本许可说明](skills/shiji-tongjian-decisions/references/sample-corpus/LICENSE.md)；不将第三方文本改标为 MIT。

设计参考项目及具体取舍见[设计来源](skills/shiji-tongjian-decisions/references/design-provenance.md)。保留原始出处，不分发参考项目快照。
