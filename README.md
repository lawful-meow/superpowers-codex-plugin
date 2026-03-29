# Superpowers Codex Plugin

Superpowers Codex Plugin packages [obra/superpowers](https://github.com/obra/superpowers) `v5.0.6` as a Codex plugin bundle.

The repository adapts the upstream Superpowers runtime surfaces into a Codex plugin layout while preserving upstream provenance and release alignment.

## Overview

The bundle includes the upstream:

- `skills/`
- `agents/`
- `commands/`
- `hooks/`

The Codex-facing structure is:

- `.agents/plugins/marketplace.json`
- `plugins/superpowers/.codex-plugin/plugin.json`
- `plugins/superpowers/skills/`
- `plugins/superpowers/agents/`
- `plugins/superpowers/commands/`
- `plugins/superpowers/hooks/`
- `plugins/superpowers/hooks.json`

## Installation

Codex installation is exposed through a single prompt:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/lawful-meow/superpowers-codex-plugin/refs/heads/main/.codex/INSTALL.md
```

Manual installation steps are documented in [`.codex/INSTALL.md`](./.codex/INSTALL.md).

## Configuration

Subagent-heavy skills benefit from enabling Codex multi-agent support:

```toml
[features]
multi_agent = true
```

Add that block to `~/.codex/config.toml` to support flows such as `dispatching-parallel-agents` and `subagent-driven-development`.

## Repository Layout

- `plugins/superpowers/.codex-plugin/plugin.json`
  Codex plugin manifest.
- `plugins/superpowers/skills/`
  Superpowers skills snapshot from upstream `v5.0.6`.
- `plugins/superpowers/agents/`
  Bundled agent prompt files.
- `plugins/superpowers/commands/`
  Bundled command markdown files.
- `plugins/superpowers/hooks/`
  Upstream hook scripts and source configs.
- `plugins/superpowers/hooks.json`
  Codex hook entrypoint for the bundled session-start hook.
- `.agents/plugins/marketplace.json`
  Local marketplace entry pointing to `./plugins/superpowers`.

## Publishing

This repository can be published as a standalone GitHub project with standard Git commands:

```bash
cd /Users/lap16355/Downloads/SUperpower/superpowers-codex-plugin
git init
git add .
git commit -m "Initial Codex wrapper for Superpowers v5.0.6"
git branch -M main
git remote add origin git@github.com:lawful-meow/superpowers-codex-plugin.git
git push -u origin main
```

Equivalent GitHub CLI workflow:

```bash
gh repo create lawful-meow/superpowers-codex-plugin --public --source=. --remote=origin --push
```

## Updating

When a new Superpowers release is adopted, refresh these directories from upstream:

- `plugins/superpowers/skills/`
- `plugins/superpowers/agents/`
- `plugins/superpowers/commands/`
- `plugins/superpowers/hooks/`

Then update:

- `plugins/superpowers/.codex-plugin/plugin.json`
- `README.md`
- `.codex/INSTALL.md`

## Provenance

- upstream repository: <https://github.com/obra/superpowers>
- upstream release packaged here: `v5.0.6`
- packaged repository: <https://github.com/lawful-meow/superpowers-codex-plugin>
