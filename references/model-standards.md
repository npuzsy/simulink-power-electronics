# Model Standards

Use this reference before editing Simulink or Simscape Electrical power-electronics models.

## Inspection Standard

Before editing:

- Identify the main model and any referenced models or libraries.
- Inspect active and intentionally disabled control paths.
- Confirm solver settings, sample times, fundamental frequency, switching period, and DC-link value.
- Identify plant measurements used for validation.
- Note generated artifacts such as `slprj/`, cache files, and autosave files.

## Control Path Standard

For inverter/converter models, document:

- topology: two-level, T-type, NPC, flying capacitor, modular multilevel, rectifier, DC-DC converter
- modulation: SPWM, SVPWM, DPWM, hysteresis, model predictive control, or custom
- gate output ordering
- active reference frame and phase sequence
- expected output measurement names

## From/Goto And Commented Subsystems

From/Goto routing is common in Simulink power electronics models, but it is easy to misread.

- Do not treat a missing or ambiguous From/Goto as a bug until commented subsystems are checked.
- If duplicate global tags exist in reference and active controller paths, verify actual plant gate signals by logging root From outputs.
- Do not comment internal Goto blocks inside a subsystem when the parent subsystem is intentionally commented unless there is a specific reason.

## Simscape Electrical Plant Safety

When inspecting or modifying a power stage:

- Confirm every switch has legal gate states.
- Check for shoot-through conditions in each bridge leg.
- Check neutral-point or DC-link capacitor balancing assumptions.
- Confirm voltage/current sensor polarity before interpreting waveforms.
- Treat unexplained solver failures as model-configuration or discontinuity clues, not just numerical noise.

## Generated Artifacts

The following are normally generated and should not be treated as source unless the user asks:

- `slprj/`
- `*.slxc`
- autosave files
- simulation cache files

Do not delete or revert them without explicit intent.
