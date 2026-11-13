# Closure Guide

收尾只维护规格、地图和必要知识；实现/验证缺口交执行者，规格决定交 Ming Spec，任务引用、依赖及状态问题交 Ming Tickets。

## Evidence and Scope

先按[分档](../../ming-spec/references/patch-workflow.md#choose-the-change-tier)处理；小修直接修正并留一行来源，不进入 Patch 收尾。标准/完整档从用户请求或已有完整交付授权定位同一 Patch、候选版本、主规格、tasks、验收/独立审查证据和并行变化。查询保持零写入，只报告可吸收项及缺口；仅改候选不自动收尾。首次补档、候选修订和旧布局迁移接续 Ming Spec 对应流程。

含 tasks.md 的 Patch 在准备吸收或查询时先按 [Run Task Checks](../../ming-tickets/references/task-checks.md)检查；无 tasks 记不适用，不补造任务。旧格式、失败或未运行按该指引处理，退出 0 仍不等于验收证据。

逐条核对本次候选、范围、依赖与实际验收、必要检查和已有审查的覆盖范围。缺少收尾审查时可准备完整拟吸收正文与地图等最终差异，交一次合并审查；通过前保持候选/待验状态，不把准备正文称为当前已交付规则。以完整已交付规则为吸收单位，保留全部条件、例外、边界和场景；单个场景通过不足以吸收整条规则。区分部分吸收和整个 Patch 收尾，列出可独立吸收项与仍留候选项。

依据缺失、过时、失败或并行重叠冲突时，报告受影响条款、证据及阻塞范围，按职责交回，独立且依据充分项可按授权继续。不能自动补实现、生成任务、放宽 AC 或覆盖并行决定；独立 Skill 入口不代替独立评审。

## Consolidate by Rule

1. 确认本次范围已获授权、验收及必要检查有依据。独立审查未完成时，以下步骤只准备完整拟吸收候选，保持待验，交合并审查后才确认吸收；已有审查满足本次覆盖时复用。首次交付可建立主规格，已有则增量更新；旧布局先迁移。正文按 [Main Specification](../../ming-spec/references/spec-home.md#independently-readable-main-specifications)，篇幅按 [Small-Step Maintenance](../../ming-spec/references/spec-home.md#small-step-maintenance)。
2. 写前重读最新主规格、目标清单和相关并行 Patch，对比实际基线，未解冲突只暂停相关写入，不按旧快照覆盖新决定。
3. 按锚点写回完整规则，保留稳定 ID、未变条件和来源；删除项留必要退役入口/替代关系，旧 ID 不悄然换义。删除或纯改名验收走 [Verify Removed or Renamed Behavior](../../ming-spec/references/spec-anchors.md#verify-removed-or-renamed-behavior)。
4. 逐目标核对正文、地址唯一与可达、基线变化、未变约束、实际吸收版本及来源；规则末尾或 Sources 可定位来源 Patch，Patch 反记实际地址/版本，地图对齐。锚点只提供定位，不提供自动语义合并。
5. 已一致允许零差异，不重写历史或累加重复来源。最终差异包含主规格、Patch、地图和必要知识，按[合并检查](../../ming-spec/references/spec-home.md#independent-reading-check)由同一独立评审先读当前正文、再核对来源与差异；相同候选已有充分结果直接复用。

## Content Disposition

在原 Patch 第五章或既有收尾记录交代每项有效条款与独立结论的去向，无需逐句登记背景：已吸收的实际地址/版本、仍在 Patch 的候选位置、历史依据，或不采纳的决定与理由。核对当前规格、候选和证据引用一致，全部拟交付项核对前不标整个 Patch absorbed。

主规格独立表达完整当前规则，不依赖历史补条件。其他有效内容须在既有位置可取回并保留引用，原始证据留原任务，不为收尾新建层级或阶段。保留未完成项、覆盖缺口和历史，去向记录不授权删除/移动 Patch。

## Finish the Delivery

有真实可复用经验或已确认过程决定时接续 Ming Runbook；无新结论不造记录。业务、知识、日志按职责分流；操作方法补明环境、权限、操作、成功/失败判据、恢复和数据影响。

对全部拟交付写入做适用检查，并把[独立阅读与最终差异检查](../../ming-spec/references/spec-home.md#independent-reading-check)合为一次、一份记录；可先审完整候选再按原文写回，最终核对无新差异。修复只补核受影响范围。原 Patch 记录实际吸收、内容去向、检查/复核、已执行/通过/失败/未运行/未知以及使用负担。不以一次调用证明长期收益或自动接续。文档收尾不等于归档目录、提交、合并、发布或部署。
