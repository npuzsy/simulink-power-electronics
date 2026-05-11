---
name: simulink-power-electronics
description: Use when working on Simulink or Simscape Electrical power-electronics models, including converters, inverters, rectifiers, motor drives, DC-DC converters, renewable and grid systems, batteries, HVDC/FACTS, gate routing, solver issues, waveform debugging, converter design guides, or simulation evidence.
---

# Simulink Power Electronics

## Overview

Use this skill to route Simulink power-electronics work to the right sub-domain, then turn a model symptom or design request into model-grounded analysis, scoped edits, and numerical verification. Prefer signal logging, topology inspection, and repeatable simulations over visual guesses.

Treat this `SKILL.md` as the top-level orchestrator. Keep general workflow in `references/`, reusable outputs in `assets/`, deterministic checks in `scripts/`, and domain-specific knowledge in `subskills/`.

## Prerequisites

For direct Simulink model access, expect MATLAB R2023a or later, Simulink, MATLAB MCP Core Server, Simulink Agentic Toolkit, and the official Simulink skills from `https://github.com/simulink/skills` or `setupAgenticToolkit("install")`. For Simscape Electrical plant inspection, the target MATLAB installation must include Simscape Electrical. For persistent model tests, Simulink Test is required.

## Resource Map

- Read `references/workflow.md` for the end-to-end inspection, diagnosis, edit, and validation loop.
- Read `references/domain-map.md` to choose the correct power-electronics sub-domain.
- Read `references/model-standards.md` before editing Simulink or Simscape Electrical converter models.
- Read `references/mcp-simulink-troubleshooting.md` when MATLAB MCP, Simulink Agentic Toolkit, `satk_initialize`, or agent tool discovery fails.
- Read `references/agent-contracts.md` only for large reviews where independent model, control, waveform, or validation work must be split explicitly.
- Read `references/output-standards.md` before writing reports or review findings.
- Read `subskills/three-phase-grid-inverter/SKILL.md` for active three-phase grid-connected inverter, SPWM/SVPWM, T-type or NPC three-level bridge, gate-routing, and waveform-balance work.
- Treat all other `subskills/*/SKILL.md` files as stubs until their references and validation scripts are populated.
- Use templates in `assets/` for project README and diagnostic reports.

## Subskill Routing

1. Identify the application domain before loading detailed references.
2. If the work is a three-phase grid-connected inverter, load `subskills/three-phase-grid-inverter/SKILL.md` and its references/scripts.
3. If the work maps to a stub subskill, use only the root workflow and public MathWorks/model evidence; do not borrow three-phase inverter assumptions unless the user explicitly asks.
4. If the domain is ambiguous, classify by plant topology, control objective, energy source/load, and validation signals before editing.

## Responsibilities

1. Own sequencing: intake, inspection, diagnosis, scoped edit, validation, and final synthesis.
2. Keep one write owner for each model, script, report, or persistent artifact.
3. Identify the domain, converter topology, active control path, modulation/control method, and expected measurements before editing.
4. Inspect hierarchy, subsystem comment state, From/Goto tags, signal dimensions, solver settings, and generated artifacts.
5. Validate gate routing, legal switch states, phase/line voltage balance, and transient-vs-steady-state behavior with logged data.
6. Persist durable project facts only when requested, without leaking machine-specific private context into open-source artifacts.

## Execution Steps

Follow `references/workflow.md`. In brief:

1. Build an intake summary: model path, domain, topology, active control path, required toolboxes, target symptom, and validation signals.
2. Inspect before editing. Confirm active vs reference paths, From/Goto routing, commented subsystems, sample times, solver settings, and measurement polarity.
3. Diagnose with artifacts: capture logged controller, gate, plant-input, and waveform evidence before proposing a fix.
4. Edit only the smallest responsible source. Preserve disabled reference implementations and generated artifacts unless the user asks otherwise.
5. Validate before saving or claiming success: update diagram, simulation, gate legality, plant-side gate match, and numerical waveform checks.
6. Report the root cause, changed paths, unchanged intentional state, simulation window, numerical evidence, and remaining risk.

Use parallel analysis only when work is genuinely independent, read-only or disjoint-write, and the merge cost is justified. Keep shared model edits, save operations, final diagnosis, and user-facing synthesis serial.

## Automation

Use subskill scripts only after the domain is selected. The currently active automation lives under `subskills/three-phase-grid-inverter/scripts/`.

## Output Standard

Write in the user's language. For completed engineering work, include:

- root cause
- exact model/file areas changed
- what was intentionally left unchanged
- verification method and simulation settings
- key numerical results
- remaining risks or suggested next checks

Keep explanations focused on the model and evidence. Add theory only when it helps the user learn or decide.
