# Local LLM Setup

This guide explains how to run open weights models locally using two MacBook Pro computers - one as the host / server and the other as the client.

## Host Machine

On the host machine serve the model using [MTPLX](https://mtplx.com/).

### Install mtplx and download model

Run the following commands to install `mtplx` and download model:

```bash
# Install MTPLX via Homebrew
brew install youssofal/mtplx/mtplx

# List models already downloaded to the local MTPLX cache (add --json for machine-readable output)
mtplx models

# [OPTIONAL] Download the model into the local MTPLX cache (skip if already listed by `mtplx models`)
mtplx pull Youssofal/Qwen3.8-27B-Optimized-Speed
```

### Run model locally

Use the following command to run the model as an interactive chat in the terminal. Use the [serve model](#serve-model) instructions to server over http and connect from a different machine.

```bash
# Interactive chat in the terminal
mtplx start cli --model Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed
```

#### Serve model

Run the following to serve your model

```bash
# Export TAILSCALE_IP 
export TAILSCALE_IP=$(tailscale ip -4)

# Serve the downloaded model and bind it to your Tailscale IP on port 8080
mtplx serve --host $TAILSCALE_IP --port 8080 --api-key my-secret-key
```

## Client Machine

On the client machine use [PI agent](https://pi.dev/).

Add the model meta to `models.json`.

```bash
cat << 'EOF' > ~/.pi/agent/models.json
{
  "providers": {
    "remote-mtplx": {
      "baseUrl": "http://TAILSCALE_IP:8080/v1",
      "api": "openai-completions",
      "apiKey": "my-secret-key",
      "models": [
        {
          "id": "Youssofal/Qwen3.8-27B-Optimized-Speed",
          "name": "Qwen 3.8 27B MTPLX",
          "contextWindow": 128000,
          "maxTokens": 16384,
          "reasoning": false,
          "input": ["text"]
        }
      ]
    }
  }
}
EOF
```

**OPTIONAL: ** Add a skills alias to `~/.pi/agent/settings.json` file so that PI agent detects all available Claude skills.

```json
"skills": [
  "~/.claude/skills"
]
```

Simply run `pi` in the terminal like so:

```bash
pi --list-models
pi --model remote-mtplx/qwen3.8-27b-optimized-speed
```