---
name: ming-tickets
description: 在明确任务编排请求或完整交付授权下，将规格和前置验证问题拆为 Patch 任务，维护引用、依赖、执行衔接及结果。
---

# Ming Tickets

版本：0.1.6。先执行[公共边界](../ming-spec/references/shared-boundaries.md)，再按下列步骤处理任务。完整相关规则按步骤展开。

## Identify the Work

1. 按[任务调用](references/task-workflow.md#task-scope)确定本次操作，说明目标 tasks.md 和预期产物。
2. 沿目标导航读取同一主责 Patch 的 SPEC、已有 tasks、证据及实际工作区基线；位置按 [Canonical Home](../ming-spec/references/spec-home.md#canonical-home)核对。
3. 从规格修订接续时，先按[修订范围](../ming-spec/references/patch-workflow.md#revision-scope)确定任务写入范围。

## Bind the Specification

1. 读取 SPEC 的完整相关规则、场景、AC、范围和设计决定。
2. 按[任务引用](references/task-workflow.md#bind-references)关联来源、版本、规则/AC、任务 ID、边界及验证方式。
3. 新任务使用[任务模板](assets/tasks.md)；格式、旧文件兼容及调用方式读取 [Run Task Checks](references/task-checks.md)。
4. 核对每项来源的唯一性和含义；将无法绑定的具体问题交回 [Ming Spec](../ming-spec/SKILL.md)。

完成时，每项任务可找到规格依据，未就绪项有明确原因。

## Decompose and Check Dependencies

1. 按[任务拆分](references/task-workflow.md#decompose-and-verify-locally)与[局部验证](references/task-workflow.md#decompose-and-verify-locally)组织可独立验收的纵向交付，关联自身测试、文档及证据位置。
2. 有准备依赖或未知技术假设时，读取[前置验证](references/task-workflow.md#prerequisite-verification)，先明确问题、环境、判据及执行边界；按规则将观察、结论、未决项回写 SPEC 第二、四、五章。
3. 大范围机械修改时，读取 [Wide Refactoring](references/wide-refactoring.md)选择原子修改或分批迁移。
4. 核对真实阻塞关系及规则/AC 覆盖，列出当前可开始任务、复用/延期项和具体缺口。
5. 生成或更新后执行 [Run Task Checks](references/task-checks.md)，读取结果再交接。

## Hand Off and Reconcile Results

1. 按[任务衔接](references/task-workflow.md#hand-off-and-record)提供 tasks、SPEC/基线、项目入口、证据和实际执行方法；提供已解析的检查命令与结果位置。
2. 按[完成记录](references/task-workflow.md#hand-off-and-record)回写候选、实际结果与未决项；每次任务状态更新后运行 [Run Task Checks](references/task-checks.md)。
3. 规格、输入或实现基线变化时，读取[任务重核](references/task-workflow.md#reconcile-results)，核对相关任务和下游的证据适用性。业务/设计新决定交回同一 SPEC。
4. 按本次允许的输出报告修改、未同步项、证据和阻塞；验收后的规格吸收接续 [Ming Archive](../ming-archive/SKILL.md)。

完成时，接手者能定位规则、范围和当前可做事项；实际交付状态由原任务的验证与审查依据支持。
