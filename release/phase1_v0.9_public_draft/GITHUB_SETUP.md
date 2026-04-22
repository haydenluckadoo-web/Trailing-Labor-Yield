# GitHub Setup Notes

This file is a practical setup guide for making GitHub the canonical public home of the first TLY release.

## Suggested Repository Name

- `trailing-labor-yield`
- `tly-white-paper`
- `tly-protocol`

## Suggested Repository Description

Trailing Labor Yield (TLY): a stablecoin-based contributor compensation mechanism with tapering legacy payouts, simulation code, and EVM reference contracts.

## Suggested Topics

- `dao`
- `solidity`
- `mechanism-design`
- `cryptoeconomics`
- `compensation`
- `stablecoin`
- `governance`
- `simulation`
- `tokenomics`

## Suggested Front Page Shape

This repo root should make four things immediately visible:

1. what TLY is;
2. where the white paper lives;
3. where the simulator lives;
4. where the Solidity reference implementation lives.

It should also make two governance signals obvious:

1. the contracts are unaudited reference contracts;
2. critique is welcome through GitHub Discussions and scoped Issues.

## Suggested Top-Level Repo Layout

- `LICENSE`
- `CONTRIBUTING.md`
- `README.md`
- `paper/`
- `sim/`
- `dao/`
- `release/phase1_v0.9_public_draft/`

This layout keeps the publication layer visible without hiding the simulator or
the Solidity reference implementation.

## Suggested First Paragraph For The Repo Root

Trailing Labor Yield (TLY) is a stablecoin-denominated contributor compensation mechanism that combines normal active pay, a small compounding active bonus tied to historical pay, and a tapering trailing payout after exit. This repository contains the public white paper, one-page summary, FAQ, simulator, and EVM reference contracts.

## Suggested Pinned Links

- White paper
- White paper PDF
- One-page summary
- FAQ
- Simulator
- Solidity contracts

## Repository Settings To Enable

- Turn on **GitHub Discussions** for mechanism-design, governance, legal-
  structure, and economic critique.
- Leave **Issues** enabled for concrete bugs in the paper, simulator, or
  contracts.
- Add the repo description and topics before the first public link goes out.

## Suggested Release Tag

- `v0.9-public-draft`
