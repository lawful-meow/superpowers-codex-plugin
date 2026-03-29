# Installing Superpowers Codex Plugin

Install Superpowers for Codex with one command:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/lawful-meow/superpowers-codex-plugin/refs/heads/main/scripts/install.sh)
```

The installer clones or updates this repository under `~/.codex/superpowers-codex-plugin`, copies the packaged plugin to `~/plugins/superpowers`, merges a `superpowers` entry into `~/.agents/plugins/marketplace.json`, enables `multi_agent` and `codex_hooks`, and writes the Superpowers hook configuration to `~/.codex/hooks.json`.

## After the Installer

Restart Codex.

The installer also writes `enabled = true` for `superpowers@<marketplace-name>` in `~/.codex/config.toml`, so no separate marketplace install click is required.

## Optional Hook Debug Mode

Enable hook logging:

```bash
touch ~/.codex/superpowers-hooks-debug
```

Restart Codex, then trigger a new session, submit a prompt, and run a Bash command through Codex. Inspect the log:

```bash
cat ~/.codex/logs/superpowers-hooks.log
```

Disable hook logging:

```bash
rm ~/.codex/superpowers-hooks-debug
```

## Verify

Check the installed files:

```bash
ls -la ~/plugins/superpowers
ls -la ~/.agents/plugins/marketplace.json
ls -la ~/.codex/hooks.json
```

Check the enabled features:

```bash
rg -n 'multi_agent|codex_hooks|superpowers@' ~/.codex/config.toml
```

Then start a new Codex session and ask for a planning-oriented task, for example:

- `Help me plan this feature before writing code.`
- `Use systematic debugging on this bug.`
- `Execute this approved plan with tests first.`

## Notes

- Codex hooks are experimental.
- `codex_hooks = true` is required.
- Codex hooks are currently disabled on Windows.
