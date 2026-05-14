# Power-Electronics Skill Self-Iteration Loop

Use this loop to evolve the skill from real Simulink and Simscape Electrical examples.

## Boundary

- External folders may be read as source material.
- Do not write, delete, or modify files outside this skill repository.
- Put downloaded repositories, temporary files, manifests, logs, and analysis outputs under `data/pe-loop/`.
- Treat MATLAB installation examples as read-only seeds unless they have been copied into `data/pe-loop/`.

## Loop Stages

1. Discover candidate `.slx`, `.mdl`, `.m`, `.mlx`, and `.sldd` files from official installed examples and public repositories.
2. Record every candidate in `data/pe-loop/manifests/examples.jsonl` with source, path, domain guess, and evidence keywords.
3. Copy or download only the examples selected for active analysis into `data/pe-loop/downloads/`.
   - Prefer whole example/project folders when available.
   - Copying a single `.slx` is enough for block-usage analysis, but often not enough for update diagram or simulation because initialization scripts, data files, dictionaries, and referenced libraries may be missing.
4. Analyze models in small batches using MATLAB MCP tools serially.
   - Use `scripts/pe_loop_select_batches.py --runnable-only` for simulation-backed batches.
   - Use library/helper models for module-interface learning, not waveform conclusions.
5. Extract common patterns:
   - module and library usage
   - plant topology
   - control topology
   - solver and `powergui` configuration
   - measurement/logging points
   - common failure/debug locations
   - domain-specific validation signals
6. Promote only stable findings into `references/`, `subskills/`, or scripts.
7. Validate repository structure and script behavior before ending a loop.

## Manifest Fields

Each manifest row should include:

- `id`
- `source_kind`: `installed`, `github`, `downloaded`, or `manual`
- `source`
- `path`
- `file_type`
- `domain`
- `score`
- `keywords`
- `status`: `candidate`, `copied`, `downloaded`, `analyzed`, `failed`, or `promoted`
- `notes`

## Domain Mapping

Classify to the existing subskills:

- `three-phase-grid-inverter`
- `motor-drives`
- `dc-dc-converters`
- `rectifiers-active-front-ends`
- `renewable-grid-systems`
- `batteries-bms`
- `hvdc-facts`
- `multilevel-mmc`
- `wireless-power-resonant`

Use `general-power-electronics` only when a model is clearly relevant but not yet specific enough.

## Analysis Record

For each analyzed model, write one JSON file under `data/pe-loop/analysis/models/`:

- model name and source
- opened/compiled status
- block hierarchy summary
- top-level interfaces
- detected libraries and block types
- solver and stop-time parameters
- domain evidence
- reusable skill findings
- errors and missing toolboxes
- missing initialization scripts, data files, dictionaries, libraries, or referenced models

## Promotion Rule

Do not turn one example into a general rule. Promote a finding when at least one of these is true:

- it appears in three or more independent examples in one domain
- it is official MathWorks guidance visible in official examples
- it prevents a repeated tool failure or unsafe debugging action
- it is a deterministic script/check that can be validated
