---
name: rectifiers-active-front-ends
description: Use when working on Simulink or Simscape Electrical rectifier or active-front-end models, including diode and thyristor rectifiers, PWM rectifiers, PFC, DC-link regulation, line-current quality, and regeneration.
---

# Rectifiers And Active Front Ends

## Status

Stub. Use this file only to recognize rectifier/AFE scope and choose evidence to collect. Apply the root workflow; this is not yet a populated rectifier or PFC methodology.

## Scope

- diode, thyristor, and controlled rectifiers
- PWM rectifiers and active front ends
- PFC stages and line-current quality
- DC-link voltage regulation and regenerative power flow
- input filter and grid-side measurement validation

## Evidence To Collect

- input source, rectifier topology, firing/modulation path, DC-link target, and load/regeneration path
- line voltage/current, DC-link voltage/ripple, power factor, and protection signals
- firing angle, PWM duty/state, synchronization, and measurement polarity assumptions
- steady-state and transient windows used for current quality or DC-link validation

## Promote When

Promote only after adding rectifier/PFC references, representative validation windows, and checks for line current, power factor, DC-link ripple, and switching legality.
