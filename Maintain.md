# RoboticNavigation Maintenance Guide

This file is the mandatory maintenance guide for future Codex runs on this repository.

When the user provides:
- the path to new `demo` materials,
- the path to new experiment handout / guide documents,
- and says the maintenance guide is `Maintain.md`,

Codex must read and follow this file before making changes.

## 1. Project Purpose

This repository is a ROS1 navigation lab project for a real robot platform.

Current goals:
- maintain a reusable `src/` catkin workspace structure,
- keep later experiments building on earlier experiments,
- prefer real-robot workflows over simulation unless the user explicitly asks for simulation,
- preserve the naming logic required by the handout,
- keep the project maintainable for repeated future extensions.

Current project authorship metadata:
- group: `group12`
- members: `Zixuan Jiang`, `Yiqin Wang`, `Jinsong Sun`
- project time: `2026`

## 2. Non-Negotiable Rules

Codex must do all of the following every time:

1. Read the new handout materials first.
2. Read the new demo materials second.
3. Identify exactly which part of the handout is required:
   real robot only, simulation only, or both.
4. Reuse the existing `src/` structure unless there is a strong technical reason not to.
5. Preserve all handout-required launch names, package names, topic names, and file names whenever they are explicitly specified by the handout.
6. Prefer extending the existing architecture over adding ad hoc one-off files.
7. Keep parameters in `config/` when possible instead of hardcoding everything inside launch files.
8. Avoid destructive changes to earlier experiments unless the earlier implementation is clearly broken or conflicts with the new experiment.
9. Update documentation when behavior, launch flows, or editable parameters change.
10. Leave the repository in a state that is understandable for the next Codex run.

## 3. Repository Baseline

Codex must assume the repository has these roles:

- `src/`
  The catkin workspace source directory and the main long-term deliverable.

- `src/ebot_bringup`
  Unified real-robot integration layer.
  New experiments should usually extend this package first.

- `src/ebot_base`
  Base driver related packages.

- `src/ebot_sensors`
  Sensor driver related packages.

- `src/ebot_navigation`
  Navigation, localization, mapping, and related algorithm packages.

- `src/robot_sim`
  Gazebo simulation package used by experiments 3-5.

- `src/vehicle_sim`
  Lightweight RViz simulation package used by experiment 2.

- `docs/`
  Experiment handouts and reference PDFs.

- `demo/`
  Teacher-provided demo materials.

- `tools/`
  Board-side utility scripts and operational helper tools.

- `group12_navigation_functions.html`
  Human-readable function and file-role explanation document.

If future work needs another package or folder, Codex must place it in a structure consistent with the above layering.

## 4. Mandatory First-Step Workflow

At the start of every maintenance task, Codex must do this in order:

1. Locate the new handout files and demo files provided by the user.
2. Inspect the current repository tree.
3. Extract the handout requirements.
4. Determine:
   - which experiment number is being added or updated,
   - which files from old experiments are meant to be reused,
   - which new nodes, launch files, configs, maps, scripts, or docs are required,
   - whether the task is real robot only or includes simulation.
5. Compare the new handout naming requirements against the current repository naming.
6. Detect conflicts before editing:
   - TF frame conflicts,
   - topic name conflicts,
   - duplicate launch responsibilities,
   - overlapping odometry publishers,
   - conflicting static transforms,
   - duplicate package names,
   - hardware serial path assumptions.

Codex must not start editing before finishing the above analysis.

## 5. Required Design Strategy For New Experiments

When a new experiment arrives, Codex must prefer this strategy:

1. Reuse existing packages where possible.
2. Extend `ebot_bringup` for new launch entrypoints and shared configuration.
3. Add new configuration files under `src/ebot_bringup/config/`.
4. Add new operational or verification scripts under `tools/` if the experiment introduces repeated manual setup or board-side checks.
5. Add new maps under `src/ebot_bringup/maps/` if the handout requires stored maps.
6. Only add a brand-new package when the new experiment introduces a genuinely new ROS package responsibility that does not belong in an existing package.

Codex must explicitly avoid:
- scattering launch files across unrelated packages without reason,
- duplicating the same parameter values in many launch files,
- hardcoding board-specific values in many places,
- mixing simulation-only logic into the real-robot path unless required,
- silently renaming handout-specified files.

## 6. Real-Robot Priority Rules

Unless the user explicitly says otherwise, Codex must treat the handout's real-robot part as higher priority than the simulation part.

This means:
- if the handout contains both simulation and real-robot steps, implement the real-robot path first,
- do not spend time on Gazebo or RViz simulation launch flows unless the user asks for them,
- ensure serial devices, TF relationships, localization chains, and operational scripts are treated as first-class concerns.

## 7. Naming Rules

Codex must follow these naming rules:

1. If the handout explicitly gives a file name, keep that exact file name.
2. If the handout explicitly gives a launch name, keep that exact launch name.
3. If the handout gives a topic or frame name requirement, preserve it unless there is a hard conflict.
4. If a conflict exists, keep the handout-facing interface unchanged and resolve the conflict internally where possible.
5. If Codex introduces a new helper file not named by the handout, use clear descriptive names and keep them consistent with the existing repository style.

Examples:
- `bringup.launch`
- `my_lidar.launch`
- `slam_hector.launch`
- `nav01_amcl.launch`
- `nav01_rf2o.launch`
- `test_amcl.launch`

