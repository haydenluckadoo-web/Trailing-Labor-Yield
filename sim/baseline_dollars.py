from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import matplotlib.pyplot as plt
import pandas as pd
import yaml

@dataclass
class DecayingAnnuityConfig:
    horizon_periods: int
    initial_workers: float
    worker_growth: float
    wage_per_worker: float
    wage_growth: float
    accrual_share: float
    turnover_rate: float
    legacy_payout_years: int
    annuity_decay_rate: float
    revenue_multiplier: float
    gross_margin: float
    output_dir: str

def load_config(path: str | Path) -> DecayingAnnuityConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw: dict[str, Any] = yaml.safe_load(f)

    return DecayingAnnuityConfig(
        horizon_periods=int(raw.get("horizon_periods", 80)),
        initial_workers=float(raw.get("initial_workers", 1000)),
        worker_growth=float(raw.get("worker_growth", 0.02)),
        wage_per_worker=float(raw.get("wage_per_worker", 100000)),
        wage_growth=float(raw.get("wage_growth", 0.02)),
        accrual_share=float(raw.get("accrual_share", 0.01)),
        turnover_rate=float(raw.get("turnover_rate", 0.08)),
        legacy_payout_years=int(raw.get("legacy_payout_years", 25)),
        annuity_decay_rate=float(raw.get("annuity_decay_rate", 0.05)),
        revenue_multiplier=float(raw.get("revenue_multiplier", 3.0)),
        gross_margin=float(raw.get("gross_margin", 0.60)),
        output_dir=str(raw.get("output_dir", "sim/output_decay_annuity")),
    )

def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out

def save_line_plot(df: pd.DataFrame, x_col: str, y_cols: list[str], title: str, y_label: str, out_path: Path) -> None:
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

def save_stack_plot(df: pd.DataFrame, x_col: str, y_cols: list[str], title: str, out_path: Path) -> None:
    plt.figure(figsize=(10, 6))
    plt.stackplot(df[x_col], *[df[col] for col in y_cols], labels=y_cols)
    plt.title(title)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def run_simulation(cfg: DecayingAnnuityConfig) -> pd.DataFrame:
    out_dir = ensure_dir(cfg.output_dir)
    records = []
    
    historical_pay_pool = 0.0
    legacy_cohorts = []
    
    for t in range(cfg.horizon_periods):
        workers = cfg.initial_workers * ((1.0 + cfg.worker_growth) ** t)
        wage = cfg.wage_per_worker * ((1.0 + cfg.wage_growth) ** t)
        base_payroll = workers * wage
        
        revenue = base_payroll * cfg.revenue_multiplier
        gross_profit = revenue * cfg.gross_margin
        
        active_bonus = (historical_pay_pool + base_payroll) * cfg.accrual_share
        
        current_legacy_payout = 0.0
        for cohort in legacy_cohorts:
            if cohort["age"] < cfg.legacy_payout_years:
                payout_this_year = cohort["amount"] * ((1.0 - cfg.annuity_decay_rate) ** cohort["age"])
                current_legacy_payout += payout_this_year
                cohort["age"] += 1
                
        total_cash_outflow = base_payroll + active_bonus + current_legacy_payout
        annuity_pct_of_gross_profit = current_legacy_payout / gross_profit if gross_profit > 0 else 0
        
        records.append({
            "period": t,
            "base_payroll": base_payroll,
            "gross_profit": gross_profit,
            "active_bonus_payout": active_bonus,
            "legacy_annuity_payout": current_legacy_payout,
            "total_cash_outflow": total_cash_outflow,
            "annuity_pct_of_gross_profit": annuity_pct_of_gross_profit * 100
        })
        
        new_legacy_cohort = active_bonus * cfg.turnover_rate
        legacy_cohorts.append({"amount": new_legacy_cohort, "age": 0})
        
        historical_pay_pool = (historical_pay_pool + base_payroll + active_bonus) * (1.0 - cfg.turnover_rate)

    df = pd.DataFrame(records)
    df.to_csv(out_dir / "decay_annuity_timeseries.csv", index=False)

    # 1. Gross Profit vs Total Cash Outflows
    save_line_plot(df, "period", ["gross_profit", "total_cash_outflow"], "Gross Profit vs Total Cash Outflows", "Dollars", out_dir / "profit_vs_outflows.png")
    
    # 2. Annuity as a percent of Gross Profit
    save_line_plot(df, "period", ["annuity_pct_of_gross_profit"], "Annuity Burden (% of Gross Profit)", "Percentage", out_dir / "annuity_burden_pct.png")

    # 3. Stacked Cash Outflows Breakdown
    save_stack_plot(df, "period", ["base_payroll", "active_bonus_payout", "legacy_annuity_payout"], "Cash Outflows Breakdown", out_dir / "cash_outflows_stack.png")

    print(f"Simulation complete. Outputs saved to {out_dir.resolve()}")
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="sim/config.yaml")
    args = parser.parse_args()
    cfg = load_config(args.config)
    run_simulation(cfg)