# Trailing Labor Yield: A White Paper

Version: v0.9 public draft  
Status: mechanism design proposal  
Repository references: `sim/`, `dao/contracts/`

## Abstract

Trailing Labor Yield (TLY) is a historical-compensation-indexed trailing labor
claim: a compensation architecture in which past compensated contribution
determines a finite, tapering stream of post-exit cash flows. Its components
resemble familiar instruments: deferred compensation, phantom participation,
contingent benefits, and runoff liabilities. Its novelty is architectural. It
links cumulative eligible compensation with the organization, finite runoff,
funding discipline, and production governance into one modelable structure. The
stablecoin- and EVM-based design presented here is a reference implementation
of that broader structure, chosen because reserve assets, programmable
settlement, and per-wallet claim accounting fit the mechanism naturally. This
first paper is concept-first, with formal mechanism sections where the
mechanism needs them and practical deployment layers where treasury,
governance, and legal choices change the worker-side promise.

## Executive Summary

- TLY is a historical-compensation-indexed trailing labor claim: compensated
  contribution history determines a finite stream of post-exit cash flows.
- TLY gives organizations a way to offer stablecoin-denominated economic
  continuation after exit without making governance tokens carry the whole
  compensation burden.
- Pure TLY defines the mechanism: active pay, active bonus accrual, a cumulative
  eligible-compensation base with the organization, and a tapering claim over a
  fixed term.
- The same mechanism can sit under different worker-side promises: a contingent
  protocol benefit, a contract-wrapped deferred-compensation right, or a
  reserve-backed / partially prefunded claim.
- The Stress Layer and Governance Wrapper decide whether the claim is prudent:
  reserve coverage, payout priority, stress semantics, eligible-compensation
  rules, ledger integrity, exceptional-comp review, and parameter control.
- The stablecoin/EVM design is a reference implementation for programmable
  settlement, not a complete legal, tax, accounting, employment, or production
  deployment package.

## Why This Exists

Workers are often offered either illiquid equity, volatile token compensation,
or ordinary cash with no continuing upside. Organizations have the mirror-image
problem: they need credible contributor upside, but governance tokens are a
fragile compensation sink and permanent obligations can become a hidden balance
sheet problem.

TLY tries to make a narrower bargain legible. It gives contributors continuing
economic exposure after exit while keeping the claim finite, tapering, and
modelable. The point is not that the claim is cheap. The point is that the
organization can see the obligation before pretending it is manageable.

## Who This Is For

This paper is written for founders, DAO operators, contributor pods, protocol
treasurers, compensation committees, and workers negotiating long-term upside.
It assumes basic familiarity with stablecoins, treasury management, and smart
contract-based payroll. It does not assume that the reader wants to start in
the Solidity or the simulator. The mechanism should make sense before any of
that.

## Thesis And Scope

The claim is architectural. TLY combines familiar economic components into a
specific compensation structure: compensated labor history determines a finite,
tapering post-exit cash-flow claim. That structure can be analyzed apart from
any one implementation, but the stablecoin/EVM version is a strong first
deployment surface because programmable settlement, reserve assets, and
per-wallet claim accounting fit the mechanism naturally.

TLY is not automatically better than equity, RSUs, phantom equity, token
vesting, or a normal deferred-bonus pool. It is most interesting where an
organization wants modelable economic continuation without turning governance
tokens into the compensation sink. Put more plainly, TLY gives organizations a
way to offer stablecoin-denominated economic continuation after exit without
making governance tokens carry the whole compensation burden.

This draft is concept-first. It formalizes the mechanism where precision
matters, but it does not pretend to settle every legal wrapper, tax treatment,
accounting treatment, or production treasury policy. Those choices are not
decorations. They change what the worker has actually been promised.

The paper uses three layers:

1. Pure TLY: the mathematical mechanism only.
2. Stress Layer: affordability, reserve coverage, payout-priority rules, pause
   semantics, and missed-epoch treatment.
3. Governance Wrapper: eligible-compensation rules, compensation-ledger
   integrity, exceptional compensation review, contributor-admin controls, and
   parameter control.

