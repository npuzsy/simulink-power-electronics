# Simulink Power Electronics Skill / Simulink 电力电子 Skill

English | [中文](#中文)

## English

`simulink-power-electronics` is a Codex skill for Simulink and Simscape Electrical power-electronics work. Its main job is to route a task to the right power-electronics domain, then keep analysis and edits grounded in model evidence.

The repository is organized as a root router plus domain subskills. The root skill contains shared workflow rules; `subskills/` contains domain-specific knowledge. Today, only the three-phase grid inverter subskill is active. The other subskills are intentional stubs that define scope and evidence to collect, not completed methodologies.

### Design Rules

- Keep `SKILL.md` concise. It routes work and points to references; it should not become a long project prompt.
- Read `references/domain-map.md` before loading domain-specific material.
- If a subskill is marked `stub`, use it only for scope recognition and evidence selection.
- Do not copy three-phase inverter assumptions into motor drives, DC-DC converters, BMS, HVDC/FACTS, or other domains.
- Promote one stub at a time, only after adding references, a realistic workflow, and repeatable validation checks or scripts.

### External Toolchain

Use this skill together with the MathWorks Simulink agent workflow:

- Official Simulink skills: https://github.com/simulink/skills
- Simulink Agentic Toolkit: https://github.com/matlab/simulink-agentic-toolkit
- MATLAB MCP Core Server: https://github.com/matlab/matlab-mcp-core-server
- Simscape Electrical documentation and examples for electrical power-stage behavior
- Motor Control Blockset documentation and examples for motor-drive workflows

Recommended split:

- Official Simulink skills: general model construction, simulation, testing, requirements, and model-based design operations.
- This repository: power-electronics domain routing, topology/control inspection, gate and waveform diagnostics, validation evidence, and reusable domain notes.

### Subskill Status

| Subskill | Status | Scope |
| --- | --- | --- |
| `subskills/three-phase-grid-inverter` | active | Three-phase grid-connected inverters, SPWM/SVPWM, T-type or NPC three-level bridges, gate routing, waveform balance |
| `subskills/motor-drives` | stub | PMSM, BLDC, induction motor drives, FOC, DTC, torque/speed/current loops |
| `subskills/dc-dc-converters` | stub | Buck, boost, buck-boost, flyback, resonant, bidirectional DC-DC converters |
| `subskills/rectifiers-active-front-ends` | stub | Rectifiers, PWM active front ends, PFC, DC-link regulation |
| `subskills/renewable-grid-systems` | stub | PV, wind, storage-coupled inverters, microgrids, PLL, grid-code validation |
| `subskills/batteries-bms` | stub | Battery packs, chargers, balancing, SOC/SOH-linked power-electronics behavior |
| `subskills/hvdc-facts` | stub | HVDC, STATCOM, SVC, UPFC, transmission-level controls |
| `subskills/multilevel-mmc` | stub | MMC, cascaded H-bridge, flying capacitor, capacitor balancing |
| `subskills/wireless-power-resonant` | stub | Resonant converters and inductive wireless power transfer |

### Active Content

The active material currently comes from three-phase grid-connected inverter debugging:

- T-type or NPC three-level SVPWM notes
- 36-small-sector state-vector table reference
- gate mapping and From/Goto routing checks
- phase/line voltage balance and gate legality validation
- MATLAB helpers for SVPWM logging and diagnostics

Maintained active content lives under `subskills/three-phase-grid-inverter/`. Use the subskill paths directly for SVPWM references and table scripts.

### Prerequisites

For full model work, install and configure:

- MATLAB R2023a or later
- Simulink
- Simscape Electrical when the model uses electrical power-stage components
- Simulink Test when persistent model tests are requested
- MathWorks Simulink Agentic Toolkit
- MATLAB MCP Core Server
- an MCP-capable coding agent such as Codex, Claude Code, GitHub Copilot, Amp, or Gemini CLI
- official Simulink skills from https://github.com/simulink/skills or `setupAgenticToolkit("install")`

Minimum capability levels:

- reading references and planning: no MATLAB session required
- printing the active SVPWM table: Python 3
- running active SVPWM diagnostics: MATLAB with Simulink
- direct model inspection and edits from an agent: MATLAB MCP and Simulink Agentic Toolkit initialized

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
│   ├── agent-contracts.md
│   ├── domain-map.md
│   ├── mcp-simulink-troubleshooting.md
│   ├── model-standards.md
│   ├── output-standards.md
│   └── workflow.md
├── scripts/
│   └── validate_skill_structure.py
└── subskills/
    ├── three-phase-grid-inverter/
    ├── motor-drives/
    ├── dc-dc-converters/
    ├── rectifiers-active-front-ends/
    ├── renewable-grid-systems/
    ├── batteries-bms/
    ├── hvdc-facts/
    ├── multilevel-mmc/
    └── wireless-power-resonant/
```

### Typical Use

Ask the agent:

```text
Use $simulink-power-electronics to classify this Simulink power-electronics model, load the relevant subskill, inspect the active control path, diagnose the waveform issue, and report simulation-backed evidence.
```

For the active three-phase grid inverter subskill:

```matlab
addpath("simulink-power-electronics/subskills/three-phase-grid-inverter/scripts")

cfg = struct();
cfg.model = "YourModel";
cfg.stateBlock = "YourModel/SVPWM/Subsystem1";
cfg.gateBlock = "YourModel/SVPWM/Subsystem3";
cfg.voltageBlocks = ["YourModel/Va", "YourModel/Vb", "YourModel/Vc"];
cfg.stopTime = "0.10";

report = svpwm_diagnostics(cfg);
```

Print the active three-level SVPWM table:

```bash
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format markdown
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format json
```

### Validation

The skill folder should pass:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/simulink-power-electronics
python3 scripts/validate_skill_structure.py
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format json
```

The Python scripts have no third-party dependencies. The MATLAB diagnostic script is intended to run inside MATLAB with Simulink available.

### License

This project is licensed under the Apache License 2.0. See [`LICENSE`](LICENSE).

## 中文

`simulink-power-electronics` 是一个面向 Simulink 和 Simscape Electrical 电力电子工作的 Codex Skill。它的主要职责是先把任务路由到正确的电力电子子领域，再保证分析和修改都建立在模型证据上。

本仓库采用“根路由 Skill + 领域 subskills”的结构。根 Skill 放公共工作流规则；`subskills/` 放领域知识。目前只有三相并网逆变器子领域是 active，其它子领域都是有意保留的 stub，只定义范围和需要收集的证据，不代表已经完成领域方法论。

### 设计规则

- 保持 `SKILL.md` 简洁。它负责路由和引用资料，不应该变成长项目提示词。
- 加载领域资料前，先读 `references/domain-map.md`。
- 如果子领域标记为 `stub`，只用它识别范围和选择证据。
- 不要把三相逆变器假设复制到电机驱动、DC-DC、BMS、HVDC/FACTS 或其它领域。
- 一次只升级一个 stub；只有在补充领域参考、真实工作流、可重复验证检查或脚本后，才把 stub 升级为 active。

### 外部工具链

建议和 MathWorks 的 Simulink agent 工具链一起使用：

- 官方 Simulink skills：https://github.com/simulink/skills
- Simulink Agentic Toolkit：https://github.com/matlab/simulink-agentic-toolkit
- MATLAB MCP Core Server：https://github.com/matlab/matlab-mcp-core-server
- Simscape Electrical 文档和示例，用于电力级行为
- Motor Control Blockset 文档和示例，用于电机控制工作流

推荐分工：

- 官方 Simulink skills：通用建模、仿真、模型测试、需求和 Model-Based Design 操作。
- 本仓库：电力电子领域路由、拓扑/控制路径检查、门极和波形诊断、验证证据和可复用领域笔记。

### 子领域状态

| 子领域 | 状态 | 范围 |
| --- | --- | --- |
| `subskills/three-phase-grid-inverter` | active | 三相并网逆变器、SPWM/SVPWM、T 型或 NPC 三电平桥、门极路由、波形平衡 |
| `subskills/motor-drives` | stub | PMSM、BLDC、感应电机驱动、FOC、DTC、转矩/速度/电流环 |
| `subskills/dc-dc-converters` | stub | buck、boost、buck-boost、flyback、谐振、双向 DC-DC |
| `subskills/rectifiers-active-front-ends` | stub | 整流器、PWM AFE、PFC、直流母线调节 |
| `subskills/renewable-grid-systems` | stub | 光伏、风电、储能并网、微电网、PLL、并网规范验证 |
| `subskills/batteries-bms` | stub | 电池包、充电器、均衡、SOC/SOH 相关电力电子行为 |
| `subskills/hvdc-facts` | stub | HVDC、STATCOM、SVC、UPFC、输电系统控制 |
| `subskills/multilevel-mmc` | stub | MMC、级联 H 桥、飞跨电容、电容均衡 |
| `subskills/wireless-power-resonant` | stub | 谐振变换器和感应式无线电能传输 |

### 当前 active 内容

目前真正成熟的内容来自三相并网逆变器调试：

- T 型或 NPC 三电平 SVPWM 笔记
- 36 小扇区状态矢量表
- 门极映射和 From/Goto 路由检查
- 相/线电压平衡和门极合法性验证
- 用于 SVPWM 日志和诊断的 MATLAB 辅助脚本

维护源位于 `subskills/three-phase-grid-inverter/`。SVPWM 参考资料和表格脚本请直接使用子领域路径。

### 使用条件

完整使用前建议安装：

- MATLAB R2023a 或更新版本
- Simulink
- 模型包含电力级器件时需要 Simscape Electrical
- 需要持久化模型测试时使用 Simulink Test
- MathWorks Simulink Agentic Toolkit
- MATLAB MCP Core Server
- 支持 MCP 的编码 agent，例如 Codex、Claude Code、GitHub Copilot、Amp 或 Gemini CLI
- 官方 Simulink skills，可来自 https://github.com/simulink/skills 或 `setupAgenticToolkit("install")`

最低能力层级：

- 只阅读资料和制定方案：不需要 MATLAB 会话
- 打印 active SVPWM 表：Python 3
- 运行 active SVPWM 诊断：MATLAB + Simulink
- 让 agent 直接检查和修改模型：需要 MATLAB MCP 与 Simulink Agentic Toolkit 初始化完成

### 安装

把本目录复制到 agent 的 skill 搜索路径。以 Codex 为例：

```bash
mkdir -p ~/.codex/skills
cp -R simulink-power-electronics ~/.codex/skills/
```

然后重启 agent 会话，让 skill 索引刷新。

另外单独安装并初始化 MathWorks 工具链：

```matlab
setupAgenticToolkit("install")
addpath("~/.matlab/agentic-toolkits/simulink")
satk_initialize
```

执行 `satk_initialize` 后，重启 coding agent 会话，或重新加载宿主 IDE，使 MCP server 能连接到当前共享的 MATLAB 会话。

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
│   ├── agent-contracts.md
│   ├── domain-map.md
│   ├── mcp-simulink-troubleshooting.md
│   ├── model-standards.md
│   ├── output-standards.md
│   └── workflow.md
├── scripts/
│   └── validate_skill_structure.py
└── subskills/
    ├── three-phase-grid-inverter/
    ├── motor-drives/
    ├── dc-dc-converters/
    ├── rectifiers-active-front-ends/
    ├── renewable-grid-systems/
    ├── batteries-bms/
    ├── hvdc-facts/
    ├── multilevel-mmc/
    └── wireless-power-resonant/
```

### 典型用法

可以这样要求 agent：

```text
Use $simulink-power-electronics to classify this Simulink power-electronics model, load the relevant subskill, inspect the active control path, diagnose the waveform issue, and report simulation-backed evidence.
```

对于 active 的三相并网逆变器子领域：

```matlab
addpath("simulink-power-electronics/subskills/three-phase-grid-inverter/scripts")

cfg = struct();
cfg.model = "YourModel";
cfg.stateBlock = "YourModel/SVPWM/Subsystem1";
cfg.gateBlock = "YourModel/SVPWM/Subsystem3";
cfg.voltageBlocks = ["YourModel/Va", "YourModel/Vb", "YourModel/Vc"];
cfg.stopTime = "0.10";

report = svpwm_diagnostics(cfg);
```

打印 active 三电平 SVPWM 表：

```bash
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format markdown
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format json
```

### 验证

Skill 目录应通过：

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/simulink-power-electronics
python3 scripts/validate_skill_structure.py
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format json
```

Python 脚本不依赖第三方库。MATLAB 诊断脚本需要在安装了 Simulink 的 MATLAB 中运行。

### 许可证

本项目使用 Apache License 2.0。完整许可证文本见 [`LICENSE`](LICENSE)。
