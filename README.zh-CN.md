<p align="center">
  <img src="assets/hci-paper-coach-hero.png" alt="HCI Paper Coach — 让贡献无可置疑" width="100%">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/RobbieRao/hci-paper-writing/actions/workflows/ci.yml"><img src="https://github.com/RobbieRao/hci-paper-writing/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-34d399.svg" alt="MIT License"></a>
  <a href="skills/hci-paper-writing/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-open%20standard-8b5cf6.svg" alt="Agent Skill"></a>
  <img src="https://img.shields.io/badge/preflight-local%20%26%20read--only-22d3ee.svg" alt="本地只读预检">
</p>

<p align="center">
  <strong>别再润色句子了——先确认论文的论证没有坏。</strong><br>
  一个面向 HCI 论文的开源 Agent Skill：诊断 contribution、追踪 claim 与
  evidence，并在真正的 reviewer 之前对稿件进行 red-team。
</p>

---

大多数学术写作工具优化的是语言。**HCI Paper Coach 检查的是 reviewer
真正需要相信的东西：这篇论文是否提出了清晰的 HCI contribution，以及它
是否由正确类型的证据支撑。**

项目面向准备投稿 **CHI、CSCW、DIS、UIST、TOCHI 及相关 HCI venue** 的作者。
它知道定性研究、interaction technique、field deployment 与
Research through Design 不能被同一套通用 rubric 粗暴评价。

> [!IMPORTANT]
> 这是作者侧的诊断与修改工具，不是中稿预测器、引用生成器，也不能替代研究者的判断。

## 三个真正有用的核心工作流

| 工作流 | 它做什么 | 你会得到什么 |
|---|---|---|
| **`hci-diagnose`** | 重建论文主张，判断 contribution type，梳理证据链 | Contribution diagnosis、claim-evidence matrix、最高风险 |
| **`hci-red-team`** | 分别从贡献、方法、读者/venue 三个视角攻击论文 | 合并去重后的 major risks、champion sentence、killer concern |
| **`hci-revision`** | 把诊断或 reviewer feedback 转换为有顺序的修改任务 | 带证据需求与验证方式的 revision ledger |

此外还包括：论文规划、章节修改、用户研究报告、interaction figure、
LLM-integrated system、隐私边界，以及投稿政策的实时核验。

## 30 秒安装

### Codex 与兼容 Agent Skills 的工具

```bash
git clone https://github.com/RobbieRao/hci-paper-writing.git
cd hci-paper-writing
./install.sh codex
```

### Claude Code

```bash
git clone https://github.com/RobbieRao/hci-paper-writing.git
cd hci-paper-writing
./install.sh claude
```

安装器会创建 symlink，因此以后执行 `git pull` 就能更新 Skill。若目标位置
已经存在，它会拒绝覆盖，避免破坏你自己的版本。

安装后可以直接说：

```text
Use $hci-paper-writing in hci-diagnose mode on my abstract and contributions.
```

或者：

```text
请用 $hci-paper-writing 对这篇 CHI 论文做 hci-red-team，
分别检查 contribution、method 与 reader/venue risks。
```

## 本地 manuscript preflight

在语义审稿前，先运行一次确定性扫描：

```bash
python3 skills/hci-paper-writing/scripts/manuscript_audit.py paper.tex
```

它会检测：

- 论文结构和常见缺失章节；
- 明确的 RQ 与 contribution 表达；
- trust、understanding、agency、usefulness 等强 construct；
- 常见的 study、ethics 与 limitations 标记；
- `TODO`、`TBD`、`FIXME` 等未完成内容。

扫描器只使用 Python 标准库，**本地运行、只读、零网络请求**。它输出的是
review leads，而不是假装精确的“论文质量分数”。

<details>
<summary><strong>查看 preflight 示例</strong></summary>

```text
# Local Manuscript Preflight

- File: synthetic-paper.md
- Sections detected: 6
- Privacy: local read-only scan; no network requests

## Contribution Candidates
- We introduce TraceLens and use it as a research artifact...

## Review Leads
- Strong-claim term detected: usefulness
- Verify that the construct is operationalized or carefully bounded
```

你可以直接用仓库里的[合成示例论文](examples/synthetic-paper.md)测试。它不包含
任何真实参与者或伦理审批信息。
</details>