## Plain-English Mechanism

TLY pays contributors normal cash compensation while they are active. It also
grants a small bonus tied to a historical compensation base. When a contributor
leaves, the same cumulative compensation base determines the initial trailing
cash-flow claim for a fixed number of periods. In the reference implementation,
that claim is paid in a stablecoin or treasury reserve asset. The payout tapers
over time, so former contributors keep some upside without leaving an
ever-growing bill behind them.

The mechanism has two states:

1. Active state: the contributor receives base pay and earns a compounding
   active bonus.
2. Legacy state: the contributor no longer earns base pay, but can claim a
   trailing payout based on cumulative eligible compensation with the
   organization.

TLY pays in a treasury reserve asset, such as a stablecoin, rather than a
governance token. That choice does a lot of work. Too many token-compensation
schemes quietly ask the same asset to govern, signal, collateralize, reward,
and absorb constant sell pressure. In practice, that bundle is often brittle.

## Mechanism At A Glance

If someone wants the short version, it is just this:

1. While active, the contributor receives base pay and earns an active bonus.
2. On exit, the protocol uses the contributor's cumulative eligible
   compensation base to define the initial trailing amount.
3. In legacy state, that amount is paid out through a tapering claim schedule
   over a fixed duration.

## Worker-Side Promise Variants

The mechanism alone does not answer the first practical question: what does the
worker actually have?

There are at least three deployment variants:

| Variant | Worker-side promise | Practical implication |
| --- | --- | --- |
| Contingent protocol benefit | Claim is payable only under disclosed treasury and governance conditions | Weakest legal/economic promise; easiest to subordinate in stress |
| Contract-wrapped deferred compensation | Claim is documented off-chain and tied to employment or contributor agreements | Stronger worker expectation; requires legal, tax, payroll, and accounting design |
| Reserve-backed or partially prefunded claim | Some future payouts are backed by reserves, escrow, or a disclosed buffer policy | More credible, but capital intensive |

These are not cosmetic wrappers. They determine whether TLY is merely
formulaic, conditionally claimable, contractually enforceable, or credibly
reserved. The same Pure TLY equation can sit underneath each version, but the
worker has not been promised the same thing.

## Reference And Conservative Variants

This paper studies recursive TLY as the reference implementation: settled
active bonuses become part of the future eligible-compensation base. That is
the strongest version of the mechanism and the one most exposed to stationarity
assumptions.

The broader TLY category does not require that exact choice:

| Variant | Eligible-compensation base | Why use it |
| --- | --- | --- |
| Reference TLY | Base pay plus settled active bonuses | Stronger continuation claim; more sensitive to growth, turnover, and taper assumptions |
| Conservative TLY | Base pay only | Easier to govern and model; weaker long-tenure upside |
| Hybrid TLY | Base pay plus partial or capped inclusion of settled bonuses | Middle ground for organizations with tighter treasury constraints |

That distinction matters. A production adopter may reasonably choose the
conservative or hybrid version without rejecting the TLY architecture.

## A Worked Example

Consider one contributor paid annually.

| Input | Value |
| --- | ---: |
| Base pay | $100,000 per year |
| Historical compensation base entering year | $250,000 |
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

If the contributor exits after that year, the reference convention uses the
accrual share applied to the contributor's cumulative eligible-compensation base
with the organization as the initial trailing amount. Under the
non-self-referential timing convention used here, the exit base for this year is
prior historical compensation plus current base pay, so the amount is the same
as the cached active-bonus amount:

$$
R = \$3{,}500.
$$

This paper uses the same timing convention as the contracts: the first
claimable trailing payout occurs one full epoch after departure and equals
$R\rho$, not $R$.

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

This small example is useful, but it is also where a clean formula can become
dangerous. Bounded means the obligation runs off structurally rather than
compounding forever; it does not mean every parameter set is prudent or fully
prefunded. That distinction matters. People hear "bounded" and often smuggle in
"affordable." Those are not the same claim. The organization-level burden still
depends on payroll growth, turnover, active accrual rate, trailing duration,
and the taper.

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

