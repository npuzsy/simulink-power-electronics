# Model Standards

Use this reference before editing Simulink or Simscape Electrical power-electronics models.

## Inspection Standard

Before editing:

- Identify the main model and any referenced models or libraries.
- Classify each `.slx` or `.mdl` as top-level runnable model, library block diagram, helper subsystem, test harness, generated artifact, or copied partial example.
- Inspect active and intentionally disabled control paths.
- Confirm solver settings, sample times, fundamental frequency, switching period, and DC-link value.
- Identify plant measurements used for validation.
- Note generated artifacts such as `slprj/`, cache files, and autosave files.

## Control Path Standard

For inverter/converter models, document:

- topology: two-level, T-type, NPC, flying capacitor, modular multilevel, rectifier, DC-DC converter
- modulation: SPWM, SVPWM, DPWM, hysteresis, model predictive control, or custom
- gate output ordering
- active reference frame and phase sequence
- expected output measurement names

## From/Goto And Commented Subsystems

From/Goto routing is common in Simulink power electronics models, but it is easy to misread.

- Do not treat a missing or ambiguous From/Goto as a bug until commented subsystems are checked.
- If duplicate global tags exist in reference and active controller paths, verify actual plant gate signals by logging root From outputs.
- Do not comment internal Goto blocks inside a subsystem when the parent subsystem is intentionally commented unless there is a specific reason.

## Simscape Electrical Plant Safety

When inspecting or modifying a power stage:

- Confirm every switch has legal gate states.
- Check for shoot-through conditions in each bridge leg.
- Check neutral-point or DC-link capacitor balancing assumptions.
- Confirm voltage/current sensor polarity before interpreting waveforms.
- Treat unexplained solver failures as model-configuration or discontinuity clues, not just numerical noise.

## Simscape Electrical Layout Safety

When generating or repairing component-level Simscape Electrical schematics,
read `references/layout-patterns-from-examples.md` and
`references/simscape-layout.md` before relying on automatic layout.

- Classify electrical nodes before placing blocks. For DC-DC converters this
  normally includes input positive, switching node, output positive, and return.
- Place high-degree common nodes as explicit local rails, especially return,
  neutral, DC-link midpoint, and ground/reference nodes.
- Choose block orientation from port positions and polarity, not only from graph
  coordinates.
- Keep control/measurement signal routing separate from the main physical power
  loop.
- Do not treat a visually tangled but electrically connected circuit as a
  satisfactory generated model unless the user explicitly only asked for
  topology, not schematic readability.

## Generated Artifacts

The following are normally generated and should not be treated as source unless the user asks:

- `slprj/`
- `*.slxc`
- autosave files
- simulation cache files

Do not delete or revert them without explicit intent.

## Library And Partial Example Models

Many official power-electronics examples include library block diagrams or helper models. These can be opened and inspected, but update diagram or simulation may be invalid because they are not top-level runnable systems.

- Use library models to learn module interfaces, masks, parameters, and internal implementation patterns.
- Do not use library models to infer waveform behavior or solver requirements.
- If a copied model fails but the original installed model compiles, treat the copied model as a partial example with missing dependencies.
- For simulation-backed conclusions, prefer the original full example folder or a copied dependency closure that includes initialization scripts, data dictionaries, `.mat` files, referenced models, and local libraries.
