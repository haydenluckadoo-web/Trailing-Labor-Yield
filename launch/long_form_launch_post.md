# Long-Form Launch Post

Trailing Labor Yield (TLY) is a contributor-compensation mechanism for organizations that want a middle path between illiquid equity and governance-token compensation.

The problem is familiar. Startup-style upside is often technically valuable but practically inaccessible to workers. Token compensation is liquid, but it can force contributors to sell the same asset the organization relies on for coordination, governance, and market confidence. Pension-like promises solve a different problem and can create long-run liabilities that grow in ways operators do not fully understand at the moment they make the promise.

TLY tries to define a narrower, more legible bargain.

While active, a contributor receives normal cash compensation and a small active bonus tied to cumulative historical pay. When the contributor exits, the final active bonus is snapshotted and converted into a tapering stablecoin payout for a fixed duration. The payout runs off over time instead of persisting as a perpetual obligation.

The point is not to claim that every organization can afford this structure. The point is to make the structure explicit, simulable, and enforceable. The public draft is careful about where TLY does and does not fit. It is most plausible for treasury-backed DAOs, profitable crypto-native firms, protocol-adjacent service organizations, and reserve-disciplined cooperatives. It is a poor fit for immediate live-payout use at cash-starved pre-revenue organizations unless the claim is prefunded, delayed, or threshold-activated.

This first public draft includes three layers:

- a white paper that explains the mechanism and the bounded-liability logic;
- a Python simulator and Streamlit dashboard for exploring burden dynamics;
- EVM reference contracts that show how to implement pull claims, fixed-point taper math, and active-pay priority in a treasury architecture.

The implementation matters. If a mechanism cannot survive contact with block gas limits, treasury stress, or contributor-admin realities, it is not much use. So the repo does not stop at the theory. It includes a registry/treasury split, bounded missed-epoch claim handling, and the ability to pause legacy claims while preserving active compensation.

I’m publishing this as a `v0.9 public draft` because I want criticism at the mechanism-design layer, not a performative sense of finality. The strongest questions are the right ones:

- Is the bounded-liability argument stated clearly enough?
- Where does this fit in practice, and where does it fail?
- What legal structure would be required for different jurisdictions?
- How should the terminal snapshot be hardened against manipulation?

If the idea is interesting, the best next step is not immediate commercialization. It is scrutiny. The first phase is simply to publish cleanly, make the idea legible, and invite serious feedback from founders, protocol operators, economists, and smart-contract engineers.

Repository:

- add GitHub link here
