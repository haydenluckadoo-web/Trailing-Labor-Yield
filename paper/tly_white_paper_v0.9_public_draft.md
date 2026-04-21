# Trailing Labor Yield: A White Paper

Version: v0.9 public draft  
Status: mechanism design proposal  
Repository references: `sim/`, `dao/contracts/`

## Abstract

Most contributor upside is trapped in illiquid equity or paid in volatile
tokens that workers must sell. Trailing Labor Yield (TLY) is a stablecoin-
denominated compensation mechanism that pays normal cash compensation while
active, adds a small bonus tied to cumulative historical pay, and converts the
final active bonus into a fixed-duration trailing payout when the contributor
exits. The payout tapers over time, giving former contributors continued
economic exposure to organizational survival without issuing governance tokens
or creating untapered pension-like claims. TLY is not appropriate for every
organization; it requires reserve planning, transparent compensation
governance, and jurisdiction-specific legal review.

## Executive Summary

- TLY offers an alternative to the usual tradeoff between illiquid equity and
  volatile token compensation.
- Contributors receive base pay while active, plus an active bonus equal to a
  small share of their historical pay pool.
- When a contributor leaves, their most recent active bonus is snapshotted into
  a trailing stablecoin payout.
- The trailing payout tapers, for example by 5 percent annually, and expires
  after a fixed period, for example 25 years.
- The taper makes the alumni liability a runoff process rather than a
  perpetuity.
- The EVM implementation uses per-wallet state and pull claims, so the treasury
  never loops over all alumni.
- Active contributor pay can be prioritized during stress by pausing trailing
  claims.
- TLY is a mechanism design proposal, not legal, tax, accounting, or investment
  advice.

## Who This Is For

This paper is written for founders, DAO operators, contributor pods, protocol
treasurers, compensation committees, and workers negotiating long-term upside.
It assumes basic familiarity with stablecoins, treasury management, and smart
contract-based payroll, but it does not require reading Solidity or the Python
simulator before understanding the mechanism.

## Plain-English Mechanism

TLY pays contributors normal cash compensation while they are active. It also
grants a small bonus tied to cumulative historical pay. When a contributor
leaves, their final active bonus is converted into a trailing stablecoin payout
for a fixed number of periods. That payout tapers over time, so former
contributors retain upside without creating permanent, growing liabilities for
the organization.

The mechanism has two states:

1. Active state: the contributor receives base pay and earns a compounding
   active bonus.
2. Legacy state: the contributor no longer earns base pay, but can claim a
   trailing payout based on their final active bonus.

The key design choice is that TLY pays in a treasury reserve asset, such as a
stablecoin, rather than a governance token. It separates labor compensation
from governance-asset dilution.

## Mechanism At A Glance

```mermaid
flowchart LR
    A[Active pay] --> B[Historical pay pool]
    B --> C[Active bonus accrual]
    C --> B
    C --> D[Exit snapshot]
    D --> E[Tapered legacy payout]
```

## A Worked Example

Consider one contributor paid annually.

| Input | Value |
| --- | ---: |
| Base pay | $100,000 per year |
| Historical pay pool entering year | $250,000 |
| Active accrual share | 1% |
| Annual taper after exit | 5% |
| Trailing duration | 25 years |

The active bonus for the year is:

$$
\text{Active Bonus}
=
(\$250{,}000 + \$100{,}000) \times 0.01
=
\$3{,}500.
$$

If the contributor exits after that year, the protocol snapshots the final
active bonus as the initial trailing amount:

$$
R = \$3{,}500.
$$

With a 5 percent annual taper, the first three trailing payouts are:

| Year after exit | Payout |
| ---: | ---: |
| 1 | $3,325.00 |
| 2 | $3,158.75 |
| 3 | $3,000.81 |

The total undiscounted payout over 25 years is approximately:

$$
\sum_{s=1}^{25} 3500 \times 0.95^s
\approx
\$48{,}054.
$$

Bounded means the obligation runs off structurally rather than compounding
forever; it does not mean every parameter set is prudent or fully prefunded.
This is not a promise that every organization can afford this schedule. It is a
transparent rule that can be simulated before adoption. At the organization
level, the burden depends on payroll growth, turnover, active accrual rate,
trailing duration, and the taper.

