# Agent Contracts

Use this reference only when a Simulink power-electronics task is large enough to split into independent work. Keep the main agent responsible for final diagnosis, model edits, save decisions, and user-facing synthesis.

## When To Split

Split work when at least two tasks can progress without shared mutable state:

- plant topology inspection
- controller or modulation path inspection
- SVPWM table comparison
- signal logging plan
- report or test artifact review

Do not split work just because the model is large. If the next action depends on one result, do that task locally.

## Contract Template

```text
Task:
Purpose:
Inputs:
Owned paths:
Forbidden paths:
Allowed tools:
Expected artifact:
Validation evidence:
Stop conditions:
```

## Standard Contracts

### Plant Inspector

Purpose: identify power-stage topology, measurement polarity, switch naming, gate input order, and physical constraints.

Expected artifact:

```text
Topology:
Plant block paths:
Gate input order:
Measurement blocks and polarity:
Switch legality constraints:
Unverified assumptions:
```

### Controller Inspector

Purpose: identify the active control path, modulation pipeline, sample times, From/Goto routing, and intentionally disabled reference paths.

Expected artifact:

```text
Active controller path:
Reference/commented paths:
Modulation pipeline:
Sample times:
Gate output order:
Routing risks:
```

### SVPWM Table Auditor

Purpose: compare the model's three-level SVPWM state-vector constants against `subskills/three-phase-grid-inverter/references/table7-state-vectors.md` or `subskills/three-phase-grid-inverter/scripts/print_table7_state_vectors.py`.

Expected artifact:

```text
Table source paths:
Encoding assumption:
Mismatched sectors:
Expected first-four vectors:
Actual first-four vectors:
Likely waveform effect:
```

### Validation Planner

Purpose: define the smallest simulation and signal logging plan that can verify the suspected fix.

Expected artifact:

```text
Stop time:
Analysis window:
Signals to log:
Pass/fail checks:
Numerical thresholds:
Toolbox or runtime risks:
```

## Merge Rules

- Prefer measured facts over inferred facts.
- If two artifacts disagree, inspect the model or logs directly before editing.
- Only the main agent should apply shared model edits or save `.slx` files.
- Keep final reports in the user's language, with exact block paths and numerical evidence.
