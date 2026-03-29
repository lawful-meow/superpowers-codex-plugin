# Superpowers Codex Plugin

Superpowers Codex Plugin packages [obra/superpowers](https://github.com/obra/superpowers) `v5.0.6` for Codex.

The repository separates Codex integration into two layers:

- a marketplace plugin for the Superpowers bundle under `~/plugins/superpowers`
- a home-wide Codex hooks setup under `~/.codex/hooks.json`

This matches the current Codex model: plugin assets are installed through the plugin marketplace, while hooks are configured through Codex config files.

## Install

Managed install:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/lawful-meow/superpowers-codex-plugin/refs/heads/main/scripts/install.sh)
```

Codex prompt install:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/lawful-meow/superpowers-codex-plugin/refs/heads/main/.codex/INSTALL.md
```

After the installer finishes, restart Codex. The installer writes the marketplace entry, enables the plugin in `~/.codex/config.toml`, and configures the home-wide hooks.

Full install and verification steps are documented in [`.codex/INSTALL.md`](./.codex/INSTALL.md).

## What the Installer Configures

The managed installer:

- clones or updates this repository under `~/.codex/superpowers-codex-plugin`
- copies the plugin bundle to `~/plugins/superpowers`
- merges a `superpowers` plugin entry into `~/.agents/plugins/marketplace.json`
- marks the home marketplace entry as `INSTALLED_BY_DEFAULT`
- ensures `multi_agent = true` and `codex_hooks = true` in `~/.codex/config.toml`
- enables `superpowers@<marketplace-name>` in `~/.codex/config.toml`
- merges Superpowers handlers into `~/.codex/hooks.json`

The plugin bundle itself includes the upstream:

- `skills/`
- `agents/`
- `commands/`
- `hooks/`

The Codex hook runtime is installed from `plugins/superpowers/hooks/`, but it is activated through `~/.codex/hooks.json` rather than through the plugin manifest.

## Verify

Plugin install:

- Restart Codex after running the installer.
- Open the Plugins marketplace and confirm `Superpowers` is already enabled in your personal marketplace.

Skill activation:

- Start a new session and ask:
  `Help me plan this feature before writing code.`
- Codex should shift into a planning-first workflow instead of going straight to implementation.

Hook activation:

- Create the debug marker:
  ```bash
  touch ~/.codex/superpowers-hooks-debug
  ```
- Restart Codex.
- Start a new session, submit a prompt, and run at least one Bash command through Codex.
- Inspect the hook log:
  ```bash
  cat ~/.codex/logs/superpowers-hooks.log
  ```
- Remove the marker to disable debug output:
  ```bash
  rm ~/.codex/superpowers-hooks-debug
  ```

Codex hooks are experimental, require `codex_hooks = true`, and are currently disabled on Windows.

## Repository Layout

- [`plugins/superpowers/.codex-plugin/plugin.json`](./plugins/superpowers/.codex-plugin/plugin.json)
  Marketplace-installed Codex plugin manifest.
- [`scripts/install.py`](./scripts/install.py)
  Managed installer that updates `~/plugins`, `~/.agents`, and `~/.codex`.
- [`scripts/install.sh`](./scripts/install.sh)
  One-command bootstrap for remote installation.
- [`plugins/superpowers/hooks/codex-hook.py`](./plugins/superpowers/hooks/codex-hook.py)
  Codex hook handler for `SessionStart`, `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, and `Stop`.
- [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
  Repo-local marketplace entry for local development and testing.

## Updating

When a new upstream Superpowers release is adopted:

1. Refresh `plugins/superpowers/skills/`, `plugins/superpowers/agents/`, `plugins/superpowers/commands/`, and `plugins/superpowers/hooks/` from upstream.
2. Keep Codex-specific files aligned with the new snapshot:
   - `plugins/superpowers/.codex-plugin/plugin.json`
   - `plugins/superpowers/hooks/codex-hook.py`
   - `scripts/install.py`
   - `.codex/INSTALL.md`
   - `README.md`
3. Re-run the installer or reinstall into a temp home directory to verify marketplace, config, and hook merges.

## Provenance

- upstream repository: <https://github.com/obra/superpowers>
- upstream release packaged here: `v5.0.6`
- packaged repository: <https://github.com/lawful-meow/superpowers-codex-plugin>
