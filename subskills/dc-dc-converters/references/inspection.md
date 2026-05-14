# DC-DC Converter Inspection Notes

Status: developing. These notes are derived from the initial PE corpus loop and are not yet a complete DC-DC methodology.

## Classify First

Before diagnosing a DC-DC model, identify:

- topology: buck, boost, buck-boost, four-switch buck-boost, chopper, resonant, isolated converter
- plant fidelity: switching model, averaged model, Simscape physical plant, or library/helper block
- control mode: voltage-mode, current-mode, duty feedforward, MPPT-linked, or open-loop PWM
- operating mode: CCM, DCM, bidirectional, startup, load-step, line-step, or regulation steady state

## Common Evidence

Collect:

- input voltage and output voltage
- inductor current and capacitor voltage/ripple
- duty command, saturation, PWM carrier, and final switch command
- load current/resistance and load-step timing
- switching frequency and controller sample time
- device voltage/current stress if the request touches hardware safety

## Observed Patterns

Initial analyzed examples show:

- many DC-DC candidates are library block diagrams rather than runnable examples
- variable-step Simscape Electrical examples and fixed-step Specialized Power Systems examples both appear
- single-file copies often miss companion scripts/data; use full folders for simulation-backed conclusions
- a model that only opens can teach topology and block usage, but should not be used to infer regulation, ripple, or device stress behavior

## Debug Priorities

1. Distinguish library/helper converter blocks from runnable converter examples.
2. Check solver and switching frequency before interpreting ripple.
3. Verify duty-cycle limits and controller saturation before changing plant parameters.
4. Use line/load-step windows for regulation claims.
5. Separate startup transient from steady-state ripple and RMS measurements.
6. Record whether conclusions are based on `opened`, `compiled`, `simulated`, or `measured` evidence.

## Generated Schematic Layout Priorities

For component-level Simscape DC-DC converters, classify nodes before using any
layout or routing algorithm:

1. `VIN_POS`: input source positive and switch input.
2. `SW`: switching node connected to freewheel path and inductor input.
3. `VOUT_POS`: inductor output, output capacitor positive, load positive.
4. `RETURN`: source negative, freewheel return, capacitor negative, load
   negative, solver configuration, and electrical reference.

The `RETURN` node must usually be drawn as a bottom rail. If automatic routing
creates a remote vertical trunk or wraps the rail around the canvas edge, the
model is not yet official-example quality even if the topology is electrically
connected.

Compare against MathWorks buck examples: the official diagrams keep the power
stage readable as a schematic, separate control/measurement routing from the
power loop, and use converter subsystems when the example focus is regulation
rather than component-level device behavior.
