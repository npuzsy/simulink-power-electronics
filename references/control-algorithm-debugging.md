# Control Algorithm Debugging Methodology

Use this reference when debugging control algorithms in Simulink power-electronics models, especially for S-Function based implementations, VSG (Virtual Synchronous Generator) inverters, and grid-connected control systems.

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

## Iron Rules

These rules must never be violated:

1. **Always trust Scope/oscilloscope measured data.** S-Function internal mexPrintf calculations may have errors (sign errors, coefficient omissions, transform errors). The only basis for judging control effectiveness is the actual waveform from Scope.
2. **Never close a model without saving.** Any time `close_system`/`bdclose` is needed, the user must first Ctrl+S in the GUI.
3. **Control parameters have physical meaning. Never use "fitted ratios" to correct.** Clarke/Park transform coefficients (1.5, 2/3, sqrt(3)) all have mathematical derivation sources. When internal and external values disagree, find the root cause (line-to-line vs phase-to-ground, transform coefficient, sign convention), not a number to fit.
4. **Do not act blindly without data.** If signal data cannot be read, immediately ask the user for help.
5. **When stuck, ask the user immediately.** Do not drill into a problem alone for dozens of steps.
6. **Engineer mindset, not programmer mindset.** Find root cause -> understand why -> fix from source. No workarounds allowed.

## PI Parameter Tuning Experience

### Anti-Windup Trap

Back-calculation anti-windup (`*integrator = y_sat - kp*error`) can lock the integrator at the negative limit when `kp*error` is large, requiring extremely long recovery time.

- When `kp*error` is large, the integrator gets clamped and cannot recover
- Typical symptom: output stuck at lower limit for extended periods
- Fix: increase KI, use conditional integration, or redesign the anti-windup mechanism

### Feedforward Priority

The main control quantity should use physical formula direct calculation (feedforward) as much as possible. PI is only for fine-tuning.

- If PI is struggling to correct a large steady-state error, the feedforward formula or parameters are wrong
- Example for grid-connected current reference:
  ```
  id_ref = Pref / (k * Vd)     % k = 1.5 (Clarke amplitude-invariant)
  iq_ref = -Qref / (k * Vd)    % sign depends on Q convention
  ```
- The coefficient `k` must be consistent with the P/Q calculation coefficient system upstream

### Integral Gain Recovery Time

When KI is too small, integrator recovery time may far exceed simulation duration.

- Example: KI=10, TS=1e-4, integrator recovery from -40 to 0 takes approximately 4 seconds
- If simulation stop time is shorter than this, the system will appear to never reach steady state

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

## Feedforward Calculation Formulas

For grid-connected current reference values, prefer feedforward (physical formula direct calculation):

```
id_ref = Pref / (k * Vd)     % k = 1.5 (Clarke amplitude-invariant)
iq_ref = -Qref / (k * Vd)    % sign depends on Q convention
```

Where `k` must be exactly consistent with the P/Q calculation coefficient system upstream.

Voltage and current sign conventions:

```text
         | Voltage | Current | P/Q sign convention
---------|---------|---------|--------------------
P (active)  | k*(vα·iα+vβ·iβ) | Consistent with load direction
Q (reactive) | k*(vβ·iα-vα·iβ) | Sign depends on α/β ordering
```

## VSG (Virtual Synchronous Generator) Control Notes

### Self-Synchronization

Grid-forming VSG inverters do not need PLL. The angle is generated by the swing equation, and power balance maintains synchronization.

- VSG generates its own reference angle through the swing equation: `J*(dω/dt) = Pm - Pe - D*(ω-ω0)`
- The angle theta is obtained by integrating omega: `theta = integral(omega)`
- Power balance is maintained through the virtual inertia and damping coefficients

### VSG Control Structure

Typical VSG control path:

```
Power Reference (Pref, Qref)
    -> Swing Equation (virtual inertia J, damping D)
    -> Angle theta (from integrating omega)
    -> Voltage Reference (from reactive power droop)
    -> dq/abc Transform
    -> PWM Modulation
    -> Gate Signals
```

### VSG vs PLL-based Control

| Aspect | VSG (Grid-forming) | PLL-based (Grid-following) |
|--------|-------------------|---------------------------|
| Synchronization | Self-synchronized via swing equation | Tracks grid via PLL |
| Angle source | Internal integration | PLL output |
| Weak grid performance | Better, provides voltage support | May lose synchronization |
| Inertia | Virtual inertia (J parameter) | No inherent inertia |

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

Once the user mentions Simulink simulation, immediately:

1. Identify model path (.slx) and S-Function code (.c/.m)
2. Use MATLAB MCP to read model structure, list all blocks and connections
3. Confirm all S-Function input ports are connected
4. Record Scope/To Workspace variable names

### Phase 2: Requirement Confirmation (Plan Mode)

Confirm with user: desired effect, control algorithm type, feedback signal source, reference value settings. Ask questions immediately, do not assume.

### Phase 3: Debug Execution

1. First look at Scope waveform (actual effect), then internal variables
2. Trace level by level along signal chain: angle -> dq transform -> controller output -> modulation signal
3. When anomaly found, first check control parameters (Kp/Ki/limit values/TS)
4. **Trace to the end, do not work around from the middle**
