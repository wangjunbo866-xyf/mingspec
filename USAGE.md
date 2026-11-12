# mingspec Usage

mingspec 是产品名，源码提供四个 Skill 入口和可选 Python CLI（空框架、只读任务检查与主规格篇幅提醒）。本文件是普通使用导航。

| Skill | 标识 | 何时使用 |
| --- | --- | --- |
| [Ming Spec](skills/ming-spec/SKILL.md) | `ming-spec` | 需求归属、业务地图、SPEC、现有 Patch 修订与对账、影响与验收 |
| [Ming Tickets](skills/ming-tickets/SKILL.md) | `ming-tickets` | 在已授权范围内生成、核对或修订 Patch 任务，维护规格引用、依赖、执行边界和结果 |
| [Ming Archive](skills/ming-archive/SKILL.md) | `ming-archive` | 部分吸收或完整收尾：核对验收与独立审查，吸收已交付规则并同步来源/地图/状态 |
| [Ming Runbook](skills/ming-runbook/SKILL.md) | `ming-runbook` | 初始化 mingspec、已确认经验/约定、AGENTS 摘要迁移和入口守卫 |

当前规格采用 `mingspec/specs/<domain>/<module>/spec.md`，新候选位于同模块 `patches/<patch-id>/spec.md`。域和模块按职责确定；跨模块目标在主责模块维护单一 Patch 并引用实际影响。根/域/模块索引分层表达地图。旧布局按 [迁移流程](skills/ming-spec/references/spec-home.md) 处理，查询只读；历史 Patch 可留原位。项目事实从目标入口读取，工具资源从完整产品安装位置读取。四条 Skill 保持隐式选择，不提供后台监听或跨会话守护。

明确要求拆任务，或已有授权覆盖完整交付时，才由 Ming Tickets 维护现有 Patch 的 tasks.md，并在开始时说明目标与产物。单纯讨论、回答澄清问题或只要求写 SPEC 不自动生成任务。实施、TDD 和独立审查由选定执行者按项目流程完成，实际采用的方法与结果留任务记录；任务生成不自动启动业务实施。执行方法由目标项目选择，不绑定工具或自动授予安装权限。

