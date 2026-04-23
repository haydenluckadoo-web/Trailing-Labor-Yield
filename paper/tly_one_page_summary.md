# Trailing Labor Yield: One-Page Summary

Version: v0.9 public draft  
Companion to the TLY white paper

## Thesis

Trailing Labor Yield (TLY) is a compensation architecture for programmable
deferred compensation. It is not a new economic species and not a magic
replacement for equity, token vesting, phantom equity, or a normal deferred
bonus pool.

The narrower claim is more useful: TLY gives organizations a way to offer
stablecoin-denominated economic continuation after exit without making
governance tokens carry the whole compensation burden.

## The Problem

Contributor compensation usually forces organizations into a bad choice.
Startup equity can be illiquid and difficult for workers to value. DAO token
compensation is liquid, but it can create sell pressure on the governance
asset. Pension-like promises can become permanent liabilities.

TLY is aimed at the middle: liquid labor upside, no governance dilution, and
clearer departure economics than many option or token packages.

## The Three Layers

1. Pure TLY: the mathematical mechanism.
2. Stress Layer: reserve coverage, affordability, payout priority, pause
   semantics, and missed-epoch treatment.
3. Governance Wrapper: realized-compensation averaging, notice/pay-lock rules,
   anti-gaming controls, and parameter governance.

## The Mechanism

Active contributors receive:

- base pay;
- an active bonus equal to a small share of realized compensation history.

When a contributor exits:

- a defined realized-compensation snapshot becomes the initial trailing amount;
- production designs should use a trailing average, not a single terminal
  bonus;
- the payout tapers each period, for example by 5 percent annually;
- the claim expires after a fixed term, for example 25 years.

## Bounded Is Not Affordable

TLY can be bounded because old claims taper and expire. That does not make the
claim safe under arbitrary parameters. The burden depends on accrual rate,
taper, payroll growth, turnover, duration, margin, reserves, and treasury
funding policy.

At minimum, an organization should track:

- trailing burden / active payroll;
- trailing burden / margin or operating surplus;
- reserve coverage;
- forward claim coverage;
- stress thresholds and missed-epoch treatment.

## Who It Is For

Good candidates:

- mature DAOs with recurring revenue;
- profitable crypto-native firms;
- protocol service organizations;
- cooperatives and mission-driven organizations with reserve discipline;
- teams that want contributor upside without governance-token dilution.

Poor candidates:

- pre-revenue teams seeking immediate live-payout TLY, unless prefunded,
  delayed, or threshold-activated;
- volatile treasuries with no stable reserve policy;
- organizations unwilling to formalize compensation governance;
- firms that need pure lottery-style upside rather than cash obligations.

## Biggest Risks

- Treasury solvency: trailing claims require real funding.
- Stress semantics: paused claims may pause, partially pay, queue, catch up, or
  skip depending on disclosed rules.
- Legal and tax treatment: deferred compensation, payroll, securities, labor,
  and benefits rules may apply.
- Snapshot manipulation: production deployments should use trailing
  realized-compensation averaging.
- Parameter risk: excessive accrual or weak taper can create large obligations.

## Implementation

The EVM contracts are reference architecture, not production recommendations.
They demonstrate per-wallet state, pull claims, fixed-point taper math, and
active-pay priority. They do not implement every production wrapper, especially
realized-compensation averaging and legal-claim semantics.

## Practical Pilot

1. Choose payment asset and epoch length.
2. Set base pay and active accrual share.
3. Set trailing duration and taper.
4. Simulate payroll, turnover, margin, reserve coverage, and stress cases.
5. Define pause, partial-payment, queue/catch-up, and missed-epoch rules.
6. Define anti-gaming and legal wrapper rules before deployment.
