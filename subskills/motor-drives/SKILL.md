---
name: motor-drives
description: Use when working on Simulink or Simscape Electrical motor-drive power-electronics models, including PMSM, BLDC, induction motor drives, FOC, DTC, torque/speed/current loops, inverter-fed machines, and drive waveform validation.
---

# Motor Drives

## Status

Developing active subskill. Use this file to recognize motor-drive scope and choose evidence to collect. Apply the root `simulink-power-electronics` workflow; do not reuse grid-inverter assumptions unless the inspected model path is genuinely shared.

Read `references/inspection.md` for corpus-derived inspection notes before diagnosing motor-drive examples. Treat those notes as developing guidance, not a complete methodology.

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

## Current Corpus-Derived Capability

Use the motor-drive subskill for inspection and debug planning when the goal is to trace machine control paths, not only to classify files. Current analyzed examples repeatedly show deep subsystem hierarchy, heavy `From`/`Goto` routing, fixed-step controller workflows, and existing scope/measurement surfaces. Before adding new logs or changing parameters, build a tag map and identify the top-level split between plant, inverter, controller, and measurements.

Treat these checks as required before tuning or editing:

- separate current-loop, speed-loop, torque-loop, and modulation/PWM paths
- record whether the inverter accepts voltage references, duty cycles, or final gates
- identify mechanical angle, electrical angle, and position offset conventions
- check sample times for current controller, speed controller, PWM, and plant
- reuse existing scopes/logging blocks where they already expose speed, torque, phase currents, or `Id/Iq`

## Promote When

Promote only after adding motor-control references, a repeatable Simulink workflow, and checks for currents, torque/speed response, sensor alignment, and inverter gate legality.
