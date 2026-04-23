# Simulator

This simulator is the fastest way to understand the burden dynamics of TLY.
It should be launchable with one command from a clean environment.

This folder contains the Python reference model and Streamlit entrypoint used
to explore TLY burden dynamics. In the revised paper framing, the simulator is
mostly a Stress Layer tool: it helps test whether a bounded mechanism is
actually affordable under payroll, turnover, margin, reserve, and parameter
assumptions.

## Core Files

- `app.py`
  - Streamlit interface
- `baseline_dollars.py`
  - baseline dollar-state simulator
- `baseline_coupons.py`
  - coupon-state simulator
- `comparative_statistics.py`
  - comparative metrics
- `plotting.py`
  - charts and output helpers
- `config.yaml`
  - baseline config
- `config_coupons.yaml`
  - coupon config

## Typical Use

From this folder:

```bash
uv run streamlit run app.py
```

The simulator is a planning tool for burden dynamics. It is not a solvency
guarantee and does not substitute for treasury, legal, or compensation review.

## What To Look For

Useful outputs for the publication draft include:

- trailing burden / active payroll;
- trailing burden / margin or operating surplus;
- reserve coverage;
- forward claim coverage;
- active versus legacy payout mix;
- cohort runoff under different taper and duration settings;
- stress cases such as revenue shock, payroll contraction, turnover spike, or
  reserve decline.

Scenario presets should eventually include conservative, growth, treasury
stress, high turnover, and early-stage threshold-activated cases.

## Quickstart

```bash
uv sync
uv run streamlit run app.py
```

## Environment

Dependencies are defined in `pyproject.toml`. If `uv` is not already
installed, see https://docs.astral.sh/uv/ for installation instructions.
