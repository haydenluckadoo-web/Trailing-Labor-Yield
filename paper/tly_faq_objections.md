# TLY FAQ And Objections Memo

Version: v0.9 public draft  
Companion to the TLY white paper

## Why not just give equity?

Equity is useful when a firm needs to preserve cash and offer high-upside
exposure. But equity is often illiquid, difficult to value, tax-complex, and
dependent on exit dynamics outside the worker's control. TLY is designed for
organizations that can support cash obligations and want to give workers
liquid, stablecoin-denominated upside without transferring ownership or
governance.

## Why not just use token vesting?

Token vesting is simple and liquid, but it ties contributor compensation to the
market price of the governance asset. Contributors who sell tokens to cover
living expenses can create continuous sell pressure. TLY separates labor
compensation from that pressure by paying in a reserve asset.

## Is this just a pension?

No. A pension is generally a retirement benefit with legal, actuarial, and
employment-specific treatment. TLY is a contributor-specific trailing claim
based on the final active bonus. It tapers and expires. That said, some
jurisdictions may still treat TLY-like arrangements under deferred
compensation, benefits, or labor rules.

## Is this just revenue share?

No. A revenue share usually pays a percentage of revenue. TLY pays a defined
trailing amount derived from compensation history. It may be funded by revenue,
margin, reserves, or a buffer pool, but the claim formula is not a direct
percentage of revenue.

## What happens if the treasury fails?

TLY depends on treasury solvency. The reference implementation allows a DAO
admin to pause legacy claims while active compensation remains claimable.
Production deployments should define whether paused claims accrue, queue,
partially defer, or remain contingent on future treasury funding.

## Is the trailing claim guaranteed debt?

Not necessarily. That depends on legal documentation, jurisdiction, entity
structure, and implementation details. A DAO could design TLY as a contingent
protocol benefit, a contractual deferred compensation obligation, or another
instrument. The white paper does not determine legal classification.

## Does TLY create tax issues?

Potentially. It may implicate payroll, withholding, deferred compensation,
securities, labor, benefits, or accounting rules. Contributors and
organizations should obtain jurisdiction-specific advice.

## Can a contributor game the exit bonus?

Yes, if the snapshot is based only on the final active bonus and governance is
weak. Defenses include rolling-average snapshots, notice periods, locked base
pay near departure, governance review for exceptional changes, and snapshot
growth limits relative to trailing averages.

## Why not cap the historical pay pool?

TLY intentionally rewards long tenure. Capping the historical pay pool weakens
the retention mechanism. Aggregate stability comes from low accrual, payroll
growth, fixed duration, and tapering legacy claims. Governance should focus on
preventing terminal manipulation rather than clipping legitimate tenure.

## What if turnover is high?

High turnover creates more alumni, but it also reduces average active tenure
and therefore lowers average historical pay pools. In the simulator, high
turnover does not mechanically explode the liability because fewer contributors
remain active long enough to accumulate large active bonuses. Parameters still
matter and must be simulated.

## What if turnover is low?

Low turnover can create larger individual lifer claims because contributors
build larger historical pay pools. But fewer contributors enter legacy status.
This is the intended retention tradeoff.

## Can TLY work for pre-revenue startups?

Only with caution. Pre-revenue firms may need a delayed activation model,
reserve escrow, small initial accrual, milestone-based payouts, or hybrid
equity/TLY structure. TLY is strongest when the organization has or can build a
credible stablecoin funding path.

## Who should control contributor administration?

The reference design uses `POD_ADMIN_ROLE` for operational contributor changes.
That role should generally be held by a multisig or accountable sub-DAO, not a
single unchecked operator. Changes should emit events and be reported publicly.

## Why use pull claims?

Pushing payments to every alumnus would require iterating through an expanding
list of recipients and would eventually fail due to gas limits. Pull claims
make each contributor responsible for claiming their own payment and keep gas
cost independent of the total alumni count.

## Why allow pausing legacy claims?

Active contributors keep the organization alive. During stress, active pay must
take priority over trailing claims. `pauseLegacyClaims()` is a liquidity valve,
not a confiscation mechanism. The legal and accounting treatment of paused
claims must be defined before deployment.

## What is the strongest criticism of TLY?

TLY makes cash obligations explicit. That is the point, but it also means the
organization must fund them. TLY is not free upside. It is a disciplined
cash-flow promise that should be adopted only when the treasury model supports
it.
