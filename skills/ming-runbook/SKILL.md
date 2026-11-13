---
name: ming-runbook
description: 对话出现初始化意图、可复用踩坑结论、已确认选型或约定时维护过程知识；编辑 AGENTS 时维护入口与行数。
---

# Ming Runbook

先执行[公共边界](../ming-spec/references/shared-boundaries.md)，再按真实意图选择操作。主动选择限于宿主已加载后的当前会话，不是后台监听、全局安装或跨宿主触发承诺。

## Detect the Work

- 真实初始化或接入意图：执行 [onboarding](../../onboarding.md)。
- 可复用踩坑结论或已确认过程决定：主任务验证明确后进入 Maintain Knowledge。
- AGENTS 实际编辑：编辑前后执行 Guard the Entry。

只出现关键词、引用他人案例、未决定讨论或无新知识的例行结果，不触发写入。只读和不保存要求优先，只报告结果及缺口，不运行会写文件的 init。

## Locate and Read

沿目标入口找到已有知识、正文及本次来源。旧规格布局接续[迁移步骤](../ming-spec/references/spec-home.md#migrate-an-existing-project)；仅补知识时只维护对应文件。业务归属和能力生命周期交 Ming Spec，验收后规格/地图收尾交 Ming Archive。已有准确入口原位维护，不运行通用 init 重建大小写索引或第二套规则。

## Maintain Knowledge

1. 在目标 `mingspec/runbook/` 按[知识分类](references/knowledge-types.md)选主要类型，优先更新同主题，按需创建大写 Markdown，不为八类建立八个空正文。
2. 写明适用范围、结论、原因/取舍、避免或复用方法、真实验证状态和来源。保留既有经验及条件，未确认猜测不升级为约定；相同结论不重复登记。
3. 业务规则/验收回 SPEC，单次日志留原任务。操作方法补明环境、权限、操作、成功/失败判据、恢复与数据影响；记录运维/发布知识不授权实际执行。
4. 首次维护确保 `mingspec/runbook/PITFALLS.md` 可达，在 AGENTS 保留“改代码前必读 PITFALLS”的链接。优先复用已有正文，无经验可仅含英文标题；知识索引只链接实际文件，不虚报知识齐备。

## Guard the Entry

AGENTS 编辑前后按物理行计数，用户更严格上限优先。达到 100 行时提醒接近 115 行并在授权内迁出详情；达到 115 行及以上先收敛再报告完成。只读时仅报告行数与需处理内容。

AGENTS 与 USAGE 的规则入口使用带适用动作的具体链接，完整约束、条件和例外留项目权威正文；本产品公开方法的正文在随包 Skill/references 中。逐项核对原约定的完整归属、触发链接和来源，保留 Repository Map、Quick Commands、Key Conventions、Current Status 四块及应用/命令/描述三列命令表、必要项目事实。既有准确结构按 onboarding 的原位维护例外处理。

新约定尚无正文时先在适当已有位置承接，再精简入口；不能为行数删条件、例外或隐藏规则。检查原文保全、本地链接、英文标题和实际行数，未收敛不宣称完成。

## Finish the Turn

核对来源、实际写入、未读与冲突、本地链接/锚点、语言和行数，按公共边界做适用验证与独立审查。结果留原任务，报告所学及未验证项，不用骨架存在代替分析或知识验收。
