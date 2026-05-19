# Layout Patterns From PE Examples

Use this reference when generating or repairing Simulink/Simscape Electrical
diagrams where readability matters.

## Contents

- Start with `Subsystem-First Top Level` when a model has many blocks or messy
  top-level wiring.
- Use `Layout Families` to choose the physical arrangement after the subsystem
  split is clear.
- Use `Generation Rules` as the final checklist before editing or accepting a
  layout.

## Evidence Base

Project-local corpus study:

- 242 MATLAB analysis records from official and open-source PE examples.
- 38 representative models opened one at a time, layout-read, then closed.
- Domains sampled: DC-DC, grid inverters, motor drives, renewable/grid systems,
  rectifiers, resonant converters, BMS, and HVDC/control examples.

## Common Layout Pattern

Good examples separate four visual layers:

- physical plant or power path in the middle
- control/reference generation above or below the plant
- measurement blocks next to the measured node
- scopes/displays at the right edge or in a diagnostic area

Top-level lines are usually short. Long lines normally represent intentional
feeders or buses, not accidental return/common-node loops.

## Subsystem-First Top Level

When a generated or repaired model contains enough blocks that control,
measurement, and diagnostic lines obscure the plant, split the top level before
polishing individual line routes.

Trigger this pattern when any of these are true:

- top-level plant, control, scenario, measurement, and scope blocks are mixed
  together
- several long signal lines cross the Simscape plant or power path
- a user says the model is visually confusing, hard to trace, or "too messy"
- a model has enough blocks that automatic layout produces a graph, not a
  readable power-electronics schematic

The desired top level is an architecture view, not a detailed schematic. It
should show a small number of named subsystems and their interfaces:

- `Power_Electronics`, `Plant`, or a topology-specific plant subsystem
- `Control`, `Supervisory_Control`, or a topology-specific controller subsystem
- optional `Scenario`, `Measurements`, or `Diagnostics` subsystem when inputs
  and scopes would clutter the controller

Use this procedure:

1. Inventory the existing blocks by role before moving anything.
   - Plant/power stage: sources, converters, switches, filters, storage,
     Simscape networks, loads, sensors, PS converters, electrical references.
   - Control: references, regulators, droop logic, PWM/modulation, limiters,
     filters, estimators, state machines, protection logic.
   - Scenario/diagnostics: step commands, variable load profiles, computed
     power/SOC signals, scopes, displays, logs, To Workspace blocks.
2. Create the top-level subsystem split before detailed routing. Keep the plant
   in one area and control/diagnostics in another area.
3. Put `Goto` blocks at the signal producer side and `From` blocks at the
   signal consumer side when a direct wire would cross subsystem boundaries or
   cut through the plant. Prefer buses only when many related signals always
   travel together.
4. Name every cross-boundary signal by physical meaning and units, for example
   `Vbus_V`, `Ibatt1_A`, `Icmd1_A`, `Pbat1_W`, `Rload_Ohm`, `Pgrid_W`, or
   `SOC1_pct`.
5. Use directional signal roles consistently:
   - plant -> control: measured voltage/current/power/SOC/status
   - control -> plant: gate commands, duty cycles, current commands, load
     commands, enable/protection commands
   - scenario -> plant/control: step times, reference profiles, load profiles
   - plant/control -> diagnostics: measured and computed signals for scopes
6. Leave short direct wires only for local connections inside a subsystem or for
   obvious top-level subsystem ports. Do not run long wires through a power
   stage just to avoid `Goto`/`From`.
7. After a hierarchy-only layout refactor, validate with update diagram and the
   same simulation or measurement window used before the refactor.

For a storage microgrid, a readable split is usually:

- `Power_Electronics`: DC bus, battery packs, bidirectional converters, super
  capacitor, load, sensors, local electrical references
- `Control`: droop sharing, current or power references, converter command
  generation, limits, load scenario commands
- `Diagnostics`: bus voltage, battery currents, converter powers, load power,
  SOC/energy estimates, scopes, logging

Do not bury all scopes inside the plant. Plant subsystems should expose the
measurements needed to debug physical behavior, while diagnostics collect and
display them outside the power stage.

## Layout Families

Pick one family before placing blocks:

- **Converter pipeline:** source -> switch/converter -> energy storage/filter ->
  load. Use for buck, boost, buck-boost, SEPIC, Cuk.
- **Bridge:** source/DC link on the left, symmetric devices in the middle,
  filter/load/grid on the right. Use for inverters and rectifiers.
- **Resonant pipeline:** input switch stage -> resonant tank -> transformer ->
  rectifier/output.
- **Drive chain:** command/controller -> inverter -> machine -> mechanical load.
- **Feeder:** source/grid/transformer/line/load left to right, with vertical
  load taps.
- **Battery pack:** battery module central, source/thermal inputs nearby,
  balancing/control to the side.

## Generation Rules

1. Choose the layout family.
2. Identify named physical nodes and high-degree common nodes.
3. Assign lanes: power path, return/neutral rail, control, measurement,
   diagnostics.
4. For block-heavy systems, choose the top-level subsystem split before routing
   internal plant or control lines.
5. Choose block orientation from port positions and polarity.
6. Connect local physical networks first.
7. Route control and measurement after the power path is stable.
8. Screenshot or inspect line points; reject remote trunks, boundary wraps, and
   accidental crossings through the plant.

Generic graph layout is useful for ordering large subsystems. It is not enough
for component-level Simscape Electrical circuits without node and lane rules.
