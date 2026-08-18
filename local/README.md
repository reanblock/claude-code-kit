# Local LLM Setup

This guide explains how to run open weights models locally using two MacBook Pro computers - one as the host / server and the other as the client.

## Host Machine

On the host machine serve the model using [MTPLX](https://mtplx.com/).

```bash
# Install MTPLX via Homebrew
brew install youssofal/mtplx/mtplx

# Start the MTPLX server and bind it to your Tailscale IP on port 8080
mtplx serve --download --host TAILSCALE_IP --port 8080 --api-key my-secret-key --model Youssofal/Qwen3.8-27B-Optimized-Speed
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

Simply run `pi` in the terminal like so:

```bash
pi --model remote-mtplx/qwen3.8-27b-optimized-speed
```