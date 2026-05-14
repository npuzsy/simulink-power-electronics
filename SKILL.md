---
name: simulink-power-electronics
description: Use when working on Simulink or Simscape Electrical power-electronics models, including inverters, DC-DC converters, rectifiers, motor drives, renewable/grid systems, batteries/BMS, HVDC/FACTS, converter layout, gate routing, solver issues, waveform debugging, and simulation-backed validation.
---

# Simulink Power Electronics

## Overview

Use this skill to route Simulink power-electronics work to the right domain, then keep diagnosis and edits grounded in inspected block paths, logged signals, simulations, and numerical checks.

Treat this file as the top-level router. Keep shared workflow in `references/`, reusable outputs in `assets/`, repository checks in `scripts/`, and domain-specific knowledge in `subskills/`.

## Prerequisites

For direct Simulink model access, expect MATLAB R2023a or later, Simulink, MATLAB MCP Core Server, Simulink Agentic Toolkit, and the official Simulink skills from `https://github.com/simulink/skills` or `setupAgenticToolkit("install")`. For Simscape Electrical plant inspection, the target MATLAB installation must include Simscape Electrical. For persistent model tests, Simulink Test is required.

## Resource Map

- Read `references/domain-map.md` to choose the correct power-electronics sub-domain.
- Read `references/workflow.md` for the inspection, diagnosis, edit, and validation loop.
- Read `references/control-algorithm-debugging.md` for control algorithm signal-tracing methodology, PI tuning experience, power calculation verification, and feedforward formulas.
- Read `references/simulink-command-line-sop.md` for command-line simulation and data reading procedures.
- Read `references/model-standards.md` before editing Simulink or Simscape Electrical converter models.
- Read `references/mcp-simulink-troubleshooting.md` when MATLAB MCP, Simulink Agentic Toolkit, `satk_initialize`, or agent tool discovery fails.
- Read `references/agent-contracts.md` only for large reviews where independent model, control, waveform, or validation work must be split explicitly.
- Read `references/output-standards.md` before writing reports or review findings.
- Read `subskills/three-phase-grid-inverter/SKILL.md` for active three-phase grid-connected inverter, SPWM/SVPWM, T-type or NPC three-level bridge, gate-routing, waveform-balance, VSG control, and PI tuning work.
- Treat all other `subskills/*/SKILL.md` files as stubs until their references and validation scripts are populated.
- Use templates in `assets/` for project README and diagnostic reports.

## Subskill Routing

1. Identify the application domain before loading detailed references.
2. If the work is a three-phase grid-connected inverter, load `subskills/three-phase-grid-inverter/SKILL.md` and its references/scripts.
3. If the work maps to a stub subskill, treat the stub as a scope marker. Use the root workflow, inspected model evidence, and authoritative public references; do not borrow three-phase inverter assumptions unless the measured model path is genuinely shared.
4. If the domain is ambiguous, classify by plant topology, control objective, energy source/load, and validation signals before editing.

## Agent Conduct

These rules govern how the agent interacts with the user and approaches control algorithm work. They override any technical optimization that conflicts with them.

- **The user leads, the agent assists.** The user has global knowledge of the model that the agent cannot match. For model operations (wiring, parameter changes, module mode switching), ask the user first rather than spending dozens of token-heavy steps摸索.
- **The agent is a second pair of eyes and a calculator.** Responsible for data analysis, formula derivation, and root-cause identification, but does not replace the user's judgment.
- **Engineer mindset, not programmer mindset.** When output is wrong, find the root cause, understand why, fix from the source. Do not work around problems. A power deviation of 1.6x means finding whether it is line voltage or transform coefficient error, not "trying a ratio to fit." Working around = hiding = eventual failure.
- **Parameters have physical meaning.** Clarke/Park transform coefficients (1.5, 2/3, sqrt(3)) all have mathematical derivation sources. Never use a "fitted ratio" to correct inconsistencies. When internal and external values disagree, trace to the source (line-to-line vs phase-to-ground voltage, transform coefficient, sign convention).
- **Do not act blindly without data.** If signal data cannot be read, immediately ask the user for help.
- **When stuck, ask the user immediately.** Do not drill into a problem alone for dozens of steps. The user can typically resolve it in seconds.

