---
name: hvdc-facts
description: Use when working on Simulink or Simscape Electrical HVDC and FACTS models, including VSC-HVDC, LCC-HVDC, STATCOM, SVC, UPFC, transmission-system controls, power-flow regulation, and grid disturbance studies.
---

# HVDC And FACTS

## Status

Stub. Use this file only to recognize HVDC/FACTS scope and choose evidence to collect. Apply the root workflow; this repository does not yet provide HVDC/FACTS-specific validation rules.

## Scope

- VSC-HVDC and LCC-HVDC systems
- STATCOM, SVC, UPFC, and related FACTS devices
- transmission-level power-flow and voltage regulation
- grid disturbance, protection, and recovery studies
- converter station control and measurement paths

## Evidence To Collect

- device type, converter station topology, network model, control mode, and operating point
- DC voltage/current, AC voltage/current, active/reactive power, firing/modulation, and protection signals
- disturbance, setpoint step, fault, or recovery scenario used for validation
- measurement bases, per-unit assumptions, and control-mode transitions

## Promote When

Promote only after adding transmission-system workflows, validation metrics, disturbance scenarios, and checks for converter station controls.
