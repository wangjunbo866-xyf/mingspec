---
name: ming-archive
description: 对指定 Patch 做部分吸收或完整规格收尾，核对验收与独立审查，将已交付规则写入主规格并同步来源、状态和导航。
---

# Ming Archive

版本：0.1.5。先执行[公共边界](../ming-spec/references/shared-boundaries.md)，再按下列步骤处理同一 Patch。

## Locate the Handoff

先核对[变更档位](../ming-spec/references/patch-workflow.md#choose-the-change-tier)。符合小修时直接接续 [Make a Small Fix](../ming-spec/SKILL.md#make-a-small-fix)并结束，不补造 Patch 或重启收尾审查；以下用于标准/完整档。

按[收尾交接](references/closure.md#evidence-and-scope)定位目标、候选版本、主规格、tasks、验收/审查依据及相关并行变化。位置和模块版本按 [Canonical Home](../ming-spec/references/spec-home.md#canonical-home)核对；候选修订、既有行为补档和迁移接续 [Ming Spec](../ming-spec/SKILL.md)对应分支。

## Choose the Scope

读取[规格收尾](references/closure.md#evidence-and-scope)，确定本次是部分吸收还是完整收尾。列出完整规则及其适用验收范围，关联仍留候选的内容；查询在证据核对后答复可吸收范围与缺口。

## Check the Evidence

1. 含 tasks.md 时先执行 [Run Task Checks](../ming-tickets/references/task-checks.md)；无任务时记录不适用。
2. 按[收尾交接](references/closure.md#evidence-and-scope)核对候选、范围、依赖与实际验收。已审结果按覆盖范围复用；尚未完成独立审查时准备完整拟吸收正文和最终差异，在下节合并审查通过前不宣称已吸收。
3. 将实现/验证缺口交执行者，业务决定交 Ming Spec，任务引用/依赖/结果问题交 [Ming Tickets](../ming-tickets/SKILL.md)。列明可独立吸收项及仍阻塞项。

## Consolidate and Reconcile

1. 读取[主规格阅读结构](../ming-spec/references/spec-home.md#independently-readable-main-specifications)，按[主规格模板](../ming-spec/assets/main-spec.md)维护本次正文。
2. 按 [Small-Step Maintenance](../ming-spec/references/spec-home.md#small-step-maintenance)统计拟写入完整正文，写后复核实际行数。
3. 执行 [Consolidate and Check](../ming-spec/references/spec-anchors.md#consolidate-and-check)逐规则写回；涉及删除或纯改名时执行[旧行为验证](../ming-spec/references/spec-anchors.md#verify-removed-or-renamed-behavior)。
4. 执行 [Close the Change](../ming-spec/references/business-map.md#close-the-change)同步受影响地图。
5. 有可复用知识或已确认过程决定时接续 [Ming Runbook](../ming-runbook/SKILL.md)。

## Review the Final Difference

1. 执行 [EARS Completion Check](../ming-spec/references/spec-anchors.md#ears-completion-check)与目标适用检查。
2. 依[合并独立检查](../ming-spec/references/spec-home.md#independent-reading-check)，由同一评审在一次审查中先记录场景判断，再核对来源与最终差异；已有覆盖充分的同候选结果直接复用。按 [Finish the Delivery](references/closure.md#finish-the-delivery)覆盖主规格、Patch、地图和知识，修复后补审受影响范围。
3. 将实际吸收地址/版本、检查与独立复核结果、未验证项留原 Patch 第五章或既有记录；按实际范围报告完成状态。