TLY sits somewhere between these structures. It gives workers a continuing
economic right after exit, but not an untapered one and not an ownership claim.

## Layer 1: Pure TLY

Pure TLY is the compensation rule. It says how active compensation updates the
historical compensation base, how the initial trailing amount is defined from
that base, and how that amount runs off after departure. It does not answer
whether the organization can afford the claim, whether paused claims queue, or
what legal form the promise takes. Those questions belong to the Stress Layer
and Governance Wrapper.

### What TLY Is

TLY is a compensation rule that turns compensated labor history into a trailing
payout right.

It is not equity because it does not transfer governance or ownership. It is
also not ordinary token compensation, because the mechanism does not depend on
workers selling the governance asset into the market. And it is not a standard
pension. The payout is tied to the contributor's compensation history, begins
from the cumulative eligible-compensation base with the organization, and then
tapers over a fixed horizon.

TLY gives contributors a continuing cash-flow claim if the organization
survives and keeps funding it. That is real upside, but it is not the same
thing as owning an open-ended equity position.

In the reference design, the active bonus is:

$$
\text{Active Bonus}
=
(\text{Historical Compensation Base} + \text{Base Pay})
\times
\text{Accrual Share}.
$$

In the reference design, the initial trailing amount is the accrual share
applied to the contributor's cumulative eligible-compensation base with the
organization. Under the timing convention used here, that base is prior
historical compensation plus current-period eligible base pay; the current
active bonus is then added to the historical compensation base for future active
periods if the contributor continues. The contracts cache the same quantity as
`lastActiveBonus`, but the economic object is not a discretionary terminal
bonus; it is the accumulated compensation ledger multiplied by the accrual
share. The trailing claim then pays:

$$
\text{Trailing Payout}_s
=
\text{Initial Trailing Amount} \times \rho^s,
$$

where $s$ is the number of epochs after departure and $\rho$ is the per-epoch
taper factor. For annual epochs and a 5 percent taper, $\rho = 0.95$.

Pure TLY does not decide whether that cash-flow claim is legally enforceable
deferred compensation, a reserve-backed benefit, or a contingent protocol
benefit. The same formula can sit under different wrappers, and those wrappers
matter.

### Historical Compensation Base And Compounding

The historical compensation base is the core state variable on the active side.
In the contracts it is named `historicalPayPool`, but it is an accounting/state
variable, not necessarily a segregated pool of funded assets. This is also the
place where many readers quite reasonably stop and ask, "Wait, what is actually
compounding here?" In the reference design, the base is not just cumulative base
salary. It is cumulative settled active compensation that remains attached to
the active workforce.

At the contributor level, while a contributor remains active:

$$
H_{i,t+1} = H_{i,t} + B_{i,t} + A_{i,t}.
$$

At the aggregate level, after turnover is applied:

$$
H_{t+1} = (H_t + B_t + A_t)(1-q).
$$

This means prior active bonuses enlarge the future bonus base. That compounding
is intentional. In TLY, the historical compensation base behaves more like a
running labor-credit account than a simple wage ledger. The mechanism is trying
to reward accumulated compensated contribution, not only elapsed tenure.

A narrower design could compound only on prior base pay and ignore past active
bonuses. That would be a different and less aggressive member of the TLY
family. It is not the reference system simulated in `sim/` or implemented in
the Solidity contracts.

There are at least three plausible variants:

| Variant | Compensation base | Tradeoff |
| --- | --- | --- |
| Full recursive design | Base pay plus prior settled active bonuses | Strongest continuation claim, but most sensitive to stationarity assumptions |
| Base-pay-only design | Base pay only | Easier to reason about, but weaker reward for accumulated compensated contribution |
| Hybrid design | Base pay plus capped or partially weighted settled bonuses | More governance discretion, but potentially easier to fit to treasury policy |

This paper uses the full recursive design as the reference mechanism. That
choice should be visible rather than smuggled into the equations. Prior settled
active bonuses enlarge the future compensation base; if that feels like a small
detail, it is not. But the architectural claim is broader than the recursive
variant. Base-pay-only and hybrid ledgers can still be TLY designs if they
convert cumulative compensated contribution into a finite, tapering post-exit
claim.

