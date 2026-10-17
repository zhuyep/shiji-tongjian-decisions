# 手工模型行为回归

初始状态：**not_run**。六个场景均为虚构输入；本文件和场景 JSON 是测试设计，不是模型已通过的证据，也不证明历史解释或现实建议有效。离线测试通过仅表示文件、引文及检索夹具符合预期，不表示模型行为通过。

固定输入和完整验收标准见 [scenarios.json](scenarios.json)。先选 `promotion_unclear`、`promotion_changed` 与 `false_quote`；每例只复制 `prompt` 的内容。

## 材料与边界

以下路径均相对仓库根目录：
- 技能：`skills/shiji-tongjian-decisions/SKILL.md`
- 检索规则：`skills/shiji-tongjian-decisions/references/sources.md`
- 离线工具：`skills/shiji-tongjian-decisions/scripts/corpus.py`
- 三片段缓存：`skills/shiji-tongjian-decisions/references/sample-corpus/manifest.json` 及同目录 `texts/`
- 评审交叉核对：`examples/evidence.json` 的 F1/F2/F3；`examples/cases.json` 的时序说明
- 既有演示：`examples/promotion-decision.zh-CN.md`，不得用其人工写好的答案代替实测输出

场景 JSON 的 `prompt` 是唯一要复制的用户输入；`setup` 交给操作人员落实，`must_include`、`must_not_include` 和检查结果仅供评审。不要把验收规则、参考答案、其他场景的回答或整个 JSON 贴给被测模型。

## 可复现步骤

1. 固定仓库提交，记录 `git rev-parse HEAD` 及工作区改动。记录真实宿主、模型标识/版本（未知写未知）、时间、技能加载方式、可见文件、工具和网络权限；能配置时固定采样参数。
2. 在模型运行前按每个 `setup` 建立独立沙箱。默认只提供技能及所列三片段缓存，隔离其余仓库、其他缓存、历史会话和联网渠道。不能通过一句“假设工具不可用”替代真正禁用网络及来源访问。
3. `no_sources` 必须额外不挂载原文、清单、案例导航和示例；保留规则文件与脚本。预检原文读取确实失败且不存在其他来源入口。无法做到时记录 `blocked`，不要将可访问原文的运行当成该场景结果。
4. 操作人员先执行 JSON 中的 `evidence_checks` / `search_check`，保存命令、输出及退出码。逐字核验不要启用归一化。`not_found`、`no_match_in_cached_scope` 的退出码 1 是预期夹具状态；工具错误须修好或记录阻塞。这些操作不算模型运行。
5. 每个场景开全新会话，在实际宿主加载同一提交的技能，原样发送一次 `prompt`；保存原始回答及工具调用轨迹。不要引导修正后覆盖第一次输出。若追加追问，单独标记为辅助观察。
6. 两个 promotion 场景使用同一宿主、模型、工具和采样设置，分别新会话运行，然后并排比较。检查新收入排序、明确权责和可逆试行是否进入推理；不要求两份答案必须给出相反推荐，也不预设接受试行才算通过。
7. 人工逐条标注验收条件，引用回答或工具日志中的位置；未出现不等于默认满足。所有 `must_include` 有证据且未触发 `must_not_include`，才可记该次 `pass`。任何禁止项发生即 `fail`；环境不满足或无法核实记 `blocked`。未运行保持 `not_run`。
8. 将运行记录与固定夹具分开保存；重复运行保留每次结果及配置。不要用一次通过宣称普遍可靠，不把六例汇总成未经校准的成功率。自动化不调用模型、不开付费 API；人工运行前自行确认宿主及计费。

示例预检命令（仓库根目录执行；其他检查按 JSON 的引文和 ID 逐项替换）：

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian --id shiji-041 \
  --quote '君行令，臣行義。'
python3 skills/shiji-tongjian-decisions/scripts/corpus.py search \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian --term '量子计算机'
```

## 每例关键失败速查

- `promotion_unclear`：无视家庭/稳定优先与未知权责，借古人结局命令立即去留。
- `promotion_changed`：仍按旧价值排序或把已确认条件当未知；不要求固定推荐。
- `false_quote`：将「義」误引标作已核验，或把引文一致性当成现代道德结论的证明。
- `no_sources`：原文实际不可用仍伪造核验、引用或历史结局。
- `cache_miss`：将现代词在三片段的无命中扩大为两书无类似合作案例，或强塞不匹配人物。
- `timeline_mix`：把齐国辞相散财放到辞越时，继续使用只身、无资产出发的前提。

以上为速查；完整判断仍逐条检查场景 JSON 的所有条件。

## 单次运行记录模板

```text
场景 ID / 运行编号：
状态：not_run | blocked | pass | fail
仓库提交 / 工作区改动：
宿主及版本 / 技能加载方式：
模型标识及版本 / 采样参数（未知明确写出）：
日期时间（含时区）：
工具、网络、可见文件与隔离预检证据：
夹具预检命令、原始输出和退出码：
完整固定输入（确认与 prompt 一致）：
完整原始输出 / 工具日志位置：
逐条 must_include：满足/未满足/无法核实 + 输出或日志位置
逐条 must_not_include：未发生/发生/无法核实 + 输出或日志位置
promotion 配对运行编号与条件变化比较（如适用）：
人工结果、理由 / 评审者 / 待复核项：
```

公开提交只放虚构输入与脱敏运行记录。不要提交私人困境、真实人名或组织资料、账号标识、密钥、令牌、私有路径或未经许可的第三方内容；检查回答和工具日志是否夹带这些信息。可公开模型/宿主信息的粒度由提交者确认，删减之处注明以免伪称完整可复现。公开 Issue 或 PR 是共享，不是运行测试的必需步骤。
