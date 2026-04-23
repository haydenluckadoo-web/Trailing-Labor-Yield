# Trailing Labor Yield (TLY)

Version: v0.9 public draft  
Status: mechanism design proposal

**Warning:** The Solidity contracts in this repository are unaudited reference
contracts. Do not route real capital through them, and do not treat them as
production-ready systems.

Trailing Labor Yield (TLY) is a stablecoin-denominated contributor
compensation mechanism for DAOs, protocol companies, cooperatives, and other
treasury-backed organizations. The claim is simple to describe but not free to
fund: active contributors receive normal pay plus a small bonus tied to their
historical pay, and departing contributors can receive a tapering trailing
payout after exit.

This repository is the Phase 1 public-release layout. The white paper and
supporting documents come first; the simulator and EVM reference implementation
stay close by so the mechanism can be pressure-tested instead of just read.

## Start Here

- White paper:
  [paper/tly_white_paper_v0.9_public_draft.md](paper/tly_white_paper_v0.9_public_draft.md)
- White paper PDF:
  [paper/tly_white_paper_v0.9_public_draft.pdf](paper/tly_white_paper_v0.9_public_draft.pdf)
- PDF export source:
  [paper/tly_white_paper_v0.9_public_draft_pdf_source.md](paper/tly_white_paper_v0.9_public_draft_pdf_source.md)
- One-page summary:
  [paper/tly_one_page_summary.md](paper/tly_one_page_summary.md)
- FAQ and objections:
  [paper/tly_faq_objections.md](paper/tly_faq_objections.md)
- Simulator:
  [sim/app.py](sim/app.py)
- Solidity contracts:
  [dao/contracts/ContributorRegistry.sol](dao/contracts/ContributorRegistry.sol)
  and
  [dao/contracts/TreasuryDistributor.sol](dao/contracts/TreasuryDistributor.sol)
- Core mechanism, in one line:
  while active, contributors receive base pay plus an active bonus; on exit,
  the final active bonus is snapshotted; in legacy state, that amount tapers
  into the trailing payout.

## Repository Layout

- `paper/`
  - public white paper
  - PDF-friendly export source
  - one-page summary
  - FAQ and objections
  - publication documents
- `sim/`
  - Python simulator and Streamlit entrypoint
- `dao/`
  - EVM reference contracts, Foundry config, and tests
- `release/phase1_v0.9_public_draft/`
  - publication checklist, GitHub setup notes, release manifest, and launch copy

## What This Release Is Trying To Do

Phase 1 is deliberately narrow:

- publish cleanly;
- make the mechanism legible quickly;
- show the economic burden and the implementation path;
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
- Feedback is most useful on the math, simulator assumptions, and EVM claim
  architecture. See [CONTRIBUTING.md](CONTRIBUTING.md). High-level critique
  belongs in GitHub Discussions; scoped bugs belong in Issues.
