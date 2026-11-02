# Contributing

Fixes to the documentation and code examples in this repository are welcome as pull requests.

## Where to send questions and bug reports

- **Documentation and example fixes:** Open a pull request or issue in this repository.
- **Service problems, billing, and account questions:** Contact support at https://tavernapi.com/contact/ instead of opening a public GitHub issue. For common API and connection errors, see https://tavernapi.com/troubleshooting/.

## Rules for pull requests and issues

- **Never include API keys or account emails:** Do not paste real `sk-tav-...` keys or account email addresses in issues, commits, or pull requests. Use `sk-tav-...` as a placeholder and read keys from the `TAVERNAPI_API_KEY` environment variable.
- **Keep examples small and dependency-light:** Each script in `examples/` should stay short and focused on a single task. `examples/doctor.py` uses only the Python standard library so it runs without extra packages.
- **Do not edit prices by hand:** `data/models.json` and the `README.md` model table are generated from the website's price data at https://tavernapi.com/pricing/. If a price looks wrong, open an issue instead of editing those files by hand.
