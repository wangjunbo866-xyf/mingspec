---
name: ming-spec
description: 按小修、标准或完整流程维护 SPEC、核对 Patch 一致性，分析影响和验收条件，管理需求归属、业务地图及规格迁移。
---

# Ming Spec

版本：0.1.6。先执行[公共边界](references/shared-boundaries.md)，再走当前操作。默认步骤直接执行；表内条件触发时，读取对应完整规则块及必要公共依赖。目标业务规则写前读全，方法参考按操作展开；依据见[按需阅读](references/spec-home.md#small-step-maintenance)。

## Identify the Request

1. 沿目标 AGENTS、README 和根→域→模块导航定位主责模块、主规格及当前 Patch，核对实际 HEAD、工作区与本次写入范围。
2. 只读查询在回答现状、来源与缺口后结束。写入前按 [Choose the Change Tier](references/patch-workflow.md#choose-the-change-tier)说明档位与依据；小修执行下节，小修完成后结束；标准/完整档起草候选或按表接续。

| 当前情况 | 读取与接续 |
| --- | --- |
| 目标/基线缺失、冲突或首次接入 | [目标定位](references/patch-workflow.md#confirm-the-target) |
| 布局、归属或跨模块边界待定 | [Canonical Home](references/spec-home.md#canonical-home)、[Business Map](references/business-map.md#assign-the-requirement) |
| 首次规格、补录既有行为 | [First Specification](references/business-map.md#first-specification) |
| 修订已有候选 | [Revise an Existing Patch](#revise-an-existing-patch) |
| 首建/修订主规格 | [主规格步骤](references/spec-home.md#independently-readable-main-specifications)及[主规格模板](assets/main-spec.md) |

## Make a Small Fix

1. 核对已有主规格与真实依据，读全受影响规则；若出现新增能力、承诺改变、跨模块或高风险，按分档升级后接续相应流程。
2. 在授权内直接修正主规格，保留稳定地址、条件和例外；规范条款按 [EARS Requirements](references/spec-anchors.md#ears-requirements)，不套候选模板。
3. 执行适用检查，按分档就近留一行来源；必要导航随实际变化同步。报告修改与检查后结束，默认不建 Patch、AC、tasks，不调用 Archive 或强制独立审查。

## Draft or Revise the Specification

1. 完整读取目标的相关业务规则、条件、例外及公共依赖，按 [Draft Content](references/patch-workflow.md#draft-content)核对正文职责、行为粒度与必要决定。使用[五章候选模板](assets/spec.md)，在主责模块的 `patches/<patch-id>/spec.md` 写本次变更；将范围、现状依据、行为/AC、设计与测试决定、未决项填入对应章节。
2. 对每个目标记录规格版本及实际工作区依据、旧/新行为与保持项，复用已有规则 ID，新增目标注明计划地址。新增规则 ID、补锚点、改名或定位有疑问时读取 [Locate the Rule](references/spec-anchors.md#locate-the-rule)。
3. 按可独立验证的行为写完整规则及稳定 AC，规范条款与预期执行 [EARS Requirements](references/spec-anchors.md#ears-requirements)。正常、异常、边界和兼容结果按实际适用性填写，未知列为具体问题。
4. 涉及旧行为修改、拆分、合并或退役时，读取[场景对账](references/spec-anchors.md#describe-the-change)，逐项记录旧场景去向及 AC。纯定位/修链接沿原任务记录；具体命名分支见下文。
5. 统计相关主规格当前行数；超 300 行、尚无主规格或需要拆分时，读取 [Small-Step Maintenance](references/spec-home.md#small-step-maintenance)处理。本次规格的必要决定、影响及测试边界明确后，进入完成检查；未解部分报告具体依赖。

## Revise an Existing Patch

1. 读取同一 Patch 的实际 SPEC、相关规则、tasks 和证据，按[修订范围](references/patch-workflow.md#revision-scope)确定写入对象。
2. 按[双向对账](references/patch-workflow.md#reconcile-a-revision)检查规则/AC、设计、任务依赖及证据适用性；旧场景按 [Describe the Change](references/spec-anchors.md#describe-the-change)逐项处理。
3. 将确认的决定写回 SPEC；任务处置按同一修订范围交 [Ming Tickets](../ming-tickets/SKILL.md#hand-off-and-reconcile-results)。
4. 写后重读受影响内容，按[修订结果](references/patch-workflow.md#reconcile-a-revision)报告变更、保持项、未同步项及缺口。

## Name the Patch Specification

普通新候选沿起草步骤给出的路径。文件身份待定、纯记录或改名时，按[正文命名](references/patch-workflow.md#name-the-candidate)选择文件名。新候选使用主责模块的 `patches/<patch-id>/spec.md`；纯记录、历史与获准改名分别执行该规则的对应场景。改名时接续[迁移核对](references/spec-home.md#migrate-an-existing-project)。

## Hand Off to Project Workflows

只有当前请求明确任务编排，或交付授权内按分档确需任务时，才按[任务调用](../ming-tickets/references/task-workflow.md#task-scope)接续 [Ming Tickets](../ming-tickets/SKILL.md)。出现准备依赖或未知技术假设时，读取[前置验证](../ming-tickets/references/task-workflow.md#prerequisite-verification)，将问题、判据和任务影响写入本次允许的产物。

## Consolidate Delivered Behavior

标准/完整档的规格吸收交 [Ming Archive](../ming-archive/SKILL.md)，携带同一 Patch、候选版本、目标及已有验收/审查依据；尚未审查时把拟吸收正文与最终差异一并交一次合并审查。小修在 Make a Small Fix 完成，不再走此分支。

## Complete the Specification Work

1. 按 [EARS Completion Check](references/spec-anchors.md#ears-completion-check)核对条款与验收预期。
2. 涉及删除或纯改名验收时执行[旧行为验证](references/spec-anchors.md#verify-removed-or-renamed-behavior)；涉及主规格首建/修订时执行[独立阅读检查](references/spec-home.md#independent-reading-check)。
3. 按公共边界完成适用检查，报告产物、结果、未验证范围与来源。仅起草/修订候选时完成作者核对即可，默认将标准/完整档的一次独立审查安排在拟交付正文与最终差异齐备时；用户明确要求现在审查 SPEC 时记录其实际范围，不把它当未来实现的验收。任务编排和吸收分别接续对应操作，不因阶段切换重复审查。
