#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
Status Line v6 - Context Window Usage
Display: folder git:(branch) | [Model] # [###---] | 42.5% used | ~115k left | session_id
Visual progress indicator with percentage and session ID
"""

import json
import os
import subprocess
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # dotenv is optional


# ANSI color codes
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BRIGHT_WHITE = "\033[97m"
DIM = "\033[90m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
RESET = "\033[0m"


def get_usage_color(percentage):
    """Get color based on usage percentage."""
    if percentage < 50:
        return GREEN
    elif percentage < 75:
        return YELLOW
    elif percentage < 90:
        return RED
    else:
        return "\033[91m"  # Bright red for critical


def create_progress_bar(percentage, width=15):
    """Create a visual progress bar."""
    filled = int((percentage / 100) * width)
    empty = width - filled

    color = get_usage_color(percentage)

    # Use block characters for the bar
    bar = f"{color}{'#' * filled}{DIM}{'-' * empty}{RESET}"
    return f"[{bar}]"


def format_tokens(tokens):
    """Format token count in human-readable format."""
    if tokens is None:
        return "0"
    if tokens < 1000:
        return str(int(tokens))
    elif tokens < 1000000:
        return f"{tokens / 1000:.1f}k"
    else:
        return f"{tokens / 1000000:.2f}M"


def get_git_branch(cwd):
    """Return the current git branch (or short SHA if detached), or None."""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        if result.returncode != 0:
            return None
        branch = result.stdout.strip()
        if branch == "HEAD":
            result = subprocess.run(
                ["git", "-C", cwd, "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            branch = result.stdout.strip() or None
        return branch
    except Exception:
        return None


def format_location(input_data):
    """Format as `folder git:(branch)`, like the oh-my-zsh robbyrussell prompt."""
    workspace = input_data.get("workspace", {}) or {}
    cwd = workspace.get("current_dir") or input_data.get("cwd") or os.getcwd()
    folder = os.path.basename(os.path.normpath(cwd)) or cwd
    location = f"{CYAN}{folder}{RESET}"
    branch = get_git_branch(cwd)
    if branch:
        location += f" {BLUE}git:({RED}{branch}{BLUE}){RESET}"
    return location


def generate_status_line(input_data):
    """Generate the context window usage status line."""
    # Get model name
    model_info = input_data.get("model", {})
    model_name = model_info.get("display_name", "Claude")

    # Get session ID
    session_id = input_data.get("session_id", "") or "--------"

    # Get context window data
    context_data = input_data.get("context_window", {})
    used_percentage = context_data.get("used_percentage", 0) or 0
    context_window_size = context_data.get("context_window_size", 200000) or 200000

    # Calculate remaining tokens from used percentage
    remaining_tokens = int(context_window_size * ((100 - used_percentage) / 100))

    # Get color for percentage display
    usage_color = get_usage_color(used_percentage)

    # Build status line
    parts = []

    # Current folder and git branch
    parts.append(format_location(input_data))

    # Model name in cyan
    parts.append(f"{CYAN}[{model_name}]{RESET}")

    # Progress bar with hash indicator
    progress_bar = create_progress_bar(used_percentage)
    parts.append(f"{MAGENTA}#{RESET} {progress_bar}")

    # Used percentage
    parts.append(f"{usage_color}{used_percentage:.1f}%{RESET} used")

    # Tokens left
    tokens_left_str = format_tokens(remaining_tokens)
    parts.append(f"{BLUE}~{tokens_left_str} left{RESET}")

    # Session ID (rightmost)
    parts.append(f"{DIM}{session_id}{RESET}")

    return " | ".join(parts)


def main():
    try:
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())

        # Generate status line
        status_line = generate_status_line(input_data)

        # Output the status line
        print(status_line)

        # Success
        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        print(f"{RED}[Claude] # Error: Invalid JSON{RESET}")
        sys.exit(0)
    except Exception as e:
        # Handle any other errors gracefully
        print(f"{RED}[Claude] # Error: {str(e)}{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
