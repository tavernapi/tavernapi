# TavernAPI

TavernAPI is a paid, OpenAI-compatible API for SillyTavern and other roleplay apps. It serves Claude, Gemini, and DeepSeek models through their official providers and bills per token in US dollars.

[Website](https://tavernapi.com/) · [Pricing](https://tavernapi.com/pricing/) · [SillyTavern setup](https://tavernapi.com/guides/sillytavern-setup/) · [Troubleshooting](https://tavernapi.com/troubleshooting/) · [Contact](https://tavernapi.com/contact/)

## Quick start

1. Create an account in the [TavernAPI console](https://tavernapi.com/console) and generate an API key (`sk-tav-...`). Copy the key right away because it is shown only once.
2. Open your roleplay app or HTTP client and paste the endpoint URL and your `sk-tav-...` key into the connection settings.
3. Click **Connect** and select one of the five 1M-context models: `claude-opus-5-5`, `claude-sonnet-5-5`, `gemini-4-argon`, `gemini-3.8-flash`, or `deepseek-v4-pro`.

For SillyTavern's **Custom (OpenAI-compatible)** source, use these exact values:

```text
API:                        Chat Completion
Chat Completion Source:     Custom (OpenAI-compatible)
Custom Endpoint (Base URL): https://tavernapi.com/v1
Custom API Key:             sk-tav-...
Model:                      gemini-4-argon
```

New accounts get a one-time $0.30 trial credit that works with `gemini-4-argon` and `gemini-3.8-flash`.

## Connect your app

Every supported app uses the same `sk-tav-...` key and the same five model IDs, but different apps expect different URL paths and field names. If you use SillyTavern, see the [SillyTavern setup guide](https://tavernapi.com/guides/sillytavern-setup/) for a walkthrough and the [presets guide](https://tavernapi.com/guides/presets/) for optional storytelling presets you can download in the console.

| App | Where in the app | URL | Where the key goes | Model |
|---|---|---|---|---|
| **SillyTavern Custom (OpenAI-compatible)** | `API Connections` → `Chat Completion` → `Custom (OpenAI-compatible)` | `https://tavernapi.com/v1` in `Custom Endpoint (Base URL)` | `Custom API Key` (`sk-tav-...`) | Pick any of the 5 models from `Available Models` |
| **SillyTavern Claude source (Reverse Proxy)** | `API Connections` → `Chat Completion` → `Claude` → `Reverse Proxy` | `https://tavernapi.com/v1` in `Proxy Server URL` | `Proxy Password` (`sk-tav-...`) | `claude-opus-5-5` or `claude-sonnet-5-5` |
| **SillyTavern Google AI Studio source (Reverse Proxy)** | `API Connections` → `Chat Completion` → `Google AI Studio` → `Reverse Proxy` | `https://tavernapi.com` (no `/v1`) in `Proxy Server URL` | `Proxy Password` (`sk-tav-...`) | `gemini-4-argon` or `gemini-3.8-flash` |
| **JanitorAI** | `API Settings` → `Proxy` | `https://tavernapi.com/v1/chat/completions` in `Proxy URL` | `API Key` (`sk-tav-...`) | Type the exact model ID by hand |
| **RisuAI, Agnaistic and other OpenAI-compatible apps** | Custom / OpenAI API settings | `https://tavernapi.com/v1` (or `https://tavernapi.com/v1/chat/completions` if the field placeholder shows the full path) | API key field (`sk-tav-...`) | Pick or type one of the 5 model IDs |
| **Your own code** | OpenAI SDK or HTTP client | Base URL `https://tavernapi.com/v1` (`GET /v1/models`, `POST /v1/chat/completions`) | `Authorization: Bearer sk-tav-...` | Pass one of the 5 model IDs in `model` |

The most common mistake when switching between apps is the URL ending: SillyTavern's Custom source and standard SDKs take the base URL (`https://tavernapi.com/v1`), whereas browser apps like JanitorAI require the full chat completions URL (`https://tavernapi.com/v1/chat/completions`).

## Models and prices

All five models provide a 1M-token context window and are billed per token in US dollars (see [`data/models.json`](data/models.json) and the [pricing page](https://tavernapi.com/pricing/) for full rate details).

<!-- models:start -->
| Model | ID | Context | Input | Output | Cache read | Cache write | Trial |
|---|---|---|---:|---:|---:|---:|:---:|
| Claude Opus 5.5 | `claude-opus-5-5` | 1M | $2.80 | $14.00 | $0.14 | $3.50 |  |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M | $1.60 | $8.00 | $0.08 | $2.00 |  |
| Gemini 4 Argon | `gemini-4-argon` | 1M | $1.20 | $6.00 | $0.06 | input rate | yes |
| Gemini 3.8 Flash | `gemini-3.8-flash` | 1M | $0.49 | $2.45 | $0.049 | input rate | yes |
| DeepSeek V4 Pro | `deepseek-v4-pro` | 1M | $1.49 | $4.49 | $0.05 | input rate |  |

USD per 1M tokens, last changed 2026-11-01. Machine-readable: [data/models.json](data/models.json).
<!-- models:end -->

## Use it from code

TavernAPI exposes a standard OpenAI-compatible interface at `https://tavernapi.com/v1`, including `GET /v1/models` (no API key required) and `POST /v1/chat/completions` (both non-streaming JSON and `stream: true` server-sent events). CORS is enabled on `/v1` and `/v1beta`, so browser applications can call the API directly.

### Python (`openai` SDK)

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://tavernapi.com/v1",
    api_key=os.environ["TAVERNAPI_API_KEY"],  # sk-tav-...
)

response = client.chat.completions.create(
    model="gemini-4-argon",
    messages=[
        {"role": "system", "content": "You are Mira, a sharp-tongued tavern keeper. Stay in character."},
        {"role": "user", "content": "A stranger walks in out of the rain and asks for a room."},
    ],
    max_tokens=400,
)
print(response.choices[0].message.content)
```

### curl (non-streaming)

```sh
curl -s https://tavernapi.com/v1/chat/completions \
  -H "Authorization: Bearer sk-tav-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.8-flash",
    "messages": [{"role": "user", "content": "Describe a rainy harbor town in two sentences."}],
    "max_tokens": 200
  }'
```

Runnable streaming and non-streaming scripts are in [`examples/python_openai.py`](examples/python_openai.py), [`examples/node_openai.mjs`](examples/node_openai.mjs), and [`examples/curl.sh`](examples/curl.sh), and the OpenAI-compatible schema is documented in [`openapi.yaml`](openapi.yaml).

## Native Claude and Gemini endpoints

If your app or SDK talks to Anthropic or Google endpoints directly instead of the OpenAI format, you can use TavernAPI's native routes with the same `sk-tav-...` key. For the Claude Messages API, send requests to `POST https://tavernapi.com/v1/messages` with the `x-api-key: sk-tav-...` header (Anthropic SDKs use base URL `https://tavernapi.com`). For the native Gemini API, call `https://tavernapi.com/v1beta/models/{model}:generateContent` or `:streamGenerateContent` with the `x-goog-api-key: sk-tav-...` header or `?key=sk-tav-...` query parameter (Google GenAI SDKs use base URL `https://tavernapi.com`).

## Check your connection

If your client cannot connect or returns an unexpected error, run [`examples/doctor.py`](examples/doctor.py) to test your setup outside the app. It requires only Python 3.8+ and the standard library:

- Checks your endpoint URL format for common mistakes such as trailing spaces, missing `/v1`, duplicate `/v1/v1`, or `/chat/completions` pasted into a base URL field.
- Calls `GET /v1/models` to verify network reachability and checks that your chosen model ID is on the active list.
- Reads your API key and sends one tiny test request (`max_tokens: 16`) to confirm your key and balance work.
- Explains any HTTP status and error `code` in plain English and prints a direct link to the matching fix on the troubleshooting page.

Run it from your terminal:

```sh
export TAVERNAPI_API_KEY=sk-tav-...
python examples/doctor.py --url https://tavernapi.com/v1 --model gemini-3.8-flash
```

If `TAVERNAPI_API_KEY` is not set in your environment, the script asks for your key via a hidden prompt (`getpass`). It never prints or stores your API key.

## Errors at a glance

When a request fails, the API returns `{"error": {"message": "...", "type": "...", "code": "..."}}` with one of the following statuses and codes:

| HTTP status | Error `code` | What to do |
|---|---|---|
| `401` | `invalid_api_key` / `missing_api_key` | Paste your complete `sk-tav-...` key without spaces, or create a new key in the [console](https://tavernapi.com/console). ([Details](https://tavernapi.com/troubleshooting/#401-invalid-api-key)) |
| `402` | `insufficient_balance` | Your balance is smaller than the pre-request hold (`input + max_tokens`). Lower **Max Response Length**, switch to a cheaper model, or top up. ([Details](https://tavernapi.com/troubleshooting/#402-insufficient-balance)) |
| `403` | `trial_restricted` / `preset_locked` | Trial credit works only with `gemini-4-argon` and `gemini-3.8-flash`; add credit to unlock all models, or turn off locked `[[tav:...]]` preset entries. ([Details](https://tavernapi.com/troubleshooting/#403-trial-or-preset)) |
| `404` | `model_not_found` | Refresh the model list or enter one of the five exact IDs: `claude-opus-5-5`, `claude-sonnet-5-5`, `gemini-4-argon`, `gemini-3.8-flash`, or `deepseek-v4-pro`. ([Details](https://tavernapi.com/troubleshooting/#404-model-not-available)) |
| `404` | `not_found` | Fix the URL path for your app (`/v1` vs `/v1/chat/completions`, and remove any duplicate `/v1/v1`). ([Details](https://tavernapi.com/troubleshooting/#404-not-found)) |
| `400` | `model_required` / `messages_required` / `preset_block_unknown` | Select a model, make sure the prompt contains at least one message, or re-download the updated preset from the console. ([Details](https://tavernapi.com/troubleshooting/#400-bad-request)) |
| `429` | `upstream_error` (`rate_limit_error`) | Too many requests at once, or the upstream provider is busy. Wait a few seconds and regenerate. ([Details](https://tavernapi.com/troubleshooting/#429-rate-limit)) |
| `502` / `503` | `upstream_error` / `no_route` | The upstream provider dropped the connection or the route is temporarily unavailable. Retry shortly or switch models. ([Details](https://tavernapi.com/troubleshooting/#5xx-server-errors)) |

See [`docs/errors.md`](docs/errors.md) and the [troubleshooting guide](https://tavernapi.com/troubleshooting/) for the full error reference, including non-HTTP issues such as [connection light staying red](https://tavernapi.com/troubleshooting/#cant-connect), [empty or cut-off replies](https://tavernapi.com/troubleshooting/#empty-or-cut-off), and [higher-than-expected bills](https://tavernapi.com/troubleshooting/#higher-bill).

## How billing works

- **Hold and settle per request:** Before forwarding a prompt, TavernAPI places a temporary hold on your balance equal to the visible input tokens plus `max_tokens` (Max Response Length) calculated at the model's output rate. When the reply completes, only the tokens actually used are charged and the unused hold is released right away.
- **No charge for failed requests:** If a request is rejected (`400`, `401`, `402`, `403`, `404`) or the upstream provider fails (`429`, `5xx`) before producing any reply text, nothing is charged. If a connection drops mid-stream, you pay only for the tokens that were generated.
- **Automatic prompt caching:** Server-side [prompt caching](https://tavernapi.com/guides/prompt-caching/) is applied automatically on every connection to lower repeated input costs in long chats.
- **Balance never expires:** Regular pay-as-you-go USD balance has no expiration date.
- **Optional 30-day credit packs:** In addition to pay-as-you-go balance, you can buy manual 30-day packs on the [pricing page](https://tavernapi.com/pricing/) (`$9` for `$10`, `$19` for `$23`, or `$39` for `$48` of credit across all five models).
- **One-time trial credit:** New accounts receive a `$0.30` trial credit that covers `gemini-4-argon` and `gemini-3.8-flash`.
- **Crypto top-ups and redeem codes:** You can top up in whole dollars from `$6` to `$500` using USDT or USDC through a NOWPayments checkout with no top-up fee from TavernAPI (see [how to pay with crypto](https://tavernapi.com/guides/pay-with-crypto/) and [payment troubleshooting](https://tavernapi.com/troubleshooting/#underpaid)), or apply a redeem code in the [console](https://tavernapi.com/console).

## Privacy and upstreams

- **No chat content storage:** TavernAPI does not store your prompts, character cards, or model replies. It logs only token counts, request time, model ID, and USD cost for billing (see the [Privacy Policy](https://tavernapi.com/privacy/)).
- **Official model upstreams:** Claude models (`claude-opus-5-5`, `claude-sonnet-5-5`) are served through AWS and Google Cloud; Gemini models (`gemini-4-argon`, `gemini-3.8-flash`) are served through Google AI Studio; `deepseek-v4-pro` is served through the official DeepSeek API.
- **Upstream safety filters:** Because traffic goes through official providers, each model provider's own safety filters still apply. Under our [Terms of Service](https://tavernapi.com/terms/), TavernAPI does not ban an account just because an upstream model refused a prompt.

## Picking any proxy safely

In roleplay communities, "proxy" can mean anything from a leaked-key paste link to a standard paid API gateway, so it pays to check who operates an endpoint, which upstream routes it uses, and what it writes to disk before sending private chats. Read [`docs/how-to-vet-a-proxy.md`](docs/how-to-vet-a-proxy.md) (or our [SillyTavern proxy guide](https://tavernapi.com/guides/sillytavern-proxy/)) for a vendor-neutral checklist you can apply to any service.

## Support

If you need help with a connection error or a top-up, reach out through the [contact page](https://tavernapi.com/contact/):

- **Telegram:** `@TavernAPI`
- **Discord:** `alexovout`
- **Email:** `support@tavernapi.com`

Do not post your `sk-tav-...` API key, account email address, or payment transaction details in public GitHub issues. Even in private support messages, never send your full API key; the last 4 characters shown in the console are enough.

## License

The code examples, schemas, and documentation in this repository are released under the MIT License ([`LICENSE`](LICENSE)).

TavernAPI is an independent service, not affiliated with or endorsed by SillyTavern, JanitorAI, Anthropic, Google, or DeepSeek.
