# Grok Bot roster (Satstreet internal)

Grok Bot has no public create-agent API from this workspace.
These files are the source of truth. In the Grok Bot app: New → Create new agent → paste Name, Job, Description from the matching file.

All bots:
- Draft only. Never send email, post, or DM.
- No client names, wallets, account numbers, or KYC.
- No Florida availability or lending product claims unless `brand/claims-allowed.md` has an approved line.
- Public Satstreet facts only. Website terms still exclude UK/US clients.

| Bot | File | Mode |
|---|---|---|
| First-Call Packer | `first-call-packer.md` | On demand |
| Referral Engine | `referral-engine.md` | Weekly automation |
| Silent-Book Re-activator | `silent-book.md` | On demand |
| Onboarding Friction Mapper | `onboarding-friction.md` | On demand |
| Florida Gatekeeper | `florida-gatekeeper.md` | On demand + Daily Intel |
| Lending Thesis Clerk | `lending-thesis.md` | Weekly automation |
| Claims Diff | `claims-diff.md` | On demand / PR |
| Desk Standup | `desk-standup.md` | Daily automation 08:00 ET |
