# mingspec

mingspec 为持续演进的项目组织需求与上下文，让人和 AI **沿业务地图找到相关规则，围绕小目标修改，并把验收后的结果沉淀回当前规格**。

它把项目入口、业务地图、需求规格、任务和经验连成一套可阅读、可追溯的文件体系。换一个人、一个 Agent 或一次对话，都能从项目入口继续查阅已有约定、正在进行的变更和完成依据。

## Why mingspec

项目越大、参与者越多，越容易遇到这些问题：相关需求散在不同文档里，同一条规则出现多个版本，一次修改越写越大，功能做完后说明却停在旧状态。mingspec 用六个相互配合的约定组织这些工作。

### 1. Find Context Through Layered Indexes

**从项目入口逐层缩小范围，让人和 AI 找到同一份上下文。** `AGENTS.md` 保留项目摘要与导航，`mingspec/` 的知识入口连接规格和经验，规格区再通过根、业务域、模块各层的 README 指向具体规则和变更。

每层索引只说明本层的职责和下一步去哪里。处理订单查询时，先定位订单域和查询模块，再完整读取受影响规则及必要依赖；接手者有路径可循，Agent 也有明确的阅读范围。已有项目沿用确定的 README/readme 文件名，不建立两套索引。

下面是一个使用方项目的示例；业务目录由项目实际职责决定，按需建立：

```text
AGENTS.md                         # 项目摘要、约定与导航
mingspec/
├── readme.md                     # 规格与过程知识入口
├── specs/
│   ├── readme.md                 # 业务域索引
│   └── orders/
│       ├── README.md             # 订单域：模块职责与入口
│       ├── order-query/
│       │   ├── README.md         # 查询模块：当前规格与变更
│       │   ├── spec.md           # 已交付且有验收依据的规则
│       │   └── patches/
│       │       └── add-date-filter/
│       │           ├── spec.md   # 本次变更、影响与验收条件
│       │           └── tasks.md  # 获准拆分后生成的任务
│       └── order-export/         # 导出模块，维护自己的规格与变更
└── runbook/                      # 已确认的决定与可复用经验
```

