# Three-Level SVPWM Standards

Use this reference for T-type or NPC three-level SVPWM control paths.

## Pipeline

A conventional three-level SVPWM path is:

`Ua/Ub/Uc -> alpha-beta -> large sector N -> small sector n -> time calculation -> time logic -> seven-segment time distribution -> state vector -> gate pulses`

The actual model may use different block names. Map by behavior, not display text.

## State Encoding

Common state-vector encoding:

- `0 = N`
- `1 = O`
- `2 = P`

If a Multiport Switch uses one-based indexes, add 1 or explicitly map values.

## T-Type Gate Mapping

For the improved T-type three-level switching pattern:

- `N -> [0 0 1 1]`
- `O -> [0 1 1 0]`
- `P -> [1 1 0 0]`

Use this mapping only after confirming the model's physical switch order. Many models use the output order:

`[SA1 SA2 SA3 SA4 SB1 SB2 SB3 SB4 SC1 SC2 SC3 SC4]`

If the bridge has a different switch naming convention, derive the mapping from the plant.

## State-Vector Table Standard

For the 36-small-sector, seven-segment scheme, every large sector must have its own vector sequence. A common defect is copying sector I into sectors III to VI, which compiles but produces biased phase voltages.

Read `table7-state-vectors.md` for the complete table.

## Validation Signals

Log these behavior classes, using the actual block names in the target model:

- large sector `N`
- small sector `n`
- seven-segment selector
- three-phase state vector `[Sa Sb Sc]`
- final gate vector
- root plant gate inputs
- three phase voltages or currents

## Healthy Pattern

In a balanced three-phase inverter after startup transient:

- large sector `N` visits 1 to 6 uniformly over one fundamental cycle
- per-phase state counts are symmetric over one fundamental cycle
- per-leg gate rows are legal switch states only
- phase RMS values are balanced
- line RMS values are balanced
- the sum of three phase-to-neutral voltages is near zero when measured with a consistent neutral reference

## Common Failure Modes

- wrong alpha-beta phase sequence or sign convention
- state encoding shifted by one before Multiport Switch indexing
- incomplete or copied state-vector tables
- gate output order mismatched to plant switch order
- duplicate global Goto tags causing misleading signal-source assumptions
- interpreting startup transient as steady-state behavior
