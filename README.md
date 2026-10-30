# 史鉴人生抉择

[![skills.sh](https://skills.sh/b/zhuyep/shiji-tongjian-decisions)](https://skills.sh/zhuyep/shiji-tongjian-decisions)

**类比可以假，引文不能假。** 把跳槽/晋升放回《史记》《资治通鉴》比路径与代价；语料引文可离线核验。

```bash
npx skills add zhuyep/shiji-tongjian-decisions --skill shiji-tongjian-decisions
```

不装先看：[跳槽完整示例](examples/job-switch-decision.zh-CN.md) · [晋升完整示例](examples/promotion-decision.zh-CN.md) · [English](README.en.md)

---

## 30 秒核源：前后对比

| 步骤 | 你会看到什么 |
| --- | --- |
| **前** | 助手随口抛出「出处：`shiji-041`，引文：`君行令，臣行意。`」——看起来像有据，但还没对着语料核过。 |
| **核** | 克隆后跑仓库自带的同一条命令（与[离线核验一分钟上手](#离线核验一分钟上手)相同）： |
| **后** | 返回 `status: exact`（含偏移与上下文）。改一个字再跑 → 不再是 `exact`；语料里没有就明说缺口，不编造。 |

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令，臣行意。'
```

## 30 秒判断值不值得

- **引文可离线核验**；找不到出处就明说缺口，不编造引文。
- 不安装也能先读[晋升](examples/promotion-decision.zh-CN.md)或[跳槽](examples/job-switch-decision.zh-CN.md)完整示例；入口见[示例索引](examples/README.md)。
- 需要时一行安装：`npx skills add zhuyep/shiji-tongjian-decisions --skill shiji-tongjian-decisions`


## 和其他「历史智慧」有什么不同

| | 常见史例鸡汤 | 史鉴 |
| --- | --- | --- |
| 引文 | 常口头引用、难核对 | **可离线核验**；缺口明说，不编造 |
| 输出 | 一句道理 / 榜样故事 | **路径 × 代价 × 反例 × 适用边界** |
| 类比 | 古今直接画等号 | **类比可以假**；只提可核实的现实条件 |
| 不该用时 | 很少写清 | README 有「何时不该用」清单 |

30 秒自证：克隆后跑上方核源命令，应得到 `status: exact`。

## 先看一次推演

> 晋升会加薪，但职责、资源和工时都没有说清。我更看重家庭时间与收入稳定。接受、协商边界，还是准备离开？

| 历史对照 | 原文纠正的直觉 | 回到今天需要核实的事 |
| --- | --- | --- |
| 范蠡辞越 | 辞越时携轻宝与随从；散财是后来在齐辞相的另一节点 | 离开的理由之外，是否已有现金流、可迁移能力和退出条件？ |
| 张良退居 | 少求封赏、闭门养病之后，仍被要求出谋、行少傅事 | 减少收益或降低头衔，能否实际减少责任？ |
| 吴起迁楚 | 换到支持自己的环境，仍面对支持者去世后的政治风险 | 新机会的支持来自制度和资源，还是某一位个人？ |

这些对照提出需要验证的问题，不能由古代君臣关系推断现代上司的动机。完整示例包含原文、出处、反事实标签和三条现代路径；现实困境为虚构，未使用个人私密经历。

**不安装也能先判断有没有用：**读[晋升](examples/promotion-decision.zh-CN.md)或[跳槽](examples/job-switch-decision.zh-CN.md)完整推演，挑一条你认为有用或不成立的判断，填[具体反馈表](https://github.com/zhuyep/shiji-tongjian-decisions/issues/new?template=experience.yml)。选择“只看公开示例”即可，无需提供私人经历；提交内容公开可见。读过示例与实际运行会分开记录。


## 何时不该用史鉴

诚实边界（类比可以假，引文不能假）：

- 要算命、宿命或「注定会怎样」的结论时，别用。
- 需要精确的现代法律、医疗或财务建议时，别用——这不是专业咨询替代品。
- 语料里查不到可靠引文、只能编造出处时，别用；应标缺口或停，不补造引文。
- 场景与史源完全不可比、只能硬凑类比时，别用。
- 只想要一句鸡汤、不要路径与代价表时，别用。

## 安装与使用

需要支持 Agent Skills 的 AI 助手；在线查找新案例需要该助手有搜索或浏览能力。安装工具需要 Node.js，离线原文核验工具需要 Python 3.10+，仅使用标准库。

```bash
npx skills add zhuyep/shiji-tongjian-decisions --skill shiji-tongjian-decisions
```

安装到 Codex：

```bash
npx skills add zhuyep/shiji-tongjian-decisions --skill shiji-tongjian-decisions --agent codex
```

完成安装后，可以直接复制下面的虚构场景到助手，不必先整理自己的私人问题：

```text
请用 $shiji-tongjian-decisions 分析这个虚构场景：
我得到一次晋升机会，会加薪，但职责、可用资源和工时还没说清。
我更看重家庭时间与收入稳定，不愿在边界不清时承担长期承诺。
请比较接受、先协商边界、准备其他去向三条路径。
从《史记》《资治通鉴》找结构相近的案例并核对原文；
列出收益、隐性代价、反例和不适用之处，不推断现代上司的动机。
找不到可核原文时说明缺口，不补造引文；最后给出一个最小下一步。
```

看结果时检查三件事：是否比较了三条路径；引文是否有可核出处或明确缺口；是否指出一个值得核实的现实条件与类比失效边界。文字流畅本身不代表推演可靠。

想检查安装后的助手是否可靠，可按[六场景自检说明](evals/README.md)复制固定输入：条件变化的晋升对照、错字引文、无源、缓存未命中和时序混淆。每题都有人工验收标准；它们是待运行的测试题，不是模型已经通过的结果。先跑晋升对照与错字题，就能检查是否机械套用建议或误认引文。

运行失败也值得记录：[反馈尝试到哪一步](https://github.com/zhuyep/shiji-tongjian-decisions/issues/new?template=experience.yml)，选择“安装或启动失败”或“用虚构问题运行过”，只写一条具体发现或错误，不必粘贴完整对话。熟悉流程后，再把场景替换为脱敏的选择、优先级和不可接受的代价。

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
- 离线工具测试、证据登记与公开 Markdown 引文/来源一致性检查，并用故意改字、错绑 ID、错改出处等变异验证检查会失败。
- 六个虚构场景及人工验收标准；自动测试只校验夹具和原文基准，尚未完成模型行为回归。
- 一条虚构困境的制作代理走读；尚无独立真人评价与真实决策效果验证。
- 没有完成两书全文精读、全书案例抽取或全书检索召回率评测。

本地脚本不联网。使用在线 AI 助手时，输入由该助手处理；请自行脱敏现实处境。历史类比只支持思考，不替代当代事实核验或专业判断。

## 反馈与贡献

**不安装也能反馈：**读上面的虚构晋升或跳槽示例后，用[一分钟反馈表](https://github.com/zhuyep/shiji-tongjian-decisions/issues/new?template=experience.yml)告诉我们：你尝试到哪一步、哪一条判断有用或不成立、什么情况下会再用。看过示例、安装失败和实际使用会分开记录；请勿提供私人经历，表单提交后公开可见。

欢迎提交[问题或使用反馈](https://github.com/zhuyep/shiji-tongjian-decisions/issues)：提供脱敏问题、引用出处、观察到的错误或遗漏，以及怎样才算改进。新增案例请同时说明不适用之处。请勿提交真实同事姓名、家庭信息或未授权材料。

```bash
python3 -m unittest discover -s tests -v
```

如果它确实帮你看清了一个此前忽略的选择或代价，欢迎 Star；更有价值的是一条具体的使用或失败反馈。

## 来源与许可

原创代码与技能说明采用 [MIT](LICENSE)。维基文库电子文本选段及其引文另见 [NOTICE](NOTICE.md) 与[文本许可说明](skills/shiji-tongjian-decisions/references/sample-corpus/LICENSE.md)；不将第三方文本改标为 MIT。

设计参考项目及具体取舍见[设计来源](skills/shiji-tongjian-decisions/references/design-provenance.md)。保留原始出处，不分发参考项目快照。