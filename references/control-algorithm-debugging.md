# Control Algorithm Debugging Methodology

Use this reference when debugging control algorithms in Simulink
power-electronics models. For grid-inverter VSG, PI/feedforward, and P/Q
formula details, also read
`subskills/three-phase-grid-inverter/references/vsg-control-notes.md`.

## Contents

- Key Understanding
- Signal Tracing Methodology
- Guardrails
- Control Parameter Checks
- Power Calculation Verification Checklist
- Common Issues Quick Reference
- Debugging Workflow for Control Algorithms

## Key Understanding

This is about the implementation characteristics inside the S-Function, not the simulation itself. The simulation may run at a different time scale (e.g., simulation step 1e-6, control algorithm step 1e-4). The TS inside the S-Function must match the control algorithm step, not the simulation step.

## Signal Tracing Methodology

When output is abnormal, trace backward along the signal chain level by level:

1. **Modulation output** (Valpha/Vbeta) — Is it saturated?
2. **Controller output** (ud/uq, ud_pi/uq_pi) — Is it saturated?
3. **Current/voltage error** (err_id, err_vd) — Difference between reference and actual
4. **Reference values** (id_ref, iq_ref, ue_ref) — Incorrectly limited?
5. **dq transform result** (Vd, Vq, ild, ilq) — Is the transform angle correct?
6. **Raw measurements** (alpha-beta components) — Is the measurement signal itself correct?

**At each level, locate the anomaly and find the root cause. Do not skip levels.**

## Guardrails

Apply these guardrails to avoid fitting symptoms instead of debugging the
implementation:

1. **Prefer measured waveforms over internal printouts.** S-Function
   `mexPrintf` calculations may contain sign, coefficient, or transform errors.
   Use Scope/logged output as the main evidence for control effectiveness, then
   use internal values to localize the implementation defect.
2. **Do not close a dirty model implicitly.** Before `close_system` or
   `bdclose`, verify whether the model has unsaved changes and ask the user if
   the intended state is unclear.
3. **Control parameters have physical meaning.** Clarke/Park transform
   coefficients such as 1.5, 2/3, and sqrt(3) come from defined transform and
   voltage conventions. When internal and external values disagree, trace line
   voltage vs phase voltage, transform coefficient, sign convention, and units
   instead of introducing a fitted correction ratio.
4. **Stop when required data is missing.** If signal data cannot be read through
   available tools, ask the user for the missing signal, screenshot, or GUI
   state instead of continuing from guesses.
5. **Fix from the source.** Prefer root-cause fixes over downstream
   compensation unless the downstream compensation is explicitly part of the
   control design.

## Control Parameter Checks

Use these checks before changing gains:

- confirm controller sample time and S-Function internal `TS`
- check saturation and anti-windup behavior before increasing PI gains
- compare required integrator recovery time with simulation stop time
- verify that feedforward formulas and units match upstream measurements
- confirm sign conventions before compensating with negative gains

For concrete VSG and grid-current formulas, use the inverter VSG reference.

## Power Calculation Verification Checklist

When S-Function internal P/Q disagrees with Scope, check in order:

1. **V-I Measurement voltage mode**: phase-to-phase (line voltage) or phase-to-ground (phase voltage)?
2. **Clarke transform coefficient**: amplitude-invariant (2/3) or power-invariant (sqrt(2/3))?
3. **P/Q formula**: `P = k*(vα·iα+vβ·iβ)`, `Q = k*(vβ·iα-vα·iβ)`, where k is determined by both Clarke coefficient and voltage type
4. **Sign convention**: Q sign depends on iα/iβ exchange and voltage reference definition; compare with standard Power block to confirm
5. **Line-to-phase conversion**: if using line voltage input and need phase voltage, `va=(vab-vca)/3`

| Symptom | Likely Cause |
|---------|--------------|
| P deviation ~1.5x | alpha-beta to power coefficient error, or line/phase voltage confusion |
| Q sign reversed | alpha/beta order or sign error in Q formula |
| P/Q both very small | Input port not connected (floating) |

## Common Issues Quick Reference

| # | Issue | Root Cause | Investigation |
|---|-------|------------|---------------|
| 1 | Signal always zero | Input port not connected | Check S-Function input wiring |
| 2 | Simulation step mismatch | TS inconsistent with control period | Compare code TS with Simulink step |
| 3 | Current explosion (hundreds of A) | LCL resonance or per-unit error | Test in C; check Valpha range |
| 4 | MEX compilation not taking effect | Old MEX locked or cached | `clear <sfunc>` then re-mex |
| 5 | dq transform result abnormal | Transform angle offset by 90° | Check angle_from_alphabeta/atan2 |
| 6 | Power cannot track reference | Current limiting or feedforward formula error | Check PI limits and feedforward coefficients |
| 7 | PI integrator not recovering | Anti-windup locked | Increase KI or use conditional integration |
| 8 | Scope data not updating | Command-line sim() not writing to workspace | Read via `ans.property_name` |

## Debugging Workflow for Control Algorithms

### Phase 1: Initialization

When debugging a control algorithm:

1. Identify model path (.slx) and S-Function code (.c/.m)
2. Use MATLAB MCP to read model structure, list all blocks and connections
3. Confirm all S-Function input ports are connected
4. Record Scope/To Workspace variable names

### Phase 2: Requirement Confirmation

Confirm the desired effect, control algorithm type, feedback signal source, and
reference value settings. Ask targeted questions when those inputs are not
available from the model.

### Phase 3: Debug Execution

1. First inspect measured/logged waveforms, then internal variables
2. Trace level by level along signal chain: angle -> dq transform -> controller output -> modulation signal
3. When anomaly found, first check control parameters (Kp/Ki/limit values/TS)
4. **Trace to the end, do not work around from the middle**
