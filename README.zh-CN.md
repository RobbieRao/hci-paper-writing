<p align="center">
  <img src="assets/hci-paper-coach-hero.png" alt="HCI Paper Coach：投稿前找到论证薄弱处" width="100%">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/RobbieRao/hci-paper-writing/actions/workflows/ci.yml"><img src="https://github.com/RobbieRao/hci-paper-writing/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-34d399.svg" alt="MIT License"></a>
  <a href="skills/hci-paper-writing/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-open%20standard-8b5cf6.svg" alt="Agent Skill"></a>
  <img src="https://img.shields.io/badge/version-0.4.0-60a5fa.svg" alt="版本 0.4.0">
  <img src="https://img.shields.io/badge/preflight-local%20%26%20read--only-22d3ee.svg" alt="本地只读预检">
  <img src="https://img.shields.io/badge/benchmark-%E6%AD%A3%E5%9C%A8%E5%BC%80%E5%8F%91-f59e0b.svg" alt="Benchmark 正在开发">
</p>

<p align="center">
  <strong>投稿前，先找到论证最薄弱的地方。</strong><br>
  一个面向 HCI 论文的开源 Agent Skill。它梳理 contribution 与 evidence，
  用 HCI 特定的 reviewer lenses 做压力测试，并让初稿到 rebuttal 的修改过程可追踪。
</p>

---

很多学术写作工具从语言润色开始。HCI Paper Coach 先看论文的论证：作者提出了
什么 HCI contribution，证据是否足以支持它，reviewer 可能在哪里失去信心。

项目面向准备投稿 **CHI、CSCW、DIS、UIST、TOCHI 及相关 HCI venue** 的作者。
定性研究、interaction technique、field deployment 和 Research through
Design 各有自己的评价标准，因此 Skill 会选择相应的 review lens。

> [!IMPORTANT]
> 这是作者侧的诊断与修改工具。它不预测中稿、不生成引用，也不能替代研究者的判断。

