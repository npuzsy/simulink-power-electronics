# Simulink Command-Line Simulation SOP

Use this reference for command-line simulation execution and data reading procedures in MATLAB/Simulink.

## Contents

- Standard Procedure
- Data Source Priority
- Important Notes
- Scope Data Structure
- Steady-State Analysis
- Common Pitfalls

## Standard Procedure

```matlab
% 1. Clear workspace (do this every time to prevent old data interference)
evalin('base', 'clear');

% 2. Compile (do not close model; just clear + mex)
clear <sfunc_name>;
mex -output <sfunc_name> <wrapper>.c <sfunc>.c

% 3. Run simulation
simOut = sim('model_name', 'StopTime', 'N');

% 4. Read data: access directly from simOut (i.e., ans) properties
%    WARNING: fieldnames(simOut) only returns 2 fields
%    MUST use simOut.property_name for direct access
pq   = simOut.<Scope_log_variable>;
pout = simOut.<ToWorkspace_variable>;

% 5. Use Scope struct
t = pq.time;                      % Time
P = pq.signals(1).values;         % Channel 1
Q = pq.signals(2).values;         % Channel 2

% 6. Steady-state analysis
idx = t >= steady_state_start & t <= steady_state_end;
fprintf('Mean: %.0f\n', mean(P(idx)));
```

## Data Source Priority

When multiple data sources are available, use in this order:

1. **Scope or logged measured data** — the primary evidence for actual behavior
2. **To Workspace** — Structured data written to workspace
3. **mexPrintf** — Internal S-Function logging, may have errors

## Important Notes

### Workspace Clearing

Clear the workspace before repeatable command-line simulations to prevent stale
data from previous runs from contaminating results:

```matlab
evalin('base', 'clear');
```

### S-Function Compilation

When recompiling S-Function after code changes:

```matlab
% Clear the old MEX binary first
clear <sfunc_name>;

% Then compile with explicit output name
mex -output <sfunc_name> <wrapper>.c <sfunc>.c
```

Do not close the model during this process. The model can remain open.

### Reading Simulation Output

The `sim()` function returns a `Simulink.SimulationOutput` object. Common mistakes:

- `fieldnames(simOut)` may not show all logged signals
- Use direct property access: `simOut.Scope_variable_name`
- For To Workspace data: `simOut.ToWorkspace_variable_name`

### Scope Data Structure

When reading Scope-logged data:

```matlab
signal_data = simOut.scope_variable_name;

% Access time vector
t = signal_data.time;

% Access signal values (1-indexed)
ch1 = signal_data.signals(1).values;
ch2 = signal_data.signals(2).values;

% Get signal dimensions
dims = signal_data.signals(1).dimensions;
```

### Steady-State Analysis

When analyzing steady-state behavior:

1. Identify the startup transient period (typically first few fundamental cycles)
2. Select analysis window after transient settles
3. Use logical indexing for the analysis window:

```matlab
idx = t >= t_start & t <= t_end;
mean_value = mean(signal(idx));
rms_value = rms(signal(idx));
```

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Stale workspace data | Results don't change after model edit | Use `evalin('base','clear')` before sim |
| Wrong variable name | Empty or missing data | Check exact variable names in model |
| fieldnames() incomplete | Missing logged signals | Use direct property access instead |
| Model not saved | sim() uses old model | Save model before running sim() |
| Short simulation | System not reaching steady state | Increase StopTime |
| Wrong analysis window | Transient included in results | Verify steady-state start time |
