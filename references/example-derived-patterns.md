# Example-Derived Patterns

Use this reference when promoting findings from local official/open-source
example analysis into stable skill behavior. Keep only repeated, actionable
patterns here.

## Structural Patterns

- PE examples commonly separate plant, controller, measurements, scopes, and
  scenario/test inputs at the top level.
- From/Goto, buses, variants, and commented reference subsystems are common.
  Trace active paths before diagnosing missing or wrong signals.
- Opening a model is weaker evidence than update diagram, simulation, or logged
  numerical measurements.
- Library/helper diagrams can teach interfaces and parameters, but they should
  not be used for waveform or solver conclusions.
- Single copied `.slx` files often miss initialization scripts, data
  dictionaries, referenced models, local libraries, or `.mat` data.

## Debugging Consequences

- Record validation state as `opened`, `compiled`, `simulated`, or `measured`.
- Classify model role before simulation-backed conclusions.
- Inspect solver type and sample times before comparing ripple, RMS, tracking,
  speed, or current-loop behavior.
- Inspect controller-to-plant routing before concluding the power stage is
  wrong.
- Record missing libraries/toolboxes and unresolved references as environment
  evidence, not model defects.

## Layout Patterns

- Choose a layout family before placing blocks: converter pipeline, bridge,
  resonant pipeline, feeder, drive chain, battery pack, or control-only diagram.
- Keep measurements local to measured nodes and scopes/displays in a diagnostic
  area.
- Use hierarchy for control-heavy systems instead of drawing every control line
  through the plant.
- For component-level Simscape Electrical circuits, identify common/return/
  neutral nodes before routing. Generic graph layout does not reliably create
  readable rails.

## Domain Promotion Notes

Motor drives:

- classify machine type before control method
- separate current, speed, torque, modulation/PWM, and plant paths
- build a From/Goto tag map for nontrivial models
- record current-loop, speed-loop, PWM, and plant sample times

DC-DC converters:

- classify topology and CCM/DCM assumptions
- inspect inductor current, output capacitor voltage, duty saturation, and
  load/input step windows
- require compiled or stronger evidence before regulation/ripple claims
- use node-first layout for generated Simscape schematics
