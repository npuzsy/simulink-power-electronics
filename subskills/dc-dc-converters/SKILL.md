---
name: dc-dc-converters
description: Use when working on Simulink or Simscape Electrical DC-DC converter models, including buck, boost, buck-boost, flyback, forward, resonant, bidirectional converters, MPPT front ends, duty-cycle control, and regulation diagnostics.
---

# DC-DC Converters

## Status

Stub. Use this file only to recognize DC-DC converter scope and choose evidence to collect. Apply the root workflow; do not reuse inverter waveform-balance rules for regulation or ripple problems.

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

## Promote When

Promote only after adding representative topologies, control-loop validation standards, transient/load-step checks, and scripts or model tests for regulation and device stress.