## The Compensation Problem

Traditional startup equity solves cash preservation for the company but often
fails workers. The worker receives paper exposure to a private capital
structure with uncertain liquidity, exercise costs, preferred-share overhang,
and limited control. The claim is called ownership, but for many workers it
behaves like a long-dated option with unclear realizable value.

DAO token compensation improves liquidity but introduces reflexivity. If
contributors receive governance tokens and sell them for living expenses, the
protocol pays labor by pressuring the same asset that coordinates governance.
If the token price falls, more tokens are required to pay the same real wage.
That can create a procyclical compensation loop.

Pensions and perpetuities fail in the opposite direction. They reduce worker
uncertainty by creating employer uncertainty. Fixed, permanent obligations can
accumulate into a large inactive claimant base. This is the Iceberg Effect:
the visible current payroll is only the surface; the hidden mass is the stock
of future obligations.

TLY sits between these structures. It gives workers a portable claim on future
treasury cash flows, but the claim tapers and expires.

## What TLY Is

TLY is a compensation rule that converts labor history into a trailing
cash-flow claim.

- It is not equity because it does not transfer governance or ownership.
- It is not ordinary token compensation because it does not require issuing or
  selling the governance asset.
- It is not a traditional pension because the payout is based on the final
  active bonus and tapers over a fixed horizon.
- It is not a generic revenue share because the claim is contributor-specific
  and derives from historical labor compensation.

TLY provides survival-contingent cash-flow exposure, not the uncapped
capital-appreciation upside of equity.

In the reference design, the active bonus is:

$$
\text{Active Bonus}
=
(\text{Historical Pay Pool} + \text{Base Pay})
\times
\text{Accrual Share}.
$$

When the contributor exits, the final active bonus becomes the initial trailing
amount. The trailing claim then pays:

$$
\text{Trailing Payout}_s
=
\text{Initial Trailing Amount} \times \rho^s,
$$

where $s$ is the number of epochs after departure and $\rho$ is the per-epoch
taper factor. For annual epochs and a 5 percent taper, $\rho = 0.95$.

## Why The Liability Stays Bounded

The liability stays bounded because old claims lose weight over time. A
trailing claim with initial amount $R$, taper factor $\rho < 1$, and duration
$K$ has total undiscounted payout:

$$
\sum_{s=1}^{K} R\rho^s
=
R\rho\frac{1-\rho^K}{1-\rho}.
$$

At a 5 percent annual taper and 25-year duration:

$$
\rho = 0.95,
$$

and:

$$
R \times 0.95 \times \frac{1-0.95^{25}}{0.05}
\approx
13.73R.
$$

This number is the lifetime multiple of the final active bonus, not of base
salary. The final active bonus is itself controlled by the active accrual
share, typically modeled at 1 percent.

At the organization level, three forces interact:

1. Low active accrual limits new trailing claims.
2. Payroll growth makes old cohorts smaller relative to current payroll.
3. The taper reduces the weight of every legacy cohort over time.

Under the simulator's baseline growth intuition of roughly 4 percent gross
payroll growth and the EVM convention that the first legacy claim receives
$R\rho$, the approximate steady burden is:

| Turnover | Active bonus ratio | Approx. trailing burden |
| ---: | ---: | ---: |
| 8% | 9.35% | 7.9% of payroll |
| 10% | 7.92% | 8.3% of payroll |
| 30% | 3.12% | 9.8% of payroll |

These values are illustrative rather than universal. The important point is
structural: the taper converts a potentially permanent alumni obligation into
a stationary runoff process. No artificial cap on an individual contributor's
historical pay pool is needed for stationarity, although organizations may
still adopt governance controls around pay changes and exit timing.

**Design Conditions**

TLY is most defensible when the following conditions hold:

- low active accrual share;
- taper factor below one;
- finite trailing duration;
- credible treasury funding policy;
- governance controls around exit timing and pay changes.

## Comparison With Adjacent Mechanisms

