# Superpowers Codex Plugin

This repository packages [obra/superpowers](https://github.com/obra/superpowers) `v5.0.6` as a Codex plugin bundle.

It includes the upstream:

- `skills/`
- `agents/`
- `commands/`
- `hooks/`

inside a Codex plugin layout:

- `.agents/plugins/marketplace.json`
- `plugins/superpowers/.codex-plugin/plugin.json`

## Quick Install

After you push this repository to GitHub, users should be able to install it with a single Codex prompt:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/<your-user>/superpowers-codex-plugin/refs/heads/main/.codex/INSTALL.md
```

The install instructions live in [./.codex/INSTALL.md](./.codex/INSTALL.md).

## Notes

- For subagent-heavy skills, enable this in `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

- The plugin name is `superpowers`.
- The marketplace entry points to `./plugins/superpowers`.
- This wrapper keeps upstream project identity for provenance.

## Publish This Repo

If this directory is not already a git repository:

```bash
cd /Users/lap16355/Downloads/SUperpower/superpowers-codex-plugin
git init
git add .
git commit -m "Initial Codex wrapper for Superpowers v5.0.6"
git branch -M main
```

Create the GitHub repo and push:

```bash
git remote add origin git@github.com:<your-user>/superpowers-codex-plugin.git
git push -u origin main
```

Or with GitHub CLI:

```bash
gh repo create <your-user>/superpowers-codex-plugin --public --source=. --remote=origin --push
```

## Update From Upstream

When a new Superpowers release comes out, replace:

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
