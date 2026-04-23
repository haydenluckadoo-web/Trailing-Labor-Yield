# Trailing Labor Yield (TLY)

Version: v0.9 public draft  
Status: mechanism design proposal

**Warning:** The Solidity contracts in this repository are unaudited reference
contracts. Do not route real capital through them, and do not treat them as
production-ready systems.

Trailing Labor Yield (TLY) is a compensation architecture for programmable
deferred compensation. It gives contributors a stablecoin-denominated trailing
claim after exit without making governance tokens carry the whole compensation
burden.

The short version: active contributors receive normal pay plus a small bonus
tied to realized compensation history; on exit, a defined snapshot becomes a
tapering trailing payout. The claim is easy to describe. Funding it is the hard
part.

## What This Repository Contains

- `paper/`: the public manuscript, PDF source, one-page summary, FAQ, and
  diagrams.
- `sim/`: economic model, baseline scenarios, and Streamlit dashboard.
- `dao/`: Solidity reference contracts, Foundry configuration, and tests.
- `release/phase1_v0.9_public_draft/`: launch notes, checklist, manifest, and
  PDF export instructions.

## Start Here

For readers:

- Start with the one-page summary:
  [paper/tly_one_page_summary.md](paper/tly_one_page_summary.md)
- Then read the main white paper:
  [paper/tly_white_paper_v0.9_public_draft.md](paper/tly_white_paper_v0.9_public_draft.md)
- PDF version:
  [paper/tly_white_paper_v0.9_public_draft.pdf](paper/tly_white_paper_v0.9_public_draft.pdf)

For researchers:

- Read the Pure TLY, Stress Layer, and Governance Wrapper sections in the white
  paper.
- Then inspect the simulator:
  [sim/app.py](sim/app.py)
- Check the FAQ and objections:
  [paper/tly_faq_objections.md](paper/tly_faq_objections.md)

For builders:

- Read the contract notes in the white paper appendix.
- Inspect the registry and treasury distributor:
  [dao/contracts/ContributorRegistry.sol](dao/contracts/ContributorRegistry.sol)
  and
  [dao/contracts/TreasuryDistributor.sol](dao/contracts/TreasuryDistributor.sol)
- Treat the contracts as reference architecture, not a production deployment
  template.

## Mechanism Shape

```text
active contributor
  -> base pay + active bonus
  -> realized-compensation history grows
  -> exit snapshot
  -> legacy runoff claim
  -> taper until expiration
```

```text
normal treasury state
  -> active pay remains claimable
  -> legacy claims follow schedule

stress treasury state
  -> active pay priority
  -> legacy claims pause, partially pay, queue, or skip according to disclosed rules
```

## Recommended Reading Order

1. One-page summary / executive overview.
2. Main paper.
3. Simulator walkthrough and scenario assumptions.
4. Contract architecture notes.
5. FAQ and objections.

## Limitations And Non-Claims

- TLY is not legal, tax, accounting, securities, employment, or investment
  advice.
- TLY is not universally better than equity, phantom equity, token vesting, or
  a normal deferred-bonus pool.
- TLY is not safe under arbitrary parameters. Bounded is not the same thing as
  affordable.
- TLY is not a substitute for treasury discipline, reserve policy, anti-gaming
  rules, or jurisdiction-specific legal work.
- The reference contracts do not implement every production recommendation,
  especially realized-compensation averaging and full legal-wrapper semantics.

## What This Release Is Trying To Do

Phase 1 is deliberately narrow:

- publish cleanly;
- make the mechanism legible quickly;
- show the economic burden and implementation path;
- invite criticism before commercialization.

## Not In Scope For This Release

- product pricing;
- factory contracts;
- legal wrappers;
- audit work;
- deployment sales.

## Notes

- The canonical publication draft is `v0.9 public draft`.
- The PDF binary is checked in. Regeneration instructions live at
  [release/phase1_v0.9_public_draft/PDF_EXPORT.md](release/phase1_v0.9_public_draft/PDF_EXPORT.md).
- The simulator and Solidity code here are reference implementations for the
  mechanism, not production-ready audited systems.
- Feedback is most useful on the math, simulator assumptions, treasury-stress
  semantics, governance wrapper, and EVM claim architecture. See
  [CONTRIBUTING.md](CONTRIBUTING.md). High-level critique belongs in GitHub
  Discussions; scoped bugs belong in Issues.
