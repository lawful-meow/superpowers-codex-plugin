#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
USING_SUPERPOWERS_PATH = PLUGIN_ROOT / "skills" / "using-superpowers" / "SKILL.md"
DEBUG_MARKER = Path.home() / ".codex" / "superpowers-hooks-debug"
DEBUG_LOG = Path.home() / ".codex" / "logs" / "superpowers-hooks.log"


def load_payload():
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def debug_enabled():
    value = os.environ.get("SUPERPOWERS_HOOK_DEBUG", "").strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    return DEBUG_MARKER.exists()


def append_debug_log(event_name, payload):
    DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
    DEBUG_LOG.open("a").write(
        json.dumps(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event_name,
                "payload": payload,
            }
        )
        + "\n"
    )


def session_context():
    using_superpowers = USING_SUPERPOWERS_PATH.read_text()
    warning_message = ""
    legacy_skills_dir = Path.home() / ".config" / "superpowers" / "skills"
    if legacy_skills_dir.exists():
        warning_message = (
            "\n\n<important-reminder>WARNING: Legacy skills under "
            "~/.config/superpowers/skills are not used by Codex. Move custom skills "
            "to Codex-native install locations and remove the old directory when you "
            "finish migrating.</important-reminder>"
        )

    return (
        "<EXTREMELY_IMPORTANT>\n"
        "You have superpowers.\n\n"
        "**Below is the full content of your 'superpowers:using-superpowers' skill - your "
        "introduction to using skills. For all other skills, use the Skill tool:**\n\n"
        f"{using_superpowers}"
        f"{warning_message}\n"
        "</EXTREMELY_IMPORTANT>"
    )


def main():
    event_name = sys.argv[1] if len(sys.argv) > 1 else None
    payload = load_payload()
    event_name = payload.get("hook_event_name", event_name)

    debug = debug_enabled()
    if debug and event_name:
        append_debug_log(event_name, payload)

    if event_name == "SessionStart":
        response = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": session_context(),
            }
        }
        if debug:
            response["systemMessage"] = "Superpowers SessionStart hook ran."
        print(json.dumps(response))
        return

    response = {}
    if debug and event_name:
        response["systemMessage"] = f"Superpowers {event_name} hook ran."

    print(json.dumps(response))


if __name__ == "__main__":
    main()
