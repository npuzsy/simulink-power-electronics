---
name: three-phase-grid-inverter
description: Use when working on Simulink or Simscape Electrical three-phase grid-connected inverter models, including SPWM/SVPWM, T-type or NPC three-level bridges, grid-side voltage/current waveform balance, gate routing, sector tables, and switching-state validation.
---

# Three-Phase Grid Inverter

## Overview

Use this active subskill for three-phase inverter and grid-connected converter work. It contains the currently populated field knowledge in this repository: three-level T-type or NPC SVPWM, state-vector table checks, gate mapping, From/Goto routing risks, and simulation-backed waveform validation.

Use the root `simulink-power-electronics` workflow first, then load this subskill when the model is in scope.

## Resource Map

- Read `references/svpwm-three-level.md` when working on T-type or NPC three-level SVPWM.
- Read `references/table7-state-vectors.md` when checking or rebuilding 36 small-sector state-vector tables.
- Use `scripts/svpwm_diagnostics.m` for repeatable MATLAB-side SVPWM gate and waveform diagnostics.
- Use `scripts/print_table7_state_vectors.py` to print the three-level SVPWM table in JSON or Markdown.

## In Scope

- three-phase grid-connected inverters
- two-level inverter diagnostics when the same gate-routing and waveform evidence workflow applies
- T-type or NPC three-level bridges
- SPWM, SVPWM, and closely related discontinuous PWM checks
- phase/line voltage balance, current balance, DC offset, and phase-sum checks
- controller-to-plant gate ordering and legal switching states

## Out Of Scope

Use a different subskill or the root workflow for:

- motor-drive torque/speed control
- DC-DC converter regulation
- rectifier/PFC-specific behavior
- battery or BMS modeling
- HVDC/FACTS studies
- MMC or flying-capacitor balancing not covered by the existing three-level inverter notes

## Workflow Additions

1. Confirm grid-side reference frame, phase sequence, and measurement polarity before interpreting waveforms.
2. Identify whether the active modulation path is SPWM, SVPWM, a reference implementation, or a commented subsystem.
3. Log controller state vectors, final gate vectors, plant-side gate inputs, and phase/line voltage or current measurements.
4. For three-level SVPWM, compare sector and small-sector state-vector tables against `table7-state-vectors.md`.
5. For T-type gate mapping, confirm physical switch order before applying `N/O/P` assumptions.
6. Validate after startup transient, not from the initial transient unless the startup behavior is the target.

## Automation

For a conventional three-level SVPWM model, add this subskill's `scripts` directory to the MATLAB path and call:

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
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format markdown
python3 subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py --format json
```
