# Reddit Launch Drafts

Adapt each post to the target community's rules and norms before publishing.

## Post 1: Mechanism Design Angle

### Suggested Title

Trailing Labor Yield: a compensation design between illiquid equity and token sell pressure

### Suggested Body

I’ve published a draft mechanism called Trailing Labor Yield (TLY).

It pays contributors in a stable treasury asset while active, adds a small active bonus tied to historical pay, and converts the final active bonus into a tapering payout after exit. The idea is to create portable upside without turning contributor compensation into continuous governance-token sell pressure.

The repo includes a white paper, a simulator, and Solidity reference contracts. I’d appreciate critique on the economics, the bounded-liability argument, and where this design clearly does or does not fit.

Link:

- add GitHub link here

## Post 2: EVM / Smart Contract Angle

### Suggested Title

Reference Solidity architecture for tapering contributor payouts in a DAO treasury

### Suggested Body

I put together a reference EVM implementation for a compensation mechanism called TLY.

The architecture uses:

- a contributor registry;
- a treasury distributor;
- pull-based active and legacy claims;
- fixed-point taper math;
- bounded missed-epoch processing;
- pausable legacy claims so active compensation can keep priority during treasury stress.

Would love feedback from Solidity engineers on the claim flow, access control, and whether the state model feels production-realistic.

Link:

- add GitHub link here

## Post 3: Founder / Operator Angle

### Suggested Title

Could DAOs pay contributors in stablecoins and still offer long-term upside?

### Suggested Body

I wrote up a mechanism called Trailing Labor Yield (TLY) that tries to answer a narrow question:

How do you give contributors real liquid upside without relying on illiquid equity or volatile token comp?

The structure is:

- base pay while active;
- a small compounding bonus tied to historical pay;
- a tapering payout after exit for a fixed duration.

The pitch is not that this works everywhere. The paper is explicit about treasury limits, pre-revenue constraints, legal risk, and the need for compensation governance. But it does seem like a plausible fit for treasury-backed DAOs and reserve-disciplined crypto-native organizations.

Link:

- add GitHub link here
