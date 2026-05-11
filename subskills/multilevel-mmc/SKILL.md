---
name: multilevel-mmc
description: Use when working on Simulink or Simscape Electrical multilevel converter models beyond the populated three-phase inverter notes, including MMC, cascaded H-bridge, flying-capacitor converters, capacitor balancing, and arm-energy control.
---

# Multilevel And MMC

## Status

Stub. Use this file only to recognize broader multilevel/MMC scope and choose evidence to collect. The active inverter subskill covers only its populated T-type/NPC three-level SVPWM notes.

## Scope

- modular multilevel converters
- cascaded H-bridge and flying-capacitor converters
- capacitor voltage balancing
- arm energy and circulating-current control
- multilevel modulation and switching-state validation beyond the existing three-level inverter table

## Evidence To Collect

- topology, submodule count, modulation path, balancing strategy, and arm/control hierarchy
- capacitor voltages, arm currents, circulating current, arm energy, and switching-state signals
- startup, balancing, step response, or disturbance window used for validation
- state encoding, bypass/insert assumptions, and measurement polarity

## Promote When

Promote only after adding representative MMC or broader multilevel workflows, validated modulation references, and checks for submodule states, balancing, and arm energy.
