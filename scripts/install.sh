#!/usr/bin/env bash

set -euo pipefail

REPO_URL="${SUPERPOWERS_REPO_URL:-https://github.com/lawful-meow/superpowers-codex-plugin.git}"
INSTALL_DIR="${SUPERPOWERS_INSTALL_DIR:-$HOME/.codex/superpowers-codex-plugin}"

SCRIPT_PATH="${BASH_SOURCE[0]:-}"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" 2>/dev/null && pwd || true)"
REPO_ROOT=""

if [ -n "$SCRIPT_DIR" ] && [ -d "${SCRIPT_DIR}/../plugins/superpowers" ]; then
  REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
fi

if [ -z "$REPO_ROOT" ]; then
  if [ -d "${INSTALL_DIR}/.git" ]; then
    git -C "$INSTALL_DIR" pull --ff-only
  else
    mkdir -p "$(dirname "$INSTALL_DIR")"
    rm -rf "$INSTALL_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
  fi
  REPO_ROOT="$INSTALL_DIR"
fi

python3 "${REPO_ROOT}/scripts/install.py" "$@"