> [!NOTE]
> 我们正在准备近五年 CHI 论文 embedding 分析，以及经权利确认的接收/拒稿投稿、
> reviews 与 rebuttals 数据集。[Benchmark 贡献者将获得私测优先邀请。](#hci-paper-coach-benchmark正在开发)

## 三个核心工作流

| 工作流 | 它做什么 | 你会得到什么 |
|---|---|---|
| **`hci-diagnose`** | 重建论文主张，判断 contribution type，梳理证据链 | Contribution diagnosis、claim-evidence matrix、最高风险 |
| **`hci-red-team`** | 分别从贡献、方法、读者/venue 三个视角攻击论文 | 合并去重后的 major risks、champion sentence、killer concern |
| **`hci-revision`** | 把诊断或 reviewer feedback 转换为有顺序的修改任务 | 带证据需求与验证方式的 revision ledger |

同一个 Skill 也支持论文规划、章节修改、用户研究报告、interaction figure、
LLM-integrated system、隐私检查和投稿政策核验。

### v0.4.0 重点能力

| 能力 | 为什么重要 |
|---|---|
| **CHI 2022–2026 趋势图谱** | 看清哪些 HCI 对话快速升温、持续成熟、剧烈波动，或在 CHI 扩张中失去相对份额 |
| **CHI 2027 情景预测** | 给出八个带置信度和反证信号的方向，不伪造“选题中稿率排行榜” |
| **分面化 closest-work 分析** | 分开比较 problem、contribution、method、findings 与 limitations，不再相信一个笼统的邻近论文列表 |
| **Threat-set 对照** | 在写 novelty delta 前，主动寻找同问题/不同方法与同方法/不同问题的工作 |
| **搜索稳定性检查** | 用等义改写和中英文检索暴露 literature coverage 不稳定的情况，避免过早下 positioning 结论 |
| **Release 隐私门禁** | CI 检查 tracked release files 中常见的 credential、私有路径、外部 symlink、大文件与本地 artifact |
| **持久化 `.hci-paper/` 工作区** | Claims、figures、reviewer comments、政策核验与修改承诺可以跨 session 保留 |
| **HCI reviewer panel** | Contribution、method tradition、reader/venue 三个 lens 先分别审阅，再做保留分歧的 meta-review |
| **Rebuttal 闭环账本** | 每个 response promise 都对应 manuscript change 与 verification |
| **机器可读一致性审计** | Reverse outline、RQ、强 claim、未完成文本和 LaTeX 图表完整性都可输出为 Markdown 或 JSON |
| **不可静默跳过的 stage gates** | 论文从 framing、study-ready、evidence-frozen、claim-locked 一直走到 review 与 submission，每步保留依据 |
| **来源与 endorsement 账本** | Chat、meeting、email、reviewer 与 coauthor 材料保留 speaker、permission、evidence 和作者认可状态 |
| **DOCX 与 submission integrity 检查** | 本地审计覆盖 DOCX、匿名泄漏、LaTeX inputs、graphics、bibliography 与 citation keys |

它不是给通用语法润色器贴一层 HCI prompt，而是从 HCI 的 contribution types
和不同研究传统出发组织整套工作流。

它还会分开记录四个不同决定：贡献是什么、属于哪个 research area、以什么
research tradition 产生知识，以及投向哪个 venue。Human-AI 论文不自动等于
systems paper，CHI 论文也不自动等于 controlled experiment。

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

如果是一篇需要多轮修改的论文：

```text
请用 $hci-paper-writing 的 hci-init 模式初始化这个项目，然后运行 hci-panel。
```

## 本地 manuscript preflight

在语义审稿前运行本地确定性扫描：

```bash
python3 skills/hci-paper-writing/scripts/manuscript_audit.py paper.tex \
  --anonymous --strict
```

它会检测：

- 论文结构和常见缺失章节；
- 明确的 RQ 与 contribution 表达；
- trust、understanding、agency、usefulness 等强 construct；
- 常见的 study、ethics 与 limitations 标记；
- 每个章节开头论证动作构成的 reverse outline；
- LaTeX 图表定义、引用、caption 与孤立 label；
- LaTeX inputs、graphics、bibliography files 与 citation-key resolution；
- author metadata、email、identifying URL、acknowledgment 等常见匿名泄漏；
- `TODO`、`TBD`、`FIXME` 等未完成内容。

扫描器只使用 Python 标准库，**本地运行、只读、零网络请求**。它支持 `.docx`、
`.md`、`.tex` 和 `.txt`，只报告值得进一步检查的位置，不给论文打质量分。
Strict mode 只会因确定性的 integrity defect 失败，不会因有争议的语义建议失败。

需要接入 agent pipeline 或 benchmark harness 时，可加 `--format json` 得到
稳定的机器可读输出。

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

## 近五年 CHI 到底变了什么？

最短的结论是：CHI 正从“AI 能完成某个任务”的通用 prototype，转向 agency、专业
实践、治理、照护、教育、身份、核验与失败处理等更难的人机问题。

| 快速变化的研究对话 | 本快照论文数，2022 → 2026 | 最应该避免的拥挤默认贡献 |
|---|---:|---|
| Chatbot agency、人格与 self-concept | 6 → 79 | 再做一个一次性 chatbot usability study |
| 生成式 AI 在专业创意实践中的部署 | 0 → 80 | 只说“AI 提升创意”，不研究作者身份、控制权、provenance 或真实工作流 |
| LLM 事实核验、人格与内容评估 | 2 → 89 | 只报模型 accuracy，不研究人如何核验或形成依赖 |
| AI 叙事共创、儿童创作与 XR 表达 | 5 → 66 | 没有发展阶段、具身、文化或安全机制的通用故事生成器 |
| AI 治理、组织采纳与责任实践 | 9 → 63 | 没有 decision rights、accountability 或部署证据的态度问卷 |

CHI 2027 的高置信度情景包括：negotiated AI agency、situated deployment、
epistemic interaction（provenance、不确定性与核验）以及多方后果。中等置信度情景
包括具身/空间生成式交互、长期 AI 关系、作为方法与治理问题的 accessibility，以及
AI 介入研究实践。

阅读完整双语图谱：
[简体中文](skills/hci-paper-writing/references/chi-trends-2022-2026.zh-CN.md) ·
[English](skills/hci-paper-writing/references/chi-trends-2022-2026.md)

这些是 proceedings 趋势，不是投稿或中稿预测。图谱会区分论文原始数量增长与年度
份额增长，并明确什么证据可能推翻每项判断。

## 给每篇论文一份可持续的记忆

在已有论文目录中初始化本地工作区：

```bash
python3 skills/hci-paper-writing/scripts/project_workspace.py \
  /path/to/paper --manuscript paper.tex
```

它会创建 `.hci-paper/`，其中包含 context，以及 claims、sources 与 endorsement、figures、reviewer
comments、revision 和已核验 venue policies 的独立账本；`runs/` 用来保存可比较的
审计报告。初始化器没有第三方依赖、不会联网，也不会覆盖已有工作区。

可以先用 `--dry-run` 查看计划，或用 `--json` 接入其他工具。

工作区包含一条有顺序的 lifecycle：

```text
framing -> study-ready -> evidence-frozen -> claim-locked -> drafted -> reviewed
-> response-ready -> submission-ready
```

每次检查完一个 gate 后只前进一步：

```bash
python3 skills/hci-paper-writing/scripts/project_workspace.py /path/to/paper \
  --advance study-ready --note "RQs、ethics 与 study plan 已检查"
```

脚本会阻止静默跳级，但不会假装一份 state file 能证明研究质量；记录的依据与
底层 artifacts 仍然需要人来检查。

## 整合笔记，不窃取其中的主张

`hci-integrate` 用于 chats、emails、meeting transcripts、reviewer comments 与
lab notes。它会先记录每个想法是谁提出、作者是否认可、有什么 evidence，以及
是否有权使用。作者尚未接受或已经否定的想法，不会擅自进入 manuscript。

`hci-positioning` 则检查论文是否先建立 importance，再给出可辩护的 unresolved
question、最小诚实 novelty delta，以及 evidence 真正能够满足其 review contract
的 contribution noun。

## 从 reviewer concern 到已验证的修改

`hci-panel` 会先收集相互隔离的 reviewer lenses，再做综合。如果运行平台无法提供
真正独立的 reviewer，Skill 会明确说明，而不会把连续扮演的 persona 包装成独立证据。

`hci-rebuttal` 会给 concern 分配稳定 ID，并追踪下面这条链：

```text
reviewer concern -> evidence -> response claim -> manuscript change -> verification
```

目的不是写一封更自信的 rebuttal，而是防止 response letter 与委员会最终看到的
manuscript 脱节。

## 它怎么工作

### Contribution 优先，语言润色靠后

“我们进行了一项用户研究”描述的是研究活动。Skill 会继续追问这项研究揭示、
验证、实现或改变了什么 HCI 知识，再判断它是否构成 contribution。

### 按研究传统选择 method lens

Qualitative、quantitative、design research、systems、field/CSCW 和 mixed
methods 论文需要不同的评价标准。Skill 会选择适合稿件的 lens，不会默认要求实验。

### 让每条批评都能回到稿件

每条主要批评都要指出 manuscript evidence，说明问题会影响什么，并给出可执行的
修复方案。强 claim 需要 evidence、citation，或者更克制的措辞。

### 语料比较要保留 provenance

使用明确声明的 corpus 比较 manuscript 时，`hci-grounded` 协议会记录 corpus、
年份、query、filters、覆盖缺口和实际查看过的来源。Embedding 可以检索相近论文，
但仅凭相似度不能判断 novelty、quality 或中稿可能性。

### 实时核验投稿政策

Venue 规则会变化。Skill 要求 agent 在运行时从官方页面核验 deadline、length、
anonymization、accessibility、ethics、AI-use disclosure 与 supplementary
material，而不是相信缓存记忆。

### 说明隐私边界

本地 scanner 不会发送 manuscript。语义审稿时的数据处理方式取决于运行 Skill
的 AI 平台，不由这个 GitHub 仓库控制。未经明确授权，不要把正在审阅的
confidential submission 上传给第三方模型。

## 仓库结构

```text
skills/hci-paper-writing/
├── SKILL.md                         # Router、guardrails、输出契约
├── agents/openai.yaml               # UI 元数据
├── assets/                          # Intake 与 revision 模板
├── scripts/
│   ├── manuscript_audit.py          # 本地确定性预检
│   ├── project_workspace.py         # 安全的持久化论文状态初始化器
│   ├── release_guard.py             # 阻止私有 artifact 进入 release
│   └── validate_skill.py            # 零依赖结构校验
└── references/
    ├── contribution-types.md
    ├── chi-trends-2022-2026.md
    ├── chi-trends-2022-2026.zh-CN.md
    ├── evidence-grounding.md
    ├── novelty-and-positioning.md
    ├── workflows.md
    ├── method-lenses.md
    ├── study-evidence.md
    ├── section-patterns.md
    ├── reviewer-checklist.md
    ├── reviewer-panel.md
    ├── rebuttal-and-revision.md
    ├── project-workspace.md
    ├── source-integration.md
    ├── llm-systems.md
    └── policy-and-privacy.md
```

## 设计原则

1. 作者保留判断权。Agent 组织批评，但不替研究者决定论文应该声称什么。
2. Skill 不虚构引用、参与者、统计数据、政策或 reviewer 共识。
3. Research strength 与 venue fit 分开报告，Skill 不生成中稿概率。
4. Rigor 按论文所属的研究传统评价。
5. 每条反馈都包含证据、严重度、修复方案与验证方式。

## Roadmap

- [x] Contribution diagnosis 与 claim-evidence workflow
- [x] 三视角 HCI red-team
- [x] 本地 Markdown / LaTeX / text preflight
- [x] 定性、定量、design、systems、field 与 mixed-method lenses
- [x] 隐私边界与实时政策核验
- [x] English / 简体中文双语 README
- [x] 持久化 per-paper workspace 与机器可读 ledgers
- [x] Reverse outline 与 LaTeX 图表一致性检查
- [x] 角色分离的 HCI reviewer panel 与 meta-review protocol
- [x] Reviewer comment、rebuttal、revision 与 verification 闭环
- [x] DOCX、匿名、LaTeX dependency、bibliography 与 citation-key 检查
- [x] 带不可跳级 transition 的论文 lifecycle
- [x] Source ownership、endorsement、permission 与 evidence tracking
- [x] Contribution form、research area、tradition 与 venue 四轴模型
- [x] 双语 CHI 2022–2026 趋势图谱与 CHI 2027 情景预测
- [x] 分面化 threat-set 分析与双语搜索稳定性检查
- [x] 公开 release 隐私门禁
- [ ] HCI Paper Coach Benchmark：可复现发布近五年 CHI 分析
- [ ] 经权利确认的接收/拒稿投稿、reviews 与 rebuttals
- [ ] 带版本化数据切分、annotations 与 data cards 的公开 benchmark
- [ ] 正文、figures 与 tables 的数字和术语一致性检查
- [ ] CSCW、DIS、UIST、accessibility 与 health HCI 专项包
- [ ] 中英文双语报告模板
- [ ] 跨 manuscript version 的 reviewer-feedback 纵向对比

<a id="hci-paper-coach-benchmark正在开发"></a>

## Benchmark 正在开发

双语的 2022–2026 趋势图谱现在已经可以使用。底层可复现的 benchmark package
仍在开发；它会按 HCI 方法传统评价论文反馈，并把三类数据分开报告：

1. 近五年 CHI 论文语料，用于 embedding 辅助的 contribution、method、topic
   与 subcommunity 分析。发布时会说明准确的覆盖范围、检索参数、来源链接和已知
   缺口。只有在许可允许时才会索引或再分发全文。
2. 作者贡献的接收与拒稿历程。数据可包含 manuscript、reviews、rebuttal、
   decision 与 revision history。每份材料必须完成权利确认、符合适用 venue
   policy，并按需匿名化。
3. 合成稿与专家标注案例，用于评测 contribution diagnosis、claim-evidence
   alignment、method fit、reviewer-risk recovery、建议的可执行性和 false positives。

这个 benchmark **尚未发布**。当前 Skill 没有使用 CHI 私密 reviews 训练或验证。

可以贡献 synthetic failure case、annotation protocol、检索或评测代码、公开
metadata source，或者经过授权的投稿历程。贡献者会获得私测优先邀请，具体安排
取决于名额以及数据与 consent 审核。参与前请阅读
[CONTRIBUTING.md](CONTRIBUTING.md)。不要在公开 issue 中附上机密材料。

## 参与贡献

目前最需要的是方法特定的失败案例、可公开的合成测试稿，以及当前官方政策来源。
参与方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果项目帮你在 review 前发现了严重问题，可以给仓库一个 Star，方便其他 HCI
研究者找到它。

## 负责任地使用

- 用于作者侧 formative feedback，不用于自动化 peer-review gatekeeping。
- 自己核验 citation 与 venue policy。
- 遵守目标 venue 的 AI-use disclosure policy。
- 不要把属于他人的 confidential manuscript 提交给第三方模型。
- 本项目与 ACM、SIGCHI、CHI、CSCW、DIS、UIST 等机构或会议没有隶属或背书关系。

## License 与来源

项目采用 MIT License。详见 [LICENSE](LICENSE) 与
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
版本记录见 [CHANGELOG.md](CHANGELOG.md)。

本项目为独立创作，参考了公开的 HCI 投稿指南与开源学术写作工作流；仓库中没有
直接打包第三方源代码。