### Bounded Runoff And Stationarity

This is the place where people most easily overclaim. Tapering the legacy side
is necessary, but it does not save the model if the active-side historical
compensation base is allowed to outrun payroll indefinitely. The old claims have
to lose weight, and the active bonus base has to remain tied to payroll rather
than becoming its own runaway ledger.

For a trailing claim with initial amount $R$, taper factor $\rho < 1$, and
duration $K$, total undiscounted payout is:

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

This number is the lifetime multiple of the initial trailing amount, not of
base salary. In the minimal reference design, that initial amount is controlled
by the active accrual share, typically modeled at 1 percent.

Tapering alone is not the whole stationarity story. Let $G$ denote gross
payroll growth from one epoch to the next, let $q$ denote turnover, and define
the aggregate historical-pool ratio:

$$
h = \frac{H_t}{B_t}.
$$

From the aggregate update equations:

$$
H_{t+1} = (H_t + B_t + A_t)(1-q)
$$

and

$$
A_t = \alpha(H_t + B_t),
$$

the key stability parameter is:

$$
c = \frac{(1-q)(1+\alpha)}{G}.
$$

If $c < 1$, then the active-side state converges to a steady ratio:

$$
h = \frac{c}{1-c}
$$

and the active bonus ratio converges to:

$$
m = \frac{A_t}{B_t} = \frac{\alpha}{1-c}.
$$

If $c \geq 1$, the historical compensation base grows at least as fast as
payroll and the active bonus ratio does not settle. So yes, tapering matters.
But tapering by itself does not rescue a badly chosen active-side design.

At the organization level, four forces interact:

1. Low active accrual limits new trailing claims.
2. Payroll growth makes old cohorts smaller relative to current payroll.
3. The taper reduces the weight of every legacy cohort over time.
4. Turnover limits how much historical pay remains attached to active workers.

Under the simulator's baseline growth intuition of roughly 4 percent gross
payroll growth and the EVM convention that the first legacy claim receives
$R\rho$, the approximate steady burden is shown below.

The active bonus ratio column is not a free input. It comes out of the
stationarity condition above. With $\alpha = 1\%$ and $G \approx 1.04$, the
model yields $m \approx 9.35\%$ at 8 percent turnover, $m \approx 7.92\%$ at
10 percent turnover, and $m \approx 3.12\%$ at 30 percent turnover. That may
look backward at first glance, but it makes sense once you sit with it: higher
turnover means fewer contributors remain active long enough to build large
historical compensation bases.

| Turnover | Active bonus ratio | Approx. trailing burden |
| ---: | ---: | ---: |
| 8% | 9.35% | 7.9% of payroll |
| 10% | 7.92% | 8.3% of payroll |
| 30% | 3.12% | 9.8% of payroll |

Higher turnover reduces the active historical base, but it also creates more
frequent legacy cohorts. That means the active-side and legacy-side effects can
move in opposite directions, which is why this table is easy to misread on a
first pass.

These values are illustrative rather than universal. Boundedness is a
mechanical property, not a solvency guarantee. The model stabilizes only when
the active bonus base remains bounded relative to payroll and the trailing side
actually runs off over time. No artificial cap on an individual contributor's
historical compensation base is needed for that result, although the governance
problem does not disappear. An administrator who can rewrite the eligible
compensation ledger or reclassify exceptional compensation can materially
affect the claim.

## Layer 2: Stress Layer

Pure TLY can be bounded and still be imprudent. The Stress Layer is where the
organization decides whether the formula is affordable, what priority legacy
claims have, and what happens when the treasury is under pressure. This is not
secondary paperwork. It is the part that keeps a mechanical runoff property from
being mistaken for a solvency guarantee.

### Treasury-Health Metrics

At minimum, a DAO considering TLY should track:

- trailing burden / active payroll;
- trailing burden / gross margin or operating surplus;
- reserve coverage, measured as stable reserves divided by projected trailing
  claims over a fixed look-ahead window;
