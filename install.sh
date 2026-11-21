#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Claude Code Configuration Installer${NC}"
echo "======================================"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"

# Directories whose *entries* are synced from this repo. Only the entries that
# exist in this repo are replaced; anything else in these folders (skills or
# commands installed separately, synced skills, etc.) is left alone.
DIRS=("skills" "commands" "hooks" "status_lines" "output-styles" "agents" "prompts")

# Records which entries this script installed, so entries later removed from
# the repo can be cleaned up without touching anything else.
MANIFEST="$CLAUDE_DIR/.claude-code-kit-manifest"

# settings.json keys managed by `claude plugins` that are preserved from the
# existing settings (merged; the repo's values win on conflict).
PRESERVED_SETTINGS_KEYS='["enabledPlugins", "extraKnownMarketplaces"]'

mkdir -p "$CLAUDE_DIR"

OLD_MANIFEST=""
if [ -f "$MANIFEST" ]; then
    OLD_MANIFEST="$(cat "$MANIFEST")"
fi
NEW_MANIFEST=""

# Step 1: Sync repo entries
echo -e "${YELLOW}Step 1: Installing repo entries (leaving other entries untouched)...${NC}"
for dir in "${DIRS[@]}"; do
    source_dir="$SCRIPT_DIR/$dir"
    target_dir="$CLAUDE_DIR/$dir"

    if [ ! -d "$source_dir" ]; then
        echo -e "  - ${RED}Warning: $source_dir not found, skipping${NC}"
        continue
    fi

    mkdir -p "$target_dir"
    for entry_path in "$source_dir"/* "$source_dir"/.[!.]*; do
        [ -e "$entry_path" ] || continue
        entry="$(basename "$entry_path")"
        # The skills folder's top-level README.md is repo documentation, not a skill
        if [ "$dir" = "skills" ] && [ "$entry" = "README.md" ]; then
            continue
        fi
        rm -rf "${target_dir:?}/$entry"
        cp -R "$entry_path" "$target_dir/"
        NEW_MANIFEST="${NEW_MANIFEST}${dir}/${entry}"$'\n'
    done
    echo "  - Synced $dir"
done
echo ""

# Step 2: Remove entries installed previously that are no longer in the repo
echo -e "${YELLOW}Step 2: Removing entries no longer in the repo...${NC}"
removed=0
while IFS= read -r rel; do
    [ -n "$rel" ] || continue
    if ! printf '%s' "$NEW_MANIFEST" | grep -Fxq -- "$rel"; then
        echo "  - Removing $CLAUDE_DIR/$rel"
        rm -rf "${CLAUDE_DIR:?}/$rel"
        removed=$((removed + 1))
    fi
done <<< "$OLD_MANIFEST"
if [ "$removed" -eq 0 ]; then
    echo "  - Nothing to remove"
fi
printf '%s' "$NEW_MANIFEST" > "$MANIFEST"
echo ""

# Step 3: Copy settings.json, preserving plugin settings
echo -e "${YELLOW}Step 3: Installing settings.json...${NC}"
SETTINGS_SOURCE="$SCRIPT_DIR/settings.json"
SETTINGS_TARGET="$CLAUDE_DIR/settings.json"
if [ -f "$SETTINGS_SOURCE" ]; then
    if [ -f "$SETTINGS_TARGET" ]; then
        echo "  - Backing up existing settings.json to settings.json.bak"
        cp "$SETTINGS_TARGET" "$SETTINGS_TARGET.bak"
        if command -v jq >/dev/null 2>&1; then
            echo "  - Merging settings.json (preserving plugin settings)"
            tmp="$SETTINGS_TARGET.tmp"
            jq --argjson keys "$PRESERVED_SETTINGS_KEYS" --slurpfile old "$SETTINGS_TARGET.bak" '
                $old[0] as $o
                | reduce $keys[] as $k (.;
                    if ($o[$k] != null or .[$k] != null)
                    then .[$k] = (($o[$k] // {}) + (.[$k] // {}))
                    else . end)
            ' "$SETTINGS_SOURCE" > "$tmp"
            mv "$tmp" "$SETTINGS_TARGET"
        else
            echo -e "  - ${RED}Warning: jq not found; plugin settings will NOT be preserved${NC}"
            cp "$SETTINGS_SOURCE" "$SETTINGS_TARGET"
        fi
    else
        echo "  - Copying settings.json to $SETTINGS_TARGET"
        cp "$SETTINGS_SOURCE" "$SETTINGS_TARGET"
    fi
else
    echo -e "  - ${RED}Warning: $SETTINGS_SOURCE not found, skipping${NC}"
fi
echo ""

# Step 4: Copy global CLAUDE.md
echo -e "${YELLOW}Step 4: Installing CLAUDE.md...${NC}"
CLAUDE_MD_SOURCE="$SCRIPT_DIR/global-CLAUDE.md"
CLAUDE_MD_TARGET="$CLAUDE_DIR/CLAUDE.md"
if [ -f "$CLAUDE_MD_SOURCE" ]; then
    if [ -f "$CLAUDE_MD_TARGET" ]; then
        echo "  - Backing up existing CLAUDE.md to CLAUDE.md.bak"
        cp "$CLAUDE_MD_TARGET" "$CLAUDE_MD_TARGET.bak"
    fi
    echo "  - Copying global-CLAUDE.md to $CLAUDE_MD_TARGET"
    cp "$CLAUDE_MD_SOURCE" "$CLAUDE_MD_TARGET"
else
    echo -e "  - ${RED}Warning: $CLAUDE_MD_SOURCE not found, skipping${NC}"
fi
echo ""

echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "The following have been installed to $CLAUDE_DIR:"
for dir in "${DIRS[@]}"; do
    if [ -d "$SCRIPT_DIR/$dir" ]; then
        echo "  ✓ $dir"
    fi
done
if [ -f "$SETTINGS_SOURCE" ]; then
    echo "  ✓ settings.json"
fi
if [ -f "$CLAUDE_MD_SOURCE" ]; then
    echo "  ✓ CLAUDE.md"
fi
echo ""
echo -e "${YELLOW}Note: You may need to restart Claude Code for changes to take effect.${NC}"
