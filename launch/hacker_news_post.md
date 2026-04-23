# Hacker News Launch Draft

## Title Options

1. Trailing Labor Yield: programmable deferred compensation for contributors
2. TLY: stablecoin trailing payouts without governance-token sell pressure
3. A white paper, simulator, and EVM reference implementation for contributor deferred comp

## Suggested Post Body

I’ve been working on a compensation architecture called Trailing Labor Yield
(TLY): a historical-compensation-indexed trailing labor claim.

The basic idea is:

- contributors receive normal cash compensation while active;
- they also accrue a small bonus tied to a historical compensation base;
- when they leave, a defined exit snapshot becomes a tapering stablecoin payout
  for a fixed duration.

The goal is not to invent a wholly new economic category. It is to make a
specific deferred-compensation promise more explicit, programmable, and
stress-testable.

The draft splits the design into three layers:

- Pure TLY: the math of active accrual, exit snapshot, and legacy runoff;
- Stress Layer: affordability, reserve coverage, payout priority, and pause /
  queue / catch-up semantics;
- Governance Wrapper: anti-gaming rules, realized-compensation averaging,
  pay-lock rules, and parameter control.

The repo includes:

- a white paper;
- a one-page summary and FAQ;
- a Python simulator;
- EVM reference contracts for registry and treasury distribution.

I’d especially value criticism on:

- whether the bounded-but-not-automatically-affordable argument is clear;
- whether the stress semantics are the right ones to expose;
- whether realized-compensation averaging is the right production default;
- where this is actually a good fit operationally.

Repo:

- add GitHub link here