- forward claim coverage, measured as stable reserves plus committed funding
  divided by active pay plus projected legacy claims over the same window;
- active bonus ratio, measured as active bonuses divided by payroll;
- the stress threshold at which legacy claims are paused, partially paid, or
  queued.

These metrics are not ornamental dashboard widgets. They are the operating
boundary of the promise. If the dashboard says the model is drifting out of
range and governance keeps issuing claims anyway, the problem is no longer the
formula.

### Stress-State Semantics

Before deployment, the organization should publish what happens in stress.
There are several different promises hiding under the phrase "pause legacy
claims":

| Stress behavior | What it means | Worker-side promise |
| --- | --- | --- |
| Pause | Legacy claims stop while active pay remains claimable | Weakest; claim is live only when treasury policy permits |
| Partial payment | Legacy claims receive a disclosed percentage or pro rata amount | More predictable, but requires allocation rules |
| Queue / catch-up | Missed claims remain recorded and can be paid later | Stronger worker promise; creates a larger treasury overhang |
| No catch-up | Missed epochs do not accrue beyond the claim rules | Cleaner solvency rule; harsher for alumni |

There is no mechanism design trick that makes future cash obligations
disappear. They are funded, subordinated, queued, partially paid, or left to
unfunded assumptions. The paper can model the first four. It should not pretend
the fifth is a policy.

### Sensitivity And Stress Cases

The baseline table above is only a starting point. A publication-ready model
should expose sensitivity to:

- accrual share;
- turnover;
- payroll growth;
- taper;
- trailing duration;
- revenue or margin assumptions;
- reserve level and reserve drawdown speed.

At least one stress case should be shown before adoption: a revenue shock,
payroll contraction, turnover spike, reserve decline, or a combined bear-market
case where several of those happen together. That is where a mechanism that
looked reasonable under smooth growth either survives contact with reality or
starts asking governance to improvise.

### Design Conditions

TLY is most defensible when the following conditions hold:

- low active accrual share;
- taper factor below one;
- finite trailing duration;
- active-side stationarity, meaning $c < 1$;
- credible treasury funding policy;
- published stress-state semantics;
- governance controls around eligible-compensation definitions and ledger
  integrity.

## Layer 3: Governance Wrapper

The Governance Wrapper is the set of rules that keeps the clean mechanism from
being gamed by people who understand exactly where the formula is sensitive.
The pure mechanism is elegant, but production safety requires wrapper rules. A
production TLY design should not let the eligible-compensation ledger become a
soft governance variable. The initial trailing amount should be derived from
cumulative eligible compensation with the organization multiplied by the
accrual share, not from a salary number or discretionary bonus chosen near
departure.

### Production Compensation-Ledger Default

The production default should be:

$$
R_i = \alpha E_{i,\tau_i},
$$

where $E_{i,\tau_i}$ is the contributor's cumulative eligible-compensation base
with the organization at exit. That base may include base pay, settled active
bonuses, or other earned compensation depending on the deployment design, but
the definition has to be fixed before the claim is earned. In the reference
recursive design, prior settled active bonuses enlarge the base; a base-pay-only
variant would be cleaner but less generous.

This is why ordinary terminal-period manipulation should not be the main risk
in the model. A contributor should not be able to improve the trailing claim by
nudging one terminal salary number. The real governance risk is upstream:
whether administrators can edit the compensation ledger, reclassify exceptional
payments as eligible compensation, or change parameters after contributors have
already relied on the rule.

Recommended wrapper rules include:

- a disclosed definition of eligible compensation;
- append-only or auditable compensation-ledger updates;
- separation between ordinary compensation updates and exceptional-comp review;
- governance review for exceptional compensation changes;
- published parameter-change procedures;
- periodic reporting of active payroll, active bonuses, projected legacy
  burden, and reserve coverage.

### Reference Implementation Versus Production Design

