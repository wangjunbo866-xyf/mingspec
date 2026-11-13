<a id="mingspec-usage"></a>
# Using mingspec

mingspec 提供四个 Skill 和可选 Python CLI。产品方法在公开 Skill 及其 references 中完整提供；使用方的业务规格从自己的项目导航读取。

## Choose a Skill

| 当前需要 | 操作入口 |
| --- | --- |
| 起草或修订需求、业务地图 | [Ming Spec](skills/ming-spec/SKILL.md) |
| 明确授权拆任务、核对依赖或交接 | [Ming Tickets](skills/ming-tickets/SKILL.md) |
| 根据已有验收与审查做部分或完整收尾 | [Ming Archive](skills/ming-archive/SKILL.md) |
| 初始化、维护经验与 AGENTS | [Ming Runbook](skills/ming-runbook/SKILL.md) |

公共边界与术语见[共享指引](skills/ming-spec/references/shared-boundaries.md)。仅改 SPEC 不写任务，规则见[修订范围](skills/ming-spec/references/patch-workflow.md#revision-scope)。实施与测试沿目标项目已有流程，不绑定执行工具。

## Choose the Workflow

| 档位 | 何时使用 | 留下什么 |
| --- | --- | --- |
| 小修 | 单模块、低风险、可直接验证，不引入新能力或改变已有承诺 | 直接修正已有主规格，做适用检查，留一行来源；默认无 Patch、AC、任务或独立审查 |
| 标准变更 | 单模块新增或调整行为，无高风险 | Patch、AC、验证结果与一次独立审查；任务按需，五章可简写 |
| 完整流程 | 跨业务模块或高风险 | 完整影响与场景对账、任务依赖、适用验证、审查及规格/地图收尾 |

判断依据、升级条件和一行来源示例见 [Choose the Change Tier](skills/ming-spec/references/patch-workflow.md#choose-the-change-tier)。所有档位保留授权、资料保护和实际验证；小修完成后直接结束，未完成行为不能写成已交付。收尾独立阅读与最终差异审查默认由同一评审合为一次、一份记录，标准和完整档均适用。

## Choose a Template

| 材料 | 模板 | 使用说明 |
| --- | --- | --- |
| Patch 候选 | [Candidate](skills/ming-spec/assets/spec.md) | 新功能先写候选，五章表达一次目标 |
| 模块主规格 | [Main Specification](skills/ming-spec/assets/main-spec.md) | 已验收规则或有据既有行为补档，不能预建待实施承诺 |
| 已获准任务 | [Tasks](skills/ming-tickets/assets/tasks.md) | 填实际规则、AC、依赖并执行声明检查 |

首次分流见 [First Specification](skills/ming-spec/references/business-map.md#first-specification)，名称与旧文件处理见 [Name the Candidate](skills/ming-spec/references/patch-workflow.md#name-the-candidate)。

<a id="use-ming-archive"></a>
## Close a Change

小修直接修正并留一行来源，不必调用 Archive。标准/完整档向 Ming Archive 提供同一 Patch、候选版本和已有验收/审查依据；尚未审查时准备完整拟吸收正文与最终差异，安排一次合并独立审查，已有同候选结果按覆盖范围复用。完整规则才可吸收，部分完成仍保留未交付候选，重复已一致可零差异。说明见 [Closure Guide](skills/ming-archive/references/closure.md)。

<a id="maintain-short-specifications"></a>
## Keep Specifications Readable

沿业务地图定位相关规则，修改前读全受影响条件和依赖。主规格超 300 行评估边界，不自动拆分；说明见 [Small-Step Maintenance](skills/ming-spec/references/spec-home.md#small-step-maintenance)。

<a id="check-task-declarations"></a>
## Check Tasks

Ming Tickets 生成/更新任务、执行者回写状态、Ming Archive 查询/吸收含 tasks 的 Patch 时，按 [Run Task Checks](skills/ming-tickets/references/task-checks.md)执行。无 tasks 不补造，声明通过不等于实际完成。

<a id="installation-and-initialization"></a>
## Join an Existing Project

从 [README](README.md#project-installation)安装并确认宿主加载，再用 [onboarding](onboarding.md)调查和整理。已有规格沿[迁移步骤](skills/ming-spec/references/spec-home.md#migrate-an-existing-project)，材料退出按[清理条件](skills/ming-spec/references/spec-home.md#retire-migration-artifacts)。只读调查不先运行 init。

<a id="project-files-and-knowledge"></a>
## Find the Documents

目标业务主规格在 `mingspec/specs/<domain>/<module>/spec.md`，候选在同模块 `patches/<patch-id>/spec.md`，知识在 `mingspec/runbook/`。这与产品自身未公开的内部目录是不同位置。地图职责见 [Business Map](skills/ming-spec/references/business-map.md)，术语见 [Terms](skills/ming-spec/references/shared-boundaries.md#terms)。

## Installation Details

完整产品包含 `skills/`（含 references、assets、agents）、`templates/`、`scripts/`、README、USAGE、onboarding 及插件清单。保持目录关系，只将四个 Skill 子目录分别接入目标宿主的发现目录；不能只复制四份 SKILL.md。方法资源按符号链接解析后的真实产品位置读取，目标业务资料从目标项目入口读取。缺包内资源时报告缺口，不借其他安装或项目正文兜底。

安装或迁移前检查同名文件、旧根链接与未知冲突，只移除已确认且获准处理的旧链接，保留项目资料及其他安装。授权内同步四入口与相关导航，验证互链、资源和宿主实际发现；文件存在不等于自动选择通过。

支持本项目插件格式的宿主可读取 [plugin.json](plugin.json)，本地目录项见 [marketplace](.agents/plugins/marketplace.json)。插件与直接 Skills 使用同一套方法，选择一种避免重复。宿主格式兼容与真实安装、升级、卸载需分别验证；边界见 [Current Limits](README.md#current-limits)。安装不授予全局配置、业务实施、提交或发布权限，不自动启动服务或安装依赖。

根 `mingspec/` 保存本产品内部开发资料，不是公开安装依赖；`templates/mingspec/` 是生成使用方空框架的必需资源，须随包保留。维护者修改方法时同步公开指引及对应内部验收，在无内部目录、无旧 Git 历史的搬迁副本运行文档与回归检查，按分档对账条件和场景，需要独立审查时并入同一次；不把内部 Patch 或原始思考过程打入公开包。

## Optional Commands

需要 Python 3.9+ 标准库，CLI 不启动服务。以下 `<product>` 为真实产品目录，`<project>` 为明确目标；在路径含空格时保留引号。运行 `python3 "<product>/scripts/mingspec" --help` 查看接口。运行与平台范围见 [README](README.md#runtime-and-platforms)。

<a id="initialize-a-project"></a>
### Initialization Command

```sh
python3 "<product>/scripts/mingspec" init "<project>"
```

省略目标使用当前目录；仅补缺失 AGENTS.md 及目标 mingspec 下 readme.md、specs/readme.md、runbook/readme.md、vendor/readme.md 和必要父目录。模板为空结构，不含具体事实；不扫描源码、不解析/追加已有文件、不迁移或做行数判断。重复运行保持已有文件字节（含非 UTF-8、未闭合 Markdown、旧标记和硬链接关联文件）。成功或帮助退出 0，帮助不写。

写前读取全部模板并检查目标、祖先及预定目录/文件。符号链接或类型冲突退出 2 且不写；系统读写失败退出 1，可能残留，核对现场修复后重跑，不承诺事务、并发协调或回滚。退役 --review、--apply、--expected-review 参数退出 2 且不写。

<a id="task-check-command"></a>
### Task Declarations

```sh
python3 "<product>/scripts/mingspec" tasks --root "<project>" --patch "mingspec/specs/<domain>/<module>/patches/<patch-id>"
```

只读检查当前任务字段、引用及依赖声明，不核验历史状态、真实完成或证据真实性。格式、执行 cwd 与结果分支见 [Run Task Checks](skills/ming-tickets/references/task-checks.md)。0 为声明通过，3 为已知违规，4 为未检查/格式不支持，1/2 为运行/参数错误；非零或未运行保留真实诊断，阻塞依赖交接/吸收。

迁移旧任务时保留原 ID、依赖条件与历史结果；数字 ID、旧 AC 表和 proposal/design 来源按[历史格式指引](skills/ming-tickets/references/task-checks.md#historical-specification-sources)处理。历史来源没有 Patch 状态时，NOTE 会说明该范围，任务检查通过不推定 absorbed 或 accepted。

### Main Specification Size

```sh
python3 "<product>/scripts/mingspec" spec-size --root "<project>" --spec "mingspec/specs/<domain>/<module>/spec.md"
```

只读统计指定主规格实际物理行数，不读取其他模块、Patch 或历史，也不判语义、验收或自动拆分。超 300 行提醒评估，统计成功仍退出 0。拟合并正文须另外完整计数，口径见 [Small-Step Maintenance](skills/ming-spec/references/spec-home.md#small-step-maintenance)。

输入必须恰为上述五段相对路径，用 `/` 分隔，各段非空、非 `.`/`..`、不含反斜杠，不先归一化后接受。非规范参数退出 2，项目根无效退出 1；文件缺失/非普通/不可读/非 UTF-8、实际路径越界、解析层级错误或符号链接失败（含循环）退出 4 并说明未检查。项目根可解析真实路径；输入及实际目标都须是项目内规范模块主规格。允许指向另一规范模块主规格的符号链接，报告输入相对路径、统计真实目标，不额外读取其他模块。
