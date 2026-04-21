// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ITreasuryDistributor {
    event ActiveCompClaimed(
        address indexed contributor,
        address indexed payoutAddress,
        uint64 indexed settledEpoch,
        uint256 basePay,
        uint256 activeBonus,
        uint256 totalPaid
    );

    event TrailingYieldClaimed(
        address indexed contributor,
        address indexed payoutAddress,
        uint64 indexed claimThroughEpoch,
        uint256 epochsClaimed,
        uint256 amount
    );

    event TreasuryFunded(address indexed funder, uint256 amount);
    event LegacyClaimsPaused(address indexed admin);
    event LegacyClaimsUnpaused(address indexed admin);

    function currentEpoch() external view returns (uint64);

    function previewActiveComp(address contributor)
        external
        view
        returns (
            uint64 epochToSettle,
            uint256 basePay,
            uint256 activeBonus,
            uint256 total
        );

    function claimActiveComp() external returns (uint256 paid);

    function previewTrailingYield(address contributor)
        external
        view
        returns (
            uint64 claimThroughEpoch,
            uint256 epochsClaimed,
            uint256 claimable
        );

    function claimTrailingYield() external returns (uint256 paid);

    function pauseLegacyClaims() external;

    function unpauseLegacyClaims() external;
}
