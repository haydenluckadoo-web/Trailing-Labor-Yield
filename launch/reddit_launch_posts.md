# Reddit Launch Drafts

Adapt each post to the target community's rules and norms before publishing.

## Post 1: Mechanism Design Angle

### Suggested Title

Trailing Labor Yield: programmable deferred comp between equity and token sell pressure

### Suggested Body

I’ve published a draft compensation architecture called Trailing Labor Yield
(TLY): a historical-compensation-indexed trailing labor claim.

It pays contributors in a stable treasury asset while active, adds a small
active bonus tied to a historical compensation base, and converts a defined
exit snapshot into a tapering payout after exit. The idea is not that this is
universally better than equity, phantom equity, token vesting, or a deferred
bonus pool. The idea is narrower: make the post-exit contributor claim
formulaic, stablecoin-denominated, and easier to model.

The paper splits the design into three layers:

- Pure TLY: the mathematical mechanism;
- Stress Layer: reserve coverage, payout priority, pause / partial payment /
  queue / catch-up semantics;
- Governance Wrapper: realized-compensation averaging, notice/pay-lock rules,
  and parameter control.

The repo includes a white paper, a simulator, and Solidity reference contracts.
I’d appreciate critique on the economics, the stress semantics, and where this
design clearly does or does not fit.

Link:

- add GitHub link here

## Post 2: EVM / Smart Contract Angle

### Suggested Title

Reference Solidity architecture for tapering contributor payouts in a DAO treasury

### Suggested Body

I put together a reference EVM implementation for a compensation architecture
called TLY.

The architecture uses:

- a contributor registry;
- a treasury distributor;
- pull-based active and legacy claims;
- fixed-point taper math;
- bounded missed-epoch processing;
- pausable legacy claims so active compensation can keep priority during
  treasury stress.

Important caveat: the contracts are reference architecture, not production
wrappers. The white paper recommends trailing realized-compensation averaging
for production snapshots, plus explicit stress rules for pause, partial
payment, queue/catch-up, and missed epochs.

Would love feedback from Solidity engineers on the claim flow, access control,
state model, and what production-hardening would be required.

Link:

- add GitHub link here

## Post 3: Founder / Operator Angle

### Suggested Title

Could DAOs offer stablecoin upside after exit without using governance tokens?

### Suggested Body

I wrote up a compensation architecture called Trailing Labor Yield (TLY), a
historical-compensation-indexed trailing labor claim that tries to answer a
narrow question:

How do you give contributors real liquid upside without relying on illiquid
equity or volatile token comp?

The structure is:

- base pay while active;
- a small compounding bonus tied to a historical compensation base;
- a defined exit snapshot;
- a tapering payout after exit for a fixed duration.

The pitch is not that this works everywhere. The paper is explicit about
treasury limits, pre-revenue constraints, legal risk, stress-state semantics,
and the need for compensation governance. It seems most plausible for
treasury-backed DAOs and reserve-disciplined crypto-native organizations.

Link:

- add GitHub link here
