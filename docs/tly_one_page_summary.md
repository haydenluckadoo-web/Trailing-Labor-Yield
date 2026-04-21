# Trailing Labor Yield: One-Page Summary

Version: v0.9 public draft  
Companion to the TLY white paper

## The Problem

Contributor compensation usually forces organizations into a bad choice.
Startup equity can be illiquid and difficult for workers to value. DAO token
compensation is liquid, but it can create sell pressure on the governance
asset. Pension-like promises can become permanent liabilities.

## The Mechanism

Trailing Labor Yield (TLY) pays contributors in a stable treasury asset while
they are active and gives them a trailing payout after they leave.

Active contributors receive:

- base pay;
- an active bonus equal to a small share of historical pay.

When a contributor exits:

- their final active bonus is snapshotted;
- that amount becomes the basis for a fixed-duration trailing payout;
- the payout tapers each period, for example by 5 percent annually;
- the claim expires after a fixed term, for example 25 years.

## Why It Stays Bounded

TLY is bounded because old claims taper. With a 5 percent annual taper, the
claim weight is multiplied by 0.95 each year. Over time, old alumni claims lose
weight while current payroll grows and new claims enter slowly through a low
active accrual rate.

In the baseline simulator, a 1 percent active accrual and 5 percent annual taper
produce a long-run trailing burden in the approximate 5-10 percent range of
active payroll across ordinary turnover regimes. This is not automatic for all
parameters. It depends on accrual rate, taper, payroll growth, turnover,
duration, and treasury funding policy.

## Who It Is For

Good candidates:

- mature DAOs with recurring revenue;
- profitable crypto-native firms;
- protocol service organizations;
- cooperatives and mission-driven organizations with reserve discipline;
- teams that want contributor upside without governance-token dilution.

Poor candidates:

- pre-revenue teams seeking immediate live-payout TLY, unless prefunded, delayed,
  or threshold-activated;
- volatile treasuries with no stable reserve policy;
- organizations unwilling to formalize compensation governance;
- firms that need pure upside rather than cash obligations.

## Biggest Risks

- Treasury solvency: trailing claims require real funding.
- Legal and tax treatment: deferred compensation, payroll, securities, labor,
  and benefits rules may apply.
- Terminal bonus manipulation: weak governance can inflate exit snapshots.
- Admin abuse: contributor roles and pay changes must be transparent.
- Parameter risk: excessive accrual or weak taper can create large obligations.

## Implementation

The reference EVM implementation uses two contracts:

- `ContributorRegistry.sol`: stores contributor status, base pay, historical
  pay pool, final active bonus, departure epoch, and claim checkpoints.
- `TreasuryDistributor.sol`: holds stablecoins, computes active pay, computes
  trailing claims, and transfers funds.

Claims are pull-based. The treasury never loops through all alumni. Active pay
has priority: `pauseLegacyClaims()` can pause trailing claims while active
contributors continue to claim active compensation.

## Practical Pilot

1. Choose payment asset and epoch length.
2. Set base pay and active accrual share.
3. Set trailing duration and taper.
4. Simulate payroll, turnover, and burden in `sim/app.py`.
5. Define treasury reserve policy and legal wrapper.
6. Deploy or mirror the equations in an off-chain agreement.
