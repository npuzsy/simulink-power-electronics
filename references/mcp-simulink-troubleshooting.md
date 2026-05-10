# MCP and Simulink Troubleshooting

Use this reference when MATLAB MCP, Simulink Agentic Toolkit, or agent tool discovery fails before model analysis can begin.

Sources reviewed on 2026-05-10:

- Official Simulink skills repository: https://github.com/simulink/skills
- MATLAB MCP Core Server README: https://github.com/matlab/matlab-mcp-core-server
- Simulink Agentic Toolkit README and Getting Started guide: https://github.com/matlab/simulink-agentic-toolkit
- MathWorks Simulink Agentic Toolkit page: https://www.mathworks.com/products/simulink-agentic-toolkit.html
- Public GitHub issues in `matlab/matlab-mcp-core-server` and `matlab/simulink-agentic-toolkit`

## First Checks

1. Confirm MATLAB and Simulink are installed and match the toolkit requirements.
   - Simulink Agentic Toolkit expects MATLAB R2023a or later with Simulink.
   - `model_test` additionally requires Simulink Test.
2. Confirm the setup add-on is installed:
   ```matlab
   which setupAgenticToolkit -all
   ```
3. Confirm MATLAB-side MCP components are installed:
   ```matlab
   which shareMATLABSession -all
   ```
4. Initialize every MATLAB session that should be shared with the agent:
   ```matlab
   addpath("~/.matlab/agentic-toolkits/simulink")
   satk_initialize
   ```
5. Restart the coding agent or reload the IDE after `satk_initialize`.

## Common Setup Problems

### `setupAgenticToolkit` is not recognized

Likely cause: the setup toolbox was not installed, was installed in another MATLAB release, or MATLAB has not refreshed its path.

Fix:

```matlab
matlab.addons.toolbox.installToolbox("agenticToolkitInstaller.mltbx")
which setupAgenticToolkit -all
setupAgenticToolkit("install")
```

Use the real downloaded `.mltbx` path, not a placeholder path.

### Add-On Manager fails to open the installer

Likely cause: headless MATLAB, corporate proxy, antivirus, certificate interception, or CEF/display issues.

Fix: install programmatically:

```matlab
matlab.addons.toolbox.installToolbox("agenticToolkitInstaller.mltbx")
```

### `shareMATLABSession` is not found

Likely cause: the MATLAB MCP Core Server Toolbox was not installed into this MATLAB release, or MATLAB was not restarted after setup.

Fix:

```bash
~/.matlab/agentic-toolkits/bin/matlab-mcp-core-server --setup-matlab --matlab-root=/path/to/MATLAB/R20XXx
```

Then restart MATLAB and run:

```matlab
which shareMATLABSession -all
satk_initialize
```

On Windows, use the corresponding `.exe` path under `%USERPROFILE%\.matlab\agentic-toolkits\bin\`.

### `satk_initialize` passes, but the agent cannot see Simulink tools

Symptoms: MATLAB reports PASS, but the agent says `model_overview`, `model_read`, or `model_edit` are unavailable.

Likely causes:

- The agent session started before MATLAB was shared.
- The host IDE has not reloaded its MCP configuration.
- Skills or MCP entries were configured for a different agent or scope.

Fix:

1. Run `satk_initialize` in MATLAB.
2. Restart the agent session.
3. For VS Code based agents, reload the VS Code window.
4. Re-run `setupAgenticToolkit("configure")` if skills or MCP entries are missing.

### Codex tool calls time out during simulations

Likely cause: default MCP tool timeout is too short for MATLAB startup, model compilation, or long simulations.

Fix: increase the timeout in the Codex MCP server config, for example:

```toml
[mcp_servers.matlab]
tool_timeout_sec = 600
```

Use a larger value for long model tests or full converter simulations.

### Simulink fails in Codex on Windows

Likely cause: Codex may strip environment variables from MCP subprocesses, and Simulink expects Windows environment context.

Fix:

```toml
[mcp_servers.matlab]
env_vars = ["WINDIR"]
```

### macOS blocks the MCP binary

Likely cause: Gatekeeper quarantine on a downloaded executable.

Fix:

```bash
xattr -d com.apple.quarantine ~/.matlab/agentic-toolkits/bin/matlab-mcp-core-server
```

### Windows Claude Desktop reports watchdog socket access denied

Symptoms include `Failed to connect to watchdog socket` or `access denied for socket file`.

Observed public reports point to Windows MSIX sandbox behavior and temporary-directory socket handling. Directly launching the binary from a normal command prompt may work while Claude Desktop fails.

Mitigations:

- Prefer an agent host verified by the current toolkit release.
- Configure a long-form log folder outside the problematic temp path:
  ```json
  "--log-folder=C:/McpLogs"
  ```
- Update the MATLAB MCP Core Server and Simulink Agentic Toolkit to the latest release.

### `shareMATLABSession` fails on Windows with file attribute or ACL errors

Symptoms include warnings about failing to get file attributes under `AppData\Roaming\MathWorks\MATLAB MCP Core Server`.

Mitigations:

- Update the MATLAB MCP Core Server and MATLAB-side toolbox.
- Re-run `--setup-matlab` for the exact MATLAB root.
- Restart MATLAB.
- If the issue persists, capture the full `satk_initialize` output and file a bug report against the upstream MCP server.

### MCP attaches to the wrong MATLAB session

Likely cause: in existing-session mode, the server attaches to the most recently shared MATLAB session. With multiple MATLAB windows and multiple worktrees, the last `shareMATLABSession` call can win.

Mitigations:

- Keep one shared MATLAB session per agent while doing model edits.
- Before tool calls, verify `pwd`, `bdroot`, and the open model in MATLAB.
- Re-run `satk_initialize` in the intended MATLAB session, then restart the agent.
- Avoid running parallel agents against different MATLAB sessions unless you have a deliberate session-pinning workflow.

### MCP call enters MATLAB debug mode and becomes stuck

Observed public reports mention `dbstop if error` leaving MCP-driven calls stuck in the debugger.

Mitigations:

```matlab
dbclear if error
dbclear if warning
```

Avoid enabling break-on-error during long unattended MCP runs. If MATLAB is already stuck in debug mode and the MCP call cannot return, manual intervention or process restart may be required.

## Lessons From Power-Electronics Model Work

These are reusable lessons from building and validating this skill.

- Do not rely on Scope screenshots alone. Log controller internals, final gate vectors, plant-side gate inputs, and measured voltages/currents.
- A commented parent subsystem can explain missing From/Goto pairs. Do not comment internal Goto blocks just because the parent path is disabled.
- Duplicate global Goto tags are a routing risk. Verify actual plant inputs by logging the root From outputs.
- Treat startup transients separately from steady state. Use at least one final fundamental cycle for RMS and balance checks.
- For three-level SVPWM, incomplete large-sector tables can compile and still produce strongly biased phase voltages. Check all 36 small sectors, not only sector I.
- Avoid hardcoding private model names, block display names, or local paths in reusable scripts.
- Diagnostic scripts should validate signal dimensions and report missing logged signals explicitly; silent empty logs are worse than hard failures.
- Keep generated artifacts such as `slprj/` and `*.slxc` out of conceptual reviews unless the task specifically concerns generated files.
