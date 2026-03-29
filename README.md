# Superpowers Codex Plugin

This repository packages [obra/superpowers](https://github.com/obra/superpowers) as a Codex plugin bundle.

It is based on upstream Superpowers release `v5.0.6` and keeps the Codex-facing parts in a plugin layout that matches the `plugin-creator` conventions:

- `.agents/plugins/marketplace.json`
- `plugins/superpowers/.codex-plugin/plugin.json`
- `plugins/superpowers/skills/`
- `plugins/superpowers/agents/`
- `plugins/superpowers/commands/`
- `plugins/superpowers/hooks/`
- `plugins/superpowers/hooks.json`

## What Superpowers Does

Superpowers is an agentic development workflow built around reusable skills. The upstream project teaches coding agents to:

- refine ideas before writing code
- turn approved designs into implementation plans
- execute plans task by task
- prefer red/green TDD
- run structured debugging workflows
- use code review and branch-finishing workflows

In practice, the core workflow is:

1. `brainstorming`
2. `using-git-worktrees`
3. `writing-plans`
4. `subagent-driven-development` or `executing-plans`
5. `test-driven-development`
6. `requesting-code-review`
7. `finishing-a-development-branch`

## What This Wrapper Includes

This Codex wrapper bundles the upstream runtime components that map cleanly into a Codex plugin:

- `skills/`
  - the full Superpowers skills library from `v5.0.6`
- `agents/`
  - upstream named-agent prompt files such as `code-reviewer.md`
- `commands/`
  - upstream command markdown files such as `brainstorm`, `write-plan`, and `execute-plan`
- `hooks/`
  - upstream session-start hook scripts and source hook configs
- `hooks.json`
  - a Codex-oriented hook entrypoint for the bundled session-start hook

This repository does not try to mirror every upstream directory. It intentionally excludes non-plugin repository content such as:

- `.claude-plugin/`
- `.cursor-plugin/`
- `.opencode/`
- `tests/`
- most repo-level docs and metadata files

## Prerequisites

- Codex
- Git

Optional, but recommended for the subagent-heavy skills:

```toml
[features]
multi_agent = true
```

Add that to `~/.codex/config.toml` if you want skills like `dispatching-parallel-agents` and `subagent-driven-development` to use Codex multi-agent support.

## Install For Local Codex Use

### Option 1: Home-local install

Clone this repository somewhere on your machine:

```bash
git clone https://github.com/<your-user>/superpowers-codex-plugin.git ~/code/superpowers-codex-plugin
cd ~/code/superpowers-codex-plugin
```

Create the standard local plugin directories:

```bash
mkdir -p ~/.agents/plugins ~/plugins
```

Copy the plugin into your home-local plugins directory:

```bash
rm -rf ~/plugins/superpowers
cp -R plugins/superpowers ~/plugins/superpowers
```

If you do not already have a home-local marketplace file, copy this repository's marketplace file:

```bash
cp .agents/plugins/marketplace.json ~/.agents/plugins/marketplace.json
```

If you already have `~/.agents/plugins/marketplace.json`, merge in the `superpowers` entry from this repository's [marketplace.json](./.agents/plugins/marketplace.json) instead of overwriting your existing file.

The required marketplace entry is:

```json
{
  "name": "superpowers",
  "source": {
    "source": "local",
    "path": "./plugins/superpowers"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Coding"
}
```

Restart Codex after installing.

### Option 2: Repo-local testing

This repository also keeps the repo-local plugin layout created by `plugin-creator`:

- `.agents/plugins/marketplace.json`
- `plugins/superpowers/`

That makes it suitable for local workspace testing and validation before you publish or copy it into `~/plugins`.

## Verify Installation

Check that the local plugin files exist:

```bash
ls -la ~/plugins/superpowers
ls -la ~/.agents/plugins/marketplace.json
```

Then restart Codex and try prompts that should trigger Superpowers behavior, for example:

- `help me plan this feature`
- `use systematic debugging on this failure`
- `execute this approved plan with tests first`

## Update From Upstream

To refresh this wrapper to a newer Superpowers release:

1. Download or clone the target upstream release.
2. Replace these directories from upstream:
   - `plugins/superpowers/skills/`
   - `plugins/superpowers/agents/`
   - `plugins/superpowers/commands/`
   - `plugins/superpowers/hooks/`
3. Update `plugins/superpowers/.codex-plugin/plugin.json`.
4. Update this README's snapshot version.
5. Review upstream Codex docs for any new platform-specific requirements.
6. Re-run the verification checks before publishing.

## Initialize Git And Make The First Push

If this wrapper repo is not already a git repository:

```bash
cd /Users/lap16355/Downloads/SUperpower/superpowers-codex-plugin
git init
git add .
git commit -m "Initial Codex wrapper for Superpowers v5.0.6"
git branch -M main
```

Before pushing to your own GitHub repository, review these files:

- `plugins/superpowers/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `README.md`

In particular, decide whether these fields should still point to upstream Superpowers for provenance or to your own wrapper repository:

- `homepage`
- `repository`

### Create The GitHub Repo With `gh`

If you use the GitHub CLI:

```bash
gh repo create <your-user>/superpowers-codex-plugin --public --source=. --remote=origin --push
```

### First Push With Standard Git Commands

If you create the GitHub repository in the browser first:

```bash
git remote add origin git@github.com:<your-user>/superpowers-codex-plugin.git
git push -u origin main
```

If you prefer HTTPS:

```bash
git remote add origin https://github.com/<your-user>/superpowers-codex-plugin.git
git push -u origin main
```

## Verification Checklist

Use the `plugin-creator` manifest and marketplace conventions as the baseline:

- `plugins/superpowers/.codex-plugin/plugin.json` exists
- plugin folder name and manifest `name` are both `superpowers`
- `.agents/plugins/marketplace.json` exists
- marketplace `source.path` is `./plugins/superpowers`
- marketplace entry includes `policy.installation`, `policy.authentication`, and `category`
- manifest JSON parses
- marketplace JSON parses
- `hooks.json` parses
- every manifest path resolves inside the plugin
- the bundled `skills/`, `agents/`, `commands/`, and `hooks/` match the intended upstream snapshot

## Provenance

This wrapper is derived from the upstream Superpowers project by Jesse Vincent:

- upstream repository: <https://github.com/obra/superpowers>
- upstream release packaged here: `v5.0.6`

The plugin metadata currently keeps upstream project identity for provenance, while this repository provides the Codex plugin packaging layer around that release.
