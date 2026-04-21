# TLY Visual Diagrams

Version: v0.9 public draft  
Companion graphics for the TLY white paper

These diagrams are intended for GitHub, Mirror, and publication decks. Mermaid
rendering support varies by platform; export diagrams to SVG or PNG before
using them in static PDFs.

## 1. Contributor State Flow

```mermaid
flowchart LR
    A[Active Contributor] --> B[Base Pay Each Epoch]
    A --> C[Active Bonus]
    C --> D[Historical Pay Pool Updates]
    D --> C
    A --> E[Exit Event]
    E --> F[Snapshot Final Active Bonus]
    F --> G[Legacy Contributor]
    G --> H[Pull Claim Each Epoch]
    H --> I[Trailing Stablecoin Payout]
    I --> J[Taper Over Fixed Duration]
```

## 2. Organization Cash-Flow Schematic

```mermaid
flowchart TD
    T[Treasury Reserve Asset] --> AP[Active Compensation]
    T --> LP[Legacy Claims]
    AP --> BP[Base Pay]
    AP --> AB[Active Bonus]
    AB --> HP[Historical Pay Pool]
    HP --> AB
    LP --> TY[Trailing Yield]
    TY --> TF[Taper Factor]
    DA[DAO Admin] --> Pause[pauseLegacyClaims]
    Pause --> LP
    Pause --> Note[Active claims remain available]
```

## 3. Pull-Claim Architecture

```mermaid
sequenceDiagram
    participant C as Contributor
    participant R as ContributorRegistry
    participant T as TreasuryDistributor
    participant S as Stablecoin

    C->>T: claimActiveComp()
    T->>R: read contributorState()
    T->>R: settleActiveEpoch()
    T->>S: transfer base pay + bonus

    C->>T: claimTrailingYield()
    T->>R: read contributorState()
    T->>T: compute bounded trailing claim
    T->>R: markLegacyClaimed()
    T->>S: transfer trailing payout
```

## 4. Taper Curve Example

For an initial trailing amount of $3,500 and a 5 percent annual taper:

| Year | Payout | Relative to initial amount |
| ---: | ---: | ---: |
| 1 | $3,325.00 | 95.0% |
| 2 | $3,158.75 | 90.3% |
| 3 | $3,000.81 | 85.7% |
| 5 | $2,708.23 | 77.4% |
| 10 | $2,095.58 | 59.9% |
| 15 | $1,621.52 | 46.3% |
| 20 | $1,254.70 | 35.8% |
| 25 | $970.86 | 27.7% |

```mermaid
xychart-beta
    title "Trailing payout as percent of initial amount"
    x-axis [1, 2, 3, 5, 10, 15, 20, 25]
    y-axis "Percent" 0 --> 100
    line [95.0, 90.3, 85.7, 77.4, 59.9, 46.3, 35.8, 27.7]
```

## 5. Mechanism Comparison Chart

| Feature | Equity | DAO token comp | Pension | Revenue share | TLY |
| --- | --- | --- | --- | --- | --- |
| Liquid while active | Low | High | Low | Medium | High for active pay |
| Governance dilution | Often | Direct | None | None | None |
| Treasury cash obligation | Low near term | Indirect | High | High | High but bounded |
| Long-run liability bounded | By equity pool | By issuance policy | Often weak | Contract-specific | Taper and term |
| Market-price dependence | High | High | Low | Medium | Low if stablecoin paid |
| Treasury-solvency dependence | Indirect | Indirect | High | High | High |
| Best fit | Venture startups | Token networks | Mature employers | Revenue assets | Treasury-backed labor systems |

## 6. Burden Logic

```mermaid
flowchart LR
    LowAccrual[Low active accrual] --> NewClaims[Smaller new trailing claims]
    PayrollGrowth[Payroll growth] --> CohortDilution[Old cohorts shrink vs current payroll]
    Taper[5% annual taper] --> Runoff[Legacy claim runoff]
    NewClaims --> Bounded[Bounded burden range]
    CohortDilution --> Bounded
    Runoff --> Bounded
```