## 它为什么不一样

### Contribution 优先，语言润色靠后

Skill 不会把“我们进行了一项用户研究”当成 contribution。它会继续追问：
这项研究揭示、验证、实现或改变了什么 HCI 知识？

### 理解方法传统，而不是迷信某一种方法

它会在 qualitative、quantitative、design research、systems、field/CSCW
与 mixed methods 之间选择适合的 lens，不会因为 controlled experiment 熟悉，
就要求所有 HCI 论文都去做实验。

### 先要证据，再给自信

每一条主要批评都必须指出 manuscript evidence、解释为什么重要，并给出
最低限度可执行的修复方案。每个强 claim 都必须对应 evidence、citation，
或者更克制的措辞。

### 查当前政策，不背过期规则

Venue 规则会变化。Skill 要求 agent 在运行时从官方页面核验 deadline、length、
anonymization、accessibility、ethics、AI-use disclosure 与 supplementary
material，而不是相信缓存记忆。

### 把隐私边界说清楚

本地 scanner 不会把 manuscript 发到任何地方。Skill 也会提醒用户：模型侧数据
如何处理，由运行 Skill 的平台决定，而不是由这个 GitHub 仓库决定。未经明确授权，
不要把你正在审阅的 confidential submission 上传给第三方模型。

## 仓库结构

```text
skills/hci-paper-writing/
├── SKILL.md                         # Router、guardrails、输出契约
├── agents/openai.yaml               # UI 元数据
├── assets/                          # Intake 与 revision 模板
├── scripts/
│   ├── manuscript_audit.py          # 本地确定性预检
│   └── validate_skill.py            # 零依赖结构校验
└── references/
    ├── contribution-types.md
    ├── workflows.md
    ├── method-lenses.md
    ├── study-evidence.md
    ├── section-patterns.md
    ├── reviewer-checklist.md
    ├── llm-systems.md
    └── policy-and-privacy.md
```

## 设计原则

1. **作者保留判断权。** Agent 负责搭建批评结构，不替研究者决定论文应该声称什么。
2. **不伪造权威。** 不虚构引用、参与者、统计数据、政策或 reviewer 共识。
3. **拒绝 acceptance theater。** 分开判断 research strength 与 venue fit，
   不生成虚假的中稿概率。
4. **尊重 HCI 的认识论多样性。** 在论文所属的研究传统内部评价 rigor。
5. **不能行动的建议就不输出。** 反馈必须包含证据、严重度、修复方案与验证方式。

## Roadmap

- [x] Contribution diagnosis 与 claim-evidence workflow
- [x] 三视角 HCI red-team
- [x] 本地 Markdown / LaTeX / text preflight
- [x] 定性、定量、design、systems、field 与 mixed-method lenses
- [x] 隐私边界与实时政策核验
- [x] English / 简体中文双语 README
- [ ] 使用合成稿与作者授权稿建立公开 benchmark
- [ ] LaTeX 跨章节一致性检查
- [ ] CSCW、DIS、UIST、accessibility 与 health HCI 专项包
- [ ] Reviewer-feedback 对比与 revision tracking

## 参与贡献

最有价值的贡献不是再加一段泛泛的提示词，而是提交一个**方法特定的失败案例**、
一篇**可公开的合成测试稿**，或者一个**当前官方政策来源**。请阅读
[CONTRIBUTING.md](CONTRIBUTING.md)。

如果它帮你提前发现了一个本来会进入 review 的致命问题，欢迎给仓库一个 Star。
这会让更多 HCI 研究者找到一个真正检查论证、而不只是检查语法的工具。

## 负责任地使用

- 用于作者侧 formative feedback，不用于自动化 peer-review gatekeeping。
- 自己核验 citation 与 venue policy。
- 遵守目标 venue 的 AI-use disclosure policy。
- 不要把属于他人的 confidential manuscript 提交给第三方模型。
- 本项目与 ACM、SIGCHI、CHI、CSCW、DIS、UIST 等机构或会议没有隶属或背书关系。

## License 与来源

项目采用 MIT License。详见 [LICENSE](LICENSE) 与
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

本项目为独立创作，参考了公开的 HCI 投稿指南与开源学术写作工作流；仓库中没有
直接打包第三方源代码。

