# Power Electronics Domain Map

Use this map to choose a subskill before loading detailed references or editing a model.

## Selection Rule

Classify by application domain first, then topology, then control method:

1. energy source or load: grid, machine, battery, PV, wind, generic load, transmission system
2. power stage: inverter, rectifier, DC-DC, multilevel converter, MMC, FACTS device
3. control objective: grid current, machine torque/speed, DC-link regulation, MPPT, balancing, protection
4. validation evidence: gates, currents, voltages, torque/speed, SOC, harmonics, power flow, protection events

If a domain-specific subskill is a stub, use it only as a scope marker and
evidence checklist. Developing subskills may contain corpus-derived inspection
rules, but still require model evidence before diagnosis or edits.

## Subskill Catalog

| Subskill | Status | Use for |
| --- | --- | --- |
| `subskills/three-phase-grid-inverter` | active | three-phase grid-connected inverters, T-type or NPC three-level bridges, SPWM/SVPWM, VSG/control tracing, gate routing, grid voltage/current waveform balance |
| `subskills/motor-drives` | developing | PMSM, BLDC, induction motor, FOC, DTC, torque/speed/current loops, inverter-fed machine drives |
| `subskills/dc-dc-converters` | developing | buck, boost, buck-boost, flyback, forward, resonant, bidirectional DC-DC, MPPT front ends, generated schematic layout |
| `subskills/rectifiers-active-front-ends` | stub | diode/thyristor rectifiers, PWM rectifiers, active front ends, PFC, DC-link regulation |
| `subskills/renewable-grid-systems` | stub | PV, wind, storage-coupled grid systems, microgrids, PLL/grid synchronization, grid-code validation |
| `subskills/batteries-bms` | stub | battery packs, BMS, balancing circuits, chargers, SOC/SOH-linked power-electronics behavior |
| `subskills/hvdc-facts` | stub | HVDC, STATCOM, SVC, UPFC, transmission-system power-electronics controls |
| `subskills/multilevel-mmc` | stub | MMC, flying capacitor, cascaded H-bridge, neutral-point or capacitor balancing beyond the active inverter scope |
| `subskills/wireless-power-resonant` | stub | resonant converters, inductive wireless power transfer, compensation networks |

## Stub Policy

A stub subskill may contain:

- intended scope
- evidence to collect
- explicit non-goals
- source links to investigate later

A stub subskill must not contain:

- unverified design rules
- copy-pasted guidance from the active inverter subskill
- scripts that claim validation without representative models

Promote a stub to active only after adding domain references, at least one realistic model workflow, and verification scripts or repeatable checks.

## Developing Policy

A developing subskill may contain repeated findings from example analysis and
layout/debug heuristics. Treat those as evidence collection rules, not final
simulation-backed design rules. Promote to active only after adding repeatable
checks or representative validation workflows.
