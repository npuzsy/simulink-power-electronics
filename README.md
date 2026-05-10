# Simulink Power Electronics Skill / Simulink 电力电子 Skill

English | [中文](#中文)

## English

`simulink-power-electronics` is a Codex skill for analyzing, debugging, and verifying Simulink and Simscape Electrical power-electronics models. It is especially useful for three-phase inverters, grid-connected converters, SPWM/SVPWM modulation, T-type or NPC three-level bridges, gate-signal routing, simulation diagnostics, and waveform validation.

This skill builds on the official MathWorks Simulink Agentic Toolkit and the official Simulink skills repository. The official tools provide the Simulink/MATLAB connection and general model workflows; this repository adds a small set of power-electronics notes, scripts, and checklists that grew out of real three-level inverter debugging work.

### Relationship To Official Simulink Skills

Use this skill together with the official Simulink skills:

- Official skills repository: https://github.com/simulink/skills
- Simulink Agentic Toolkit: https://github.com/matlab/simulink-agentic-toolkit
- MATLAB MCP Core Server: https://github.com/matlab/matlab-mcp-core-server

Recommended pattern:

- Use the official Simulink skills for general model construction, simulation, model testing, requirements, and model-based design workflows.
- Use `simulink-power-electronics` when the work is specifically about power converters, modulation, gate routing, switching legality, waveform balance, or SVPWM table validation.

### Current Scope

The current version focuses on three-level inverter work, especially T-type or NPC three-level SVPWM. The included reference table, diagnostic script, and validation checklist were written and tested around that use case.

Other converter types are not fully covered yet, including two-level inverters, rectifiers, DC-DC converters, MMCs, flying-capacitor converters, motor-drive control loops, and grid-control outer loops. Contributions are welcome: new references, scripts, model checks, test patterns, and field notes are all useful.

### Prerequisites

To use the full skill, install and configure:

- MATLAB R2023a or later.
- Simulink.
- Simscape Electrical when the model uses electrical power-stage components.
- Simulink Test when using persistent model tests through `model_test`.
- MathWorks Simulink Agentic Toolkit.
- MATLAB MCP Core Server.
- An MCP-capable coding agent such as Codex, Claude Code, GitHub Copilot, Amp, or Gemini CLI.
- The official Simulink skills from https://github.com/simulink/skills, or the skills installed by `setupAgenticToolkit("install")`.

Minimum capability levels:

- For reading references and generating plans: no MATLAB session is required.
- For running `scripts/print_table7_state_vectors.py`: Python 3 is enough.
- For `scripts/svpwm_diagnostics.m`: MATLAB with Simulink is required.
- For direct model inspection and edits from an agent: MATLAB MCP and Simulink Agentic Toolkit must be configured and initialized.

### Installation

Copy this folder into a skill search path used by your agent. For Codex:

```bash
mkdir -p ~/.codex/skills
cp -R simulink-power-electronics ~/.codex/skills/
```

Then restart the agent session so the skill index is refreshed.

Install and initialize the MathWorks toolchain separately:

```matlab
setupAgenticToolkit("install")
addpath("~/.matlab/agentic-toolkits/simulink")
satk_initialize
```

After `satk_initialize`, restart the coding agent session or reload the host IDE so the MCP server attaches to the shared MATLAB session.

### What It Provides

- A model-grounded workflow for power-electronics debugging.
- Standards for inspecting converter topology, active control paths, From/Goto routing, solver settings, and generated artifacts.
- A three-level SVPWM reference, including the 36 small-sector state-vector sequences used by this implementation.
- A MATLAB diagnostic script for logging three-level SVPWM state vectors, gate outputs, root plant gates, and output voltage balance.
- Troubleshooting notes for common MATLAB MCP and Simulink Agentic Toolkit setup failures.
- Templates for project README files and diagnostic reports.

### Directory Layout

```text
simulink-power-electronics/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── diagnostic-report-template.md
│   └── project-readme-template.md
├── references/
│   ├── mcp-simulink-troubleshooting.md
│   ├── model-standards.md
│   ├── output-standards.md
│   ├── svpwm-three-level.md
│   ├── table7-state-vectors.md
│   └── workflow.md
└── scripts/
    ├── print_table7_state_vectors.py
    └── svpwm_diagnostics.m
```

### Typical Use

Ask the agent:

```text
Use $simulink-power-electronics to inspect this Simulink inverter model, identify why the SVPWM waveform is unbalanced, fix the smallest responsible subsystem, and verify with logged gate and voltage data.
```

For a conventional three-level SVPWM model, add the scripts folder to the MATLAB path and run:

```matlab
addpath("simulink-power-electronics/scripts")

cfg = struct();
cfg.model = "YourModel";
cfg.stateBlock = "YourModel/SVPWM/Subsystem1";
cfg.gateBlock = "YourModel/SVPWM/Subsystem3";
cfg.voltageBlocks = ["YourModel/Va", "YourModel/Vb", "YourModel/Vc"];
cfg.stopTime = "0.10";

report = svpwm_diagnostics(cfg);
```

To print the built-in three-level SVPWM table:

```bash
python3 scripts/print_table7_state_vectors.py --format markdown
python3 scripts/print_table7_state_vectors.py --format json
```

### Troubleshooting

Read `references/mcp-simulink-troubleshooting.md` first when:

- `setupAgenticToolkit` is not recognized.
- `satk_initialize` reports `shareMATLABSession` warnings.
- The agent cannot see `model_overview`, `model_read`, `model_edit`, or other Simulink MCP tools.
- The MCP server connects to the wrong MATLAB instance.
- Codex or another agent times out during long simulations.
- Windows, Claude Desktop, VS Code, or sandboxed agent hosts behave differently from the MATLAB command window.

### Validation

The skill folder should pass the Codex skill validator:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/simulink-power-electronics
```

The Python table script has no third-party dependencies. The MATLAB diagnostic script is intended to run inside MATLAB with Simulink available.

### Contributing

This is an early, focused skill. Issues and pull requests are welcome, especially for:

- additional power-electronics topologies
- SPWM/SVPWM/DPWM variants
- model-test examples
- Simscape Electrical plant checks
- grid-connection validation
- clearer MCP setup notes across operating systems and agent hosts

### License

Choose a license before publishing this repository. If this skill is shared with the community, include a top-level `LICENSE` file in the repository that contains this skill.

## 中文

`simulink-power-electronics` 是一个面向 Codex 的 Skill，用于分析、调试和验证 Simulink 与 Simscape Electrical 电力电子模型。它特别适合三相逆变器、并网变换器、SPWM/SVPWM 调制、T 型或 NPC 三电平桥、门极信号路由、仿真诊断和波形验证。

这个 Skill 基于 MathWorks 官方 Simulink Agentic Toolkit 和官方 Simulink skills 使用。官方工具负责 MATLAB/Simulink 连接和通用建模流程；这里沉淀的是我们在三电平逆变器调试中反复用到的电力电子笔记、脚本和检查清单。

### 与官方 Simulink Skills 的关系

建议把这个 Skill 和官方 Simulink skills 一起使用：

- 官方 skills 仓库：https://github.com/simulink/skills
- Simulink Agentic Toolkit：https://github.com/matlab/simulink-agentic-toolkit
- MATLAB MCP Core Server：https://github.com/matlab/matlab-mcp-core-server

推荐使用方式：

- 通用的模型搭建、仿真、模型测试、需求和 Model-Based Design 流程，优先使用官方 Simulink skills。
- 当任务涉及电力电子拓扑、调制算法、门极路由、开关合法性、波形平衡或 SVPWM 表格校验时，使用 `simulink-power-electronics`。

### 当前支持范围

当前版本主要支持三电平逆变器，尤其是 T 型或 NPC 三电平 SVPWM。仓库里的状态矢量表、诊断脚本和验证清单，都是围绕这个场景整理和测试的。

其他电力电子场景还需要后续补充，例如两电平逆变器、整流器、DC-DC 变换器、MMC、飞跨电容拓扑、电机控制闭环、并网外环控制等。欢迎大家一起共创：补充参考资料、诊断脚本、模型检查项、测试样例和实际项目经验都很有价值。

### 使用条件

完整使用本 Skill 前，建议安装和配置：

- MATLAB R2023a 或更新版本。
- Simulink。
- 如果模型包含电力级器件，需要 Simscape Electrical。
- 如果要使用 `model_test` 做持久化模型测试，需要 Simulink Test。
- MathWorks Simulink Agentic Toolkit。
- MATLAB MCP Core Server。
- 支持 MCP 的编码 agent，例如 Codex、Claude Code、GitHub Copilot、Amp 或 Gemini CLI。
- 官方 Simulink skills，来源可以是 https://github.com/simulink/skills，也可以是 `setupAgenticToolkit("install")` 安装后的 skills。

不同能力层级的最低要求：

- 只阅读参考资料、制定方案：不需要 MATLAB 会话。
- 运行 `scripts/print_table7_state_vectors.py`：只需要 Python 3。
- 运行 `scripts/svpwm_diagnostics.m`：需要 MATLAB 和 Simulink。
- 让 agent 直接检查和修改 Simulink 模型：需要 MATLAB MCP 与 Simulink Agentic Toolkit 已完成配置并初始化。

### 安装

把这个文件夹复制到 agent 的 skill 搜索路径。以 Codex 为例：

```bash
mkdir -p ~/.codex/skills
cp -R simulink-power-electronics ~/.codex/skills/
```

然后重启 agent 会话，让 skill 索引刷新。

另外需要单独安装和初始化 MathWorks 工具链：

```matlab
setupAgenticToolkit("install")
addpath("~/.matlab/agentic-toolkits/simulink")
satk_initialize
```

执行 `satk_initialize` 后，重启 coding agent 会话，或重新加载宿主 IDE，使 MCP server 能连接到当前共享的 MATLAB 会话。

### 提供的能力

- 面向电力电子调试的模型证据驱动工作流。
- 检查变换器拓扑、有效控制路径、From/Goto 路由、求解器设置和生成文件的标准。
- 三电平 SVPWM 参考，包括当前实现使用的 36 个小扇区状态矢量序列。
- MATLAB 诊断脚本，用于记录三电平 SVPWM 状态矢量、门极输出、根部 plant gate 和输出电压平衡性。
- MATLAB MCP 与 Simulink Agentic Toolkit 常见安装/连接问题排障笔记。
- 项目 README 和诊断报告模板。

### 目录结构

```text
simulink-power-electronics/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── diagnostic-report-template.md
│   └── project-readme-template.md
├── references/
│   ├── mcp-simulink-troubleshooting.md
│   ├── model-standards.md
│   ├── output-standards.md
│   ├── svpwm-three-level.md
│   ├── table7-state-vectors.md
│   └── workflow.md
└── scripts/
    ├── print_table7_state_vectors.py
    └── svpwm_diagnostics.m
```

### 典型用法

可以这样要求 agent：

```text
Use $simulink-power-electronics to inspect this Simulink inverter model, identify why the SVPWM waveform is unbalanced, fix the smallest responsible subsystem, and verify with logged gate and voltage data.
```

对于常规三电平 SVPWM 模型，可以把 scripts 目录加入 MATLAB path 后运行：

```matlab
addpath("simulink-power-electronics/scripts")

cfg = struct();
cfg.model = "YourModel";
cfg.stateBlock = "YourModel/SVPWM/Subsystem1";
cfg.gateBlock = "YourModel/SVPWM/Subsystem3";
cfg.voltageBlocks = ["YourModel/Va", "YourModel/Vb", "YourModel/Vc"];
cfg.stopTime = "0.10";

report = svpwm_diagnostics(cfg);
```

打印内置三电平 SVPWM 表格：

```bash
python3 scripts/print_table7_state_vectors.py --format markdown
python3 scripts/print_table7_state_vectors.py --format json
```

### 排障

遇到下列问题时，优先阅读 `references/mcp-simulink-troubleshooting.md`：

- `setupAgenticToolkit` 无法识别。
- `satk_initialize` 报告 `shareMATLABSession` 相关警告。
- agent 看不到 `model_overview`、`model_read`、`model_edit` 或其他 Simulink MCP 工具。
- MCP server 连接到了错误的 MATLAB 实例。
- Codex 或其他 agent 在长仿真中超时。
- Windows、Claude Desktop、VS Code 或受沙箱限制的 agent host 与 MATLAB 命令窗口行为不一致。

### 验证

Skill 文件夹应通过 Codex skill validator：

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/simulink-power-electronics
```

Python 表格脚本不依赖第三方库。MATLAB 诊断脚本需要在安装了 Simulink 的 MATLAB 中运行。

### 欢迎共创

这是一个早期且聚焦的 Skill。欢迎通过 issue 或 pull request 补充：

- 更多电力电子拓扑
- SPWM/SVPWM/DPWM 变体
- 模型测试示例
- Simscape Electrical 电力级检查
- 并网验证方法
- 不同操作系统和 agent host 下更清晰的 MCP 配置经验

### 许可证

正式开源前，请为仓库选择许可证。如果这个 Skill 要分享给社区，建议在包含本 Skill 的仓库顶层加入 `LICENSE` 文件。
