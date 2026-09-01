# satstreet-ops

Private operating system for Satstreet internal marketing, sales, and compliance comms.

This repository is the source of truth for **approved language**. Models (Grokbot, Claude, ChatGPT) draft from these files. Humans approve anything external.

## Layout

```text
brand/          claims-allowed.md, claims-forbidden.md
prompts/        model instructions
templates/      reusable external copy (CI-scanned)
drafts/         work in progress (CI-scanned)
scripts/        CI checkers
.github/        GitHub Actions
```

## Claims rule

1. Update `brand/claims-allowed.md` first.
2. Open a pull request.
3. CI must pass.
4. Compliance reviews the diff.
5. Only then may drafts use the new wording.

`claims-allowed.md` is currently **DRAFT — not approved for external use**.

## CI

On every pull request and push to `main`:

- `scripts/check_claims.py` confirms claims files exist and scans drafts for forbidden phrases
- `actionlint` checks workflow YAML
- Gitleaks scans for secrets

Enable Actions on this private repo the first time if GitHub prompts you. Make the `CI` workflow a required status check on `main` once it is green.

## Do not commit

- Client names, KYC files, trade tickets, wallet addresses
- API keys for OpenAI, Anthropic, xAI, or GitHub
- Anything that is not already public or internally approved for this repo
