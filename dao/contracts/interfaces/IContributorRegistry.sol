// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IContributorRegistry {
    enum Status {
        None,
        Active,
        Legacy,
        Removed
    }

    struct ContributorState {
        Status status;
        address payoutAddress;
        uint256 basePayPerEpoch;
        uint256 historicalPayPool;
        uint256 lastActiveBonus;
        uint256 initialLegacyAmount;
        uint64 joinedEpoch;
        uint64 lastSettledEpoch;
        uint64 departureEpoch;
        uint64 lastLegacyClaimEpoch;
    }

    event ContributorAdded(
        address indexed contributor,
        address indexed payoutAddress,
        uint256 basePayPerEpoch,
        uint64 joinedEpoch
    );

    event PayoutAddressUpdated(
        address indexed contributor,
        address indexed oldPayoutAddress,
        address indexed newPayoutAddress
    );

    event BasePayUpdated(
        address indexed contributor,
        uint256 oldBasePayPerEpoch,
        uint256 newBasePayPerEpoch
    );

    event ContributorSettled(
        address indexed contributor,
        uint64 indexed epoch,
        uint256 basePay,
        uint256 activeBonus,
        uint256 historicalPayPool
    );

    event ContributorTransitionedToLegacy(
        address indexed contributor,
        uint64 indexed departureEpoch,
        uint256 initialLegacyAmount
    );

    event LegacyClaimMarked(
        address indexed contributor,
        uint64 indexed claimEpoch
    );

    function contributorState(address contributor)
        external
        view
        returns (ContributorState memory);

    function addContributor(
        address contributor,
        address payoutAddress,
        uint256 basePayPerEpoch,
        uint64 joinedEpoch
    ) external;

    function updatePayoutAddress(
        address contributor,
        address newPayoutAddress
    ) external;

    function updateBasePay(
        address contributor,
        uint256 newBasePayPerEpoch
    ) external;

    function removeContributor(
        address contributor,
        uint64 departureEpoch
    ) external;

    function settleActiveEpoch(
        address contributor,
        uint64 epoch,
        uint256 activeBonus
    ) external;

    function transitionToLegacy(
        address contributor,
        uint64 departureEpoch
    ) external;

    function markLegacyClaimed(
        address contributor,
        uint64 claimEpoch
    ) external;
}