| Feature | Startup equity | DAO token comp | Pension / perpetuity | Revenue share | TLY |
| --- | --- | --- | --- | --- | --- |
| Liquid while active | Usually no | Usually yes | No | Sometimes | Yes, for base and active pay |
| Direct governance dilution | Often yes | Yes | No | No | No |
| Treasury cash obligation | No near-term cash | Often indirect | Yes | Yes | Yes |
| Bounded long-run liability | Cap table bounded, value uncertain | Issuance may expand | Often weak or no | Depends on contract | Yes, via taper and term |
| Portable after exit | Sometimes, but illiquid | Yes | Yes | Sometimes | Yes |
| Depends on market price | High | High | Low | Medium | Low if paid in stablecoins |
| Depends on treasury solvency | Indirect | Indirect | High | High | High |
| Legal / tax complexity | High | High | High | Medium to high | Medium to high |
| Fit for pre-revenue startups | Strong | Common but volatile | Weak | Weak | Limited unless prefunded, delayed, or threshold-activated |

TLY is not categorically better than these mechanisms. It is designed for a
narrow target: liquid labor upside paid outside the governance asset, with
long-run obligations tapered by rule.

## Where TLY Fits Best

TLY is most attractive for organizations that already have, or can reasonably
develop, stable treasury capacity.

Good candidates include:

- mature DAOs with recurring protocol revenue;
- profitable crypto-native firms;
- protocol-adjacent service organizations;
- cooperatives or mission-driven organizations with reserve discipline;
- treasury-backed ecosystems that want alumni alignment without token sell
  pressure.

Poor candidates include:

- pre-revenue startups seeking immediate live-payout TLY, unless prefunded,
  delayed, or threshold-activated;
- organizations with highly volatile treasuries and no stable reserve policy;
- teams unwilling to formalize compensation governance;
- firms that need pure upside asymmetry rather than bounded cash obligations;
- organizations that cannot manage jurisdiction-specific labor, tax, and
  deferred-compensation requirements.

## Operational Design And Governance Rules

The reference EVM architecture has two contracts:

| Contract | Role |
| --- | --- |
| `ContributorRegistry.sol` | stores contributor status, base pay, historical pay pool, final active bonus, departure epoch, and claim checkpoints |
| `TreasuryDistributor.sol` | holds the payment token, computes active compensation, computes trailing claims, and transfers funds |

The system uses per-contributor accounting. The registry stores each
contributor's `historicalPayPool`, `lastActiveBonus`, `initialLegacyAmount`,
`departureEpoch`, and `lastLegacyClaimEpoch`.

The treasury uses pull payments:

- active contributors call `claimActiveComp()`;
- legacy contributors call `claimTrailingYield()`.

The treasury never iterates through all alumni. That is essential for gas
safety.

The governance design separates roles:

- `POD_ADMIN_ROLE`: operational sub-DAO or multisig that can add contributors,
  remove contributors, and update base pay.
- `DAO_ADMIN_ROLE`: treasury-level role that can pause and unpause legacy
  claims during stress.

If legacy claims are paused, active compensation remains claimable. This keeps
current labor funded during bear markets or treasury stress.

## Capitalization Models For TLY

The pre-revenue question is central. TLY is a cash-flow claim. It should not be
adopted casually by organizations that lack a path to funding future claims.

Possible capitalization models include:

1. Reserve-funded model: the treasury prefunds expected trailing claims from
   stable reserves.
2. Margin-funded model: each epoch's claims are paid from operating surplus.
3. Hybrid model: early-stage contributors receive a small TLY schedule, with
   larger accrual activated after revenue maturity.
4. Milestone activation: legacy payouts begin only after revenue, treasury, or
   runway thresholds are met.
5. Buffer-pool model: a portion of active payroll or operating margin funds a
   reserve pool for future trailing claims.

These models can be combined. For example, an early protocol might accrue TLY
internally but delay claim activation until a stablecoin reserve threshold is
met. The design question is not whether the claim can be written on-chain. It
is whether the organization has a credible funding policy.

## Risks, Limitations, And Failure Modes

### Treasury Solvency And The Cash-Flow Paradox

