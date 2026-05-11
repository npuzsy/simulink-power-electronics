---
name: motor-drives
description: Use when working on Simulink or Simscape Electrical motor-drive power-electronics models, including PMSM, BLDC, induction motor drives, FOC, DTC, torque/speed/current loops, inverter-fed machines, and drive waveform validation.
---

# Motor Drives

## Status

Stub. Use this file only to recognize motor-drive scope and choose evidence to collect. Apply the root `simulink-power-electronics` workflow; do not reuse grid-inverter assumptions unless the inspected model path is genuinely shared.

## Scope

- PMSM, BLDC, and induction motor drives
- field-oriented control, direct torque control, six-step control, and current/torque/speed loops
- inverter-fed machine gate, phase-current, torque, and speed validation
- encoder, resolver, Hall, or sensorless feedback paths

## Evidence To Collect

- machine type, inverter topology, DC-link value, sample times, and active control mode
- current, speed, torque, rotor-position, and sensor-alignment signals
- gate order, phase sequence, and controller-to-plant signal routing
- load step, speed command, torque command, or startup window used for validation

## Promote When

Promote only after adding motor-control references, a repeatable Simulink workflow, and checks for currents, torque/speed response, sensor alignment, and inverter gate legality.
