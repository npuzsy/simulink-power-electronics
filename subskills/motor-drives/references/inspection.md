# Motor-Drive Inspection Notes

Status: developing. These notes are derived from the initial PE corpus loop and are not yet a complete motor-drive methodology.

## Classify First

Before diagnosing a motor-drive model, identify:

- machine type: PMSM, IPMSM, BLDC, induction, switched reluctance, multi-phase PMSM
- control mode: FOC, DTC, six-step, open-loop, torque control, speed control, current control
- plant fidelity: Simscape physical plant, Specialized Power Systems plant, averaged model, or controller-only model
- sensor path: QEP, Hall, resolver, sensorless estimator, ideal measurement
- inverter path: duty-cycle interface, PWM/gate interface, averaged voltage source, or switching bridge

## Common Evidence

Collect:

- speed command and measured speed
- torque command/load and electromagnetic torque
- `Id/Iq` or phase-current feedback
- position/speed sensor signals and offset/calibration assumptions
- duty cycles, PWM, or gate signals from controller to plant
- DC-link voltage and current limits
- sample times for current loop, speed loop, PWM, and plant

## Observed Patterns

Current analyzed examples show:

- motor-drive examples frequently use fixed-step discrete solvers for controller/switching workflows
- deep subsystem hierarchy is normal; start at the top-level plant/controller/measurement partition before opening controller internals
- `From`/`Goto`, buses, `RateTransition`, Mux/Demux, and scopes are common routing surfaces
- existing scopes are often numerous enough to reuse before adding new logging points
- controller outputs may be voltage references, duty cycles, PWM signals, or final gates; identify the interface before judging inverter behavior
- some files are library block diagrams and cannot be update-diagram/simulation targets
- multi-phase PMSM examples require avoiding hardcoded three-phase assumptions

## Debug Priorities

1. Confirm initialization scripts and motor/inverter parameter structures are loaded.
2. Build a `From`/`Goto` tag map for speed, torque, phase currents, `Id/Iq`, rotor position, PWM, and gates.
3. Confirm sensor scaling and phase-current reconstruction before tuning controllers.
4. Confirm position offset and electrical/mechanical angle conventions.
5. Confirm current-loop output units and inverter interface: voltage reference, duty cycle, or gates.
6. Confirm current-loop, speed-loop, PWM, and plant sample times before interpreting oscillation or ripple.
7. Confirm load torque/speed profile and analysis window.
