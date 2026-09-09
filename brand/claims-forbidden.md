# Satstreet — Claims Forbidden

**Status:** DRAFT — companion to `claims-allowed.md`  
**Owner:** Compliance  
**How CI uses this file:** `scripts/check_claims.py` scans `templates/`, `drafts/`, and `prompts/` for the phrases below. This file and `claims-allowed.md` are excluded from the scan so we can document the ban.

Phrases are case-insensitive. A match fails the pull request.

## Never say

| Phrase | Why |
|---|---|
| CIPF member | Not claimed |
| CIPF-insured | Digital assets are not CIPF-protected |
| CDIC-insured | Not a bank deposit |
| FDIC-insured | Not a US bank |
| SIPC | Not applicable |
| risk-free | False |
| no risk | False |
| guaranteed return | False |
| guaranteed fill | Execution is not guaranteed |
| zero slippage | Not an approved claim |
| your bitcoin is insured | Insurance is not a client wrap |
| insured up to $100 million | Misstates custodian policy |
| US$320 million | Not Satstreet's approved figure |
| fully licensed securities dealer | Overstates Restricted Dealer |
| IIROC member | Not claimed |
| CIRO member | Not claimed |
| retail investors welcome | Retail is not eligible |
| open to everyone | Contradicts eligibility |
| available in the United States | Conflicts with current website terms until Legal withdraws ELIG-04 |
| available in the United Kingdom | Conflicts with current website terms |
| investment advice | Firm does not provide it |
| tax advice | Firm does not provide it |
| we are a bank | Disclaimer says otherwise |
| assets under management | Wrong metric |
| $5 billion | Volume must stay at approved C$4 billion lifetime figure |
| $5B | Same |
| SOC 2 of Satstreet | Not an approved claim |

## Allowed to appear only in claims files

The words “insurance”, “custody”, “Restricted Dealer”, and “C$4 billion” are allowed when they match `claims-allowed.md` wording. Do not invent new numbers around them.