布局与阅读规则见 [Specification Home](skills/ming-spec/references/spec-home.md#canonical-home)。

### 2. Organize Collaboration Around Business Modules

**按业务职责组织文件，让分工有明确边界。** 业务地图说明有哪些域、每个模块负责什么、需求归哪里以及当前规格在哪。例如，一位开发者维护订单查询，另一位开发者或 Agent 维护订单导出，各自的规格与变更就近保存。

一条规则只有一个权威归属。跨模块变更确定一个主责模块，用引用关联其他受影响模块，显式记录共享规则和真实依赖。这样既便于分类查找，也给并行协作提供可核对的分工依据；共享接口和重叠修改仍需协调。具体方法见 [Business Map](skills/ming-spec/references/business-map.md)。

### 3. Keep Changes Traceable as Requirements Evolve

**让“当前是什么”和“这次要改什么”各有归属，变更前后能够对账。** 模块主规格记录已交付且有验收依据的规则；一次具体变更保存在同模块的 Patch 中，写清读取基线、影响、目标和验收条件。任务引用这些规则与条件，执行结果留在原任务。

标准和完整变更修订时，核对旧场景、新规则、存在的任务与证据，保留稳定标识、条件和例外。验收及一次合并独立审查通过后，将完整交付的规则吸收进主规格，并保留来源；未完成部分继续留在 Patch。接手者可以追到“为什么改、改了哪里、凭什么算完成”，减少需求在对话和文档之间悄悄漂移的机会。

修订与收尾分别见 [Revise a Patch](skills/ming-spec/SKILL.md#revise-an-existing-patch) 和 [Ming Archive](skills/ming-archive/SKILL.md)。

### 4. Keep Each Step Small Enough to Review

**每次围绕一个可独立验收的目标推进，让人能读完、审清楚。** 查询、改写和审阅按需展开相关规则与依赖；能分别交付验收的目标，可以拆成具有明确依赖的小变更。

主规格超过 **300 行**时，评估是否包含可以独立描述的模块职责，并提出拆分建议或说明保留理由。300 行是评估提醒，不是硬性上限，也不会自动拆文件；缩短正文时必须保留完整条件、例外和场景。小步演进控制单次审阅范围，篇幅评估帮助维护长期可读性。详见 [Small-Step Maintenance](skills/ming-spec/references/spec-home.md#small-step-maintenance)。

### 5. Make Requirements Observable with EARS

**把模糊愿望写成有条件、有响应、可核对结果的需求。** mingspec 使用 EARS（Easy Approach to Requirements Syntax）句式组织要求，例如“当〈事件〉时，〈系统〉应〈可观察响应〉”，并为验收条件保留稳定编号。

以订单日期筛选为例，“支持日期筛选，异常时友好提示”还不足以让开发者和评审者形成一致判断。进一步明确规则后，可以写成：

| 验收条件 | 需求示例 |
| --- | --- |
| AC-01：正常范围 | 当用户提交起止日期且开始日期不晚于结束日期时，订单列表应只显示创建日期位于该范围内的订单，包含起止两日。 |
| AC-02：输入错误 | 如果开始日期晚于结束日期，那么订单列表应阻止本次查询，并提示“开始日期不能晚于结束日期”。 |
| AC-03：无匹配结果 | 当用户提交起止日期、开始日期不晚于结束日期且查询无匹配订单时，订单列表应显示空结果，并保留用户已选择的起止日期。 |

这些是写法示例，日期口径等业务条件仍需项目确认。句式帮助暴露缺失条件，验收编号让任务、测试和审查能引用同一预期；实际测试与独立审查负责判断实现是否满足要求。完整写法见 [EARS Requirements](skills/ming-spec/references/spec-anchors.md#ears-requirements)。

本仓旧主规格仍有 `MUST/WHEN/THEN` 写法，采用“新增即用 EARS，改到哪条就转换哪条”的渐进策略。转换覆盖受影响规则的规范正文、场景与验收预期，保留原有语义和稳定编号；其他旧规则与历史记录保持原貌。仅修链接、错字或导航时沿用原表达。具体边界见 [Legacy Rule Migration](skills/ming-spec/references/spec-anchors.md#legacy-rule-migration)。

### 6. Carry Project Knowledge into the Next Change

**让已确认的经验可以复用，让团队延续自己的执行方式。** Runbook 保存决策的背景与取舍、容易重复遇到的问题，以及有验证依据的操作方法。换人、换 Agent 或开始下一次变更时，可以从项目入口找到这些资料，减少重复调查和遗漏约定。

业务规则归规格，可复用经验归 Runbook，单次执行证据留原任务。团队可以继续使用已有的编码、测试和评审方式，由四个 Skill 协助组织上下文、需求、任务与收尾。知识需要按实际结果维护，文件存在并不代表 Agent 已读取或正确执行。详见 [Knowledge Types](skills/ming-runbook/references/knowledge-types.md)。

## When to Choose mingspec

如果项目需要长期演进，参与者经常跨模块协作或交接，而你最关心的是上下文定位、规则归属、变更追溯和人类审阅负担，mingspec 值得试用。它将这些要求连在同一套工作方法中：**沿索引找上下文，按业务归属组织规则，以小步变更推进，用明确条件验收，再更新当前规格与可复用经验。**

可以从团队的实际困难判断是否适合：

- 新人或新 Agent 接手时，需要反复解释背景：用分层索引提供阅读路径，并完整展开相关规则与依赖。
- 多人并行修改时，需求散落、归属不清：用业务地图确定模块职责和规则的权威位置，并记录跨模块影响。
- 多轮需求调整后，难以判断当前行为和完成依据：分别维护当前规格、候选变更与验收证据，修订及收尾时逐项对账。
- 规格越来越长，人类难以审清：按可独立验收的目标小步演进，并评估主规格的职责与篇幅。

这些收益依赖团队维护索引、核对变化和完成审查。若团队暂时不愿持续维护规格与项目知识，仅安装 Skill 或生成目录不会带来上述结果。

### How the Approaches Differ

mingspec 的差异化价值在于默认采用的实践组合与组织重点。规格演进、团队协作、验收条件和工具可定制性并非 mingspec 独有。以下按各项目公开说明概括选择依据，不作功能穷举或优劣排名。

| 工具 | 可以优先考虑的需要 | 公开方法与能力 |
| --- | --- | --- |
| mingspec | 长期维护按业务模块组织的需求与上下文，重视多人、多 Agent 接手以及人类审阅 | 分层索引、业务地图、模块内 Patch、小步演进、EARS 与验收引用、Runbook 经验维护，通过四个 Skill 配合使用。 |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 围绕具体变更开展提案、设计、实施与归档，并使用其工具集成和共享规格能力 | 以 specs 与 changes 组织规格和变更，归档时更新规格；支持迭代工作方式，提供跨仓共享规格的 Stores（beta）。 |
| [Spec Kit](https://github.com/github/spec-kit) | 从规格推进到计划、任务、实施与结果核对，或定制团队开发流程 | 提供结构化流程与可复用模板，通过扩展、预设和工作流等机制定制过程；也提供既有规格演进的指引。 |

竞品说明依据上述官方仓库于 2026-11-12 的公开内容，后续能力可能变化。选择 mingspec 的理由，是你认同并需要这套业务组织与上下文维护方式；其他工具也可以通过配置和团队约定实现部分相近实践。

mingspec 当前仍是 beta。实际适用性需要在项目中验证，运行平台与宿主加载的已知边界见 [Current Limits](#current-limits)。规格和知识保存在项目文件中，可阅读、修改和纳入版本管理；实施与测试可以继续使用团队已有方式。

<a id="use-the-skills"></a>
## Four Skills

| 名称 | 什么时候用 | 得到什么 |
| --- | --- | --- |
| Ming Spec | 开始做功能或修改需求时 | 需求说明：做什么、哪些情况需要考虑、怎样判断完成 |
| Ming Tickets | 需求明确，需要安排工作时 | 任务清单：每项做什么、先后顺序、怎样检查结果 |
| Ming Archive | 功能经过验收和独立检查后 | 更新后的功能说明，清楚区分已完成和仍待完成的内容 |
| Ming Runbook | 接入已有项目，或形成可复用经验时 | 整理后的项目入口、确认的决定，以及下次能用上的经验 |

按当前需要选择即可，不必每次调用全部四个。只想讨论或写需求时，可以明确说“先不实施”；整理任务也不会自动启动代码修改。编写代码和测试由你选定的执行者完成；独立检查交给未参与这部分工作的评审者，可以是另一位开发者或另一个 AI，检查是否符合需求和项目约定。

<a id="project-installation"></a>
## Installation

先将公开产品仓库完整下载或克隆到本地，保留公开包内的目录和文件，不能只复制四份 Skill 说明。自行从开发源码准备安装包时，按 [Installation Details](USAGE.md#installation-details) 保留公开资源并排除内部资料。使用 mingspec 需要能读取本地项目文件并加载 Skill 的 AI 编程助手；配套命令工具需要 Python 3.9 或以上版本。

以下是 WSL/Linux 下的项目安装方式。先在所用助手的 Skill 设置或说明中确认它支持从项目 `.agents/skills/` 目录加载指引；无法确认时先不要执行命令，不同助手的安装入口可能不同。把 `/path/to/mingspec` 换成下载后的产品目录，把 `/path/to/your-project` 换成你要开发的项目目录。先检查是否已有同名文件或链接；来源不明时保留现场，不覆盖或删除。

```sh
mkdir -p "/path/to/your-project/.agents/skills"
ln -s "/path/to/mingspec/skills/ming-spec" "/path/to/your-project/.agents/skills/ming-spec"
ln -s "/path/to/mingspec/skills/ming-tickets" "/path/to/your-project/.agents/skills/ming-tickets"
ln -s "/path/to/mingspec/skills/ming-archive" "/path/to/your-project/.agents/skills/ming-archive"
ln -s "/path/to/mingspec/skills/ming-runbook" "/path/to/your-project/.agents/skills/ming-runbook"
```

用编程助手打开目标项目，查看可用 Skill 中是否出现上面的四个名称。没有出现时，先检查路径和助手的加载方式，再重新打开会话；安装命令成功不等于助手已经加载。可以先说：“列出你能使用的 mingspec Skill，先不要修改文件。”

<a id="plugin-installation"></a>
如果助手支持本项目的插件格式，也可以通过插件方式加载同一套四个 Skill；同一项目选择一种方式，避免重复。插件安装、升级和卸载尚未完成实际验证，详细设置见 [插件与安装排查](USAGE.md#installation-details)。

## Choose the Workflow

按实际影响选择流程，不按改动行数判断：

| 档位 | 适用范围 | 做法 |
| --- | --- | --- |
| 小修 | 单模块、低风险且不改变已有承诺的修正 | 直接改主规格，做适用检查，留一行来源 |
| 标准变更 | 单模块新增或调整行为，没有高风险 | Patch、验收条件（AC）、适用验证、一次独立审查；任务按需 |
| 完整流程 | 跨业务模块或高风险 | 完整影响分析、任务依赖、验证和规格收尾 |

小修默认不建 Patch 或任务，也不要求独立审查。标准与完整档的收尾检查默认合为一次：同一评审先读当前规则，再核对来源和最终差异，留一份记录。实际影响扩大时升级流程；具体边界见[流程选择](USAGE.md#choose-the-workflow)。

## Quick Start

安装并确认助手能看到四个 Skill 后，在你的项目里开始对话。首次接入可以先说：“用 Ming Runbook 查看这个项目，说明已有资料和建议整理的内容，先不要修改文件。”需要实际整理时，再明确允许修改的范围；已有授权不必重复确认。

下面以“给订单列表增加日期筛选”为例。没有订单功能的项目，可以换成你自己的一个小需求。需求说明记录这次打算做什么；功能说明记录已经完成并经过检查的行为，保存在项目的 `mingspec/specs/` 中。

1. 写清需求：

   > 用 Ming Spec 帮我写清楚订单日期筛选的需求，包括正常使用、没有结果和输入错误时的行为。暂时不要写代码。

   助手会结合现有项目整理需求说明，并列出尚未确定的问题。你可以检查日期范围、默认值和完成条件是否符合预期。

2. 按需安排任务：

   > 需求已经确认。用 Ming Tickets 整理实现任务，注明先后顺序和每项怎样检查，暂时不要开始实施。

   有协作或依赖需要时，会得到与需求对应的任务清单；标准变更也可以直接依据 Patch 和 AC 实施。这里的任务安排不会自动启动代码修改。

3. 实现并检查：

   把需求说明和任务清单交给你选定的执行者，明确允许实施的范围。执行者完成代码和测试，留下实际结果；独立审查可与下一步的规格收尾合并安排。验收时再对照前面确认的完成条件，判断功能是否达到要求。mingspec 不绑定执行工具；测试失败或证据不足时，相关工作仍不能算完成。

4. 更新功能说明：

   > 这项功能的验收结果记录在这里。用 Ming Archive 准备更新后的功能说明，安排一次合并独立审查，通过后完成收尾，保留尚未完成的内容。

   把“这里”替换为实际结果记录的位置。助手会核对本次功能的验收依据，把当前规则阅读与最终差异核对合为一次独立审查；已有同候选审查结果可复用，满足条件后才完成更新；缺少依据时会指出缺口。更新说明不会自动提交代码、发布或部署。

工作中解决了可复用的问题，还可以说：“用 Ming Runbook 记录这次问题的原因、解决方法和验证结果，方便下次查阅。”一次普通讨论不会自动成为项目约定。

<a id="runtime-and-platforms"></a>
<a id="verified-scope"></a>
## Current Limits

- 工作由编程助手在对话中执行，依赖助手实际加载并遵循 Skill；没有后台监听或跨会话自动运行。
- 需求和任务文档帮助组织工作，不能代替代码实现、测试、验收和独立检查。配套工具只补空框架、检查任务声明或提醒说明过长，不判断功能是否正确。
- 修改文件和执行操作以你的授权范围为准。只读请求保持只读；安装、迁移或整理资料不会自动获得提交、发布或部署权限。
- 历史项目试用、本项目当前使用的检查、模拟项目测试分别记录结果，只证明各自记录中的版本和范围；历史成功不表示现在已经重跑，也不证明你的项目已通过验证。
- `tasks` 检查面向声明 `mingspec-tasks-v1` 的任务，支持保留数字 ID 和显式历史规格来源。本仓旧任务已迁入当前格式；其他项目的自由格式仍须按[转换边界](skills/ming-tickets/references/task-checks.md#write-compatible-tasks)处理。历史来源未声明 Patch 状态时会明确提示，检查通过不补造该状态或重验历史结果。
- 当前运行与回归环境为 WSL/Linux。Windows 原生、macOS、最低 Python 3.9、独立可执行打包/安装，以及桌面插件安装、升级和卸载尚未验证；其他编程助手的兼容性和自动选择效果也需分别验证。

## Further Reading

<a id="specification-home"></a>
<a id="project-context"></a>
<a id="business-map"></a>
<a id="learn-and-maintain"></a>
[详细用法](USAGE.md)：更多请求示例、项目文件位置和经验记录。

<a id="initialize-a-project"></a>
<a id="check-task-declarations"></a>
<a id="check-main-specification-size"></a>
[可选命令](USAGE.md#optional-commands)：手动创建空框架、检查任务声明和统计说明篇幅。普通对话使用无需先执行初始化命令。

<a id="develop-mingspec"></a>
<a id="verify"></a>
<a id="design-history"></a>
[完整包与维护边界](USAGE.md#installation-details)：公开方法随 Skill 和 references 分发。根目录 `mingspec/` 的内部规格与开发过程不随包发布，使用产品无需读取这些资料；初始化模板 `templates/mingspec/` 保留。
