# Hacker News Launch Draft

## Title Options

1. Trailing Labor Yield: a stablecoin compensation mechanism for DAOs
2. TLY: tapering legacy payouts instead of token comp or illiquid equity
3. A white paper and EVM reference implementation for stablecoin-based contributor compensation

## Suggested Post Body

I’ve been working on a compensation mechanism called Trailing Labor Yield (TLY).

The basic idea is:

- contributors receive normal cash compensation while active;
- they also accrue a small bonus tied to cumulative historical pay;
- when they leave, their final active bonus becomes a tapering stablecoin payout for a fixed duration.

The goal is to sit between two common failure modes:

- illiquid startup-style upside that workers may never realize;
- governance-token compensation that workers must sell into the market.

The repo includes:

- a white paper;
- a one-page summary and FAQ;
- a Python simulator;
- EVM reference contracts for registry and treasury distribution.

I’d especially value criticism on:

- whether the bounded-liability argument is stated clearly;
- where this is actually a good fit operationally;
- how people would harden the legal and compensation-governance edge cases.

Repo:

- add GitHub link here
