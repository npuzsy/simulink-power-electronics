# Simulink Power Electronics Skill

`simulink-power-electronics` is a Codex skill for Simulink and Simscape
Electrical power-electronics models. It adds domain-specific guidance for
topology recognition, signal debugging, schematic layout, and validation on top
of generic Simulink model-building and simulation tools.

中文摘要：`simulink-power-electronics` 是一个面向 Codex 的
Simulink/Simscape Electrical 电力电子 Skill，用于帮助识别拓扑、检查模型、
调试波形和控制链路、优化元件布局与走线，并用可复查的仿真证据说明结果。

## What It Does / 它能做什么

- Classifies power-electronics models by application domain, topology, and
  control objective.
- Inspects solver settings, sample times, variants, From/Goto routing,
  plant/control boundaries, measurement polarity, and generated artifacts before
  edits.
- Helps debug three-phase grid inverters, including SPWM/SVPWM, gate mapping,
  waveform balance, VSG control paths, and P/Q checks.
- Guides signal logging and measurement-point selection so model outputs can be
  collected at key plant and control locations for performance analysis.
- Provides developing inspection guidance for DC-DC converters and motor-drive
  models.
- Adjusts Simulink and Simscape component placement and wiring using layout
  patterns learned from MathWorks examples and open-source projects.
- Reports validation state explicitly as `opened`, `compiled`, `simulated`, or
  `measured`.

- 按应用域、拓扑和控制目标识别电力电子模型。
- 在修改模型前检查 solver、sample time、variant、From/Goto、plant/control
  分层、测量极性和生成产物。
- 支持三相并网逆变器的 SPWM/SVPWM、门极映射、波形平衡、VSG 控制链路和
  P/Q 检查。
- 指导 AI 选择和读取关键 plant/control 位置的输出信号，用于辅助模型性能分析。
- 为 DC-DC converter 和 motor-drive 模型提供开发中的检查清单。
- 可以基于 MathWorks 样例和开源项目经验调整 Simulink/Simscape 元件布局和走线。
- 在结果中明确区分 `opened`、`compiled`、`simulated`、`measured` 等验证状态。

## Quick Use

Install or copy this folder as a Codex skill, restart Codex, then invoke it when
reviewing, editing, generating, or validating Simulink power-electronics models:

```text
$simulink-power-electronics
```

With the Codex skill installer:

```text
$skill-installer install https://github.com/npuzsy/simulink-power-electronics
```

This repository is maintained and validated as a Codex skill. Claude Code
compatibility has not been verified yet.

Suggested prompt:

```text
Please use $simulink-power-electronics to read the current project, confirm
that the Simulink MCP tools are reachable, and summarize the architecture of
the Simulink model. Then check for known bugs, modeling risks, or improvement
opportunities. My goal is to [describe your goal]. Please propose an edit plan
first, and wait for my approval before making model or file changes.
```

## Layout Example

When generating or repairing Simscape Electrical models, prefer readable circuit
schematics over generic graph layouts. For a DC-DC converter, identify nodes
such as `VIN_POS`, `SW`, `VOUT_POS`, and `RETURN` first, then place the power
path, control blocks, and measurement blocks around those nodes.

The Buck converter below was laid out with those rules. The v4 model completed
update diagram and a 3 ms simulation with `ode23t`.

![Buck converter v4 layout](assets/images/buck-v4-layout.png)

## Repository Structure

```text
simulink-power-electronics/
├── SKILL.md
├── agents/
├── assets/
│   └── images/
├── references/
├── scripts/
└── subskills/
    ├── three-phase-grid-inverter/
    ├── dc-dc-converters/
    ├── motor-drives/
    └── ...
```

## Important References

- `references/domain-map.md`: choose the right power-electronics subdomain.
- `references/workflow.md`: inspect, diagnose, edit, and validate.
- `references/model-standards.md`: model-editing standards.
- `references/layout-patterns-from-examples.md`: layout patterns extracted from
  example models.
- `references/simscape-layout.md`: Simscape Electrical schematic layout rules.
- `references/capability-map.md`: current capability boundary.

## Subskill Status

| Subskill | Status | Scope |
| --- | --- | --- |
| `three-phase-grid-inverter` | active | SPWM/SVPWM, three-level inverter gate routing, waveform balance, VSG/control tracing |
| `dc-dc-converters` | developing | Buck/boost/buck-boost, regulation evidence, schematic layout |
| `motor-drives` | developing | PMSM/BLDC/induction drive inspection and control-path tracing |
| others | stub | Scope markers and evidence checklists |

## Toolchain

Real model inspection, editing, and validation require:

- MATLAB R2023a or later
- Simulink
- MATLAB MCP Core Server
- Simulink Agentic Toolkit

Models that use physical electrical networks also require:

- Simscape
- Simscape Electrical

Use Simulink Agentic Toolkit or model-based-design skills for generic model
creation, editing, simulation, and testing mechanics.

Platform notes:

- macOS and Linux are the preferred targets for the current MCP workflow.
- Windows may work, but MCP subprocess environment variables, socket access, or
  file-permission issues are more common.
- If MATLAB MCP or Simulink Agentic Toolkit is unavailable, model-level
  inspection and validation cannot be claimed.

## Validation

Before committing, run:

```bash
python3 scripts/validate_skill_structure.py --quiet
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format json
```

## Contributing

This skill can improve itself when users explicitly allow self-iteration:
reviewing additional MathWorks examples or open-source Simulink projects,
extracting repeatable patterns, and promoting validated findings into the skill.
Contributions are welcome, especially model-derived debugging notes, layout
rules, validation scripts, and focused subskill improvements.

## License

Apache License 2.0. See [LICENSE](LICENSE).
