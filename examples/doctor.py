#!/usr/bin/env python3
"""TavernAPI connection doctor.

Checks the URL, API key and model ID you put into SillyTavern, JanitorAI or any
OpenAI-compatible app, and explains in plain words what is wrong.
Standard library only (Python 3.8+).

    python doctor.py
    python doctor.py --url https://tavernapi.com/v1 --model gemini-4-argon

The key is read from the TAVERNAPI_API_KEY environment variable, or asked for
without echo. It is never printed or saved. With a key, the doctor sends one
tiny chat request (a few tokens, a small fraction of a cent).
"""
import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "https://tavernapi.com/v1"
DEFAULT_MODEL = "gemini-3.8-flash"
HELP = "https://tavernapi.com/troubleshooting/"
TIMEOUT = 60

# Error code (or HTTP status) -> (anchor on the troubleshooting page, what it means).
DIAGNOSIS = {
    "missing_api_key": ("401-invalid-api-key", "No API key reached the server. Paste your sk-tav-... key into the key field."),
    "invalid_api_key": ("401-invalid-api-key", "The key was rejected: it is incomplete, has a space in it, was deleted in the console, or belongs to another service. Paste it again or create a new key in the console (it is shown only once)."),
    "insufficient_balance": ("402-insufficient-balance", "Your balance is lower than the hold for this request (visible input + max response length at the output price). Top up, lower Max Response Length, or pick a cheaper model."),
    "trial_restricted": ("403-trial-or-preset", "Trial credit only works with gemini-4-argon and gemini-3.8-flash. Pick one of those, or add credit to unlock every model."),
    "preset_locked": ("403-trial-or-preset", "Your preset uses locked TavernAPI entries that your account has not unlocked yet."),
    "account_banned": ("403-trial-or-preset", "This account is suspended. Contact support: https://tavernapi.com/contact/"),
    "model_not_found": ("404-model-not-available", "This model ID is not available. Use one of the IDs listed above, exactly as written."),
    "not_found": ("404-not-found", "The URL path is wrong. The base URL is https://tavernapi.com/v1 (apps that want the full URL: https://tavernapi.com/v1/chat/completions)."),
    "model_required": ("400-bad-request", "No model was sent. Pick a model in your app."),
    "messages_required": ("400-bad-request", "The request had no messages."),
    "no_route": ("5xx-server-errors", "This model is temporarily unavailable. Try another model."),
    429: ("429-rate-limit", "Too many requests at once, or the model provider is busy. Wait a few seconds and try again."),
    502: ("5xx-server-errors", "The model provider failed or the connection dropped. Try again in a moment."),
    503: ("5xx-server-errors", "The model is temporarily unavailable. Try another model."),
}


def say(tag, text):
    print("[" + tag + "] " + text)


def request(method, url, key=None, body=None):
    """Returns (status, content_type, parsed_json_or_None, raw_text)."""
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("User-Agent", "tavernapi-doctor/1.0")
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    if key:
        req.add_header("Authorization", "Bearer " + key)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
            status, ctype, raw = res.status, res.headers.get("Content-Type", ""), res.read()
    except urllib.error.HTTPError as err:
        status, ctype, raw = err.code, err.headers.get("Content-Type", ""), err.read()
    text = raw.decode("utf-8", "replace")
    try:
        parsed = json.loads(text)
    except ValueError:
        parsed = None
    return status, ctype, parsed, text