The current Solidity reference stores `lastActiveBonus` for simplicity and gas
economy. In this design, `lastActiveBonus` is the cached result of applying the
accrual share to the contributor's historical compensation base for the last
settled active epoch. It should not be read as a discretionary terminal-period
bonus. Production deployments should still harden compensation-ledger updates,
exceptional-comp review, role controls, and parameter-change procedures.

### Operational Design And Governance Rules

The reference EVM architecture has two contracts:

| Contract | Role |
| --- | --- |
| `ContributorRegistry.sol` | stores contributor status, base pay, historical compensation base (`historicalPayPool`), cached active bonus, departure epoch, and claim checkpoints |
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

## What Is Actually New Here?

TLY's components are familiar. Deferred compensation, phantom participation,
contingent benefits, runoff liabilities, and bonus pools all cover nearby
ground. The novelty is architectural: TLY links a historical compensation base
to a finite, tapering post-exit cash-flow claim.

- active compensation updates a historical compensation base;
- the exit claim is formulaic rather than negotiated from scratch;
- the post-exit claim is money-denominated, tapering, and finite;
- the claim can be implemented with per-wallet state and pull-based settlement;
- treasury stress can be expressed as an explicit priority rule rather than
  hidden in token-price volatility.

That combination is the research object. It makes a deferred-compensation
promise legible, programmable, and modelable under defined assumptions.

## Why Not Simpler Hybrids?

A simpler salary-plus-bonus-plus-deferred-pool design may be better for many
organizations. So may RSUs, phantom equity, SARs, standard equity, or token
vesting. The case for TLY is strongest when the organization has sufficient
operating cash flow, reserve discipline, and governance maturity to support a
formulaic continuation claim that does not transfer governance and can be
modeled as a runoff burden.

| Mechanism | What it does well | Where TLY differs |
| --- | --- | --- |
| Salary + bonus + deferred pool | Simple, familiar, easy to document | TLY makes the post-exit runoff formula explicit and contributor-specific |
| RSUs | Familiar equity-linked compensation for later-stage companies | TLY is cash-flow based rather than share-settlement based |
| Phantom equity / SAR | Mirrors company value without issuing stock | TLY avoids valuation fights by paying from a treasury reserve asset |
| Token vesting | Liquid and crypto-native | TLY avoids paying labor through governance-token sell pressure |
| Standard equity/options | Strong upside and familiar investor logic | TLY gives clearer departure economics but less open-ended upside |
| Revenue share | Ties payment to organization performance | TLY is based on compensation history, not a direct revenue percentage |

If a simpler hybrid gives workers the same clarity with less machinery, use the
simpler hybrid. The reason to use TLY is not elegance. It is the specific mix of
liquidity, non-dilutive economic continuation, and modelable exit economics.

## Comparison With Adjacent Mechanisms

| Feature | Standard equity/options | RSUs | Phantom equity / SAR | Deferred bonus pool | Token vesting | TLY |
| --- | --- | --- | --- | --- | --- | --- |
| Liquid while active | Usually no | Usually no | Usually no | Usually yes for salary | Usually yes | Yes, for base and active pay |
| Direct governance dilution | Often yes | Often yes | No | No | Yes | No |
| Near-term cash obligation | Low | Low to medium | Usually later | Yes | Often indirect | Yes |
| Retained economics after exit | Sometimes, often illiquid | Plan-specific | Usually yes | Plan-specific | Yes | Yes |
| Market-price dependence | High | High | High | Low | High | Low if paid in stablecoins |
| Treasury-solvency dependence | Indirect | Indirect | Medium to high | High | Indirect | High |
| Fit for pre-revenue startups | Strong | Limited | Limited | Possible if deferred | Common but volatile | Limited unless prefunded, delayed, or threshold-activated |

TLY is not categorically better than these mechanisms. It is aimed at a fairly
specific problem: giving contributors live, money-denominated upside without
leaning on governance-token issuance and without pretending the organization
can promise a perpetual tail.

Equity may still be superior for early-stage startups that need pure upside
without near-term cash obligations. TLY is better understood as a potential
substitute or complement where operating cash flow, reserve discipline, and
governance maturity are already present or plausibly reachable.

## Where TLY Fits Best

