## Dev Container

Running `claude` in an isolated Docker container is recommended! Use the `claude-code-devcontainer` from [here](https://github.com/reanblock/claude-code-devcontainer)

### Installation

1. Install the prerequistes (**using the Reanblock fork**) listed [here](https://github.com/reanblock/claude-code-devcontainer?tab=readme-ov-file#prerequisites) - which is `docker`, `@devcontainers/cli`, `claude-code-devcontainer `.
2. In each new project you need to run `devc .` once only.
3. Now you can enter the container to start working using `devc shell`.
4. Spin up `claude` and check that it is running with `bypassPermissions` set and the hooks are enabled (run `cat ~/.claude/settings.json` in your contaier)

```bash
devc .              Install template + start container in current directory
devc up             Start the devcontainer
devc rebuild        Rebuild container (preserves persistent volumes)
devc down           Stop the container
devc shell          Open zsh shell in container
devc exec CMD       Execute command inside the container
devc upgrade        Upgrade Claude Code in the container
devc mount SRC DST  Add a bind mount (host → container)
devc template DIR   Copy devcontainer files to directory
devc self-install   Install devc to ~/.local/bin
```