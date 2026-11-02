# Changelog

Public-facing changes to TavernAPI and this repository, newest first.

## 2026-11-03

- Enabled CORS on `/v1` and `/v1beta` so browser-based apps (JanitorAI, RisuAI web, and Agnaistic) can call the endpoints directly.
- Updated TavernAPI's SillyTavern presets to pass the character and persona names on every SillyTavern source, including Google AI Studio. Re-download the preset from https://tavernapi.com/console to update your local file (guide: https://tavernapi.com/guides/presets/).
- Published the [Troubleshooting](https://tavernapi.com/troubleshooting/) and [Pay with crypto](https://tavernapi.com/guides/pay-with-crypto/) guides on the website.
- Published this repository.

## 2026-11-02

- Added native Claude Messages API (`POST /v1/messages`) and Gemini (`/v1beta`) endpoints for SillyTavern's Claude and Google AI Studio sources.
- Set the minimum crypto top-up to `$6` (whole dollars from `$6` to `$500` via USDT or USDC).
- Unpaid crypto orders now close automatically after 1 hour; payments that arrive later are still credited once confirmed.

## 2026-11-01

- Public launch with `claude-opus-5-5`, `claude-sonnet-5-5`, `gemini-4-argon`, `gemini-3.8-flash`, and `deepseek-v4-pro` on `https://tavernapi.com/v1`.
- Published per-token USD prices on https://tavernapi.com/pricing/, with a machine-readable copy in `data/models.json`.
- Added a one-time `$0.30` trial credit for new accounts on `gemini-4-argon` and `gemini-3.8-flash`.
- Added 30-day credit packs (`$9` for `$10`, `$19` for `$23`, and `$39` for `$48` of credit).
