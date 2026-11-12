---
status: current
version: current-v1
---

# {{Module Title in English}}

<!-- 使用说明：本模板仅用于有依据的当前规则。首次新增或既有行为补档须先按 First Specification 分流；新功能仍先写 Patch，满足既有验收与独立审查门槛后才建立主规格。current-v1 仅为新模块首版默认值，修订接续实际版本，保留稳定 ID、旧锚点和未变条件，不用模板重置正文或状态。 -->

<!-- 首建或修订前必须执行 [Main Specification Contract](../references/spec-home.md#independently-readable-main-specifications)，完成前执行 [Independent Reading Check](../references/spec-home.md#independent-reading-check)；首次分流见 [First Specification](../references/business-map.md#first-specification)。首建可按实际需要简写或合并章节；既有规格沿用已采用结构，未授权章节调整时不得因模板删章或重排。 -->

<!-- 生成时将填写提示换为项目实际内容，删除教学说明和占位符；教学链接从真实模板位置读取，需留在产物中的来源或交接指引按目标位置改为可读取的实际地址，不照抄模板相对链接或个人临时路径。标题英文、正文中文，代码、命令、路径和标识符保留原样。 -->

## Scope

说明本模块解决的问题、适用对象/版本、当前覆盖能力、明确不覆盖项与已知规格缺口。未交付目标通过模块入口指向候选，不写成当前承诺。

## Terms and Model

定义理解规则所必需的术语、对象、状态及关系；已有公共定义通过下节具体引用。简单模块可在规则首次使用时定义，不为凑结构造模型。

## Dependencies and Shared Rules

列出理解当前行为必需的公共规则/定义的真实文件与锚点，说明约束本模块哪个行为、适用条件及作用；无依赖时写明。读取必要依赖后仍无法判定的冲突、循环或缺失定义应保留为具体缺口，不能把历史来源列成公共规则来补齐正文。

## Behavior

<a id="rule-example"></a>
### {{Rule Title in English}}

用目标稳定 ID 替换示例 ID；保留已有规则及场景 ID。必须按 [EARS Requirements](../references/spec-anchors.md#ears-requirements) 写完整行为：主体、前提或触发、必要输入、可观察结果；许可、禁止、条件与例外强度保持。

#### Scenarios

按本条实际适用性写正常、异常、边界和兼容场景，包含必要的错误/状态变化、重复操作及旧调用方/格式/数据约束。每项给出可确定的条件与结果；不机械补四类空场景，不适用说明依据，未知保留缺口。适用的公共条件在此明确引用并说明作用。

来源：填写该规则实际吸收的 Patch/确认基线及版本，或指向下文能定位该规则来源的条目；来源仅用于追溯，当前有效条件已包含在正文与明确公共引用中。

## Interfaces and Compatibility

按实际契约说明输入输出、格式/单位、默认值、错误、状态及版本兼容承诺。没有独立接口时将约束并入对应行为并在此引用；章节合并仅按上述首建或获准调整边界处理，不凭模板推导未经确认的兼容保证。

## Sources

按规则对应实际来源、吸收版本与必要决定依据；已在规则末尾完整列出的来源可在此简记归属，首建或获准调整结构时才按实际需要省略本节。原始验收证据留原任务；正文与明确公共引用应足以判断当前行为，无需拼接历史来源。