TLY makes the most sense where treasury capacity is already real or at least
plausibly reachable. That sounds almost too obvious to write down, but it needs
to be written down because mechanism papers have a habit of sneaking past the
funding question and acting like good equations fund themselves.

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

## Funding Models For TLY

Pre-revenue teams are where this gets dangerous fastest. Writing the claim
on-chain is trivial compared with funding it later, and teams without a
believable treasury path should say that plainly rather than bury it under
future-growth assumptions.

Possible funding models include:

1. Operating cash-flow funding: each epoch's claims are paid from ordinary
   operating cash flow.
2. Margin-linked funding: claim capacity scales with gross margin or operating
   surplus.
3. Reserve-buffer hybrid: a portion of active payroll, margin, or revenue funds
   a reserve buffer for future trailing claims.
4. Threshold-activated payout: legacy payouts begin only after revenue,
   treasury, runway, or reserve-coverage thresholds are met.
5. Waterfall priority model: active pay, operating obligations, reserves, and
   legacy claims are paid in a disclosed order of priority.

These models can be combined. For example, an early protocol might accrue TLY
internally but delay claim activation until a stablecoin reserve threshold is
met. That may sound less elegant than a fully live system from day one, but it
is often the more honest design. The real question is not whether the claim can
be written on-chain. It is whether the organization has a credible funding
policy and a disclosed stress rule.

Funding policy determines whether TLY is merely formulaic, credibly reserved,
contract-wrapped, or only conditionally claimable. The mechanism does not choose
among those variants by itself.

## Risks, Limitations, And Failure Modes

### Treasury Solvency And The Cash-Flow Paradox

TLY is not for cash-starved organizations with no realistic treasury path. It
works best for profitable, treasury-backed, or reserve-capitalized entities.
Pre-revenue organizations may need delayed activation, reserve escrows, smaller
initial accrual rates, or hybrid token-cash structures. A protocol with
unstable revenue but a liquid governance token has not solved the cash problem;
it has moved it.

Trailing claims should be described precisely. In the reference on-chain
design, they are contingent claims that sit behind active compensation during
stress unless an off-chain agreement grants claimants different rights. That is
not a small drafting detail. It changes what workers are actually being offered.
If treasury funds are insufficient, the organization must define whether missed
claims accrue, queue, partially defer, or remain claimable only when the
treasury is funded.

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

### Compensation-Ledger Integrity

The natural TLY definition removes the usual terminal-period manipulation
problem. The initial trailing claim is not supposed to be based on the
contributor's final salary, a final-period bonus, or a number selected at
departure. It is the
accrual share multiplied by the contributor's cumulative eligible-compensation
base with the organization.

That does not make governance irrelevant. It moves the problem to the place
where it belongs: the definition and administration of eligible compensation.
If a DAO admin can retroactively edit compensation history, classify a one-off
grant as eligible compensation without review, or change the accrual rule after
the fact, then the mechanism can still be abused. The right defenses are:

- a clear eligible-compensation definition before accrual begins;
- append-only or auditable compensation-ledger updates;
- review of exceptional compensation and retroactive adjustments;
- role separation for contributor administration, treasury control, and
  parameter changes;
- reporting that lets contributors and governance see the historical
  compensation base that will drive future claims.

The current reference contract stores `lastActiveBonus` for simplicity and gas
economy. Economically, that value should be read as a cached accrual-rate result
derived from historical compensation, not as a discretionary terminal bonus.

### Treasury Stress And Insolvency

The Solidity reference includes `pauseLegacyClaims()` so a DAO admin can block
legacy withdrawals while preserving active compensation. There is nothing fancy
about this. It is just a hard priority rule. It is also not a complete
insolvency framework.

Before deployment, organizations should define:

- whether paused claims accrue or simply wait;
- whether claimants can later catch up using aggregate claims;
- whether partial payment is allowed;
- whether legacy claims are legally enforceable debt or contingent protocol
  benefits;
- what disclosures contributors receive before accepting the structure.

### Governance Abuse And Favoritism

