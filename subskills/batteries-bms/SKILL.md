---
name: batteries-bms
description: Use when working on Simulink or Simscape Electrical battery, charger, and BMS-linked power-electronics models, including pack behavior, balancing, SOC/SOH, bidirectional charging, protection, and storage converter interfaces.
---

# Batteries And BMS

## Status

Stub. Use this file only to recognize battery/BMS scope and choose evidence to collect. Apply the root workflow; do not infer battery, charger, or BMS rules from inverter diagnostics.

## Scope

- battery packs and charger power stages
- BMS-linked converter behavior
- cell balancing and protection events
- SOC/SOH-linked control behavior
- bidirectional charging and storage converter interfaces

## Evidence To Collect

- cell/pack model type, charger or converter topology, thermal coupling, and protection paths
- cell voltages/currents, pack voltage/current, SOC/SOH, temperature, balancing, and fault signals
- charge/discharge profile, current limit, balancing window, or protection trigger scenario
- sensor polarity, units, initial conditions, and estimation reset assumptions

## Promote When

Promote only after adding domain references and checks for cell voltage/current limits, balancing behavior, charger regulation, protection triggers, and thermal assumptions.
