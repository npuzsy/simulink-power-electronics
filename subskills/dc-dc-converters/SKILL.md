---
name: dc-dc-converters
description: Use when working on Simulink or Simscape Electrical DC-DC converter models, including buck, boost, buck-boost, flyback, forward, resonant, bidirectional converters, MPPT front ends, duty-cycle control, and regulation diagnostics.
---

# DC-DC Converters

## Status

Developing stub. Use this file to recognize DC-DC converter scope and choose evidence to collect. Apply the root workflow; do not reuse inverter waveform-balance rules for regulation or ripple problems.

Read `references/inspection.md` for corpus-derived inspection notes before diagnosing DC-DC examples. Treat those notes as developing guidance, not a complete methodology.

For generated or repaired Simscape Electrical schematics, also read
`../../references/simscape-layout.md`. DC-DC converters are sensitive to
schematic readability because the return node, switch node, and output node are
high-degree physical networks that generic automatic layout often routes poorly.

## Scope

- buck, boost, buck-boost, flyback, forward, and isolated DC-DC converters
- resonant and soft-switching DC-DC converters
- bidirectional converters for batteries, storage, and DC buses
- duty-cycle, current-mode, voltage-mode, and MPPT-linked control paths

## Evidence To Collect

- topology, operating mode, switching frequency, input/output voltage, load, and duty range
- inductor current, capacitor voltage, switch stress, and controller saturation signals
- startup, load-step, line-step, or MPPT transient window used for validation
- continuous/discontinuous conduction assumptions and sensor polarity
- visual node map for generated component-level models: input positive,
  switching node, output positive, and return rail

## Generated Layout Workflow

When asked to generate or clean up a DC-DC Simscape model:

1. Select the visual family:
   - simple converter pipeline for buck/boost/buck-boost/SEPIC/Cuk
   - bridge/symmetric layout for full-bridge or bidirectional converters
   - resonant pipeline for LLC/series/parallel resonant converters
   - subsystem-level converter block when the purpose is control/regulation
2. Name the electrical nodes before drawing:
   - `VIN_POS`
   - `SW` or commutation midpoint
   - `VOUT_POS`
   - `RETURN`
3. Place the physical power stage before control or scopes:
   - source on the left
   - switching device and freewheel path in the middle-left
   - energy storage/output filter in the middle-right
   - load on the right
   - return rail as a bottom local rail
4. Place PWM/control below or above the switch, and place measurement/scopes at
   the measured node or at the right edge.
5. Reject layouts where the return/common node routes to a remote canvas edge or
   wraps around unrelated blocks.

## Current Corpus-Derived Boundary

The current corpus contains many DC-DC library/helper candidates and fewer compiled runnable examples than motor drives. Use this subskill confidently for classification and evidence planning, but require a `compiled`, `simulated`, or `measured` state before promoting regulation/ripple rules.

For copied or downloaded DC-DC examples, prefer whole example folders or dependency closures. A single `.slx` often opens but does not provide enough initialization context for simulation-backed conclusions.

## Promote When

Promote only after adding representative topologies, control-loop validation standards, transient/load-step checks, and scripts or model tests for regulation and device stress.
