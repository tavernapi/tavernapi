#!/usr/bin/env sh
# TavernAPI with plain curl. Set your key first:
#   export TAVERNAPI_API_KEY=sk-tav-...

# List the available model IDs (no key needed).
curl -s https://tavernapi.com/v1/models

# One reply.
curl -s https://tavernapi.com/v1/chat/completions \
  -H "Authorization: Bearer $TAVERNAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.8-flash",
    "messages": [{"role": "user", "content": "Describe a rainy harbor town in two sentences."}],
    "max_tokens": 200
  }'

# The same reply, streamed as server-sent events.
curl -sN https://tavernapi.com/v1/chat/completions \
  -H "Authorization: Bearer $TAVERNAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.8-flash",
    "messages": [{"role": "user", "content": "Describe a rainy harbor town in two sentences."}],
    "max_tokens": 200,
    "stream": true
  }'
