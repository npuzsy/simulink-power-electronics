---
name: wireless-power-resonant
description: Use when working on Simulink or Simscape Electrical resonant converter or wireless power transfer models, including compensation networks, inductive links, frequency control, soft switching, and resonant-tank validation.
---

# Wireless Power And Resonant Converters

## Status

Stub. Use this file only to recognize resonant or wireless-power scope and choose evidence to collect. Apply the root workflow; this repository does not yet provide resonant-converter or wireless-power-specific checks.

## Scope

- resonant DC-DC converters
- inductive wireless power transfer systems
- compensation networks and coupled coils
- frequency-control and soft-switching behavior
- resonant-tank voltage/current validation

## Evidence To Collect

- resonant topology, compensation network, coupling model, switching frequency, and load condition
- tank voltage/current, device voltage/current, phase relationship, soft-switching, and output regulation signals
- frequency sweep, startup, load-step, or coupling-change scenario used for validation
- parasitic, initial-condition, and measurement-polarity assumptions

## Promote When

Promote only after adding representative resonant or wireless-power models, tank validation metrics, soft-switching checks, and repeatable simulation workflows.
