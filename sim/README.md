# Simulator

This folder contains the Python reference model and Streamlit entrypoint used
to explore TLY burden dynamics.

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
streamlit run app.py
```

The simulator is a planning tool for burden dynamics. It is not a solvency
guarantee and does not substitute for treasury, legal, or compensation review.
