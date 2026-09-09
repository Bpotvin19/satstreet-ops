# satstreet-ops

Operating-system prototype for Satstreet internal marketing, sales, and compliance comms.

The status and approval log in each claims file govern whether wording may be used externally. Models may use DRAFT material only for internal drafting. Humans approve anything external.

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
- claims-scanned directories accept only explicitly supported UTF-8 text formats; every other format fails closed
- matching applies Unicode compatibility normalization, removes zero-width formatting characters, and collapses whitespace
- `actionlint` checks workflow YAML
- Gitleaks scans for secrets

The checker is a guardrail, not semantic review. Homoglyph substitutions, paraphrases, images, and meaning expressed without a listed phrase may evade automated matching. Human Compliance review remains mandatory.

The GitHub repository is currently public and personally owned. Confirm whether it should be private or transferred to a Satstreet organization before adding sensitive internal material. Make the `CI` workflow a required status check on `main` once it is green.

## Do not commit

- Client names, KYC files, trade tickets, wallet addresses
- API keys for OpenAI, Anthropic, xAI, or GitHub
- Anything that is not already public or internally approved for this repo
