---
name: simulink-power-electronics
description: Use when working on Simulink or Simscape Electrical power-electronics models, including inverters, converters, rectifiers, motor drives, renewable/grid systems, batteries, HVDC/FACTS, gate routing, solver issues, waveform debugging, and simulation-backed validation.
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
3. If the work maps to a stub subskill, treat the stub as a scope marker. Use the root workflow, inspected model evidence, and authoritative public references; do not borrow three-phase inverter assumptions unless the measured model path is genuinely shared.
4. If the domain is ambiguous, classify by plant topology, control objective, energy source/load, and validation signals before editing.

## Operating Rules

- Inspect before editing: active/reference paths, commented subsystems, From/Goto routing, sample times, solver settings, measurement polarity, and generated artifacts.
- Prefer logs over screenshots: capture controller internals, final gates, plant-side inputs, and validation waveforms before drawing conclusions.
- Edit the smallest responsible source: tables, mappings, signs, parameters, or active control paths. Preserve reference implementations and generated artifacts unless asked otherwise.
- Validate before saving or claiming success: update diagram, run the relevant simulation, compare plant-side gates, check legal switch states, and report numerical waveform results.
- Keep shared model edits, save operations, final diagnosis, and user-facing synthesis serial. Split only independent read-only or disjoint-write work.

## Automation

Use scripts only after selecting the domain. The currently active automation lives under `subskills/three-phase-grid-inverter/scripts/`.

## Output Standard

Write in the user's language. For completed engineering work, include:

- root cause
- exact model/file areas changed
- what was intentionally left unchanged
- verification method and simulation settings
- key numerical results
- remaining risks or suggested next checks

Keep explanations focused on the model and evidence. Add theory only when it helps the user learn or decide.
