# Simscape Electrical Layout Notes

Use after `references/layout-patterns-from-examples.md` when generating or
repairing component-level Simscape Electrical schematics.

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
