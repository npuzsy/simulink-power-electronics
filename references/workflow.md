# Execution Workflow

Use this workflow for Simulink power-electronics model analysis, waveform debugging, modulation implementation, or model review.

## 1. Load Context

1. Read project documentation if present.
2. Identify the main `.slx`, MATLAB release, required toolboxes, and linked guide/specification files.
3. Identify the converter topology and active control path.
4. Load relevant Simulink skills when available:
   - building Simulink models
   - simulating Simulink models
   - testing Simulink models when persistent tests are requested

## 2. Inspect Before Editing

1. Use `model_overview` or `model_read` to identify hierarchy and interfaces.
2. Inspect plant topology, control topology, measurement blocks, and signal routing.
3. Confirm subsystem comment states before diagnosing missing signals.
4. Inspect From/Goto paths if the plant receives gates through tags.
5. Record assumptions about signal order, phase sequence, and units.

## 3. Diagnose Waveforms

1. Log relevant intermediate control signals.
2. Log final gate signals and plant-side gate inputs.
3. Log output voltages/currents used by the scopes.
4. Simulate long enough to separate transient from steady-state.
5. Compare expected and actual:
   - switching legality
   - state or duty symmetry
   - phase RMS balance
   - line RMS balance
   - DC offset
   - conservation checks such as phase sum

## 4. Edit Safely

1. Keep edits scoped to the smallest responsible subsystem.
2. Prefer correcting source tables, mappings, or sign conventions over downstream compensation.
3. Preserve reference implementations unless the user asks to remove them.
4. Use `model_edit` for structural or parameter edits when possible.
5. Avoid changing generated artifacts as if they were source.

## 5. Validate

Minimum validation:

1. Update diagram passes.
2. A simulation completes.
3. Logged gate signals match the plant-side inputs.
4. Illegal switch states are absent.
5. Steady-state numerical measurements are balanced or match the requirement.

For reusable tests, create persistent model tests instead of one-off scripts.

## 6. Report

Include:

- root cause
- exact subsystem or block path changed
- what was intentionally left unchanged
- simulation duration and analysis window
- numerical verification
- remaining risks or recommended next checks
