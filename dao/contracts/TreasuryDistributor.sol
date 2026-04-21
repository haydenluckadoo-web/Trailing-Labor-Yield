// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

import {IContributorRegistry} from "./interfaces/IContributorRegistry.sol";
import {ITreasuryDistributor} from "./interfaces/ITreasuryDistributor.sol";
import {WadMath} from "./libraries/WadMath.sol";

contract TreasuryDistributor is AccessControl, ReentrancyGuard, ITreasuryDistributor {
    using SafeERC20 for IERC20;
    using WadMath for uint256;

    bytes32 public constant DAO_ADMIN_ROLE = keccak256("DAO_ADMIN_ROLE");
    uint256 private constant WAD = 1e18;

    error ZeroAddress();
    error InvalidConfig();
    error NotActive();
    error NotLegacy();
    error NothingToClaim();
    error NoSettledEpochAvailable();
    error LegacyClaimsArePaused();

    IERC20 public immutable paymentToken;
    IContributorRegistry public immutable registry;

    uint64 public immutable startTimestamp;
    uint64 public immutable epochLength;
    uint64 public immutable maxLegacyEpochs;
    uint64 public immutable maxEpochsPerClaim;

    uint256 public immutable accrualShareWad;
    uint256 public immutable taperFactorPerEpochWad;

    bool public legacyClaimsPaused;

    constructor(
        IERC20 paymentToken_,
        IContributorRegistry registry_,
        uint64 startTimestamp_,
        uint64 epochLength_,
        uint256 accrualShareWad_,
        uint256 taperFactorPerEpochWad_,
        uint64 maxLegacyEpochs_,
        uint64 maxEpochsPerClaim_,
        address daoAdmin
    ) {
        if (
            address(paymentToken_) == address(0) ||
            address(registry_) == address(0) ||
            daoAdmin == address(0)
        ) {
            revert ZeroAddress();
        }

        if (
            epochLength_ == 0 ||
            accrualShareWad_ > WAD ||
            taperFactorPerEpochWad_ > WAD ||
            maxLegacyEpochs_ == 0 ||
            maxEpochsPerClaim_ == 0
        ) {
            revert InvalidConfig();
        }

        paymentToken = paymentToken_;
        registry = registry_;
        startTimestamp = startTimestamp_;
        epochLength = epochLength_;
        accrualShareWad = accrualShareWad_;
        taperFactorPerEpochWad = taperFactorPerEpochWad_;
        maxLegacyEpochs = maxLegacyEpochs_;
        maxEpochsPerClaim = maxEpochsPerClaim_;

        _grantRole(DEFAULT_ADMIN_ROLE, daoAdmin);
        _grantRole(DAO_ADMIN_ROLE, daoAdmin);
    }

    function fund(uint256 amount) external {
        paymentToken.safeTransferFrom(msg.sender, address(this), amount);
        emit TreasuryFunded(msg.sender, amount);
    }

    function pauseLegacyClaims() external onlyRole(DAO_ADMIN_ROLE) {
        legacyClaimsPaused = true;
        emit LegacyClaimsPaused(msg.sender);
    }

    function unpauseLegacyClaims() external onlyRole(DAO_ADMIN_ROLE) {
        legacyClaimsPaused = false;
        emit LegacyClaimsUnpaused(msg.sender);
    }

    function currentEpoch() public view returns (uint64) {
        if (block.timestamp < startTimestamp) {
            return 0;
        }

        return uint64((block.timestamp - startTimestamp) / epochLength);
    }

    function previewActiveComp(address contributor)
        public
        view
        returns (
            uint64 epochToSettle,
            uint256 basePay,
            uint256 activeBonus,
            uint256 total
        )
    {
        IContributorRegistry.ContributorState memory state =
            registry.contributorState(contributor);

        if (state.status != IContributorRegistry.Status.Active) {
            revert NotActive();
        }

        epochToSettle = state.lastSettledEpoch + 1;

        if (currentEpoch() < epochToSettle) {
            revert NoSettledEpochAvailable();
        }

        basePay = state.basePayPerEpoch;
        activeBonus =
            (state.historicalPayPool + state.basePayPerEpoch).mulWadDown(accrualShareWad);
        total = basePay + activeBonus;
    }

    function claimActiveComp() external nonReentrant returns (uint256 paid) {
        address contributor = msg.sender;

        (
            uint64 epochToSettle,
            uint256 basePay,
            uint256 activeBonus,
            uint256 total
        ) = previewActiveComp(contributor);

        IContributorRegistry.ContributorState memory state =
            registry.contributorState(contributor);

        registry.settleActiveEpoch(contributor, epochToSettle, activeBonus);

        paid = total;
        paymentToken.safeTransfer(state.payoutAddress, paid);

        emit ActiveCompClaimed(
            contributor,
            state.payoutAddress,
            epochToSettle,
            basePay,
            activeBonus,
            paid
        );
    }

    function previewTrailingYield(address contributor)
        public
        view
        returns (
            uint64 claimThroughEpoch,
            uint256 epochsClaimed,
            uint256 claimable
        )
    {
        IContributorRegistry.ContributorState memory state =
            registry.contributorState(contributor);

        if (state.status != IContributorRegistry.Status.Legacy) {
            revert NotLegacy();
        }

        uint64 claimFromEpoch = state.lastLegacyClaimEpoch + 1;
        uint64 finalClaimableEpoch = currentEpoch();
        uint64 finalLegacyEpoch = state.departureEpoch + maxLegacyEpochs;

        if (finalClaimableEpoch > finalLegacyEpoch) {
            finalClaimableEpoch = finalLegacyEpoch;
        }

        if (claimFromEpoch > finalClaimableEpoch) {
            return (state.lastLegacyClaimEpoch, 0, 0);
        }

        epochsClaimed = finalClaimableEpoch - claimFromEpoch + 1;

        if (epochsClaimed > maxEpochsPerClaim) {
            epochsClaimed = maxEpochsPerClaim;
        }

        claimThroughEpoch = claimFromEpoch + uint64(epochsClaimed) - 1;
        claimable = _legacyClaimSum(state, claimFromEpoch, uint64(epochsClaimed));
    }

    function claimTrailingYield() external nonReentrant returns (uint256 paid) {
        if (legacyClaimsPaused) {
            revert LegacyClaimsArePaused();
        }

        address contributor = msg.sender;

        (
            uint64 claimThroughEpoch,
            uint256 epochsClaimed,
            uint256 claimable
        ) = previewTrailingYield(contributor);

        if (claimable == 0) {
            revert NothingToClaim();
        }

        IContributorRegistry.ContributorState memory state =
            registry.contributorState(contributor);

        registry.markLegacyClaimed(contributor, claimThroughEpoch);

        paid = claimable;
        paymentToken.safeTransfer(state.payoutAddress, paid);

        emit TrailingYieldClaimed(
            contributor,
            state.payoutAddress,
            claimThroughEpoch,
            epochsClaimed,
            paid
        );
    }

    function _legacyClaimSum(
        IContributorRegistry.ContributorState memory state,
        uint64 claimFromEpoch,
        uint64 epochsClaimed
    ) private view returns (uint256 claimable) {
        for (uint64 i = 0; i < epochsClaimed; ++i) {
            uint256 elapsedEpochs = claimFromEpoch + i - state.departureEpoch;
            uint256 taperMultiplierWad =
                WadMath.rpowWad(taperFactorPerEpochWad, elapsedEpochs);

            claimable += state.initialLegacyAmount.mulWadDown(taperMultiplierWad);
        }
    }
}
