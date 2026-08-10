#!/usr/bin/env sh
set -eu

usage() {
  echo "Usage: ./install.sh codex|claude"
}

if [ "$#" -ne 1 ]; then
  usage
  exit 2
fi

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir="$repo_dir/skills/hci-paper-writing"

case "$1" in
  codex)
    install_root="${AGENT_SKILLS_HOME:-$HOME/.agents/skills}"
    ;;
  claude)
    install_root="${CLAUDE_SKILLS_HOME:-$HOME/.claude/skills}"
    ;;
  *)
    usage
    exit 2
    ;;
esac

target="$install_root/hci-paper-writing"
mkdir -p "$install_root"

if [ -e "$target" ] || [ -L "$target" ]; then
  echo "Refusing to overwrite existing installation: $target" >&2
  echo "Remove or move it explicitly, then run the installer again." >&2
  exit 1
fi

ln -s "$source_dir" "$target"
echo "Installed hci-paper-writing -> $target"
echo "Restart your agent if it does not discover the skill immediately."