TLY is not for cash-starved organizations with no realistic treasury path. It
works best for profitable, treasury-backed, or reserve-capitalized entities.
Pre-revenue organizations may need delayed activation, reserve escrows, smaller
initial accrual rates, or hybrid token-cash structures.

Trailing claims should be described precisely. Depending on legal structure,
they may be contingent claims rather than guaranteed debt. If treasury funds
are insufficient, the organization must define whether missed claims accrue,
queue, partially defer, or remain claimable only when the treasury is funded.

### Legal, Tax, And Deferred Compensation Risk

TLY may trigger deferred compensation, payroll, securities, labor, tax,
employment-benefit, or accounting issues depending on jurisdiction. In some
jurisdictions, the legacy claim may need to be implemented through an off-chain
employment, contractor, deferred-compensation, or bonus-rights agreement rather
than treated as a purely on-chain entitlement. Actual deployment may require
wrappers, employer-of-record structures, written off-chain agreements, entity
design, and tax withholding processes.

This paper is a mechanism design proposal, not legal, tax, accounting, or
investment advice.

### Terminal Bonus Manipulation

If the trailing claim is based only on the last active bonus, parties may try
to manipulate the terminal period. Defenses include:

- using a rolling average of recent active bonuses instead of a single final
  bonus;
- locking base pay changes near expected departure;
- requiring notice periods before legacy conversion;
- requiring governance review for exceptional compensation changes;
- capping snapshot growth relative to a trailing average, while still avoiding
  a cap on the contributor's historical pay pool itself.

The current reference contract snapshots `lastActiveBonus`. Production
deployments may choose a more conservative snapshot policy.

### Treasury Stress And Insolvency

The Solidity reference includes `pauseLegacyClaims()` so a DAO admin can block
legacy withdrawals while preserving active compensation. This is a priority
rule, not a complete insolvency framework.

Before deployment, organizations should define:

- whether paused claims accrue or simply wait;
- whether claimants can later catch up using aggregate claims;
- whether partial payment is allowed;
- whether legacy claims are legally enforceable debt or contingent protocol
  benefits;
- what disclosures contributors receive before accepting the structure.

### Governance Abuse And Favoritism

TLY depends on credible compensation administration. A pod admin that can
update base pay or time departures can influence future trailing claims.

Mitigations include:

- transparent compensation policies;
- multisig-controlled contributor administration;
- published parameter changes;
- auditable events for base pay updates and exits;
- notice periods and review windows near departure;
- periodic reporting of active payroll, active bonuses, and projected trailing
  burden.

### Parameter Risk

The mechanism is bounded only under coherent parameters. A high accrual rate,
weak taper, very long duration, or low-growth payroll can create excessive
cash obligations. The simulator should be used before governance adopts or
changes parameters.

## Implementation Path And Pilot Model

A practical pilot can be small and explicit:

1. Choose the payment asset, usually a stablecoin or treasury reserve asset.
2. Choose epoch length, such as monthly or annual.
3. Choose an initial accrual share, such as 1 percent.
4. Choose a trailing duration, such as 25 annual epochs or 300 monthly epochs.
5. Convert the annual taper into a per-epoch WAD factor.
6. Simulate expected burden under growth, wage, turnover, revenue, and margin
   assumptions.
7. Define treasury funding policy and stress rules.
8. Define compensation governance, including pod admin authority and review
   rules near departure.
9. Deploy contracts or begin with an off-chain legal agreement that mirrors the
   same equations.
10. Publish recurring reports comparing actual burden against simulated burden.

The repository contains two practical tools:

- `sim/app.py`: Streamlit dashboard for scenario analysis.
- `dao/contracts/`: EVM-compatible reference contracts for registry and
  treasury distribution.

## Legal And Regulatory Disclaimer

This document is for mechanism design and technical research only. It is not
legal, tax, accounting, employment, securities, benefits, or investment advice.
On-chain enforceability does not eliminate off-chain legal obligations.
Organizations considering TLY should obtain jurisdiction-specific advice before
deployment.

## Conclusion

TLY offers an alternative to the common compensation tradeoff between illiquid
equity and volatile token issuance. It can separate contributor upside from
governance-asset dilution while giving the organization a modeled, tapering
obligation.

