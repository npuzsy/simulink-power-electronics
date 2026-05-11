---
name: three-phase-grid-inverter
description: Use when working on Simulink or Simscape Electrical three-phase grid-connected inverter models, including SPWM/SVPWM, T-type or NPC three-level bridges, grid-side voltage/current waveform balance, gate routing, sector tables, and switching-state validation.
---

# Three-Phase Grid Inverter

## Overview

Use this active subskill for three-phase grid-connected inverter work. It contains the populated knowledge in this repository: T-type/NPC three-level SVPWM, state-vector table checks, gate mapping, From/Goto routing risks, and simulation-backed waveform validation.

Use the root `simulink-power-electronics` workflow first, then load this subskill when the model is in scope.

## Resource Map

- Read `references/svpwm-three-level.md` for T-type or NPC three-level SVPWM logic, sector handling, and gate mapping.
- Read `references/table7-state-vectors.md` when auditing or rebuilding the 36 small-sector state-vector table.
- Use `scripts/svpwm_diagnostics.m` when MATLAB/Simulink can run and the model exposes state, gate, and voltage signals.
- Use `scripts/print_table7_state_vectors.py` when a deterministic JSON or Markdown copy of the reference table is needed.

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

1. Confirm grid-side reference frame, phase sequence, measurement polarity, and analysis window before interpreting waveforms.
2. Identify the active modulation path: SPWM, SVPWM, disabled reference path, or commented subsystem.
3. Log controller state vectors, final gate vectors, plant-side gate inputs, and phase/line voltage or current measurements.
4. For three-level SVPWM, compare every large sector and small sector against `table7-state-vectors.md`; partial sector-I checks are not enough.
5. For T-type/NPC gate mapping, confirm the physical switch order before applying `N/O/P` assumptions.
6. Validate after startup transient unless startup behavior is the target.

## Evidence Checks

- controller gate vector equals plant-side gate input
- no illegal switch state appears in any bridge leg
- phase and line RMS values are balanced in the selected steady-state window
- phase sum, DC offset, and current polarity match the model objective
- sector/state-vector counts are plausible for the modulation method and operating point

## Automation

For a conventional three-level SVPWM model with accessible logging points, add this subskill's `scripts` directory to the MATLAB path and call:

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
