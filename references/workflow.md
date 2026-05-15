# Execution Workflow

Use this workflow for Simulink power-electronics model analysis, waveform debugging, modulation implementation, or model review. Select the sub-domain from `domain-map.md` before loading domain-specific references.

## Contents

- Core Rule
- 1. Load Context
- 2. Inspect Before Editing
- 3. Diagnose Waveforms
- 4. Edit Safely
- 5. Validate
- 6. Report
- Parallel Work

## Core Rule

Every diagnosis or edit must be traceable to model evidence. Maintain a short working artifact as you go: intake summary, inspected block paths, assumptions, logged signals, simulation settings, observed defect, edit target, validation result, and remaining risk.

Use the user's language for user-facing notes. Use exact Simulink block paths and signal names for technical claims.

## 1. Load Context

1. Read project documentation if present.
2. Identify the main `.slx`, MATLAB release, required toolboxes, and linked guide/specification files.
3. Classify each model file as top-level runnable model, library/reference model, test harness, generated artifact, or helper subsystem.
4. Identify the power-electronics domain, converter topology, and active control path.
5. Load relevant Simulink skills when available:
   - building Simulink models
   - simulating Simulink models
   - testing Simulink models when persistent tests are requested
5. If MATLAB MCP or Simulink Agentic Toolkit tools are unavailable, stop model diagnosis and use `mcp-simulink-troubleshooting.md`.

Expected checkpoint:

```text
Model:
Model role:
Domain:
Topology:
Active control path:
Symptom or request:
Validation signals:
Tooling status:
Assumptions:
```

## 2. Inspect Before Editing

1. Use `model_overview` or `model_read` to identify hierarchy and interfaces.
2. Inspect plant topology, control topology, measurement blocks, and signal routing.
3. Confirm subsystem comment states before diagnosing missing signals.
4. Inspect From/Goto paths if the plant receives gates through tags.
5. Separate active Variant Subsystem choices from inactive/all-variant content.
6. Record assumptions about signal order, phase sequence, and units.
7. Identify generated artifacts and do not treat them as source.

Do not edit before this checkpoint unless the user asks for a text-only artifact unrelated to an existing model.

Expected checkpoint:

```text
Inspected paths:
Active paths:
Reference/commented paths:
Gate order assumption:
Measurement polarity assumption:
Generated artifacts observed:
```

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
6. Separate observations from inference. If a conclusion is inferred from topology rather than measured logs, label it as inferred.

For SVPWM or gate-routing defects, do not rely on scope appearance alone. At minimum compare final controller gates against plant-side gate inputs.

For control algorithm defects (current tracking, power regulation, dq transform issues), use the signal-tracing methodology from `control-algorithm-debugging.md`: trace backward level by level from modulation output through controller output, error signals, reference values, dq transform, and raw measurements. At each level, locate the anomaly and find the root cause before moving to the next.

## 4. Edit Safely

1. Keep edits scoped to the smallest responsible subsystem.
2. Prefer correcting source tables, mappings, or sign conventions over downstream compensation.
3. Preserve reference implementations unless the user asks to remove them.
4. Use `model_edit` for structural or parameter edits when possible.
5. Avoid changing generated artifacts as if they were source.
6. Make one conceptual change at a time when simulation feedback is available.

Save gate:

- Do not save a model immediately after structural edits.
- Run update diagram first.
- Run the minimum simulation needed to check the edited behavior.
- Save only after validation passes, unless the user explicitly asks for an unsaved draft state.

## 5. Validate

Track validation state explicitly:

- `opened`: MATLAB can open the model.
- `compiled`: update diagram succeeds.
- `simulated`: a simulation completed.
- `measured`: logged signals or output data were numerically checked.

Minimum validation:

1. Update diagram passes.
2. A simulation completes.
3. Logged gate signals match the plant-side inputs.
4. Illegal switch states are absent.
5. Steady-state numerical measurements are balanced or match the requirement.

For reusable tests, create persistent model tests instead of one-off scripts.

Recommended evidence table:

```text
Check                         Result
Update diagram                pass/fail
Simulation stop time          ...
Analysis window               ...
Gate mismatch samples         ...
Illegal switch states         ...
Phase RMS                     ...
Line RMS                      ...
Phase sum / DC offset         ...
```

If a validation step cannot run because of missing MATLAB, missing toolboxes, long runtime, licensing, or unavailable model files, report that as a verification gap rather than a pass.

## 6. Report

Include:

- root cause
- exact subsystem or block path changed
- what was intentionally left unchanged
- simulation duration and analysis window
- numerical verification
- remaining risks or recommended next checks

## Parallel Work

Use parallel work only for independent tasks with clear artifacts, such as:

- one read-only agent inspecting plant topology while another inspects controller logic
- one agent comparing an SVPWM table against `subskills/three-phase-grid-inverter/references/table7-state-vectors.md` while another prepares simulation signals
- one agent reviewing report wording while the main agent owns model edits

Do not split:

- edits to the same `.slx`
- save operations
- final root-cause synthesis
- tasks that require shared MATLAB state unless the toolchain explicitly supports isolated sessions

For complex splits, read `agent-contracts.md` and assign each worker an input, owned paths, forbidden paths, required output, and validation evidence.
