# TavernAPI error reference

When a request fails, TavernAPI returns an OpenAI-compatible JSON error body with a human-readable `message`, an error `type`, and a machine-readable `code` (shown in SillyTavern's error pop-up or server console):

```json
{"error": {"message": "...", "type": "...", "code": "..."}}
```

This page is a compact lookup reference for SillyTavern, JanitorAI, and custom code; full step-by-step explanations live on [https://tavernapi.com/troubleshooting/](https://tavernapi.com/troubleshooting/).

## First checks

- **Source:** In SillyTavern, set **API** to `Chat Completion` and **Chat Completion Source** to `Custom (OpenAI-compatible)` (or expand **Reverse Proxy** under the native `Claude` or `Google AI Studio` source).
- **URL:** Use `https://tavernapi.com/v1` for SillyTavern Custom and Claude sources, `https://tavernapi.com` (no `/v1`) for SillyTavern's Google AI Studio source, and `https://tavernapi.com/v1/chat/completions` for JanitorAI or other apps that ask for the full endpoint path.
- **API key:** Paste your full `sk-tav-...` key into **Custom API Key** (or **Proxy Password** on native SillyTavern sources) with no spaces before or after it.
- **Model ID:** Click **Connect** to load the dropdown, or type one of the five exact model IDs: `claude-opus-5-5`, `claude-sonnet-5-5`, `gemini-4-argon`, `gemini-3.8-flash`, or `deepseek-v4-pro`.
- **Balance:** Open [https://tavernapi.com/console](https://tavernapi.com/console) and check that your USD balance or `$0.30` trial credit is above zero (trial credit works with `gemini-4-argon` and `gemini-3.8-flash`).

## By status code

| Status | Code | Message | Usually means | Fix | Charged? |
|---|---|---|---|---|---|
| 401 | `invalid_api_key` | `Invalid API key` | Key is cut off, has spaces, was deleted, or comes from another service. | Paste your `sk-tav-...` key again or create a new one in the console (shown once). [more](https://tavernapi.com/troubleshooting/#401-invalid-api-key) | No |
| 401 | `missing_api_key` | `Missing API key...` | No key header reached the server. | Paste `sk-tav-...` into **Custom API Key**, **Proxy Password**, or `Authorization: Bearer sk-tav-...`. [more](https://tavernapi.com/troubleshooting/#401-invalid-api-key) | No |
| 402 | `insufficient_balance` | `Insufficient balance` | Remaining balance is below the temporary pre-request hold for this turn. | Lower **Max Response Length** (`max_tokens`), pick a cheaper model, or top up in the console. [more](https://tavernapi.com/troubleshooting/#402-insufficient-balance) | No |
| 403 | `trial_restricted` | `Model "<id>" is not available with trial credit. Add credit to unlock it.` | Your account only has `$0.30` trial credit and requested a non-trial model. | Switch to `gemini-4-argon` or `gemini-3.8-flash`, or add credit in the console to unlock all five models. [more](https://tavernapi.com/troubleshooting/#403-trial-or-preset) | No |
| 403 | `preset_locked` | `"<preset pack name>" is not included in your account...` | Your active preset contains `[[tav:...]]` blocks your account has not unlocked. | Switch to a local preset, toggle off locked `[[tav:...]]` entries, or unlock the preset in the console. [more](https://tavernapi.com/troubleshooting/#403-trial-or-preset) | No |
| 403 | `account_banned` | `Account suspended` | The account has been suspended under the Terms of Service. | Contact support with your account email. [more](https://tavernapi.com/troubleshooting/#403-trial-or-preset) | No |
| 404 | `model_not_found` | `Model "<id>" is not available` | Model ID has a typo, a provider prefix, or is not one of the five supported IDs. | Refresh the model list or enter `claude-opus-5-5`, `claude-sonnet-5-5`, `gemini-4-argon`, `gemini-3.8-flash`, or `deepseek-v4-pro`. [more](https://tavernapi.com/troubleshooting/#404-model-not-available) | No |
| 404 | `not_found` | `Not found` | Request URL path is wrong (such as `/v1/v1` or `/chat/completions` in a base URL field). | Enter `https://tavernapi.com/v1` as base URL, or `https://tavernapi.com/v1/chat/completions` in JanitorAI. [more](https://tavernapi.com/troubleshooting/#404-not-found) | No |
| 400 | `model_required` | `model is required` | Request body did not include a model ID. | Click **Connect** in your app and select a model before sending. [more](https://tavernapi.com/troubleshooting/#400-bad-request) | No |
| 400 | `messages_required` | `messages must be a non-empty array` | Outgoing `messages` array is empty or was stripped by a script. | Send at least one message and check prompt-modifying extensions or regex rules. [more](https://tavernapi.com/troubleshooting/#400-bad-request) | No |
| 400 | `preset_block_unknown` | `Unknown preset block [[tav:...]]...` | Local preset file uses an outdated or hand-edited `[[tav:...]]` placeholder. | Download the latest preset JSON from the console and import it again. [more](https://tavernapi.com/troubleshooting/#400-bad-request) | No |
| 429 | `upstream_error` (`type`: `rate_limit_error`) | `Upstream error (429)` | Too many concurrent requests or the upstream provider is temporarily busy. | Wait a few seconds and regenerate the reply. [more](https://tavernapi.com/troubleshooting/#429-rate-limit) | No |
| 502 | `upstream_error` | `Upstream error (502)` | Upstream model provider failed or dropped the connection. | Wait a few seconds and try the request again. [more](https://tavernapi.com/troubleshooting/#5xx-server-errors) | Only tokens generated if cut mid-reply; none before text starts |
| 503 | `no_route` | `No upstream route is configured for this model` | Model is temporarily unavailable across configured upstream routes. | Switch to another model while the route recovers. [more](https://tavernapi.com/troubleshooting/#5xx-server-errors) | No |
| 500 | `preset_block_error` (and other `preset_...` codes) | `preset_...` | Server error while expanding a locked `[[tav:...]]` preset block. | Test without the preset (or disable locked entries) and contact support with the time and model ID. [more](https://tavernapi.com/troubleshooting/#5xx-server-errors) | No |

## The 402 hold, explained

Before forwarding a request, TavernAPI places a temporary hold on your balance equal to the visible input tokens plus your full **Max Response Length** (`max_tokens`) calculated at the model's output rate. Once the reply finishes, only the tokens actually used are charged and the unused hold is released right away (if the provider fails before producing any text, nothing is charged). For example, using round illustrative numbers on an expensive model, if you have `$0.15` left and set `max_tokens` to `16000` on a long chat, the pre-request hold might be `$0.25` even though a normal `400`-token reply would cost only a few cents. Because `$0.15` is below that `$0.25` hold, the request stops with `402 insufficient_balance` until you lower **Max Response Length** (such as `1024` or `2048`), switch to a lower-cost model ([pricing](https://tavernapi.com/pricing/)), or add credit in the [console](https://tavernapi.com/console).

## No error code, but something is wrong

- **Can't connect or model list stays blank:** Confirm the URL starts with `https://` with no spaces, and if you use SillyTavern's native Claude or Google AI Studio source, expand **Reverse Proxy** and put your `sk-tav-...` key in **Proxy Password** ([troubleshooting](https://tavernapi.com/troubleshooting/#cant-connect), [SillyTavern setup guide](https://tavernapi.com/guides/sillytavern-setup/)).
- **Empty or cut-off replies:** Raise **Max Response Length** (`max_tokens`) to `1024`–`2048` so models that think before answering do not spend the entire budget on internal reasoning before writing the visible reply; upstream providers' own safety filters can also end or blank a reply ([troubleshooting](https://tavernapi.com/troubleshooting/#empty-or-cut-off)).
- **Preset not applied or raw `[[tav:...]]` text appears:** Check that your active connection points to `https://tavernapi.com/v1`, the TavernAPI preset is selected with its prompt entries enabled, and you have imported the latest preset file from the console ([troubleshooting](https://tavernapi.com/troubleshooting/#preset-not-applied), [presets guide](https://tavernapi.com/guides/presets/)).
- **Higher bill than expected:** Roleplay apps re-send your chat history and character card every turn; automatic prompt caching lowers repeated input cost, so higher charges usually come from a very long context or a cache miss after a break or an edit near the top of the prompt ([troubleshooting](https://tavernapi.com/troubleshooting/#higher-bill), [prompt caching guide](https://tavernapi.com/guides/prompt-caching/)).

## Payments

Crypto top-ups in USDT or USDC (`$6` to `$500` in whole dollars, with no top-up fee from TavernAPI) and 30-day credit packs go through a NOWPayments checkout; see [how to pay with crypto](https://tavernapi.com/guides/pay-with-crypto/) for network selection and withdrawal steps.

- **Underpaid (`Partially paid`):** When an exchange subtracts its withdrawal fee from the sent amount, the portion that arrived is credited in proportion automatically; create a new checkout order if you want to add the difference, and do not send a second transfer to the old address ([more](https://tavernapi.com/troubleshooting/#underpaid)).
- **Order shows `Expired`:** Unpaid orders close after 1 hour, but a transfer already sent that confirms on-chain after the 1-hour window still credits your balance automatically ([more](https://tavernapi.com/troubleshooting/#expired)).
- **Payment not credited yet:** Blockchain confirmations usually take a few minutes; if your console Billing page has not updated after about 30 minutes, contact support with the TXID, coin, network, amount, and account email ([more](https://tavernapi.com/troubleshooting/#not-credited)).
- **Overpaid:** Only the invoiced order amount is credited automatically when you send extra; contact support with your TXID and account email so the extra amount can be added ([more](https://tavernapi.com/troubleshooting/#overpaid)).
- **Wrong network or coin:** If you withdrew over a network or coin that did not match the checkout screen, contact support right away with your TXID, coin, network, and amount ([more](https://tavernapi.com/troubleshooting/#wrong-network)).

## Still stuck

Run `python examples/doctor.py` from this repository to check your base URL, `GET /v1/models`, and `sk-tav-...` key from a terminal without printing or saving the key.

If you need help from a person, reach out on [https://tavernapi.com/contact/](https://tavernapi.com/contact/) (Telegram `@TavernAPI`, Discord `alexovout`, or email `support@tavernapi.com`; see [contact details](https://tavernapi.com/troubleshooting/#contact)):

- **API or preset issues:** Send your account email, model ID, approximate timestamp (with time zone), HTTP status and error `code`, preset name (if used), and the output of `examples/doctor.py`.
- **Payment issues:** Send your account email, transaction hash (TXID), coin, network, and amount sent.
- **Never send your full `sk-tav-...` API key.** If support needs to identify a key, send only the last 4 characters shown in [https://tavernapi.com/console](https://tavernapi.com/console).
