# Run Task Checks

## When to Run

- Ming Tickets：生成或更新 tasks.md 后运行，再交接任务。
- 执行者：回写任务状态后运行，实际结果留原任务/证据；Ming Tickets 交接时提供本步骤和实际命令。
- Ming Archive：准备吸收或只读查询含 tasks.md 的 Patch 时，先运行检查；没有任务文件时记录不适用，继续原有验收与独立审查核对，不创建任务。只读查询保持项目不变，结果只在答复报告。

## Resolve and Execute

1. 解析正在使用的 SKILL.md 的符号链接真实路径，从 skills/<skill>/ 上溯到完整产品根；读取明确目标的项目根和 Patch 位置。产品根和目标项目是两个不同职责，不能以当前目录或 PATH 中另一个版本代替产品来源。
2. 以目标项目根为工作目录，填入实际绝对产品/项目路径和非空项目相对 Patch 目录，再执行：

```sh
python3 "<product>/scripts/mingspec" tasks --root "<project>" --patch "mingspec/specs/<domain>/<module>/patches/<patch-id>"
```

3. 读取退出码与完整诊断。将实际命令、cwd、退出码、结果/未检查部分记录在原任务或已有 evidence；只读时仅在答复报告。交接命令使用本次已解析路径，并提示接手者在另一台机器重新解析产品路径。

| 结果 | 处置 |
| --- | --- |
| 0 | 当前声明检查通过；继续核对业务验收、任务完成证据、结果适用性与独立审查 |
| 3 | 已知违规；按诊断定位任务/引用，在已有授权内修正后重跑，不能降低状态或伪造引用绕过 |
| 4 | 来源缺失、越界或格式不支持；保留旧任务，报告未检查部分；已知违规也须保留 |
| 1 / 2 | 运行失败 / 参数错误；保留真实错误，修正环境或调用参数后重跑 |
| 未运行 | Python 3.9+ 或该产品 CLI 不可用、执行受限；明确原因，不自动安装 |

非零或未运行时暂停依赖该检查的交接/吸收，报告受影响任务及缺口；独立且依据充分的工作可继续。已有语义核对结果保留，但不得将手工核对、文件存在或计划调用称为命令通过。命令不核验状态历史、真实完成或证据真实性；退出 0 也不自动允许吸收。

## Write Compatible Tasks

新建任务用[任务模板](../assets/tasks.md)：文件开头声明 `format: mingspec-tasks-v1`，每项用 `## <Task-ID> <Title>`；二级标题只用于任务。五字段各一次：state 为 pending/in_progress/completed/needs_recheck/retired；其他四项为单行 JSON 数组，无项用 `[]`。rules、acs、questions 至少一项非空。交付、边界、验证和实际结果继续放正文；状态/依赖/引用只维护这一组字段，不另加完成勾选或旧字段。

任务 ID 支持 ASCII 字母开头的字母/数字/下划线/连字符，以及原有纯数字、点分数字（如 `1`、`1.1`）。blocked_by 只声明整项任务完成依赖；仅等待某项部分成果的条件留在正文，保持原并行边界，不升级为整项阻塞。

blocked_by 用同文件 ID 或 `relative/tasks.md#ID`；rules/acs 用 `relative/spec.md#ID`；questions 每项为 `["问题位置#锚点", "判据位置#锚点"]`，同段可指同一锚点。路径从承载文档定位，解析后须在目标项目根内。规则/问题锚点支持显式 HTML id/name 与 ATX 标题。AC ID 来自 `### Acceptance` 或旧五章 `## 3. Behavior and Acceptance` 内的简单单行 ID 表格；首列可有一个空的 HTML 锚点再接 ID，其他章节的表格不作为 AC 定义。采用者应从实际 SPEC 填入定位，删除模板占位符；缺失或不支持的定义交回 Ming Spec，不能仅为检查通过改业务条件。

旧自由版式、复杂表格或不兼容 Patch 状态可能返回 4 或 3，按实际诊断处理。查询不改写；只有授权覆盖当前文件的格式转换时才转换，并先保全可取回原件、任务 ID、依赖及历史结果。不得批量转换其他 Patch；已有 completed 也不能为消除错误降成 pending。没有转换授权时报告这一具体缺口，保留原任务。

### Historical Specification Sources

旧 Patch 沿用 proposal/design 且同目录没有 spec.md 时，在 tasks frontmatter 显式填写 `legacy_spec: proposal.md`（或实际历史 Markdown 相对路径）。检查器只读该真实来源和任务引用，不猜文件、不生成 spec.md；现存 spec.md 与该声明冲突时返回 3。

历史来源未声明 status 时，输出 NOTE 明示“历史来源未声明 Patch 状态”，检查任务状态、依赖与引用。退出 0 也不代表历史 Patch 状态已确认；已声明的非法/重复 status 仍失败。来源缺失、空白、不可读或越界返回 4；非 Markdown、绝对地址、任务自身或其别名作为来源返回 3。默认仍检查同目录 spec.md，旧文件仅在明确转换授权下使用此分支。
