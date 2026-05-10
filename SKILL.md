---
name: simulink-power-electronics
description: Analyze, build, debug, and verify Simulink and Simscape Electrical power-electronics models, especially three-phase inverters, grid-connected converters, SPWM/SVPWM modulation, T-type or NPC three-level bridges, gate-signal routing, solver/simulation issues, and waveform validation. Use when Codex works on Simulink power electronics projects, reads converter design guides or PDFs, modifies modulation/control subsystems, diagnoses incorrect scope waveforms, compares expected and actual gate pulses, or creates reusable project documentation and simulation evidence.
---

# Simulink Power Electronics

## Overview

Use this skill to turn a power-electronics waveform symptom into a model-grounded diagnosis, a scoped Simulink edit, and a numerical verification report. Prefer signal logging, model topology, and repeatable simulations over visual guesses.

## Prerequisites

For direct Simulink model access, expect MATLAB R2023a or later, Simulink, MATLAB MCP Core Server, Simulink Agentic Toolkit, and the official Simulink skills from `https://github.com/simulink/skills` or `setupAgenticToolkit("install")`. For Simscape Electrical plant inspection, the target MATLAB installation must include Simscape Electrical. For persistent model tests, Simulink Test is required.

## Resource Map

- Read `references/workflow.md` for the end-to-end inspection, diagnosis, edit, and validation loop.
- Read `references/model-standards.md` before editing Simulink or Simscape Electrical converter models.
- Read `references/mcp-simulink-troubleshooting.md` when MATLAB MCP, Simulink Agentic Toolkit, `satk_initialize`, or agent tool discovery fails.
- Read `references/svpwm-three-level.md` when working on T-type or NPC three-level SVPWM.
- Read `references/table7-state-vectors.md` when checking or rebuilding 36 small-sector state-vector tables.
- Read `references/output-standards.md` before writing reports or review findings.
- Use `scripts/svpwm_diagnostics.m` for repeatable MATLAB-side SVPWM gate and waveform diagnostics.
- Use `scripts/print_table7_state_vectors.py` to print the three-level SVPWM table in JSON or Markdown.
- Use templates in `assets/` for project README and diagnostic reports.

## Responsibilities

1. Identify the converter topology, active control path, modulation method, and expected measurements.
2. Inspect the model before editing: hierarchy, subsystem comment state, From/Goto tags, signal dimensions, solver settings, and generated artifacts.
3. Diagnose control and plant issues using logged signals and simulation outputs.
4. Keep fixes scoped to the responsible subsystem unless the user explicitly asks for broader refactoring.
5. Validate gate routing, legal switch states, phase/line voltage balance, and transient-vs-steady-state behavior.
6. Persist durable project facts when requested, without leaking machine-specific private context into open-source artifacts.

## Execution Steps

1. Load context.
   - Read project documentation if present.
   - Identify the main `.slx`, relevant PDF/specification, MATLAB release, required toolboxes, and intended active control path.
   - Load available Simulink skills for model building, simulation, and testing.
   - If Simulink MCP tools are missing or stale, diagnose setup before analyzing the model.

2. Inspect before editing.
   - Use Simulink model tools to inspect hierarchy and connections.
   - Confirm which controller path is active and which paths are reference or intentionally commented.
   - Treat duplicate global Goto tags as a routing risk; verify actual signals by logging.

3. Diagnose with evidence.
   - Log intermediate controller signals, final gate vectors, root plant gate inputs, and relevant voltage/current measurements.
   - Simulate at least one fundamental cycle. Simulate longer when filters or plants have startup transients.
   - Compare expected and actual state counts, gate patterns, RMS values, and conservation checks such as `Va+Vb+Vc`.

4. Edit safely.
   - Use `model_edit` for model edits when possible.
   - Preserve intentionally disabled reference implementations.
   - Fix table, mapping, or routing defects at their source rather than adding compensating inversions downstream.
   - Avoid rearranging plant layout or generated artifacts unless needed.

5. Validate and report.
   - Run update diagram.
   - Run simulation-based checks.
   - Save only after validation passes.
   - Report the root cause, changed paths, unchanged intentional state, simulation window, and key numerical evidence.

## Automation

For a conventional three-level SVPWM model, add this skill's `scripts` directory to the MATLAB path and call:

```matlab
cfg = struct();
cfg.model = "YourModel";
cfg.svpwmSubsystem = "YourModel/SVPWM";
cfg.stateBlock = "YourModel/SVPWM/Subsystem1";
cfg.gateBlock = "YourModel/SVPWM/Subsystem3";
cfg.voltageBlocks = ["YourModel/Voltage Measurement2", "YourModel/Voltage Measurement3", "YourModel/Voltage Measurement4"];
cfg.stopTime = "0.10";
report = svpwm_diagnostics(cfg);
```

For the bundled table reference:

```bash
python3 scripts/print_table7_state_vectors.py --format markdown
python3 scripts/print_table7_state_vectors.py --format json
```

## Output Standard

Write in the user's language. For completed engineering work, include:

- root cause
- exact model/file areas changed
- what was intentionally left unchanged
- verification method and simulation settings
- key numerical results
- remaining risks or suggested next checks

Keep explanations focused on the model and evidence. Add theory only when it helps the user learn or decide.
