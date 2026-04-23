# TLY Visual Diagrams

Version: v0.9 public draft  
Companion graphics for the TLY white paper

These diagrams are intended for GitHub, Mirror, and publication decks. Mermaid
rendering support varies by platform; export diagrams to SVG or PNG before
using them in static PDFs.

## 1. Three-Layer Architecture

```mermaid
flowchart TD
    A[Pure TLY] --> B[Stress Layer]
    B --> C[Governance Wrapper]

    A --> A1[Active pay + active bonus]
    A --> A2[Realized compensation history]
    A --> A3[Tapering legacy runoff]

    B --> B1[Treasury-health metrics]
    B --> B2[Reserve coverage]
    B --> B3[Pause / partial pay / queue / catch-up]

    C --> C1[Trailing realized-compensation average]
    C --> C2[Notice and pay-lock rules]
    C --> C3[Parameter governance]
```

## 2. Contributor State Flow

```mermaid
flowchart LR
    A[Active Contributor] --> B[Base Pay Each Epoch]
    A --> C[Active Bonus]
    C --> D[Realized Compensation History]
    B --> D
    D --> C
    A --> E[Exit Event]
    E --> F[Defined Exit Snapshot]
    F --> G[Legacy Contributor]
    G --> H[Pull Claim Each Epoch]
    H --> I[Trailing Stablecoin Payout]
    I --> J[Taper Over Fixed Duration]
```

## 3. Treasury Stress Branch

```mermaid
flowchart TD
    T[Treasury Reserve Asset] --> AP[Active Compensation]
    T --> LP[Legacy Claims]
    AP --> BP[Base Pay]
    AP --> AB[Active Bonus]
    AB --> HP[Realized Compensation History]
    HP --> AB
    LP --> TY[Trailing Yield]
    TY --> TF[Taper Factor]

    Health[Treasury-Health Metrics] --> Stress{Stress Threshold Hit?}
    Stress -->|No| Normal[Legacy claims follow schedule]
    Stress -->|Yes| Rule[Disclosed stress rule]
    Rule --> Pause[Pause]
    Rule --> Partial[Partial Payment]
    Rule --> Queue[Queue / Catch-Up]
    Rule --> Skip[No Catch-Up]
    Pause --> Note[Active claims remain available]
    Partial --> Note
    Queue --> Note
    Skip --> Note
```

## 4. Pull-Claim Architecture

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

## 5. Taper Curve Example

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

## 6. Mechanism Comparison Chart

| Feature | Salary + deferred pool | Phantom equity / SAR | Startup equity | DAO token comp | TLY |
| --- | --- | --- | --- | --- | --- |
| Liquid while active | Usually yes for salary | Usually no | Usually no | Usually yes | Yes, for base and active pay |
| Governance dilution | No | No | Often | Direct | None |
| Treasury cash obligation | Yes | Usually later | Low near term | Indirect | Yes |
| Long-run liability bounded | Plan-specific | Plan-specific | By cap table | By issuance policy | Taper and term |
| Market-price dependence | Low | High | High | High | Low if stablecoin paid |
| Treasury-solvency dependence | High | Medium to high | Indirect | Indirect | High |
| Best fit | Simple deferred comp | Valuation-linked upside | Venture startups | Token networks | Treasury-backed labor systems |

## 7. Burden Logic

```mermaid
flowchart LR
    LowAccrual[Low active accrual] --> NewClaims[Smaller new trailing claims]
    PayrollGrowth[Payroll growth] --> CohortDilution[Old cohorts shrink vs current payroll]
    Taper[Taper + finite term] --> Runoff[Legacy claim runoff]
    Reserves[Reserve coverage] --> Solvency[Operational affordability]
    StressRules[Stress-state semantics] --> Solvency
    NewClaims --> Bounded[Bounded mechanism]
    CohortDilution --> Bounded
    Runoff --> Bounded
    Bounded --> Caveat[Bounded is not automatically affordable]
    Solvency --> Caveat
```