## 8. TF And Topic Safety Checklist

Before finishing a maintenance task, Codex must verify that it has thought through all of these:

1. Who publishes `map -> odom`?
2. Who publishes `odom -> base_footprint`?
3. Who publishes `base_footprint -> base_link`?
4. Who publishes `base_link -> laser_link` or equivalent sensor frame?
5. Is any transform being published twice?
6. Is any odometry topic published by more than one active node?
7. Are there hidden conflicts between wheel odometry, RF2O, Hector, AMCL, or later navigation nodes?
8. Are frame names consistent with the handout and the actual robot?
9. Are scan topics and map topics consistent across launch files?

If the new experiment changes TF ownership, Codex must document that change clearly.

## 9. Parameter Management Rules

Codex must keep editable runtime parameters centralized.

Required behavior:
- put sensor parameters in `config/lidar/` or another relevant config folder,
- put mapping parameters in `config/slam/`,
- put localization parameters in `config/localization/`,
- put future planning or navigation stack parameters in a similarly named config area,
- keep launch files focused on wiring and composition,
- avoid baking frequently changed hardware settings into source code.

When board-specific values exist, Codex must identify them clearly.

Typical board-specific values include:
- serial port paths,
- baud rates,
- lidar model flags,
- static TF mounting offsets,
- map file paths,
- network addresses,
- camera or sensor calibration values.

## 10. Demo Intake Rules

When new teacher demo materials are provided, Codex must not blindly copy everything into `src/`.

Instead Codex must:

1. Identify which demo files are actually relevant to the required handout section.
2. Separate:
   - third-party packages,
   - teacher-provided package templates,
   - one-off demo launch files,
   - simulation-only content,
   - real-robot content.
3. Only import the minimum required subset.
4. Patch imported code only where needed for:
   - correctness,
   - buildability,
   - maintainability,
   - integration with the existing repository structure.
5. Preserve provenance mentally:
   imported code should remain understandable and should not be arbitrarily rewritten.

## 11. Required Documentation Updates

Whenever Codex changes project behavior, Codex must update documentation accordingly.

At minimum, check whether the following need updates:

1. `group12_navigation_functions.html`
   Update when new functions, packages, or launch roles become important to users.

2. `tools/`
   Add or update scripts when new experiments introduce repeated manual checks.

3. This `Maintain.md`
   Update when the maintenance workflow itself changes, or when new recurring repository conventions become necessary.

Codex should also consider adding a short README in new package directories if they become operationally important.

## 12. Required Validation Steps

Before claiming a maintenance task is complete, Codex must validate as much as the environment allows.

Minimum required validation:

1. Syntax-check new shell scripts.
2. Parse XML launch files and package manifests if possible.
3. Parse YAML config files if possible.
4. Check for obvious path mistakes in launch files.
5. Check that the package structure is coherent.

If a ROS environment is available, Codex should also try:
- `catkin_make`
- selective package build checks
- launch-file sanity review

If a ROS environment is not available, Codex must say so explicitly and must not pretend the build was verified.

## 13. Deliverable Requirements For Each Maintenance Run

At the end of a maintenance run, Codex should leave:

1. Updated source files in `src/`.
2. Updated launch/config integration if required.
3. Updated operational tools if required.
4. Updated documentation if required.
5. A concise summary of:
   - what changed,
   - what still needs board-side verification,
   - which parameters the user is most likely to adjust manually.

## 14. Board-Side Reality Check Rules

For real-robot experiments, Codex must assume some values cannot be finalized offline.

These often require on-board confirmation:
- actual serial device path,
- actual lidar mounting direction,
- actual lidar model communication parameters,
- actual map quality,
- actual RF2O / AMCL tuning quality,
- actual network IP for SSH access.

Codex should design the repository so these values are easy for the user to inspect and change.

## 15. When To Edit Existing Files vs Add New Files

Codex should edit existing files when:
- the handout extends a current workflow,
- a parameter belongs to an existing config domain,
- a launch entrypoint is a versioned continuation of an earlier experiment,
- a bug in existing integration would break the new experiment.

Codex should add new files when:
- the handout explicitly requires new named artifacts,
- a new experiment introduces a distinct launch entrypoint,
- a new config group is needed,
- a new operational helper script would reduce repeated manual work,
- documentation would otherwise become unclear.

## 16. Mandatory Final Self-Check

Before finishing, Codex must ask itself:

1. Did I read the new handout and demo first?
2. Did I keep handout naming intact?
3. Did I preserve the reusable `src/` architecture?
4. Did I avoid simulation work unless requested?
5. Did I avoid TF and topic conflicts?
6. Did I centralize editable parameters?
7. Did I update docs and tools if the workflow changed?
8. Did I clearly separate verified facts from board-side assumptions?

If any answer is no, Codex should keep working before concluding.

## 17. Short Instruction For Future Codex Runs

If the user says:
- here is the new demo path,
- here is the new handout path,
- the maintenance guide is `Maintain.md`,

then Codex must:
- read `Maintain.md`,
- inspect the provided materials,
- identify the required real task scope,
- extend the current repository instead of starting over,
- keep the project maintainable for the next experiment.

When simulation support is requested, Codex should keep the real-robot
default launch path unchanged and add simulation via explicit
`mode:=sim` style switches where possible.