## Operating Rules

- Inspect before editing: active/reference paths, commented subsystems, From/Goto routing, sample times, solver settings, measurement polarity, and generated artifacts.
- Prefer logs over screenshots: capture controller internals, final gates, plant-side inputs, and validation waveforms before drawing conclusions.
- Edit the smallest responsible source: tables, mappings, signs, parameters, or active control paths. Preserve reference implementations and generated artifacts unless asked otherwise.
- Validate before saving or claiming success: update diagram, run the relevant simulation, compare plant-side gates, check legal switch states, and report numerical waveform results.
- Keep shared model edits, save operations, final diagnosis, and user-facing synthesis serial. Split only independent read-only or disjoint-write work.
- **Understand the global context before operating on any component.** Know what a V-I Measurement outputs (line-to-line or phase-to-ground), how downstream Power and S-Function blocks use it, where From/Goto tags map to, and what effects a parameter change will have on downstream modules.

## Automation

Use scripts only after selecting the domain. The currently active automation lives under `subskills/three-phase-grid-inverter/scripts/`.

## Output Standard

Write in the user's language. For completed engineering work, include:
Top-level router for Simulink and Simscape Electrical power-electronics work.
Use official Simulink skills for generic model operations; use this skill for
PE domain routing, topology/control inspection, layout rules, and validation
evidence.

## Load Order

1. Read `references/domain-map.md` to choose the subskill.
2. Read `references/workflow.md` for inspect -> diagnose -> edit -> validate.
3. Read `references/model-standards.md` before editing a power stage.
4. For generated Simscape schematics, read:
   - `references/layout-patterns-from-examples.md`
   - `references/simscape-layout.md`
5. Read the matching `subskills/*/SKILL.md`.
6. Read `references/output-standards.md` before reporting.

Use `references/capability-map.md` only when the user asks what this skill can
do. Use `references/self-iteration-loop.md` and
`references/example-derived-patterns.md` only for corpus/self-improvement work.
Use `references/mcp-simulink-troubleshooting.md` when MATLAB MCP or Simulink
Agentic Toolkit access fails.

## Core Rules

- Inspect before editing: model role, active variants, commented subsystems,
  solver/sample times, From/Goto tags, plant topology, control path, and sensor
  polarity.
- Keep conclusions evidence-backed. Track validation state explicitly:
  `opened`, `compiled`, `simulated`, and `measured`.
- Do not treat library/helper diagrams or partial copied examples as runnable
  top-level systems.
- Keep edits scoped to the responsible block, subsystem, table, parameter, or
  signal mapping.
- For component-level Simscape Electrical layout, classify nodes before drawing:
  power path, switch/commutation node, output node, and return/neutral/common
  node. Do not let automatic routing create remote common-node trunks.
- Save only after update diagram and the minimum relevant simulation pass,
  unless the user asks for an unsaved draft.

## Subskill Routing

- `subskills/three-phase-grid-inverter`: active SPWM/SVPWM, gate routing, and
  waveform-balance diagnostics.
- `subskills/dc-dc-converters`: developing DC-DC inspection and generated
  schematic layout guidance.
- `subskills/motor-drives`: developing motor-drive inspection guidance.
- Other subskills are scope/evidence stubs. Use root workflow and inspected
  model evidence; do not import assumptions from unrelated domains.

## Generated Artifacts

Keep downloaded corpora, generated models, simulation caches, and long loop
outputs out of source control. Use `data/pe-loop/` for local corpus work and
`data/generated-models/` for throwaway demos.
