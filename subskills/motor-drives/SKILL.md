---
name: motor-drives
description: Use when working on Simulink or Simscape Electrical motor-drive power-electronics models, including PMSM, BLDC, induction motor drives, FOC, DTC, torque/speed/current loops, inverter-fed machines, and drive waveform validation.
---

# Motor Drives

## Status

Stub. Use the root `simulink-power-electronics` workflow for now. Do not apply three-phase grid-inverter assumptions unless the user explicitly asks and the model evidence supports them.

## Intended Scope

- PMSM, BLDC, and induction motor drives
- field-oriented control, direct torque control, six-step control, and current/torque/speed loops
- inverter-fed machine gate, phase-current, torque, and speed validation
- encoder, resolver, Hall, or sensorless feedback paths

## Not Yet Provided

- motor-control-specific inspection checklist
- FOC/DTC signal validation standards
- machine parameter and sensor alignment checks
- reusable MATLAB diagnostics
- representative model tests

## Promotion Criteria

Promote this stub to active only after adding domain references, at least one repeatable Simulink workflow, and validation checks for currents, torque/speed response, sensor alignment, and inverter gate legality.