新增功能包括首次能力，统一先建 Patch，验收与独立审查通过后由 Ming Archive 吸收进模块主规格。既有行为首次补档可建立有据基线并说明缺口，详见 [First Specification](skills/ming-spec/references/business-map.md#first-specification)。历史 change 与 Patch 同义，后续新候选统一 patches 下的 spec.md；纯记录及历史按[命名边界](skills/ming-spec/SKILL.md#name-the-patch-specification)保留职责。模块主规格独立版本化并保留来源，不要求 OpenSpec 专用产物或校验。

实施有准备依赖或技术假设未证实时，必须按 [Ming Tickets 前置验证步骤](skills/ming-tickets/SKILL.md#decompose-and-check-dependencies) 在授权内安排同一 Patch 的前置任务，观察、决定和未决项回写 Patch。仅获准写 SPEC 时只记录问题、判据和任务影响，不创建 tasks 或执行验证。原始证据复用已有位置，不新建独立 verification/；技术可行不代替功能验收。

规则按可独立验证行为组织；修改旧规则逐场景对账，删除或纯改名按旧行为验收，收尾说明有效内容去向。各任务就近交付必要测试、文档和实际结果；任务方法见 [Ming Tickets](skills/ming-tickets/SKILL.md)，规格步骤见 [Ming Spec](skills/ming-spec/SKILL.md) 与[锚点指引](skills/ming-spec/references/spec-anchors.md)，不增加阶段。

修订已有 Patch 使用 [Ming Spec 的修订操作](skills/ming-spec/SKILL.md#revise-an-existing-patch)，对账规则、设计、任务与证据。只改 SPEC 时保持 tasks 不变并报告任务影响；明确同步已有规格和任务或完整交付授权覆盖时，再由 Ming Tickets 修订相关任务。已有授权不逐文件重问，缺失材料、新目标和未交付状态分别说明；本操作不增加阶段。

## Choose a Template

从完整产品的实际安装位置读取模板，按资料身份选择：

| 资料 | 模板与结构 | 使用边界 |
| --- | --- | --- |
| 当前模块主规格 | [Main Specification](skills/ming-spec/assets/main-spec.md)：范围、术语与模型、公共依赖、行为、接口与兼容、来源六章 | 首建或修订有依据的当前规则；新功能须先 Patch 并满足原验收及独立审查门槛 |
| Patch 候选 | [Patch Specification](skills/ming-spec/assets/spec.md)：目标、现状影响、行为验收、设计测试、未决与来源五章 | 记录变更和稳定 AC，不将候选五章直接搬为主规格章节 |
| Patch 任务 | [Tasks](skills/ming-tickets/assets/tasks.md)：state、blocked_by、rules、acs、questions 五字段 | 仅在任务维护授权内使用；格式、旧任务转换与检查按下方 Check Task Declarations |

模板默认版本、状态和示例 ID 不用于重置既有资料。修订保留实际状态、版本沿革、稳定规则/AC/任务 ID、旧锚点及完整条件；既有主规格沿已采用结构，未经授权不因模板调整重排章节。生成时去除占位提示，需保留的链接改为目标位置可读的实际来源。模板不自动创建任务、启动实施或吸收规格。

首建或修订主规格时，必须执行 [主规格阅读契约](skills/ming-spec/references/spec-home.md#independently-readable-main-specifications)；完成前由未参与修改者先读主规格及明确公共引用、记录判断，再按 [Independent Reading Check](skills/ming-spec/references/spec-home.md#independent-reading-check) 对账来源。必要缺口阻止相关完成，链接检查不代替语义核对或业务验收。

## Use Ming Archive

下面是自然语言请求示例，P-01 代表你指定的实际 Patch，不是新增命令或阶段；步骤见 [Choose the Scope](skills/ming-archive/SKILL.md#choose-the-scope)。

| 你可以这样说 | 处理范围 |
| --- | --- |
| “看看 P-01 能不能收尾，只读说明。” | 核对已有验收、审查与冲突，报告可吸收范围和缺口，不修改文件 |
| “吸收 P-01 中已验收的查询规则，导出继续留在 Patch。” | 核对查询规则的完整验收与审查依据，吸收后保留导出候选和整份 Patch 未完成状态 |
| “完成 P-01 的收尾。” | 核对全部拟交付内容的去向，完成吸收、来源/导航同步和最终独立复核；依据不足时报告缺口 |

部分吸收与完整收尾使用相同的验收和独立审查门槛，部分吸收也包含写后独立复核。单项任务标记完成或一条 AC 的部分场景通过，都不等于完整规则可吸收。当前仅提供单个 Patch 的上述操作及相关并行冲突核对，批量收尾尚未提供；目录搬迁、提交、合并和部署仍按各自授权处理。

## Maintain Short Specifications

按需读全相关规则及依赖，每个 Patch 围绕一个可验收目标演进。主规格超过 300 行时评估功能模块边界，内聚正文可说明理由后保留；条件、例外和场景保持完整。操作见 [Small-Step Maintenance](skills/ming-spec/references/spec-home.md#small-step-maintenance)，只读统计见 [spec-size 命令](#main-specification-size)。

## Check Task Declarations

Ming Tickets 生成或更新任务后、执行者回写状态后、Ming Archive 准备吸收或只读查询含任务的 Patch 时，由 Agent 按 [任务检查步骤](skills/ming-tickets/references/task-checks.md)调用 [tasks 命令](#task-check-command)，通常无需另行提醒；Archive 先检查再核对其余依据，只读查询仅在答复报告结果。新任务使用五字段模板；旧格式和工具不可用时会报告缺口，暂停依赖的交接/吸收，不自动迁移或安装。没有任务的吸收或查询记录不适用，检查通过仍不等于真实完成或业务验收。这是 Skill 指引，依赖宿主加载和执行，不是后台钩子。

## Installation and Initialization

仅需空框架时使用 [CLI](#initialize-a-project)；工具不分析仓库、整理入口或生成虚构域/模块。安装可选 [直接 Skills 包](README.md#project-installation) 或 [插件包装](#installation-details)，两者复用四条 Skill 和资源，先核对已有来源并选择一种。初始化见 [onboarding](onboarding.md)，布局与迁移方法见 [Specification Home](skills/ming-spec/references/spec-home.md)。旧材料清理须已有授权，且迁移检查与独立复核完成、有效内容有归属、原件可取回、引用和工具依赖已核对。必须按 [Retire Migration Artifacts](skills/ming-spec/references/spec-home.md#retire-migration-artifacts) 执行退出条件；保留项说明用途，临时项说明退出条件，只读核对不触发删除。

## Project Files and Knowledge

本文中的 SPEC 指需求和行为说明；Patch 指围绕一次具体变更保存候选说明、任务和结果的记录；AC 指可逐项核对的验收条件。当前已交付行为留模块主规格，待完成的新行为留 Patch，过程经验留 runbook。这些名称用于定位项目文件，不是额外执行阶段。

从目标项目根的 AGENTS、README 和规格导航读取实际职责、当前文件、检查方式和授权范围；目标资料不能从工具安装副本代取。项目事实、名称及业务划分以目标来源为准，不要求额外机器配置。资料缺失或冲突只暂停依赖步骤，查询保持只读。

当前规格位于 `mingspec/specs/<domain>/<module>/spec.md`，同模块的 `patches/<patch-id>/spec.md` 保存候选。根/域/模块索引分别维护域职责、模块边界、规格及状态；沿用已确定的 README.md 或 readme.md 名称，不建立大小写双入口或第二份地图。域按长期职责、模块按可独立描述和验收的能力划分，Skill、CLI或插件名称不决定业务归属。完整步骤按 [Business Map](skills/ming-spec/references/business-map.md) 的对应分支执行。

旧布局写入前必须按 [迁移步骤](skills/ming-spec/references/spec-home.md#migrate-an-existing-project) 核对原件、映射、引用及工具配置，完成验证和独立复核后切换入口。明确迁移授权可直接复用；仅写一份规格不允许整批迁移。未迁移时报告缺口，不并建当前正文、不继续向旧目录新增，也不自动恢复被删除的资料。旧材料退出沿 Installation and Initialization 的完整条件执行，不默认留导航壳；历史原件和独立证据保全。

新能力在明确授权内建立最小候选，旧入口缺失不能当作首次未建；迁移保留稳定身份、当前引用和历史，废弃保留决定和遗留依赖。跨模块目标只在主责模块维护一份 Patch 并引用全部影响；能分别交付验收才拆分，并说明真实依赖。收尾对齐说明、变更和地图，已一致允许零差异；模块版本与 Skill 方法、产品包版本分开。

项目经验留 `mingspec/runbook/`，记录前必须执行 [知识分类与记录要求](skills/ming-runbook/references/knowledge-types.md)：复用既有位置，写清结论、适用范围、依据和实际验证状态，有实质内容才建正文，不将日志、猜测或外部材料直接升级为约定。Ming Runbook 维护项目入口和过程知识，需求归属与能力生命周期交 Ming Spec，验收后的说明更新交 Ming Archive。

首次整理的调查与原文保护执行 [onboarding](onboarding.md)。固定保留 PITFALLS.md 和“改代码前先看 PITFALLS”入口，无经验时可以只有标题。编辑 AGENTS 前后必须执行 [Guard the Entry](skills/ming-runbook/SKILL.md#guard-the-entry)：100行起在授权内迁出详情，115行及以上收敛后才报完成，更严上限优先，只读只提醒；保留四块摘要、强约束和条件，不靠挤行或删规则达标。旧原文默认保存到同级 PROJECT_CONTEXT.md，已有文件不覆盖，已迁移的不重复迁移，摘要保留原文链接。知识记录不授予运维、安装、提交或发布权限。

## Installation Details

以下是基本安装之外的设置、旧入口迁移和排查；基本安装步骤见 [README](README.md#project-installation)。直接 Skills 与插件方式复用同一完整产品，同一宿主/项目先核对已有来源并选择一种。切换前保留产品及项目资料，不覆盖或移除未知链接；业务仓安装与全局配置分别核实授权。

四个标识为 `ming-spec`、`ming-tickets`、`ming-archive`、`ming-runbook`，显示名分别为 Ming Spec、Ming Tickets、Ming Archive、Ming Runbook。元数据位于各自的 `agents/openai.yaml`，保持隐式选择开启；宿主未加载时可重新打开项目会话后核对。菜单发现、自动选择与实际执行须分别验证；发现入口不授予写入权限，关键词、引用别人的案例和未定讨论不触发知识写入。

完整分发保留 scripts、templates、skills、onboarding.md 及随附文档，不能只复制 SKILL.md。Skill 资源按符号链接解析后的真实产品位置读取，目标项目的 `mingspec/runbook/` 是知识目录；USAGE.md 和旧 onboard README 是普通导航，不参与 Skill 发现。

迁移旧整包安装时，确认 `.agents/skills/mingspec` 确实链接到该产品后，只移除旧链接，保留产品与知识目录。新路径已有未知内容时先保留现场。安装后核对实际四入口；本产品不再提供 `mingspec`、`runbook` 或 `mingspec-onboard` 名称的 Skill。迁移后需要在所用宿主中重新核对四入口的发现和执行。

完整产品根目录同时是插件源目录：[plugin.json](plugin.json) 使用 Agent Plugins 1.0，包装版本独立标识，以该清单为准；各 Skill 的方法版本仍以自身正文为准。包直接复用四条 Skill、scripts、templates、onboarding.md 及随附文档，不另存一份操作规则。项目 SPEC、Patch、tasks 与 runbook 继续留目标项目，插件更新不负责改写这些资料。

包内的 [本地目录项](.agents/plugins/marketplace.json) 名为 mingspec-local，指向同一产品根并声明 AVAILABLE；它只提供可安装入口，不自动安装。插件方式要求宿主支持该清单和目录项，请按所用宿主的安装说明操作，本包未验证真实桌面安装。复制产品时保留隐藏的 .agents 目录；单独复制 plugin.json 或 skills 目录不足以构成完整产品。

本包的验证范围见 [Release Notes](RELEASE_NOTES.md)；本产品不维护另一份 .codex-plugin 清单。插件视图可将入口显示为 `mingspec:ming-spec`、`mingspec:ming-tickets`、`mingspec:ming-archive`、`mingspec:ming-runbook`；这是命名空间，仍是同一份四条 Skill。宿主需要本地文件访问能力，调用 CLI 时需要 Python 3.9+；不提供 MCP、服务或生命周期钩子。

本包保留插件清单版本 `0.2.0`，预发布包标识为 `0.2.0-beta.1`；各 Skill 的方法版本独立维护。清单中的三段版本号不代表本包已经成为稳定版。桌面安装/升级/卸载、自然语言自动选择及跨宿主兼容尚未验证；清单解析、项目链接和共享资源可读不能代替这些验证。

## Optional Commands

命令工具为 Python 3.9+ 标准库程序，运行不要求网络、第三方包或 Git。下面命令从完整产品根运行，`/path/to/project` 替换为实际目标项目；移动产品后从新产品位置调用，目标仍传明确项目。使用旧路径 `./bin/mingspec` 的调用请改为 `./scripts/mingspec`。当前平台和宿主验证边界见 [Current Limits](README.md#current-limits)。这些命令不会启动服务或后台任务。

### Initialize a Project

初始化内容由 runbook 完成：读取实际来源、迁移旧 AGENTS 原文、写四块摘要与链接，创建固定 PITFALLS 入口。细节见 [初始化说明](onboarding.md)。用户无需先执行命令。

如果只需要空框架，从产品根运行以下可选工具：

```sh
./scripts/mingspec init /path/to/project
```

省略 path 使用当前目录。它只补缺失文件的标题、空表和静态目录链接：

```text
<project>/
├── AGENTS.md
└── mingspec/
    ├── readme.md
    ├── specs/readme.md
    ├── runbook/readme.md
    └── vendor/readme.md
```

已有文件逐字保留，包括 AGENTS；init 不解析 Markdown、不追加导航、不迁移原文、不做行数提醒或填项目事实。框架生成不等于知识整理完成。新 AGENTS 的 Quick Commands 只有“应用／命令／描述”三列空表；来源、项目命令及状态由 runbook 按实际内容维护。

目标/祖先及受控路径的符号链接或类型冲突在写前退出 2；参数错误退出 2，帮助退出 0 不写入。已有非 UTF-8、未闭合 Markdown 或硬链接文件只保留，不为追加进行解析。系统失败退出 1，可能留下部分框架；核对现场后修复重跑，不自动回滚，不承诺事务/并发协调。旧 review/apply 参数仍不支持。

### Task Check Command

对已采用明确任务字段的 Patch，运行只读检查：

```sh
./scripts/mingspec tasks --root /path/to/project --patch mingspec/specs/domain/module/patches/PATCH-ID
```

检查当前状态词、任务依赖图和规则/AC/前置问题引用。输入字段与示例见下方 [Task Declaration Format](#task-declaration-format)。旧自由格式返回无法检查，不自动改写。退出码：0 当前声明检查通过、1 运行失败、2 参数错误、3 已知违规、4 必要来源或格式不足；结果不证明任务真实完成，也不检查状态历史或证据真实性。命令从明确项目范围读取文件，不联网、不执行正文命令，也不修改任务内容。

### Main Specification Size

按需展开阅读、单目标演进、保持主规格短而完整，操作见 [Small-Step Maintenance](skills/ming-spec/references/spec-home.md#small-step-maintenance)。检查指定模块主规格：

```sh
./scripts/mingspec spec-size --root /path/to/project --spec mingspec/specs/domain/module/spec.md
```

只读统计物理行数（包含空行、表格、代码与元数据），超过 300 行提醒评估是否按独立功能模块拆分；允许说明理由后保留内聚正文。提醒不使检查失败，不自动拆分，也不代表语义完整或业务验收通过。Agent 在原 Patch 留评估；吸收前统计拟写入的完整正文，写后复核实际行数。完整操作边界见 [Small-Step Maintenance](skills/ming-spec/references/spec-home.md#small-step-maintenance)。

命令不扫描其他模块、候选或历史；仅支持项目内 `mingspec/specs/<domain>/<module>/spec.md`，符号链接解析后仍须满足位置约束。退出码：0 完成统计（包括超限提醒）、1 项目根无效、2 参数错误、4 来源缺失/不可读/非普通文件/非 UTF-8/越界。完整产品移动后从实际安装位置调用，目标仍传明确项目根。


## Task Declaration Format

`--patch` 使用非空的项目相对目录，命令读取其中的 `spec.md`、`tasks.md` 以及显式引用的文件。引用路径相对承载文档解析，解析后必须在 `--root` 指定的项目内；必要文件缺失不能算检查通过。操作步骤见 [Run Task Checks](skills/ming-tickets/references/task-checks.md)。

每份 `tasks.md` 以如下声明开始；二级标题只用于任务，ID 必须以 ASCII 字母开头，后面可含字母、数字、下划线和连字符：

```markdown
---
format: mingspec-tasks-v1
---

# Tasks

## T1 Add Date Filtering

- state: pending
- blocked_by: []
- rules: ["spec.md#rule-date-filter"]
- acs: ["spec.md#AC-FILTER-01"]
- questions: []

交付：订单列表增加日期筛选。边界、验收与测试预期从同目录 spec.md 读取。
```

此示例的 `spec.md` 至少需要对应规则和验收表；请替换为你的实际需求：

```markdown
---
status: ready
---

# Date Filtering

<a id="rule-date-filter"></a>
## Date Filter

当用户选择起止日期时，订单列表应显示该日期范围内的订单。

### Acceptance

| ID | 条件 | 验收预期 |
| --- | --- | --- |
| AC-FILTER-01 | 选择起止日期 | 订单列表应只显示所选范围内的订单。 |
```

五个字段均必填且只出现一次；不要同时添加完成勾选或另一组状态/依赖字段。完整规格和任务模板见 [Choose a Template](#choose-a-template)。

| 字段 | 值与含义 |
| --- | --- |
| `state` | `pending`、`in_progress`、`completed`、`needs_recheck` 或 `retired` |
| `blocked_by` | 单行 JSON 数组；同文件任务 ID，或 `relative/tasks.md#Task-ID`；无依赖用 `[]` |
| `rules` | 单行 JSON 字符串数组，引用 `relative/spec.md#规则锚点` |
| `acs` | 单行 JSON 字符串数组，引用 `relative/spec.md#验收ID` |
| `questions` | 单行 JSON 数组，每项是 `["spec.md#问题锚点", "spec.md#判据锚点"]` |

`rules`、`acs`、`questions` 至少一项非空。任务 ID 在文件内唯一，依赖不能缺失、自引用、成环或指向已退役任务。声明 `completed` 时，所有阻塞任务也必须声明 `completed`。每份任务同目录的 `spec.md` 必须声明支持的 Patch 状态：`draft`、`ready`、`implemented`、`accepted`、`absorbed` 或 `retired`。检查器只核对声明，不验证真实完成或状态历史。

### Supported Parsing

规则和问题地址支持显式 HTML `<a id="...">` / `<a name="...">` 以及 ATX 标题。行内代码不定义 HTML 锚点。标题地址先转小写，删除 Unicode 字母、数字、下划线、连字符和普通空格以外的字符，再将每个普通空格换为连字符；同名标题依次加 `-1`、`-2`。显式与生成地址碰撞会被判为重复。

AC 从 `### Acceptance` 下带分隔行、首列为 ID 的简单单行表格读取；重复 ID 会产生歧义，不支持转义竖线或多行单元格。

frontmatter 只支持独占行 `---` 和单行 `key: value`。键以 ASCII 字母开头，可含字母、数字、下划线和连字符；值不得包含方括号、花括号、单/双引号、竖线或大于号。值去除首尾空白，内部冒号和 `#` 保留为普通字符，不解释 YAML 引号、转义或注释；format/status 必须完整匹配支持值。

检查器忽略代码围栏、缩进代码及 HTML 注释中的示例，只解析顶层任务字段。它递归读取 `blocked_by` 指向的任务文件及各任务显式引用的 SPEC，不扫描整个仓库。

### Diagnostics

未知格式、复杂 frontmatter、未闭合代码围栏/注释或必需来源不足返回 4。已声明格式中的缺字段、重复字段、类型/ID 错误、并列完成勾选以及缺失/歧义的目标 ID 返回 3。路径越出项目或引用无法解析返回 4；项目根无法解析返回 1。混合问题保留全部可判定诊断，退出优先级为 1、4、3、0；参数错误返回 2 且不开始检查。

旧自由格式只报告不支持，不自动转换。需要转换时，先确认授权并保留原文、任务 ID、依赖及历史结果。遇到非零退出码或工具无法运行时，报告缺口并暂停依赖的交接/吸收；不要通过降低状态或伪造引用消除错误。
