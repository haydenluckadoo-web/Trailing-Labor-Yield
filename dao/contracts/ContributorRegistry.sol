// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

import {IContributorRegistry} from "./interfaces/IContributorRegistry.sol";

contract ContributorRegistry is AccessControl, IContributorRegistry {
    bytes32 public constant POD_ADMIN_ROLE = keccak256("POD_ADMIN_ROLE");

    error ZeroAddress();
    error ContributorExists();
    error ContributorMissing();
    error NotTreasuryDistributor();
    error NotActive();
    error NotLegacy();
    error InvalidEpoch();
    error NoActiveBonus();

    address public treasuryDistributor;

    mapping(address contributor => ContributorState state) private contributors;

    event TreasuryDistributorSet(address indexed treasuryDistributor);

    modifier onlyTreasuryDistributor() {
        if (msg.sender != treasuryDistributor) {
            revert NotTreasuryDistributor();
        }
        _;
    }

    constructor(address daoAdmin, address podAdmin) {
        if (daoAdmin == address(0) || podAdmin == address(0)) {
            revert ZeroAddress();
        }

        _grantRole(DEFAULT_ADMIN_ROLE, daoAdmin);
        _grantRole(POD_ADMIN_ROLE, podAdmin);
    }

    function setTreasuryDistributor(address newTreasuryDistributor)
        external
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        if (newTreasuryDistributor == address(0)) {
            revert ZeroAddress();
        }

        treasuryDistributor = newTreasuryDistributor;
        emit TreasuryDistributorSet(newTreasuryDistributor);
    }

    function contributorState(address contributor)
        external
        view
        returns (ContributorState memory)
    {
        return contributors[contributor];
    }

    function addContributor(
        address contributor,
        address payoutAddress,
        uint256 basePayPerEpoch,
        uint64 joinedEpoch
    ) external onlyRole(POD_ADMIN_ROLE) {
        if (contributor == address(0) || payoutAddress == address(0)) {
            revert ZeroAddress();
        }

        if (contributors[contributor].status != Status.None) {
            revert ContributorExists();
        }

        contributors[contributor] = ContributorState({
            status: Status.Active,
            payoutAddress: payoutAddress,
            basePayPerEpoch: basePayPerEpoch,
            historicalPayPool: 0,
            lastActiveBonus: 0,
            initialLegacyAmount: 0,
            joinedEpoch: joinedEpoch,
            lastSettledEpoch: joinedEpoch,
            departureEpoch: 0,
            lastLegacyClaimEpoch: 0
        });

        emit ContributorAdded(contributor, payoutAddress, basePayPerEpoch, joinedEpoch);
    }

    function updatePayoutAddress(
        address contributor,
        address newPayoutAddress
    ) external onlyRole(POD_ADMIN_ROLE) {
        if (newPayoutAddress == address(0)) {
            revert ZeroAddress();
        }

        ContributorState storage state = _existingContributor(contributor);

        address oldPayoutAddress = state.payoutAddress;
        state.payoutAddress = newPayoutAddress;

        emit PayoutAddressUpdated(contributor, oldPayoutAddress, newPayoutAddress);
    }

    function updateBasePay(
        address contributor,
        uint256 newBasePayPerEpoch
    ) external onlyRole(POD_ADMIN_ROLE) {
        ContributorState storage state = _existingContributor(contributor);

        if (state.status != Status.Active) {
            revert NotActive();
        }

        uint256 oldBasePayPerEpoch = state.basePayPerEpoch;
        state.basePayPerEpoch = newBasePayPerEpoch;

        emit BasePayUpdated(contributor, oldBasePayPerEpoch, newBasePayPerEpoch);
    }

    function removeContributor(
        address contributor,
        uint64 departureEpoch
    ) external onlyRole(POD_ADMIN_ROLE) {
        _transitionToLegacy(contributor, departureEpoch);
    }

    function settleActiveEpoch(
        address contributor,
        uint64 epoch,
        uint256 activeBonus
    ) external onlyTreasuryDistributor {
        ContributorState storage state = _existingContributor(contributor);

        if (state.status != Status.Active) {
            revert NotActive();
        }

        if (epoch != state.lastSettledEpoch + 1) {
            revert InvalidEpoch();
        }

        state.historicalPayPool =
            state.historicalPayPool + state.basePayPerEpoch + activeBonus;
        state.lastActiveBonus = activeBonus;
        state.lastSettledEpoch = epoch;

        emit ContributorSettled(
            contributor,
            epoch,
            state.basePayPerEpoch,
            activeBonus,
            state.historicalPayPool
        );
    }

    function transitionToLegacy(
        address contributor,
        uint64 departureEpoch
    ) external onlyRole(POD_ADMIN_ROLE) {
        _transitionToLegacy(contributor, departureEpoch);
    }

    function markLegacyClaimed(
        address contributor,
        uint64 claimEpoch
    ) external onlyTreasuryDistributor {
        ContributorState storage state = _existingContributor(contributor);

        if (state.status != Status.Legacy) {
            revert NotLegacy();
        }

        if (claimEpoch <= state.lastLegacyClaimEpoch) {
            revert InvalidEpoch();
        }

        state.lastLegacyClaimEpoch = claimEpoch;

        emit LegacyClaimMarked(contributor, claimEpoch);
    }

    function _transitionToLegacy(address contributor, uint64 departureEpoch) private {
        ContributorState storage state = _existingContributor(contributor);

        if (state.status != Status.Active) {
            revert NotActive();
        }

        if (departureEpoch < state.lastSettledEpoch) {
            revert InvalidEpoch();
        }

        if (state.lastActiveBonus == 0) {
            revert NoActiveBonus();
        }

        state.status = Status.Legacy;
        state.departureEpoch = departureEpoch;
        state.lastLegacyClaimEpoch = departureEpoch;
        state.initialLegacyAmount = state.lastActiveBonus;

        emit ContributorTransitionedToLegacy(
            contributor,
            departureEpoch,
            state.initialLegacyAmount
        );
    }

    function _existingContributor(address contributor)
        private
        view
        returns (ContributorState storage state)
    {
        state = contributors[contributor];

        if (state.status == Status.None) {
            revert ContributorMissing();
        }
    }
}
