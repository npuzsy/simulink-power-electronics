---
name: simulink-power-electronics
description: Use when working on Simulink or Simscape Electrical power-electronics models, including inverter, DC-DC converter, rectifier, motor-drive, battery/BMS, renewable-grid, HVDC/FACTS, converter layout, gate-routing, solver, waveform, control-algorithm, or simulation validation tasks.
---

# Simulink Power Electronics

Use this skill for Simulink/Simscape Electrical power-electronics work:
model inspection, waveform/control debugging, schematic layout, validation, and
corpus self-improvement. Keep conclusions grounded in inspected block paths,
logged signals, simulations, and numeric checks.

## Core Workflow

1. Classify by domain, topology, and control objective.
2. Load only the narrow context needed: usually `references/workflow.md`, one
   domain subskill, and one triggered reference.
3. Prefer MATLAB MCP and Simulink Agentic Toolkit evidence. If model tools are
   unavailable, report the gap and stop model diagnosis.
4. Track validation state explicitly: `opened`, `compiled`, `simulated`,
   `measured`.

## Lean Loading Rules

- Treat this root file as a router, not a handbook.
- Do not bulk-load README, every reference, or every subskill.
- Read platform and MCP setup details only when tool status is uncertain.
- Promote new notes only when they are grounded in official sources, inspected
  models, or repeatable validation.

## Read When Needed

- `references/domain-map.md` to choose the subskill.
- `references/workflow.md` for inspect -> diagnose -> edit -> validate.
- `references/model-standards.md` before editing PE models.
- `references/layout-patterns-from-examples.md` and
  `references/simscape-layout.md` for generated or repaired Simscape schematics.
- `references/control-algorithm-debugging.md` for control tracing,
  PI/feedforward, and P/Q checks.
- `references/simulink-command-line-sop.md` for command-line simulation and
  output reading.
- `references/mcp-simulink-troubleshooting.md` for supported platform, MCP
  dependency, or tool discovery questions.
- `references/output-standards.md` before reports.
- `references/capability-map.md` only when asked about scope.
- `references/self-iteration-loop.md` and `references/example-derived-patterns.md`
  for corpus/self-improvement.
- `subskills/three-phase-grid-inverter/SKILL.md` for active grid-inverter work.
- Treat other `subskills/*/SKILL.md` files as evidence guides until populated.
- Use Simulink Agentic Toolkit or model-based-design skills for generic build,
  edit, simulate, and test mechanics; use this skill for PE-specific routing
  and evidence rules.
- Use `assets/` templates when output needs a project README or diagnostic
  report.

## Operating Rules

- Inspect before editing: active/reference paths, commented subsystems,
  From/Goto routing, sample times, solver settings, measurement polarity, and
  generated artifacts.
- For control defects, trace backward level by level from modulation output to
  raw measurements.
- Parameters have physical meaning. Do not fit a ratio to hide line/phase
  voltage, transform, sign, or unit errors.
- For Simscape layout, classify nodes before drawing and keep common/return
  nodes local.
- Validate before success: update diagram, run the minimum relevant
  simulation, compare plant-side gates, check legal switch states, and report
  numeric results.
- Ask for missing model data, logs, or GUI state when available tools cannot
  access them.

## Subskill Routing

- `subskills/three-phase-grid-inverter`: active SPWM/SVPWM, gate routing,
  waveform balance, VSG, PI/feedforward, and P/Q checks.
- Developing or stub subskills: use only as scope markers and evidence
  checklists.
- If the domain is ambiguous, classify by source/load, topology, control
  objective, and validation signals first.

## Boundary

- This skill does not manage OS-level schedulers, background jobs, or other
  system automation.
- This skill does not replace Simulink build/simulate/test skills; it adds
  PE-specific routing, evidence standards, and diagnostics.
- Keep downloaded corpora, generated models, caches, and long-loop outputs out
  of source control under `data/pe-loop/` or `data/generated-models/`.

## Reporting

Report root cause, changed paths, validation state, and remaining risks in the
user's language.
