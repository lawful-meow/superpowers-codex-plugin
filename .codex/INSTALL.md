# Installing Superpowers Codex Plugin

Install this wrapper by cloning the repository, copying the packaged plugin to your home-local plugins directory, and registering the marketplace entry.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/lawful-meow/superpowers-codex-plugin.git ~/.codex/superpowers-codex-plugin
   ```

2. Create the local plugin directories:

   ```bash
   mkdir -p ~/.agents/plugins ~/plugins
   ```

3. Copy the plugin bundle into `~/plugins`:

   ```bash
   rm -rf ~/plugins/superpowers
   cp -R ~/.codex/superpowers-codex-plugin/plugins/superpowers ~/plugins/superpowers
   ```

4. Register the marketplace entry:

   If `~/.agents/plugins/marketplace.json` does not exist yet, copy the repository version:

   ```bash
   cp ~/.codex/superpowers-codex-plugin/.agents/plugins/marketplace.json ~/.agents/plugins/marketplace.json
   ```

   If you already have `~/.agents/plugins/marketplace.json`, merge this plugin entry into it instead of overwriting the file:

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

5. Optional, but recommended for subagent-heavy skills:

   Add this to `~/.codex/config.toml`:

   ```toml
   [features]
   multi_agent = true
   ```

6. Restart Codex.

## Verify

Check the installed files:

```bash
ls -la ~/plugins/superpowers
ls -la ~/.agents/plugins/marketplace.json
```

Then ask Codex for something that should trigger Superpowers, for example:

- `help me plan this feature`
- `use systematic debugging on this bug`
- `execute this approved plan with tests first`