TLY depends on credible compensation administration. A pod admin that can
update base pay or time departures can influence future trailing claims. If
that sounds like a governance headache, that is because it is one.

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
cash obligations. A 1 percent accrual share sounds small until it compounds
through a large historical compensation base under weak turnover assumptions.
The simulator should be used before governance adopts or changes parameters.

## Implementation Path And Pilot Model

A useful pilot can be small and explicit:

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

TLY is best understood as a layered compensation architecture. Pure TLY defines
the formula. The Stress Layer asks whether the organization can fund it and
what happens when it cannot. The Governance Wrapper decides whether the formula
is robust enough to survive real people with incentives.

That framing keeps the claim in proportion. TLY can separate contributor upside
from governance-asset dilution, offer more liquidity than lottery-style equity,
and make departure economics clearer than many option or token packages. None
of that makes the claim cheap or easy. It still has to be funded, documented,
governed, and legally wrapped in a way that matches the jurisdiction.

If an organization actually has reserve discipline, TLY at least makes the
trade legible: contributors get a real trailing claim, and the organization can
model the burden before pretending it is manageable. That is the contribution:
post-exit labor upside made explicit, finite, modelable, and governable.

## Appendix A: Full Formulas

Lowercase subscripts refer to contributor-level quantities. Aggregate
quantities omit contributor indexing. Unless otherwise stated, all quantities
are per epoch.

### A.1 Notation

- $B_{i,t}$: contributor $i$'s base pay in epoch $t$.
- $H_{i,t}$: contributor $i$'s historical compensation base entering epoch $t$,
  defined in the reference model as cumulative settled active compensation
  while active. In the contracts this is stored as `historicalPayPool`.
- $E_{i,t}$: cumulative eligible-compensation base used for accrual in epoch
  $t$. Under the reference timing convention, $E_{i,t}=H_{i,t}+B_{i,t}$.
- $\alpha$: active accrual share.
- $A_{i,t}$: active bonus.
- $R_i$: initial trailing amount after exit.
- $s$: elapsed epochs since departure, starting at $s=1$ for the first
  claimable legacy epoch.
- $\delta$: taper rate.
- $\rho = 1-\delta$: per-epoch taper factor.
- $K$: maximum trailing duration.
- $q$: turnover rate.
- $G$: gross payroll growth factor.
- $L_t$: aggregate trailing payout in epoch $t$.

### A.2 Active State

Contributor-level active bonus:

$$
A_{i,t} = \alpha E_{i,t}
= \alpha(H_{i,t} + B_{i,t}).
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

Exit compensation-base rule:

$$
R_i = \alpha E_{i,\tau_i}.
$$

Here $E_{i,\tau_i}$ is the contributor's cumulative eligible-compensation base
with the organization at exit under the disclosed timing convention. In the
Solidity reference, `lastActiveBonus` caches the same accrual-rate calculation
for the last settled active epoch. That cache is an implementation shortcut,
not a separate discretionary exit bonus.

This paper uses the EVM timing convention throughout: the first claimable
legacy payout occurs one full epoch after departure, so $s=1$ at the first
claimable epoch.

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
- historical compensation base (`historicalPayPool`);
- cached last active bonus;
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
claim based on cumulative eligible compensation with the organization. It
tapers and expires.

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

Not by manipulating a terminal salary number, if TLY is implemented according
to the natural definition. The initial trailing amount is the accrual share
multiplied by cumulative eligible compensation with the organization.
Governance risk instead sits in the compensation ledger: what counts as
eligible compensation, who can update it, and how exceptional or retroactive
compensation is reviewed.

### Does this create tax or legal issues?

Potentially. TLY may implicate deferred compensation, payroll, securities,
labor, tax, benefits, or accounting rules. Legal design is jurisdiction-
specific.

### Why not cap historical compensation?

The reference mechanism intentionally avoids artificial caps on the historical
compensation base because long-tenure contributors are supposed to earn larger
trailing claims. Aggregate stability comes from low active accrual, payroll
growth, finite duration, and tapering legacy obligations. Governance may still
restrict manipulation of the eligible-compensation ledger.
