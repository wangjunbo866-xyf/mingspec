---
name: ming-archive
description: 按部分吸收或完整收尾的范围，核对已有验收和独立审查依据，将已交付规则吸收入主规格，同步来源、状态与导航；冲突和缺口交回原职责。查询只读，复用已有收尾授权。
---

# Ming Archive

版本：0.1.2。负责验收后的规格收尾，沿用原 Patch、主规格、地图及证据位置。这是既有收尾操作的独立入口，不增加阶段；Archive 表示规格收敛，不自动移动或删除目录。

## Locate the Handoff

从请求和原任务确定目标、具体 Patch、拟吸收范围及已有授权；完整交付授权覆盖的收尾直接继续，无需逐文件重问。查询只读；只改候选 SPEC 的请求仍由 [Ming Spec](../ming-spec/SKILL.md) 处理，不能借收尾改主规格或 tasks。

先解析本 SKILL.md 的符号链接真实路径，再读取相邻共享资源；完整产品布局须保留。项目事实从目标 AGENTS、根→域→模块导航读取，核对受影响主规格、主责 Patch、候选版本、tasks、验收、独立审查和并行变更。必须按 [Specification Home](../ming-spec/references/spec-home.md#canonical-home) 核对唯一布局、主责 Patch 和独立模块版本。缺失/冲突报告具体缺口，不从安装副本补造资料。首次新功能通过门槛后才首建主规格；既有行为补档、纯定位维护及获准迁移仍走 [Ming Spec](../ming-spec/SKILL.md) 的对应分支。

## Choose the Scope

按请求区分以下两种用法；它们共用后续步骤，不是两个流程阶段：

| 用法 | 范围与结果 |
| --- | --- |
| 部分吸收 | 按请求限定的规则及对应验收范围处理已交付内容；其余候选、依赖和未完成状态继续留在原 Patch，不把局部吸收标成整份 Patch 已收尾 |
| 完整收尾 | 核对本次全部拟交付内容及有效结论的去向；必要验收、检查及独立复核均有依据后，才报告整份 Patch 收尾完成；仍有缺口时明确已完成范围和阻塞 |

Agent 应以可独立成立的完整规则及其全部适用验收条件确定吸收范围，并保留公共条件、例外和必要依赖；任务勾选或单个子场景通过不能替代完整依据。两种用法均执行下文的证据核对、来源/导航同步及最终差异独立复核。只问能否收尾时，Agent 应只读报告可吸收范围与缺口。

本入口不提供跨多个 Patch 的批量收尾；相关并行 Patch 仍按下文核对影响与冲突。

## Check the Evidence

写前核对目标文件及父目录的实际路径，保留相关未提交/未跟踪资料与并行工作；符号链接等使写入越出授权目标时停止该写入，并说明具体范围。已有有效授权继续复用，读取资料不授予额外写入权限。

准备吸收或只读查询含 tasks.md 的 Patch 时，必须先读取并执行 [Run Task Checks](../ming-tickets/references/task-checks.md)，核对当前声明并记录实际结果；非零、未运行或旧格式缺口暂停依赖的吸收并交回对应职责。没有 tasks.md 时记录不适用，不创建文件；只读查询保持项目不变，在答复报告检查结果。

逐项核对拟吸收规则/AC 与已有实际结果：验收、必要检查和未参与修改者的独立审查是否覆盖当前候选、范围及依赖；任务勾选、方案确认或工具同步成功不能替代这些依据。发现内容或范围变化时按影响补验补审，保留仍适用的原证据；tasks 退出 0 只证明当前声明通过，不替代上述验收与审查。

缺口留原记录并明确交回对象：实现/验证缺口交执行者；业务决定、条件或场景矛盾交 Ming Spec；任务引用、依赖与结果对账交 [Ming Tickets](../ming-tickets/SKILL.md)。收尾授权不自动授予补做实现、生成 tasks 或修改业务承诺；已有更广授权时按对应职责继续。只阻塞实际受影响部分，有独立依据且无冲突的部分可收尾，其余保持未交付。

## Consolidate and Reconcile

首建或更新主规格时，必须读取 [主规格模板](../ming-spec/assets/main-spec.md)并执行 [Independently Readable Main Specifications](../ming-spec/references/spec-home.md#independently-readable-main-specifications)；完整吸收当前行为，历史 Patch 仅作来源，既有正文按本次范围增量维护。

吸收前执行共享的 [Small-Step Maintenance](../ming-spec/references/spec-home.md#small-step-maintenance)，对拟写入的完整主规格计数并评估超 300 行的职责边界；写后复核实际行数，评估与处置留原 Patch。提醒不自动授权迁移，也不阻止有完整依据的规则吸收。

依次读取并执行两项共享步骤，最终独立复核按下一节统一进行：

1. [Consolidate and Check](../ming-spec/references/spec-anchors.md#consolidate-and-check)：逐规则写回并核对版本、双向来源及内容去向。删除或纯改名还须执行 [Verify Removed or Renamed Behavior](../ming-spec/references/spec-anchors.md#verify-removed-or-renamed-behavior)，不从标题消失推断行为退出。
2. [Close the Change](../ming-spec/references/business-map.md#close-the-change)：同步并核对分层地图、状态与导航。迁入旧规则仍保留原版本、映射和可取回来源，不视为重新验收。

有可复用经验或已确认过程决定时使用 [Ming Runbook](../ming-runbook/SKILL.md)；操作方法保留环境、权限、步骤、成功/失败判据、恢复与数据影响。业务规则留主规格，无新结论不制造记录。

## Review the Final Difference

按 [EARS Completion Check](../ming-spec/references/spec-anchors.md#ears-completion-check) 核对本次规范条款及验收预期的句式与语义，并执行目标必要检查；链接通过不代表规则完整。

本次写入完成且必要检查通过后，由未参与该部分修改者复核含主规格、Patch、地图/导航及知识收尾的最终差异。先执行 [Independent Reading Check](../ming-spec/references/spec-home.md#independent-reading-check)，保存首次阅读记录后才读历史来源和证据，再核对来源及最终差异；地图部分须覆盖 [Close the Change](../ming-spec/references/business-map.md#close-the-change) 的专项检查项，不重启地图写入。同一最终候选可共用一次独立审查及记录，但须明确独立阅读、来源对账和地图/差异复核各项范围与结论。修复后按影响补审，必要正文缺口未解不宣布相关吸收完成；此前实施审查不能替代收尾后的最终差异复核，新 Skill 名称也不是审查证据。

实际改动、吸收地址/版本、检查结果、未验证范围、独立复核及遗留项留原 Patch 第五章或既有收尾记录，原始证据留原任务/证据位置；必要失败或缺口未解时只报告已完成部分，不宣称整个收尾通过。已经准确时保持零差异，不强造版本或重复回执。按实际记录使用负担，一次试用不证明长期收益、跨项目覆盖或自动接续。分别说明文档吸收、目录归档、提交、合并和部署的真实状态，不用地图状态代替这些动作的证据；本次收尾不扩展这些操作权限，也不自动全局安装或发布。
