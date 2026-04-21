from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import yaml


@dataclass
class Phase1Config:
    """
    Phase 1 deterministic simulation of labor-derived claim issuance.

    Economic interpretation:
    - Workers receive wages each period.
    - A fixed share of payroll is converted into newly issued claim units.
    - Each claim unit is a security-like object that pays a fixed coupon each period
      while it remains outstanding and while the firm survives.
    - Existing claim units run off each period via mortality, redemption, legal sunset, etc.
    """

    horizon_periods: int

    initial_workers: float
    worker_growth: float

    wage_per_worker: float
    wage_growth: float

    accrual_share: float
    coupon_per_unit: float

    default_hazard: float
    discount_rate: float
    runoff_components: dict[str, float]

    issue_price_mode: str
    fixed_issue_price: float

    initial_claim_units: float
    cohort_plot_top_n: int
    output_dir: str

    # Optional operating support diagnostics.
    # This is not part of the pricing model itself, but helps evaluate sustainability.
    operating_margin_on_payroll: float = 0.0

    @property
    def runoff_rate(self) -> float:
        return float(sum(self.runoff_components.values()))

    def validate(self) -> None:
        if self.horizon_periods <= 0:
            raise ValueError("horizon_periods must be positive.")
        if self.initial_workers < 0:
            raise ValueError("initial_workers must be non-negative.")
        if self.wage_per_worker < 0:
            raise ValueError("wage_per_worker must be non-negative.")
        if not (0.0 <= self.accrual_share <= 1.0):
            raise ValueError("accrual_share must be between 0 and 1.")
        if self.coupon_per_unit < 0:
            raise ValueError("coupon_per_unit must be non-negative.")
        if not (0.0 <= self.default_hazard < 1.0):
            raise ValueError("default_hazard must be in [0, 1).")
        if self.discount_rate < 0.0:
            raise ValueError("discount_rate must be non-negative.")
        if not (0.0 <= self.runoff_rate < 1.0):
            raise ValueError("runoff_rate must be in [0, 1).")
        if self.issue_price_mode not in {"fair", "fixed"}:
            raise ValueError("issue_price_mode must be 'fair' or 'fixed'.")
        if self.issue_price_mode == "fixed" and self.fixed_issue_price <= 0.0:
            raise ValueError("fixed_issue_price must be positive when issue_price_mode='fixed'.")
        if self.initial_claim_units < 0.0:
            raise ValueError("initial_claim_units must be non-negative.")
        if self.cohort_plot_top_n <= 0:
            raise ValueError("cohort_plot_top_n must be positive.")
        if self.operating_margin_on_payroll < 0.0:
            raise ValueError("operating_margin_on_payroll must be non-negative.")


def load_config(path: str | Path) -> Phase1Config:
    with open(path, "r", encoding="utf-8") as f:
        raw: dict[str, Any] = yaml.safe_load(f)

    cfg = Phase1Config(
        horizon_periods=int(raw["horizon_periods"]),
        initial_workers=float(raw["initial_workers"]),
        worker_growth=float(raw["worker_growth"]),
        wage_per_worker=float(raw["wage_per_worker"]),
        wage_growth=float(raw["wage_growth"]),
        accrual_share=float(raw["accrual_share"]),
        coupon_per_unit=float(raw["coupon_per_unit"]),
        default_hazard=float(raw["default_hazard"]),
        discount_rate=float(raw["discount_rate"]),
        runoff_components={k: float(v) for k, v in raw["runoff_components"].items()},
        issue_price_mode=str(raw["issue_price_mode"]).strip().lower(),
        fixed_issue_price=float(raw["fixed_issue_price"]),
        initial_claim_units=float(raw["initial_claim_units"]),
        cohort_plot_top_n=int(raw.get("cohort_plot_top_n", 12)),
        output_dir=str(raw["output_dir"]),
        operating_margin_on_payroll=float(raw.get("operating_margin_on_payroll", 0.0)),
    )
    cfg.validate()
    return cfg


