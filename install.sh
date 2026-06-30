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
CLAUDE_DIR="$HOME/.claude"

# Define directories to clean and install
DIRS=("skills" "commands" "hooks" "status_lines" "output-styles" "agents" "prompts")

# Step 1: Remove existing installations
echo -e "${YELLOW}Step 1: Removing existing installations...${NC}"
for dir in "${DIRS[@]}"; do
    target_dir="$CLAUDE_DIR/$dir"
    if [ -d "$target_dir" ]; then
        echo "  - Removing $target_dir"
        rm -rf "$target_dir"
    else
        echo "  - $target_dir does not exist, skipping"
    fi
done
echo ""

# Step 2: Create .claude directory if it doesn't exist
if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "${YELLOW}Creating $CLAUDE_DIR directory...${NC}"
    mkdir -p "$CLAUDE_DIR"
fi
echo ""

# Step 3: Copy new installations
echo -e "${YELLOW}Step 2: Installing new configurations...${NC}"
for dir in "${DIRS[@]}"; do
    source_dir="$SCRIPT_DIR/$dir"
    target_dir="$CLAUDE_DIR/$dir"

    if [ -d "$source_dir" ]; then
        echo "  - Copying $dir to $target_dir"
        cp -R "$source_dir" "$CLAUDE_DIR/"
    else
        echo -e "  - ${RED}Warning: $source_dir not found, skipping${NC}"
    fi
done
echo ""

# Step 3: Copy settings.json
echo -e "${YELLOW}Step 3: Installing settings.json...${NC}"
SETTINGS_SOURCE="$SCRIPT_DIR/settings.json"
SETTINGS_TARGET="$CLAUDE_DIR/settings.json"
if [ -f "$SETTINGS_SOURCE" ]; then
    if [ -f "$SETTINGS_TARGET" ]; then
        echo "  - Backing up existing settings.json to settings.json.bak"
        cp "$SETTINGS_TARGET" "$SETTINGS_TARGET.bak"
    fi
    echo "  - Copying settings.json to $SETTINGS_TARGET"
    cp "$SETTINGS_SOURCE" "$SETTINGS_TARGET"
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
echo "The following have been installed to ~/.claude:"
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
