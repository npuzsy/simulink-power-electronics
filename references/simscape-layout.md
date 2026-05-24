# Simscape Electrical Layout Notes

Use after `references/layout-patterns-from-examples.md` when generating or
repairing component-level Simscape Electrical schematics.

## Contents

- Use `Node-First Procedure` for the physical circuit inside the plant.
- Use `Subsystem-First Layout For Larger Models` when top-level plant and
  control wiring are tangled.
- Use `Acceptance Criteria` before claiming the layout is readable.

## Core Principle

Draw a schematic, not a generic graph. Automatic layout and `routeLine` can
improve ordinary signal diagrams, but they do not know PE conventions such as
return rails, DC-link midpoint locality, bridge symmetry, or sensor polarity.

## Node-First Procedure

Before adding lines, classify electrical nodes. For a Buck converter:

- `VIN_POS`: source positive and high-side switch input
- `SW`: switching midpoint, freewheel device, and inductor input
- `VOUT_POS`: inductor output, capacitor positive, load positive, sensors
- `RETURN`: source negative, freewheel return, capacitor/load return, reference

Then place blocks so important ports face their node:

- put the main power path left to right
- put vertical components between their upper node and the return rail
- keep high-degree common nodes local as rails or local reference symbols
- keep control and measurement routing outside the main power loop
- put sensors adjacent to the node they measure

## Subsystem-First Layout For Larger Models

For models with enough blocks that plant and control lines obscure the
schematic, split layout before routing individual lines:

- top level: one plant/power-electronics subsystem, one control subsystem, and
  optional diagnostics or scenario subsystems
- subsystem names should be short and scan-friendly. Use names such as
  `Power`, `Control`, `Diagnostics`, `Load`, `Plant`, or
  `Power_Electronics`; move longer explanations to annotations
- plant subsystem: Simscape network, power stage, local return/common rails,
  sensors, and Simulink-PS or PS-Simulink converter blocks
- control subsystem: references, regulators, filters, limiters, estimators,
  scenario profiles, command generation, and protection logic
- diagnostics subsystem: computed power/SOC signals, scopes, displays, and data
  logs when those blocks would clutter the controller
- cross-boundary signals: use explicit `Goto`/`From` tags or buses with units in
  names; avoid long top-level wires through the plant
- validation: after refactoring hierarchy, update diagram and simulate using
  the same measurement windows used before the layout change

When generating a Simulink model rather than a text-only derivation, make the
model readable as blocks and relationships. Do not hide the main electrical
plant, storage interface, load path, or droop/control architecture inside a
single large MATLAB Function block. Use ordinary Simulink/Simscape blocks and
named `Goto`/`From` tags so the topology can be inspected visually.

Use compact, consistent spacing. For routine generated layouts, target 25 px
horizontal and vertical clearance between neighboring blocks, allow 20 px as
the minimum, and avoid exceeding 30 px unless separating larger functional
zones or removing unavoidable wire crossings.

This pattern is especially useful for averaged converters, storage systems,
microgrids, BMS-linked plants, and other systems where control paths are much
denser than the physical plant.

Inside the plant subsystem, still draw a circuit schematic:

- arrange the main energy path left to right from source/storage to converter,
  DC bus, filter, grid, or load
- place the return, neutral, DC-link midpoint, or electrical reference close to
  the devices that share it
- place voltage and current sensors next to the node or branch being measured
- keep PS-Simulink converter outputs near the sensors, then send measured
  signals out through subsystem ports or `Goto` blocks
- keep Simulink-PS converter inputs near actuated plant elements, such as duty
  commands, load-resistance commands, or controlled sources

Inside the control subsystem, draw a signal-flow diagram:

- arrange reference or scenario inputs on the left
- arrange droop sharing, PI/current control, filters, limiters, and modulation
  left to right in the order they execute
- keep feedback `From` blocks near the controller stage that consumes them
- put command `Goto` blocks at the right edge so plant-facing commands are easy
  to find

Cross-boundary naming should make signal direction obvious without opening the
subsystems. Examples:

- `Vbus_V`: plant bus-voltage measurement used by control and diagnostics
- `Ibatt1_A`, `Ibatt2_A`: plant battery-current measurements
- `Pbat1_W`, `Pbat2_W`: computed battery powers for droop verification
- `Icmd1_A`, `Icmd2_A`: control current commands sent to converters
- `Rload_Ohm`: scenario or control command sent to a variable resistor
- `GateBatt1`, `GateBatt2`, or `DutyBatt1`, `DutyBatt2`: converter commands

For droop-controlled parallel storage, keep the ratio logic readable. Put the
sharing law, gains, and limits together in `Control`; expose the measured
powers and commands to `Diagnostics`; keep the two battery/converter branches
parallel and symmetric in `Power_Electronics`. If one branch is intended to
deliver twice the other, label the references or droop gains so the intended
2:1 sharing target is visible without tracing constants through the plant.

## Acceptance Criteria

A generated schematic is acceptable only if:

- the main power path is visually traceable
- return/common/neutral nodes are local and intentional
- no high-degree node routes to a remote canvas edge
- source and sensor polarity were checked from actual block ports
- gate/control lines do not cross the plant unnecessarily
- the model reaches at least `compiled` before layout guidance is reused

If the purpose is regulation or system integration, prefer subsystem/library
converter blocks. Use discrete component-level Simscape blocks when the user
needs topology, switching behavior, device stress, or sensor-polarity detail.