def fair_value_outstanding_unit(cfg: Phase1Config) -> float:
    """
    Fair value of one claim unit already outstanding at the start of the period,
    just before the current period coupon is paid.

    If each unit pays coupon_per_unit each period, then:

        q_outstanding = kappa / (1 - ((1-mu)(1-lambda)/(1+r)))

    where:
    - mu = runoff rate
    - lambda = default hazard
    - r = discount rate

    Interpretation:
    A claim unit is a security-like object paying a fixed coupon while it survives
    runoff and while the firm survives.
    """
    carry = ((1.0 - cfg.runoff_rate) * (1.0 - cfg.default_hazard)) / (1.0 + cfg.discount_rate)
    denom = 1.0 - carry
    if denom <= 0.0:
        raise ValueError(
            "Outstanding unit value is not finite under current parameters. "
            "Decrease carry by increasing runoff/default or discounting."
        )
    return cfg.coupon_per_unit / denom


def fair_value_new_issue_unit(cfg: Phase1Config) -> float:
    """
    Fair value of one unit issued at the END of the current period.
    It first becomes an outstanding coupon-paying unit next period,
    provided the firm survives into next period.

        q_issue = ((1-lambda)/(1+r)) * q_outstanding
    """
    return ((1.0 - cfg.default_hazard) / (1.0 + cfg.discount_rate)) * fair_value_outstanding_unit(cfg)


def claim_issue_price(cfg: Phase1Config) -> float:
    """
    Actual issuance price used in the simulation.
    """
    if cfg.issue_price_mode == "fair":
        return fair_value_new_issue_unit(cfg)
    return cfg.fixed_issue_price


def workers_in_period(cfg: Phase1Config, t: int) -> float:
    return cfg.initial_workers * ((1.0 + cfg.worker_growth) ** t)


def wage_in_period(cfg: Phase1Config, t: int) -> float:
    return cfg.wage_per_worker * ((1.0 + cfg.wage_growth) ** t)


def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out


