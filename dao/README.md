# TLY DAO Contracts

**Warning:** These Solidity contracts are unaudited reference contracts for the
TLY mechanism. Do not route real capital through them, do not deploy them as
production systems, and do not treat this folder as audit-cleared code.

This folder contains an initial Solidity architecture for the Trailing Labor
Yield (TLY) compensation model modeled in `sim/app.py` and
`sim/baseline_dollars.py`. The contracts demonstrate the Pure TLY mechanism and
some Stress Layer behavior. They do not implement the full Governance Wrapper
recommended in the white paper.

The Python simulator uses:

```text
active_bonus = (historical_pay_pool + base_payroll) * accrual_share
legacy_payout = initial_legacy_amount * taper_factor ^ age
historical_pay_pool_next = historical_pay_pool + base_pay + active_bonus
```

The on-chain version maps the aggregate simulation into per-contributor state:

- Active contributors claim base pay plus their active bonus.
- When a contributor exits, the registry uses `lastActiveBonus` as
  `initialLegacyAmount`. In this reference design, `lastActiveBonus` is the
  cached accrual-rate result from the contributor's historical compensation
  base, not a discretionary terminal bonus.
- Legacy contributors call `claimTrailingYield()` to pull one or more missed epochs.
- The treasury never loops over alumni.
- The protocol does not cap `historicalPayPool` or active bonuses; the accrual
  and taper parameters are the liability controls.

Production deployments should harden the eligible-compensation ledger:
definitions of eligible compensation, exceptional-comp review, admin role
separation, and auditability are production concerns beyond this minimal
reference implementation.

## Contracts

- `contracts/ContributorRegistry.sol`
  - Owns contributor state.
  - Tracks active/legacy status, base pay, historical compensation base
    (`historicalPayPool`), cached active bonus, and legacy claim checkpoints.
  - Uses OpenZeppelin `AccessControl`.
  - `POD_ADMIN_ROLE` can add contributors, remove contributors, and update base
    pay.
  - Can only be settled by the configured treasury distributor.

- `contracts/TreasuryDistributor.sol`
  - Holds the payment token.
  - Computes active compensation.
  - Computes tapered legacy claims using WAD fixed-point math.
  - Transfers funds using a pull-claim flow.
  - Uses OpenZeppelin `AccessControl`, `SafeERC20`, and `ReentrancyGuard`.
  - `DAO_ADMIN_ROLE` can pause and unpause legacy claims while active claims
    remain available.

- `contracts/libraries/WadMath.sol`
  - Provides WAD multiplication and fixed-point exponentiation.
  - `rpowWad(base, exponent)` computes `base ^ exponent` in `O(log exponent)`.

## Precision

Percentages use WAD precision:

```text
1e18 = 100%
0.01e18 = 1%
0.95e18 = 95%
```

Token amounts remain in the ERC-20 token's native decimals. For example, if the
payment token is USDC, pay amounts should be stored in 6 decimals while WAD is
used only for multipliers.

## Epoch Configuration

For annual epochs and a 5% annual taper:

```text
epochLength = 365 days
taperFactorPerEpochWad = 0.95e18
maxLegacyEpochs = 25
```

For monthly epochs and a 5% annual taper, precompute the monthly factor off-chain:

```text
taperFactorPerEpochWad = floor((0.95 ^ (1 / 12)) * 1e18)
maxLegacyEpochs = 25 * 12
```

This avoids fractional exponent math on-chain.

## Skipped Legacy Epochs

Legacy contributors can claim multiple missed epochs in one call. The treasury
pays the oldest unclaimed legacy epochs first and caps each transaction at
`maxEpochsPerClaim`, for example 12 monthly epochs. If an alumnus is behind by
more than the cap, they can call again.

The claim sum is:

```text
sum(initialLegacyAmount * taperFactorPerEpoch ^ elapsedEpoch)
```

where the loop is bounded by `maxEpochsPerClaim`, not by the total alumni count
or by an unbounded claim history.

The reference implementation treats missed claimable epochs as payable when the
claim is eventually made, subject to available treasury balance and pause state.
A production Stress Layer should state explicitly whether missed epochs pause,
partially pay, queue, catch up, or expire without catch-up.

## Deployment Order

1. Install dependencies:

```bash
forge install OpenZeppelin/openzeppelin-contracts foundry-rs/forge-std
```

2. Deploy `ContributorRegistry` with the DAO admin and pod admin multisigs.
3. Deploy `TreasuryDistributor`, pointing it at the registry and payment token.
4. Call `ContributorRegistry.setTreasuryDistributor(treasury)`.
5. Fund the treasury with stablecoins.
6. Add contributors through `ContributorRegistry.addContributor`.

## Audit Notes

This is an initial architecture draft. Before production use:

- Consider PRBMath, Solmate, or Solady for fixed-point math.
- Add unit tests for epoch boundaries, skipped claims, underfunded treasury
  behavior, token decimal assumptions, and transition timing.
- Add tests for stationarity and non-stationarity parameter cases, taper timing,
  pause/resume behavior, missed-epoch semantics, and compensation-ledger
  assumptions.
- Add compensation versioning before production. In this draft, active claims
  settle one epoch at a time using the contributor's current base pay, so the DAO
  should settle outstanding active epochs before changing base pay.
- Treasury shortfall policy is implemented as tranche priority:
  `pauseLegacyClaims()` blocks alumni claims while active contributors can still
  claim active compensation.
- Add production ledger logic or an off-chain wrapper for eligible-compensation
  definitions, exceptional-comp review, and auditability.
- Document the worker-side promise: contingent protocol benefit,
  contract-wrapped deferred compensation, or reserve-backed / partially
  prefunded claim.
