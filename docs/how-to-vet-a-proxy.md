# How to vet a SillyTavern or JanitorAI proxy

In roleplay communities, a "proxy" is the API endpoint URL you paste into SillyTavern, JanitorAI, or another app to connect external AI models. Free proxies often run on leaked keys, while paid providers range from legitimate gateways to unverified resellers. Use this checklist to evaluate any API provider before you send a prompt or add funds; for setup steps and deeper background, see the [full SillyTavern proxy guide](https://tavernapi.com/guides/sillytavern-proxy/).

## Four things people call a proxy

Community threads and setup guides use the word "proxy" for four different tools:

| What people call it | Where it appears | What it does | Do you need it to chat with Claude, Gemini, or DeepSeek? |
| --- | --- | --- | --- |
| **Model API endpoint** | SillyTavern **API Connections** (`Custom` or `Reverse Proxy`); JanitorAI **API Settings → Proxy** | Sends your prompt over HTTPS to a remote model API and streams back the reply. | **Yes** — unless you use an upstream provider's key directly or run a local model. |
| **SillyTavern's outgoing network proxy** | `config.yaml` in your SillyTavern folder | Routes SillyTavern's outbound traffic through a local HTTP or SOCKS tunnel. | **No** — only needed if your local network blocks outbound connections. |
| **Web reverse proxy** | Self-hosting guides (`nginx`, `Caddy`) | Adds HTTPS and a domain in front of a self-hosted SillyTavern server. | **No** — only needed if you expose your own SillyTavern server to the internet. |
| **Old local middleware** | Outdated 2023–2024 guides (such as `simple-proxy-for-tavern`) | Ran a local script to translate API formats before SillyTavern added native support. | **No** — modern SillyTavern connects to OpenAI-compatible, Claude, and Gemini endpoints directly. |

## Risks of free or shared-key proxies

Running frontier models costs money on every turn. When an endpoint offers free or shared access without a clear way to pay for compute, you take on four risks:

- **Keys get revoked without warning.** Endpoints built on leaked keys, abused trials, or unauthorized billing get shut down as soon as upstream providers detect the traffic, cutting off your chat mid-scene.
- **The operator can read and log chats.** Every prompt, character card, and reply passes through the proxy server in readable text. Without a real privacy policy, an operator can store or publish your messages.
- **The model may not be the one advertised.** Because the proxy server controls routing, it can accept a request for a flagship Claude or Gemini model and silently answer with a smaller, cheaper model.
- **There is no support or refund path.** Informal servers rarely publish terms or run support channels, leaving you with no recourse if a paid slot or shared endpoint disappears.

## The checklist

Run any provider through these seven checks before you connect your app or add balance:

1. **It names its upstream per model.** Check the documentation to confirm which official cloud or API channel serves each model (such as AWS, Google Cloud, Google AI Studio, or the official DeepSeek API) rather than relying on vague "private routes."
2. **You pay for your own usage with dated public prices.** Look for a public pricing table with a visible update date that lists per-token rates (or clear credit pack rules). You should generate a personal API key in your own account rather than using a shared password.
3. **A privacy policy says what is stored and what is not.** Read the privacy page before sending private writing. It should explicitly separate billing metadata (token counts, request time, model, and cost) from message content and character cards.
4. **A reachable operator publishes terms and more than one contact channel.** Check for public Terms of Service and at least two working ways to reach a person—such as email, Telegram, or Discord—if a top-up or request fails.
5. **The model you get matches the model you picked.** Test the endpoint with a prompt or multi-character scene you know well to verify that reasoning depth, prose style, and speed match the genuine model.
6. **The price is plausible.** Server-side prompt caching and volume tiers can lower per-token bills, but frontier compute is never free. Be wary of "free unlimited Claude" or flat-rate access priced below real API costs.
7. **You can start small and check the usage log.** Begin with a free trial or the smallest top-up, send a few test replies, and verify in the usage log that token counts and charges match the published rates.

## Red flags

Skip any provider that shows these warning signs:

- **A password shared in a Discord channel** or paste page instead of individual accounts and private API keys.
- **No public pricing page**, or rates hidden behind registration or a private group.
- **"Unlimited" claims** for expensive models like Claude or Gemini at a low flat fee.
- **Asks for your other providers' API keys**, account passwords, or wallet recovery phrases.
- **No way to contact anyone**, or a site with no Terms of Service and no Privacy Policy.
- **Payment in a chat DM to a personal wallet** instead of an automated checkout in your account console.

## How TavernAPI answers the checklist

Here is how [TavernAPI](https://tavernapi.com) maps to the same seven points:

- **Named official upstreams:** Five 1M-context models run through official providers—`claude-opus-5-5` and `claude-sonnet-5-5` through AWS and Google Cloud, `gemini-4-argon` and `gemini-3.8-flash` through Google AI Studio, and `deepseek-v4-pro` through the official DeepSeek API.
- **Dated public prices and private keys:** Per-token USD rates are listed on the [pricing page](https://tavernapi.com/pricing/) and in [`data/models.json`](../data/models.json). You create your own `sk-tav-...` key in the [console](https://tavernapi.com/console).
- **Clear privacy policy:** TavernAPI does not store message content; it logs only token counts, request time, model, and cost ([Privacy Policy](https://tavernapi.com/privacy/)).
- **Reachable operator and published terms:** Public [Terms of Service](https://tavernapi.com/terms/) are posted on the site, with support on Telegram (`@TavernAPI`), Discord (`alexovout`), and email (`support@tavernapi.com`) via the [contact page](https://tavernapi.com/contact/).
- **Plausible per-token pricing:** Usage is billed per token in USD with automatic [prompt caching](https://tavernapi.com/guides/prompt-caching/), balance that never expires (top-ups from $6 to $500), and optional 30-day credit packs ($9 for $10, $19 for $23, $39 for $48).
- **Small trial and request logs:** New accounts get a one-time $0.30 trial credit for `gemini-4-argon` and `gemini-3.8-flash`, crypto top-ups start at $6 via NOWPayments ([how to pay with crypto](https://tavernapi.com/guides/pay-with-crypto/)), and every turn's tokens and cost appear in the [console](https://tavernapi.com/console).

**Honest limits:** TavernAPI is not free after the $0.30 trial credit is used. Because requests go through official providers, the model providers' own safety filters still apply (TavernAPI does not ban an account just because an upstream model refused a prompt). Finally, TavernAPI serves only the five Claude, Gemini, and DeepSeek models listed above.