def save_line_plot(
    df: pd.DataFrame,
    x_col: str,
    y_cols: list[str],
    title: str,
    y_label: str,
    out_path: Path,
) -> None:
    plt.figure(figsize=(10, 6))
    for y_col in y_cols:
        plt.plot(df[x_col], df[y_col], label=y_col)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_label)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def save_cohort_stackplot(
    ledger_df: pd.DataFrame,
    out_path: Path,
    top_n: int,
) -> None:
    if ledger_df.empty:
        return

    cohort_sizes = (
        ledger_df.groupby("cohort_birth_t", as_index=False)["claim_units_if_alive"]
        .max()
        .sort_values("claim_units_if_alive", ascending=False)
    )
    top_births = cohort_sizes["cohort_birth_t"].head(top_n).tolist()

    filtered = ledger_df[ledger_df["cohort_birth_t"].isin(top_births)].copy()
    pivot = filtered.pivot_table(
        index="period",
        columns="cohort_birth_t",
        values="claim_units_if_alive",
        aggfunc="sum",
        fill_value=0.0,
    ).sort_index(axis=1)

    plt.figure(figsize=(10, 6))
    plt.stackplot(
        pivot.index,
        *[pivot[col].values for col in pivot.columns],
        labels=[str(c) for c in pivot.columns],
    )
    plt.title("Top Claim-Issuance Cohorts by Birth Period")
    plt.xlabel("period")
    plt.ylabel("claim_units_if_alive")
    plt.legend(title="cohort_birth_t", loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def build_summary(cfg: Phase1Config, df: pd.DataFrame) -> str:
    q_out = fair_value_outstanding_unit(cfg)
    q_issue = fair_value_new_issue_unit(cfg)
    issue_px = claim_issue_price(cfg)

    lines: list[str] = []
    lines.append("PHASE 1 SUMMARY")
    lines.append("=" * 60)
    lines.append(f"horizon_periods: {cfg.horizon_periods}")
    lines.append(f"runoff_rate_total: {cfg.runoff_rate:.6f}")
    lines.append(f"runoff_components: {cfg.runoff_components}")
    lines.append(f"default_hazard: {cfg.default_hazard:.6f}")
    lines.append(f"discount_rate: {cfg.discount_rate:.6f}")
    lines.append(f"coupon_per_unit: {cfg.coupon_per_unit:.6f}")
    lines.append(f"fair_value_outstanding_unit: {q_out:.6f}")
    lines.append(f"fair_value_new_issue_unit: {q_issue:.6f}")
    lines.append(f"claim_issue_price_used: {issue_px:.6f}")
    lines.append(f"issue_price_mode: {cfg.issue_price_mode}")
    lines.append(f"issue_price / fair_new_issue_value: {issue_px / q_issue:.6f}")
    lines.append(f"operating_margin_on_payroll: {cfg.operating_margin_on_payroll:.6f}")
    lines.append("")

    final_row = df.iloc[-1]
    lines.append("FINAL PERIOD SNAPSHOT")
    lines.append("-" * 60)
    for key in [
        "period",
        "workers",
        "wage_per_worker",
        "payroll",
        "accrual_dollars",
        "new_claim_units_issued",
        "new_issuance_proceeds",
        "outstanding_claim_units_if_alive",
        "coupon_cash_obligation_if_alive",
        "coupon_to_payroll_if_alive",
        "coupon_to_accrual_ratio",
        "issuance_coverage_ratio",
        "ponzi_financing_gap",
        "operating_cash_flow",
        "operating_coupon_coverage_ratio",
        "residual_after_coupons",
        "survival_prob_start",
        "expected_coupon",
        "market_value_of_claims_if_alive",
        "survival_weighted_market_value",
    ]:
        lines.append(f"{key}: {final_row[key]:,.6f}")

    zero_growth = math.isclose(cfg.worker_growth, 0.0, abs_tol=1e-12) and math.isclose(cfg.wage_growth, 0.0, abs_tol=1e-12)
    if zero_growth and cfg.runoff_rate > 0.0:
        payroll_0 = cfg.initial_workers * cfg.wage_per_worker
        steady_issue_price = claim_issue_price(cfg)
        steady_new_units = cfg.accrual_share * payroll_0 / steady_issue_price
        theoretical_l_star = steady_new_units / cfg.runoff_rate
        theoretical_coupon_star = cfg.coupon_per_unit * theoretical_l_star
        theoretical_coupon_to_payroll = theoretical_coupon_star / payroll_0 if payroll_0 > 0 else math.nan
        theoretical_issuance_proceeds = steady_new_units * steady_issue_price
        theoretical_issuance_coverage_ratio = (
            theoretical_issuance_proceeds / theoretical_coupon_star
            if theoretical_coupon_star > 0 else math.nan
        )
        theoretical_operating_cash_flow = cfg.operating_margin_on_payroll * payroll_0
        theoretical_operating_coupon_coverage = (
            theoretical_operating_cash_flow / theoretical_coupon_star
            if theoretical_coupon_star > 0 else math.nan
        )

        lines.append("")
        lines.append("THEORETICAL STEADY STATE (ZERO-GROWTH CASE)")
        lines.append("-" * 60)
        lines.append(f"theoretical_new_claim_units_per_period: {steady_new_units:,.6f}")
        lines.append(f"theoretical_L_star: {theoretical_l_star:,.6f}")
        lines.append(f"theoretical_coupon_star: {theoretical_coupon_star:,.6f}")
        lines.append(f"theoretical_coupon_to_payroll: {theoretical_coupon_to_payroll:,.6f}")
        lines.append(f"theoretical_new_issuance_proceeds: {theoretical_issuance_proceeds:,.6f}")
        lines.append(f"theoretical_issuance_coverage_ratio: {theoretical_issuance_coverage_ratio:,.6f}")
        lines.append(f"theoretical_operating_cash_flow: {theoretical_operating_cash_flow:,.6f}")
        lines.append(f"theoretical_operating_coupon_coverage_ratio: {theoretical_operating_coupon_coverage:,.6f}")

    return "\n".join(lines)


def run_phase1(cfg: Phase1Config) -> tuple[pd.DataFrame, pd.DataFrame]:
    out_dir = ensure_dir(cfg.output_dir)

    q_out = fair_value_outstanding_unit(cfg)
    q_issue_fair = fair_value_new_issue_unit(cfg)
    issue_px = claim_issue_price(cfg)

    # Claim cohorts are issuance vintages.
    # Each cohort stores the number of outstanding claim units that remain alive.
    claim_cohorts: list[dict[str, float]] = []
    if cfg.initial_claim_units > 0.0:
        claim_cohorts.append({"birth_t": -1.0, "units": cfg.initial_claim_units})

    records: list[dict[str, float]] = []
    ledger: list[dict[str, float]] = []

    # Survival probability at the start of period t.
    survival_prob = 1.0

    for t in range(cfg.horizon_periods):
        workers = workers_in_period(cfg, t)
        wage = wage_in_period(cfg, t)
        payroll = workers * wage

        outstanding_claim_units_if_alive = sum(c["units"] for c in claim_cohorts)
        expected_claim_units = survival_prob * outstanding_claim_units_if_alive

        coupon_cash_obligation_if_alive = cfg.coupon_per_unit * outstanding_claim_units_if_alive
        expected_coupon = survival_prob * coupon_cash_obligation_if_alive

        market_value_of_claims_if_alive = q_out * outstanding_claim_units_if_alive
        survival_weighted_market_value = survival_prob * market_value_of_claims_if_alive

        coupon_to_payroll_if_alive = (
            coupon_cash_obligation_if_alive / payroll if payroll > 0 else math.nan
        )
        market_value_to_payroll_if_alive = (
            market_value_of_claims_if_alive / payroll if payroll > 0 else math.nan
        )

        # Dollar value of compensation diverted into newly issued claims this period.
        accrual_dollars = cfg.accrual_share * payroll

        # New claim units issued at end of period.
        new_claim_units_issued = accrual_dollars / issue_px if issue_px > 0 else 0.0

        # Gross proceeds notionally associated with new issuance.
        new_issuance_proceeds = new_claim_units_issued * issue_px

        # Diagnostic: how much of current coupon obligations would be covered
        # if the current period's new issuance proceeds were used to pay them?
        issuance_coverage_ratio = (
            new_issuance_proceeds / coupon_cash_obligation_if_alive
            if coupon_cash_obligation_if_alive > 0 else math.nan
        )

        # Diagnostic: coupon burden relative to this period's fresh accrual pool.
        coupon_to_accrual_ratio = (
            coupon_cash_obligation_if_alive / accrual_dollars
            if accrual_dollars > 0 else math.nan
        )

        # Positive means coupons exceed current issuance proceeds.
        # This does not prove a Ponzi structure, but measures the financing gap
        # that must be covered by operating cash flow or other sources.
        ponzi_financing_gap = coupon_cash_obligation_if_alive - new_issuance_proceeds

        # Optional operating support diagnostics.
        operating_cash_flow = cfg.operating_margin_on_payroll * payroll
        operating_coupon_coverage_ratio = (
            operating_cash_flow / coupon_cash_obligation_if_alive
            if coupon_cash_obligation_if_alive > 0 else math.nan
        )
        residual_after_coupons = operating_cash_flow - coupon_cash_obligation_if_alive

        records.append(
            {
                "period": float(t),
                "workers": workers,
                "wage_per_worker": wage,
                "payroll": payroll,
                "accrual_dollars": accrual_dollars,
                "survival_prob_start": survival_prob,
                "runoff_rate": cfg.runoff_rate,
                "default_hazard": cfg.default_hazard,
                "discount_rate": cfg.discount_rate,
                "coupon_per_unit": cfg.coupon_per_unit,
                "fair_value_outstanding_unit": q_out,
                "fair_value_new_issue_unit": q_issue_fair,
                "claim_issue_price_used": issue_px,
                "issue_price_to_fair_new_issue_ratio": issue_px / q_issue_fair,
                "outstanding_claim_units_if_alive": outstanding_claim_units_if_alive,
                "expected_claim_units": expected_claim_units,
                "coupon_cash_obligation_if_alive": coupon_cash_obligation_if_alive,
                "expected_coupon": expected_coupon,
                "coupon_to_payroll_if_alive": coupon_to_payroll_if_alive,
                "coupon_to_accrual_ratio": coupon_to_accrual_ratio,
                "market_value_of_claims_if_alive": market_value_of_claims_if_alive,
                "survival_weighted_market_value": survival_weighted_market_value,
                "market_value_to_payroll_if_alive": market_value_to_payroll_if_alive,
                "new_claim_units_issued": new_claim_units_issued,
                "new_issuance_proceeds": new_issuance_proceeds,
                "issuance_coverage_ratio": issuance_coverage_ratio,
                "ponzi_financing_gap": ponzi_financing_gap,
                "operating_cash_flow": operating_cash_flow,
                "operating_coupon_coverage_ratio": operating_coupon_coverage_ratio,
                "residual_after_coupons": residual_after_coupons,
            }
        )

        for c in claim_cohorts:
            ledger.append(
                {
                    "period": float(t),
                    "cohort_birth_t": c["birth_t"],
                    "cohort_age": float(t - c["birth_t"]),
                    "claim_units_if_alive": c["units"],
                    "expected_claim_units": survival_prob * c["units"],
                }
            )

        # Transition to next period:
        # 1) existing claim units run off
        # 2) new claim units are issued at end of period and appear next period
        for c in claim_cohorts:
            c["units"] *= (1.0 - cfg.runoff_rate)

        if new_claim_units_issued > 0.0:
            claim_cohorts.append({"birth_t": float(t), "units": new_claim_units_issued})

        # Firm survival to next period
        survival_prob *= (1.0 - cfg.default_hazard)

    df = pd.DataFrame(records)
    ledger_df = pd.DataFrame(ledger)

    df.to_csv(out_dir / "phase1_timeseries.csv", index=False)
    ledger_df.to_csv(out_dir / "phase1_claim_cohort_ledger.csv", index=False)

    save_line_plot(
        df,
        x_col="period",
        y_cols=["outstanding_claim_units_if_alive", "expected_claim_units"],
        title="Outstanding Claim Units",
        y_label="units",
        out_path=out_dir / "claim_units_over_time.png",
    )

    save_line_plot(
        df,
        x_col="period",
        y_cols=["coupon_cash_obligation_if_alive", "expected_coupon"],
        title="Coupon Cash Obligation",
        y_label="dollars per period",
        out_path=out_dir / "coupon_obligation_over_time.png",
    )

    save_line_plot(
        df,
        x_col="period",
        y_cols=["market_value_of_claims_if_alive", "survival_weighted_market_value"],
        title="Market Value of Outstanding Claims",
        y_label="dollars",
        out_path=out_dir / "market_value_over_time.png",
    )

    save_line_plot(
        df,
        x_col="period",
        y_cols=["coupon_to_payroll_if_alive", "market_value_to_payroll_if_alive"],
        title="Claim Burden Relative to Payroll",
        y_label="ratio",
        out_path=out_dir / "burden_relative_to_payroll.png",
    )

    save_line_plot(
        df,
        x_col="period",
        y_cols=["new_issuance_proceeds", "coupon_cash_obligation_if_alive", "ponzi_financing_gap"],
        title="Coupon Burden vs New Issuance Proceeds",
        y_label="dollars",
        out_path=out_dir / "coupon_vs_issuance.png",
    )

    save_line_plot(
        df,
        x_col="period",
        y_cols=["issuance_coverage_ratio", "operating_coupon_coverage_ratio"],
        title="Coverage Ratios",
        y_label="ratio",
        out_path=out_dir / "coverage_ratios.png",
    )

    save_line_plot(
        df,
        x_col="period",
        y_cols=["survival_prob_start"],
        title="Firm Survival Probability at Start of Period",
        y_label="probability",
        out_path=out_dir / "survival_probability.png",
    )

    save_cohort_stackplot(
        ledger_df=ledger_df,
        out_path=out_dir / "top_claim_cohort_stack.png",
        top_n=cfg.cohort_plot_top_n,
    )

    summary_text = build_summary(cfg, df)
    (out_dir / "summary.txt").write_text(summary_text, encoding="utf-8")

    print(summary_text)
    print(f"\nSaved outputs to: {out_dir.resolve()}")

    return df, ledger_df


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run phase 1 deterministic claim-issuance cohort simulation."
    )
    parser.add_argument(
        "--config",
        type=str,
        default="sim/config_coupons.yaml",
        help="Path to YAML config file.",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    run_phase1(cfg)


if __name__ == "__main__":
    main()