---
name: dc-dc-converters
description: Use when working on Simulink or Simscape Electrical DC-DC converter models, including buck, boost, buck-boost, flyback, forward, resonant, bidirectional converters, MPPT front ends, duty-cycle control, and regulation diagnostics.
---

# DC-DC Converters

## Status

Stub. Use the root `simulink-power-electronics` workflow for now. Do not reuse inverter waveform-balance rules for DC-DC regulation problems.

## Intended Scope

- buck, boost, buck-boost, flyback, forward, and isolated DC-DC converters
- resonant and soft-switching DC-DC converters
- bidirectional converters for batteries, storage, and DC buses
- duty-cycle, current-mode, voltage-mode, and MPPT-linked control paths

## Not Yet Provided

- topology-specific inspection standards
- inductor/capacitor ripple validation
- duty-cycle and saturation checks
- control-loop and load-step diagnostics
- reusable MATLAB diagnostics

## Promotion Criteria

Promote this stub to active only after adding representative topologies, control-loop validation standards, transient/load-step checks, and scripts or model tests that verify regulation and device stress.