The active state rewards tenure through compounding accrual. The legacy state
turns the final active bonus into a trailing stablecoin claim. The taper turns
an alumni obligation into a runoff process. The EVM design maps this process
to per-wallet state, pull-based claims, bounded missed-epoch processing, and
stress controls for legacy withdrawals.

The claim is not free. It must be funded, governed, disclosed, and legally
structured. But for reserve-disciplined organizations, TLY can create a more
legible bargain: contributors receive liquid, trailing upside; the
organization preserves governance integrity and can model the long-run burden
before making the promise.

## Appendix A: Full Formulas

Lowercase subscripts refer to contributor-level quantities. Aggregate
quantities omit contributor indexing. Unless otherwise stated, all quantities
are per epoch.

### A.1 Notation

- $B_{i,t}$: contributor $i$'s base pay in epoch $t$.
- $H_{i,t}$: contributor $i$'s historical pay pool entering epoch $t$.
- $\alpha$: active accrual share.
- $A_{i,t}$: active bonus.
- $R_i$: initial trailing amount after exit.
- $\delta$: taper rate.
- $\rho = 1-\delta$: per-epoch taper factor.
- $K$: maximum trailing duration.
- $q$: turnover rate.
- $G$: gross payroll growth factor.
- $L_t$: aggregate trailing payout in epoch $t$.

### A.2 Active State

Contributor-level active bonus:

$$
A_{i,t} = \alpha(H_{i,t} + B_{i,t}).
$$

Contributor-level historical-pool update:

$$
H_{i,t+1} = H_{i,t} + B_{i,t} + A_{i,t}.
$$

Aggregate simulator update with turnover:

$$
H_{t+1} = (H_t + B_t + A_t)(1-q).
$$

### A.3 Legacy State

Exit snapshot:

$$
R_i = A_{i,\tau_i}.
$$

Trailing payout $s$ epochs after departure:

$$
Y_{i,s} = R_i\rho^s.
$$

Total finite-horizon trailing payout:

$$
\sum_{s=1}^{K} R_i\rho^s
=
R_i\rho\frac{1-\rho^K}{1-\rho}.
$$

Infinite-horizon upper bound:

$$
\sum_{s=1}^{\infty} R_i\rho^s
=
R_i\frac{\rho}{1-\rho}.
$$

### A.4 Aggregate Burden Approximation

New legacy cohort from turnover:

$$
N_t = qA_t.
$$

Aggregate trailing payout:

$$
L_t = \sum_{j=1}^{K} N_{t-j}\rho^{j-1}.
$$

Payroll growth:

$$
B_{t+1}=GB_t.
$$

Active bonus ratio:

$$
m_t = \frac{A_t}{B_t}.
$$

Historical-pool ratio:

$$
h = \frac{H_t}{B_t}.
$$

Steady-state relationship:

$$
h = \frac{(1-q)(1+\alpha)}{G}(h+1).
$$

Let:

$$
c = \frac{(1-q)(1+\alpha)}{G}.
$$

If $c < 1$:

$$
h = \frac{c}{1-c}
$$

and:

$$
m = \frac{\alpha}{1-c}.
$$

Approximate burden ratio:

$$
\frac{L_t}{B_t}
\approx
qm\sum_{j=1}^{K}\frac{\rho^{j-1}}{G^j}.
$$

Infinite-horizon upper bound:

$$
\frac{L_t}{B_t}
\leq
\frac{qm}{G-\rho}.
$$

If the first post-departure claim receives $R_i\rho$, as in the EVM
convention:

$$
\frac{L_t}{B_t}
\leq
\frac{qm\rho}{G-\rho}.
$$

## Appendix B: Simulation Assumptions

The Python simulator in `sim/app.py` and `sim/baseline_dollars.py` models the
macro version of TLY using cohorts.

Core inputs include:

- `horizon_periods`;
- `initial_workers`;
- `worker_growth`;
- `wage_per_worker`;
- `wage_growth`;
- `accrual_share`;
- `turnover_rate`;
- `legacy_payout_years`;
- `annuity_decay_rate`, which corresponds to the TLY taper rate;
- `revenue_multiplier`;
- `gross_margin`.

The simulator computes:

