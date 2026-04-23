# Contributing

Thanks for taking the mechanism seriously enough to critique it.

## What Feedback Is Most Useful

At this stage, the most valuable contributions are:

- mathematical edge cases or errors in the burden logic;
- critiques of the steady-state or runoff assumptions;
- critiques of the Pure TLY / Stress Layer / Governance Wrapper separation;
- simulation bugs, parameter inconsistencies, or missing sensitivity tests;
- missing treasury-health metrics, reserve-coverage logic, or stress cases;
- EVM architecture concerns, especially claim logic, access control, and gas;
- anti-gaming concerns, especially exit snapshots, realized-compensation
  averaging, pay-lock rules, and contributor-admin authority;
- naming, clarity, or framing changes that make the paper more legible to
  founders, operators, and researchers.

## Where To Put Feedback

- Use **GitHub Discussions** for high-level mechanism, economic, governance, or
  legal-structure discussion.
- Use **Issues** for concrete bugs, broken links, simulator failures, test
  failures, or clearly scoped implementation defects.

If Discussions are not yet enabled on the repository, enabling them should be
treated as part of the publication setup.

## Out Of Scope For This Draft

This repository is not currently seeking:

- audit sign-off;
- production deployment requests;
- token launch design;
- legal wrappers or jurisdiction-specific contract drafting;
- commercialization or pricing discussions.

## Before Opening A Technical Report

Please try to include:

- the file and section involved;
- the parameter set or scenario that exposes the issue;
- expected behavior versus observed behavior;
- for simulator reports, the exact command used to reproduce the issue.

## Security

These Solidity contracts are unaudited reference contracts. Do not route real
capital through them. If you identify a security-sensitive issue, please report
it responsibly instead of framing it as production-safe code.
