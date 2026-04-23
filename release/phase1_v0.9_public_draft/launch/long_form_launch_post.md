# Long-Form Launch Post

Trailing Labor Yield (TLY) is a compensation architecture for programmable
deferred compensation. It is meant for organizations that want a middle path
between illiquid equity and governance-token compensation without pretending
that a clean formula funds itself.

The problem is familiar. Startup-style upside is often technically valuable but
practically inaccessible to workers. Token compensation is liquid, but it can
force contributors to sell the same asset the organization relies on for
coordination, governance, and market confidence. Pension-like promises solve a
different problem and can create long-run liabilities that grow in ways
operators do not fully understand at the moment they make the promise.

TLY tries to define a narrower, more legible bargain.

While active, a contributor receives normal cash compensation and a small active
bonus tied to realized compensation history. When the contributor exits, a
defined snapshot becomes a tapering stablecoin payout for a fixed duration. The
payout runs off over time instead of persisting as a perpetual obligation.

This is not a claim that every organization can afford the structure. The point
is to make the structure explicit, simulable, and governable. The public draft
is careful about where TLY does and does not fit. It is most plausible for
treasury-backed DAOs, profitable crypto-native firms, protocol-adjacent service
organizations, and reserve-disciplined cooperatives. It is a poor fit for
immediate live-payout use at cash-starved pre-revenue organizations unless the
claim is prefunded, delayed, or threshold-activated.

The paper now presents TLY in three layers:

- Pure TLY: the mathematical mechanism for active accrual, exit snapshot, and
  legacy runoff.
- Stress Layer: affordability, reserve coverage, payout priority, pause
  semantics, partial payment, queue/catch-up, and missed-epoch treatment.
- Governance Wrapper: trailing realized-compensation averaging, notice and
  pay-lock rules, anti-gaming controls, and parameter governance.

That layering matters because "bounded" is not the same thing as "affordable."
A claim can run off structurally and still be irresponsible if the treasury
cannot support it. The right question is not only whether the formula converges.
It is also what happens under revenue shock, payroll contraction, turnover
spikes, reserve decline, and weak contributor administration.

The repo includes:

- a white paper that explains the mechanism, comparison set, and layer model;
- a one-page summary, FAQ, and diagram notes;
- a Python simulator and Streamlit dashboard for exploring burden dynamics;
- EVM reference contracts showing per-wallet state, pull claims, fixed-point
  taper math, bounded missed-epoch processing, and active-pay priority.

The implementation matters. If a mechanism cannot survive contact with block
gas limits, treasury stress, or contributor-admin realities, it is not much
use. The contracts are still reference architecture, not production wrappers.
In particular, production deployments should use trailing realized-compensation
averaging for exit snapshots and should disclose stress-state semantics before
anyone accepts the claim.

I’m publishing this as a `v0.9 public draft` because I want criticism at the
mechanism-design layer, not a performative sense of finality. The strongest
questions are the right ones:

- Is the Pure TLY / Stress Layer / Governance Wrapper split useful?
- Is the bounded-but-not-automatically-affordable argument stated clearly?
- What treasury-health metrics should be canonical?
- What legal structure would be required for different jurisdictions?
- Is trailing realized-compensation averaging the right production default?
- Where does this fit in practice, and where does it fail?

If the idea is interesting, the best next step is not immediate
commercialization. It is scrutiny. The first phase is simply to publish cleanly,
make the idea legible, and invite serious feedback from founders, protocol
operators, economists, lawyers, compensation designers, and smart-contract
engineers.

Repository:

- add GitHub link here