def check_url(raw):
    """Normalizes the URL the user typed and reports common mistakes."""
    url = raw.strip()
    ok = True
    if url != raw:
        say("warn", "The URL has spaces around it. Remove them in your app.")
    if not url.startswith("https://"):
        say("fail", "The URL must start with https://")
        return None, False
    if url.endswith("/chat/completions"):
        say("info", "This is the full URL that web apps like JanitorAI want. SillyTavern's Custom source and SDKs want the base URL that ends in /v1.")
        url = url[: -len("/chat/completions")]
    url = url.rstrip("/")
    if url.endswith("/v1/v1"):
        say("fail", "/v1 appears twice. Use " + url[: -len("/v1")])
        url = url[: -len("/v1")]
        ok = False
    if not url.endswith("/v1"):
        say("warn", "The base URL should end with /v1, for example " + DEFAULT_URL + " (only SillyTavern's Google AI Studio source uses https://tavernapi.com without /v1).")
        url = url + "/v1"
        ok = False
    return url, ok


def main():
    parser = argparse.ArgumentParser(description="Check a TavernAPI connection and explain errors.")
    parser.add_argument("--url", default=DEFAULT_URL, help="base URL from your app (default: %(default)s)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="model ID to test (default: %(default)s)")
    args = parser.parse_args()
    healthy = True

    print("TavernAPI connection doctor")
    print("-" * 27)

    base, url_ok = check_url(args.url)
    healthy = healthy and url_ok
    if base is None:
        return 1
    say("info", "Testing " + base)

    # 1. Model list: public, no key needed.
    try:
        status, ctype, parsed, _ = request("GET", base + "/models")
    except (urllib.error.URLError, OSError) as err:
        say("fail", "Could not reach the server: " + str(getattr(err, "reason", err)) + ". Check the URL and your internet connection.")
        return 1
    if status != 200 or not isinstance(parsed, dict):
        hint = " It returned a web page instead of the API, so the path is wrong." if "html" in ctype else ""
        say("fail", "GET /models answered HTTP " + str(status) + "." + hint)
        say("help", HELP + "#404-not-found")
        return 1
    ids = [m.get("id") for m in parsed.get("data", []) if isinstance(m, dict)]
    say("ok", "Model list reachable: " + (", ".join(ids) if ids else "(empty)"))
    model = args.model.strip()
    if ids and model not in ids:
        say("warn", "'" + model + "' is not in that list, so requests with it will fail with 404.")
        healthy = False

    # 2. Key: from the environment, or a hidden prompt when run in a terminal.
    # (Both streams are checked: on Windows the NUL device also reports isatty.)
    key = os.environ.get("TAVERNAPI_API_KEY") or ""
    if not key and sys.stdin.isatty() and sys.stdout.isatty():
        key = getpass.getpass("API key (input hidden, Enter to skip): ")
    if not key.strip():
        say("info", "No key given, so the chat test was skipped.")
        return 0 if healthy else 1
    if key != key.strip() or " " in key.strip():
        say("warn", "The key contains spaces. Copy it again without spaces.")
        key = key.strip()
        healthy = False
    if not key.startswith("sk-tav-"):
        say("warn", "TavernAPI keys start with sk-tav-. This looks like a key from another service.")

    # 3. One tiny chat request.
    body = {
        "model": model,
        "messages": [{"role": "user", "content": "Reply with the single word OK."}],
        "max_tokens": 16,
        "stream": False,
    }
    try:
        status, _, parsed, text = request("POST", base + "/chat/completions", key=key, body=body)
    except (urllib.error.URLError, OSError) as err:
        say("fail", "The chat request did not get through: " + str(getattr(err, "reason", err)))
        return 1

    if status == 200:
        usage = (parsed or {}).get("usage") or {}
        say("ok", "Key accepted and " + model + " answered (" + str(usage.get("total_tokens", "?")) + " tokens). Your connection works.")
        return 0 if healthy else 1

    error = (parsed or {}).get("error") or {}
    code = error.get("code")
    message = error.get("message") or text[:200]
    say("fail", "HTTP " + str(status) + (" " + code if code else "") + ": " + str(message))
    anchor, meaning = DIAGNOSIS.get(code) or DIAGNOSIS.get(status) or ("", "")
    if meaning:
        say("why", meaning)
    say("help", HELP + ("#" + anchor if anchor else ""))
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(130)
