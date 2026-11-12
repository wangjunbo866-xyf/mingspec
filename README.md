# mingspec

**0.2.0-beta.1 · 预发布版**。适合试用和反馈，版本、验证结果及已知限制见 [Release Notes](RELEASE_NOTES.md)。

mingspec 帮助你和 AI 编程助手把需求说清楚、拆成可执行的任务，并在功能完成后更新功能说明。讨论中确认的决定和解决问题的经验，也会保存在项目里，方便下次继续工作。

它提供四个 Skill，也就是供 AI 编程助手使用的工作指引。安装到支持这些指引的助手后，你可以直接用对话提出要求。需求、任务和经验都以文件保存在你的项目中，可以阅读和修改。

## Why mingspec

与 AI 一起开发时，一次对话通常不够完成整个功能。换了对话或接手的人，容易忘记需求为什么这样定、还有哪些任务没做，以及功能说明是否仍然准确。

mingspec 帮助你把这些内容留下来：开始前写清需求和完成条件，实施时让任务对应需求，完成后更新功能说明。每次围绕一个能检查结果的小目标推进，只展开相关内容，让说明保持简短，同时保留必要条件和例外。

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

先将发布包完整解压到一个固定目录，保留隐藏的 `.agents/` 和全部随附资源，不能只复制四份 Skill 说明。使用 mingspec 需要能读取本地项目文件并加载 Skill 的 AI 编程助手；配套命令工具需要 Python 3.9 或以上版本。

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

## Quick Start

安装并确认助手能看到四个 Skill 后，在你的项目里开始对话。首次接入可以先说：“用 Ming Runbook 查看这个项目，说明已有资料和建议整理的内容，先不要修改文件。”需要实际整理时，再明确允许修改的范围；已有授权不必重复确认。

下面以“给订单列表增加日期筛选”为例。没有订单功能的项目，可以换成你自己的一个小需求。需求说明记录这次打算做什么；功能说明记录已经完成并经过检查的行为，保存在项目的 `mingspec/specs/` 中。

1. 写清需求：

   > 用 Ming Spec 帮我写清楚订单日期筛选的需求，包括正常使用、没有结果和输入错误时的行为。暂时不要写代码。

   助手会结合现有项目整理需求说明，并列出尚未确定的问题。你可以检查日期范围、默认值和完成条件是否符合预期。

2. 安排任务：

   > 需求已经确认。用 Ming Tickets 整理实现任务，注明先后顺序和每项怎样检查，暂时不要开始实施。

   你会得到与需求对应的任务清单。这里完成的是工作安排，代码还没有因此实现。

3. 实现并检查：

   把需求说明和任务清单交给你选定的执行者，明确允许实施的范围。执行者完成代码和测试，并安排独立检查，留下实际结果。验收时再对照前面确认的完成条件，判断功能是否达到要求。mingspec 不绑定执行工具；测试失败或证据不足时，相关工作仍不能算完成。

4. 更新功能说明：

   > 这项功能的验收和独立检查已经完成，结果记录在这里。用 Ming Archive 核对记录，把已完成的行为更新到功能说明中，保留尚未完成的内容。

   把“这里”替换为实际结果记录的位置。助手会核对本次功能的验收和检查依据，满足条件后才更新；缺少依据时会指出缺口。更新说明不会自动提交代码、发布或部署。

工作中解决了可复用的问题，还可以说：“用 Ming Runbook 记录这次问题的原因、解决方法和验证结果，方便下次查阅。”一次普通讨论不会自动成为项目约定。

<a id="runtime-and-platforms"></a>
<a id="verified-scope"></a>
## Current Limits

- 工作由编程助手在对话中执行，依赖助手实际加载并遵循 Skill；没有后台监听或跨会话自动运行。
- 需求和任务文档帮助组织工作，不能代替代码实现、测试、验收和独立检查。配套工具只补空框架、检查任务声明或提醒说明过长，不判断功能是否正确。
- 修改文件和执行操作以你的授权范围为准。只读请求保持只读；安装、迁移或整理资料不会自动获得提交、发布或部署权限。
- 本包的检查范围和实际结果见 [Release Notes](RELEASE_NOTES.md)。本地文件测试与受控 Skill 试用不等于你的项目已经通过验收，也不证明宿主会自动选择 Skill。
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
[本地检查](#local-checks)：运行随包提供的测试和文档检查。

<a id="design-history"></a>
[方法与模板](USAGE.md#choose-a-template)：按操作选择包内的指引和模板。


## Package Contents

发布包包含 `scripts/`、`skills/`、`templates/`、`tests/`、插件清单及公开说明。`scripts/mingspec` 是 CLI 入口。

`templates/mingspec/` 是创建空框架的模板；使用工具后，你的项目中会产生自己的 `mingspec/` 资料目录。发布包本身不附带维护者的内部规格、讨论记录或 Git 历史。使用产品无需这些内部资料。

## Local Checks

在解压后的产品根目录执行：

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_documents.py .
python3 -B scripts/mingspec --help
```

测试使用临时项目。文档检查只验证本地链接、锚点和英文标题，不能代替内容审查、宿主发现或业务验收。若 ZIP 解压工具未保留可执行权限，可以用 `python3 -B scripts/mingspec` 替代 `./scripts/mingspec`。

## License

本发布包采用 [Apache License 2.0](LICENSE)。
