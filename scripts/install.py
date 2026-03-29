#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path


PLUGIN_NAME = "superpowers"
MARKETPLACE_NAME = "superpowers-local"
MARKETPLACE_DISPLAY_NAME = "Superpowers Local"
DEBUG_MARKER_NAME = "superpowers-hooks-debug"


def superpowers_marketplace_entry(installation_policy="AVAILABLE"):
    return {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": f"./plugins/{PLUGIN_NAME}",
        },
        "policy": {
            "installation": installation_policy,
            "authentication": "ON_INSTALL",
        },
        "category": "Coding",
    }


def merge_marketplace_doc(existing, installation_policy="AVAILABLE"):
    if not existing:
        existing = {
            "name": MARKETPLACE_NAME,
            "interface": {"displayName": MARKETPLACE_DISPLAY_NAME},
            "plugins": [],
        }

    merged = {
        "name": existing.get("name", MARKETPLACE_NAME),
        "plugins": [],
    }

    interface = existing.get("interface")
    if interface:
        merged["interface"] = interface
    elif not existing.get("name"):
        merged["interface"] = {"displayName": MARKETPLACE_DISPLAY_NAME}

    replacement = superpowers_marketplace_entry(installation_policy=installation_policy)
    replaced = False

    for entry in existing.get("plugins", []):
        if entry.get("name") == PLUGIN_NAME:
            merged["plugins"].append(replacement)
            replaced = True
        else:
            merged["plugins"].append(entry)

    if not replaced:
        merged["plugins"].append(replacement)

    return merged


def upsert_plugin_enablement(config_text, marketplace_name):
    section_header = f'[plugins."{PLUGIN_NAME}@{marketplace_name}"]'
    lines = config_text.splitlines()
    output = []
    in_target_section = False
    found_section = False
    inserted = False

    for line in lines:
        stripped = line.strip()
        is_section_header = stripped.startswith("[") and stripped.endswith("]")

        if is_section_header:
            if in_target_section and not inserted:
                output.append("enabled = true")
                inserted = True
            in_target_section = stripped == section_header
            if in_target_section:
                found_section = True
            output.append(line)
            continue

        if in_target_section and stripped.startswith("enabled ="):
            continue

        output.append(line)

    if in_target_section and not inserted:
        output.append("enabled = true")
        inserted = True

    if not found_section:
        if output and output[-1] != "":
            output.append("")
        output.extend([section_header, "enabled = true"])

    return "\n".join(output).rstrip() + "\n"


def merge_config_text(existing_text, marketplace_name=None):
    lines = existing_text.splitlines()
    output = []
    features_found = False
    in_features = False
    inserted_features = False

    for line in lines:
        stripped = line.strip()
        is_section_header = stripped.startswith("[") and stripped.endswith("]")

        if is_section_header:
            if in_features and not inserted_features:
                output.append("multi_agent = true")
                output.append("codex_hooks = true")
                inserted_features = True
            in_features = stripped == "[features]"
            if in_features:
                features_found = True
            output.append(line)
            continue

        if in_features and stripped.startswith(("multi_agent =", "codex_hooks =")):
            continue

        output.append(line)

    if in_features and not inserted_features:
        output.append("multi_agent = true")
        output.append("codex_hooks = true")
        inserted_features = True

    if not features_found:
        if output and output[-1] != "":
            output.append("")
        output.extend(
            [
                "[features]",
                "multi_agent = true",
                "codex_hooks = true",
            ]
        )

    merged_text = "\n".join(output).rstrip() + "\n"

    if marketplace_name:
        return upsert_plugin_enablement(merged_text, marketplace_name)

    return merged_text


def hook_command(plugin_root, event_name):
    hook_script = plugin_root / "hooks" / "codex-hook.py"
    return f'python3 "{hook_script}" "{event_name}"'


def build_superpowers_hooks_doc(plugin_root):
    return {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_command(plugin_root, "SessionStart"),
                            "statusMessage": "Loading Superpowers context",
                        }
                    ],
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_command(plugin_root, "PreToolUse"),
                        }
                    ],
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_command(plugin_root, "PostToolUse"),
                        }
                    ],
                }
            ],
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_command(plugin_root, "UserPromptSubmit"),
                        }
                    ],
                }
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_command(plugin_root, "Stop"),
                        }
                    ],
                }
            ],
        }
    }


def is_superpowers_hook_group(group):
    for hook in group.get("hooks", []):
        command = hook.get("command", "")
        if "/superpowers/hooks/codex-hook.py" in command or "\\superpowers\\hooks\\codex-hook.py" in command:
            return True
    return False


def merge_hooks_doc(existing, plugin_root):
    if not existing:
        existing = {"hooks": {}}

    merged = {"hooks": dict(existing.get("hooks", {}))}
    new_doc = build_superpowers_hooks_doc(plugin_root)

    for event_name, new_groups in new_doc["hooks"].items():
        current_groups = merged["hooks"].get(event_name, [])
        filtered_groups = [group for group in current_groups if not is_superpowers_hook_group(group)]
        merged["hooks"][event_name] = filtered_groups + new_groups

    return merged


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def load_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text())


def ensure_debug_marker(home_dir, debug_hooks):
    marker_path = home_dir / ".codex" / DEBUG_MARKER_NAME
    if debug_hooks:
        marker_path.parent.mkdir(parents=True, exist_ok=True)
        marker_path.write_text("enabled\n")
    elif marker_path.exists():
        marker_path.unlink()


def run_install(repo_root, home_dir, debug_hooks=False):
    repo_root = Path(repo_root).resolve()
    home_dir = Path(home_dir).resolve()

    source_plugin = repo_root / "plugins" / PLUGIN_NAME
    if not source_plugin.exists():
        raise FileNotFoundError(f"Missing plugin source at {source_plugin}")

    installed_plugin = home_dir / "plugins" / PLUGIN_NAME
    installed_plugin.parent.mkdir(parents=True, exist_ok=True)
    if installed_plugin.exists():
        shutil.rmtree(installed_plugin)
    shutil.copytree(source_plugin, installed_plugin)

    marketplace_path = home_dir / ".agents" / "plugins" / "marketplace.json"
    marketplace_doc = merge_marketplace_doc(
        load_json(marketplace_path),
        installation_policy="INSTALLED_BY_DEFAULT",
    )
    write_json(marketplace_path, marketplace_doc)

    config_path = home_dir / ".codex" / "config.toml"
    existing_config = config_path.read_text() if config_path.exists() else ""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        merge_config_text(existing_config, marketplace_name=marketplace_doc["name"])
    )

    hooks_path = home_dir / ".codex" / "hooks.json"
    hooks_doc = merge_hooks_doc(load_json(hooks_path), installed_plugin)
    write_json(hooks_path, hooks_doc)

    ensure_debug_marker(home_dir, debug_hooks)

    return {
        "plugin_root": str(installed_plugin),
        "marketplace_path": str(marketplace_path),
        "config_path": str(config_path),
        "hooks_path": str(hooks_path),
        "debug_enabled": debug_hooks,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Install the Superpowers Codex plugin and home-wide hooks.")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the repository root that contains plugins/superpowers.",
    )
    parser.add_argument(
        "--home",
        default=str(Path.home()),
        help="Target home directory for ~/.codex, ~/.agents, and ~/plugins.",
    )
    parser.add_argument(
        "--debug-hooks",
        action="store_true",
        help="Enable hook debug logging after install.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    result = run_install(args.repo_root, args.home, debug_hooks=args.debug_hooks)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
