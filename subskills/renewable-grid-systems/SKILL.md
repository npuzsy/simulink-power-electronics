---
name: renewable-grid-systems
description: Use when working on Simulink or Simscape Electrical renewable and grid-connected power-electronics systems, including PV, wind, storage-coupled inverters, microgrids, MPPT, PLL, grid synchronization, and grid-code validation.
---

# Renewable And Grid Systems

## Status

Stub. Use this file only to recognize renewable/grid-system scope and choose evidence to collect. Apply the root workflow and any active converter subskill that matches the plant; grid-code and PLL checks are not yet fully specified here.

## Scope

- photovoltaic and wind power conversion systems
- storage-coupled inverters and hybrid plants
- microgrids and grid-forming/grid-following studies
- MPPT, PLL, synchronization, islanding, and ride-through behavior
- grid-code-oriented validation evidence

## Evidence To Collect

- source model, converter topology, grid model, control mode, and active synchronization path
- PLL, MPPT, DC-link, active/reactive power, current-limit, and protection signals
- grid disturbance, irradiance/wind/load step, islanding, or ride-through scenario
- validation windows and any grid-code clause or project requirement being checked

## Promote When

Promote only after adding references and checks for synchronization, power flow, grid disturbances, ride-through behavior, and representative renewable-source dynamics.
