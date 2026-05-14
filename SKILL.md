---
name: simulink-power-electronics
description: Use when working on Simulink or Simscape Electrical power-electronics models, including inverters, DC-DC converters, rectifiers, motor drives, renewable/grid systems, batteries/BMS, HVDC/FACTS, converter layout, gate routing, solver issues, waveform debugging, and simulation-backed validation.
---

# Simulink Power Electronics

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