```text
base_payroll = workers * wage
active_bonus = (historical_pay_pool + base_payroll) * accrual_share
legacy_payout = cohort_amount * (1 - taper_rate) ^ cohort_age
historical_pay_pool_next =
    (historical_pay_pool + base_payroll + active_bonus) * (1 - turnover_rate)
```

The simulator is intentionally stylized. It does not model legal enforceability,
tax treatment, default litigation, stablecoin depegging, claimant mortality,
or endogenous contributor behavior. It is a planning tool for burden dynamics,
not a solvency guarantee.

## Appendix C: Smart Contract Architecture

The reference EVM implementation lives in `dao/contracts`.

### C.1 Contributor Registry

`ContributorRegistry.sol` stores:

- contributor status: none, active, legacy, removed;
- payout address;
- base pay per epoch;
- historical pay pool;
- last active bonus;
- initial legacy amount;
- joined epoch;
- last settled active epoch;
- departure epoch;
- last legacy claim epoch.

`POD_ADMIN_ROLE` can:

- add contributors;
- update payout addresses;
- update base pay;
- remove contributors into legacy status.

Only the configured treasury distributor can settle active epochs and mark
legacy claims as paid.

### C.2 Treasury Distributor

`TreasuryDistributor.sol` holds the payment token and computes claims.

Active claim:

```solidity
activeBonus =
    (state.historicalPayPool + state.basePayPerEpoch).mulWadDown(accrualShareWad);
```

Legacy claim:

```solidity
uint256 taperMultiplierWad =
    WadMath.rpowWad(taperFactorPerEpochWad, elapsedEpochs);

claimable += state.initialLegacyAmount.mulWadDown(taperMultiplierWad);
```

The treasury uses OpenZeppelin `AccessControl`, `SafeERC20`, and
`ReentrancyGuard`.

### C.3 Pull Claims And Gas Safety

The system uses pull claims:

- `claimActiveComp()` for active contributors;
- `claimTrailingYield()` for legacy contributors.

Legacy missed-epoch claims are processed oldest-first and capped by
`maxEpochsPerClaim`. This makes transaction cost independent of the total
number of alumni.

### C.4 Tranche Priority

`pauseLegacyClaims()` blocks legacy withdrawals while preserving active
compensation. This supports active-pay priority during treasury stress.

## Appendix D: FAQ And Objections

### Is TLY just a pension?

No. A pension is typically a broad retirement benefit with employer-specific
legal and actuarial treatment. TLY is a contributor-specific trailing cash-flow
claim based on a final active bonus. It tapers and expires.

### Is TLY just revenue share?

No. A generic revenue share usually pays a percentage of revenue. TLY pays a
defined trailing amount based on contributor compensation history. It may be
funded by revenue, reserves, margin, or a hybrid policy, but the claim formula
is not a direct revenue percentage.

### Why not just give equity?

Equity may be better for early-stage startups that need pure upside and cannot
support cash obligations. TLY is better suited to organizations that want
liquid, stablecoin-denominated labor upside without transferring governance or
ownership.

### Why not just use token vesting?

Token vesting is liquid and simple, but it ties compensation to token price and
can create sell pressure on the governance asset. TLY can reduce that coupling
by paying in a reserve asset.

### What if the treasury fails?

TLY depends on treasury solvency. The reference implementation includes
active-pay priority and pausable legacy claims, but this does not eliminate
funding risk. Organizations must define whether claims are contingent, queued,
partially paid, or legally enforceable.

### Can someone game the exit bonus?

Yes, if governance is weak. Production deployments should consider rolling
average snapshots, notice periods, review of exceptional pay changes, and
rules that lock base pay near departure.

### Does this create tax or legal issues?

Potentially. TLY may implicate deferred compensation, payroll, securities,
labor, tax, benefits, or accounting rules. Legal design is jurisdiction-
specific.

### Why not cap historical pay?

The reference mechanism intentionally avoids artificial caps because long-tenure
contributors are supposed to earn larger trailing claims. Aggregate stability
comes from low active accrual, payroll growth, finite duration, and tapering
legacy obligations. Governance may still restrict manipulation of terminal
compensation.
