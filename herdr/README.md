# Herdr

[Herdr](https://herdr.dev/) runs coding agents (Claude Code, etc.) inside a background server on your machine, so they keep running when you close the window. A sidebar shows which agents are working, done, or waiting on you. Remote machines can be added over SSH.

There are two separate products: the **App** and the **TUI**.

## Install the App

macOS / Linux:

```bash
curl -fsSL https://releases.herdr.dev/app/install.sh | sh
```

Or download the [DMG](https://releases.herdr.dev/app/Herdr.dmg) on macOS.

More options: [herdr.dev/download](https://herdr.dev/download/)

## Install the TUI

macOS / Linux:

```bash
curl -fsSL https://herdr.dev/install.sh | sh
```

Homebrew, Nix and manual installs: [herdr.dev/tui/docs/install](https://herdr.dev/tui/docs/install/). Source: [github.com/herdrdev/herdr](https://github.com/herdrdev/herdr).

## App vs TUI

| | App | TUI |
|---|---|---|
| Interface | Desktop GUI | Terminal UI (the original Herdr) |
| Server | `herdr-core` | Its own built-in server |
| Remote machines | `hc machine add <name>` | `herdr machine add <name>` |
| Mobile | Official Herdr mobile app ([iOS](https://apps.apple.com/app/id6828898364) / [Android](https://play.google.com/store/apps/details?id=dev.herdr.app)) | **Healer for Herdr** app on iPhone |

**The two servers are not shared.** Agents started in the TUI do not appear in the App, and vice versa — pick one per workflow.

**iPhone + TUI:** the official Herdr mobile app only connects to the App's `herdr-core` server. To use the TUI from an iPhone, use the **Healer for Herdr** app instead.

## Docs

- [Guide](https://herdr.dev/guide/)
- [herdr-core](https://herdr.dev/core/)
- [TUI docs](https://herdr.dev/tui/)
- [Mobile](https://herdr.dev/mobile/)
