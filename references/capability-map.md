# Capability Map

This skill provides four practical capabilities for Simulink and Simscape Electrical power-electronics work.

## Contents

- 1. Common PE Module Usage
- 2. PE Model Debugging
- 3. Supplement To Official Simulink Skills
- 4. Self-Iteration Mechanism
- Current Ability Boundary

## 1. Common PE Module Usage

Use the skill to identify and reason about common power-electronics modules:

- converter power stages: inverter, DC-DC converter, rectifier, chopper, multilevel converter
- electrical infrastructure: sources, loads, sensors, breakers, `powergui`, Solver Configuration, electrical references
- control blocks: PWM, SPWM, SVPWM, PLL, VSG, PI/feedforward loops, current controllers, speed/torque controllers, MPPT, balancing logic
- measurement blocks: voltage/current sensors, RMS/THD/power calculation, scopes, logged signals, buses

Module guidance must be grounded in inspected model paths. When the model uses a MathWorks library block, inspect block parameters and library references before inferring behavior from the display name.

## 2. PE Model Debugging

Use the skill to debug PE models by collecting evidence in this order:

1. model files, initialization scripts, data dictionaries, and required toolboxes
2. model role: top-level runnable model, library model, helper subsystem, test harness, or partial copied example
3. solver settings, stop time, sample times, `powergui` or Simscape Solver Configuration
4. active plant topology and commented/reference subsystems
5. controller inputs, outputs, buses, From/Goto tags, and variant choices
6. measurement polarity, signal units, logging points, scopes, and expected validation windows
7. simulation or update-diagram failures with exact diagnostics

Common edit targets:

- incorrect source table or lookup values
- wrong sign, phase sequence, unit scaling, or per-unit base
- line/phase voltage, Clarke/Park coefficient, or P/Q sign convention mismatch
- mismatched gate order between controller and plant
- missing initialization variables or data dictionary links
- wrong active variant or commented subsystem
- solver/sample-time mismatch or inappropriate discrete/continuous configuration
- library/helper model incorrectly treated as a runnable top-level system
- partial example copy missing initialization scripts, data dictionaries, local libraries, or referenced models

Do not call a waveform issue fixed until the relevant inputs, outputs, and plant-side signals have been logged or measured numerically.

## 3. Supplement To Simulink Skills

Simulink Agentic Toolkit or model-based-design skills own generic operations:

- model creation and structural edits
- parameter queries and variable resolution
- simulation execution
- Gherkin model tests
- requirements and model-based design artifacts

This skill adds the PE-specific layer:

- domain routing across PE applications
- topology/control-path inspection checklists
- gate, modulation, measurement, and waveform diagnostics
- control-algorithm signal tracing for selected PE controllers
- solver and sample-time pitfalls common in power electronics
- example-driven rules learned from official and public PE models

Lean boundary:

- keep generic Simulink mechanics in official skills
- keep domain-specific PE routing and evidence rules in this skill
- keep long topology notes in references or subskills, not the root `SKILL.md`
- do not promote example-specific findings unless they recur or are validated

## 4. Self-Iteration Mechanism

The self-iteration loop turns examples into skill improvements:

1. discover official and open-source examples
2. materialize selected examples under `data/pe-loop/`
3. analyze models in small MATLAB MCP batches
4. summarize recurring structures and failures
5. promote stable findings into references, subskills, or scripts
6. validate the skill repository after each promotion

Read `references/self-iteration-loop.md` before running the loop.

## Current Ability Boundary

Active, domain-specific capability:

- three-phase grid inverter SVPWM and gate/waveform diagnostics
- grid-inverter VSG/control-algorithm tracing, PI/feedforward checks, and
  P/Q coefficient consistency checks

Not included:

- OS-level schedulers, background jobs, or persistent automation orchestration
- general MATLAB scripting guidance unrelated to PE models
- generic Simulink build/test procedures already owned by Simulink skills
- claims of model validation when MATLAB MCP or required toolboxes are missing

Developing capability from current corpus:

- motor-drive topology and control-path inspection
- DC-DC converter regulation/ripple/debug evidence
- battery/BMS balancing and protection evidence
- renewable/grid system synchronization and power-flow evidence

Stub capability:

- HVDC/FACTS
- broader MMC/multilevel beyond the current three-level inverter notes
- wireless/resonant converters
