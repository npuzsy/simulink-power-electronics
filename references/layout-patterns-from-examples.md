# Layout Patterns From PE Examples

Use this reference when generating or repairing Simulink/Simscape Electrical
diagrams where readability matters.

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
4. Choose block orientation from port positions and polarity.
5. Connect local physical networks first.
6. Route control and measurement after the power path is stable.
7. Screenshot or inspect line points; reject remote trunks, boundary wraps, and
   accidental crossings through the plant.

Generic graph layout is useful for ordering large subsystems. It is not enough
for component-level Simscape Electrical circuits without node and lane rules.
