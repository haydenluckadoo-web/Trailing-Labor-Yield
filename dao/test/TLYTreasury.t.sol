// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import {ContributorRegistry} from "../contracts/ContributorRegistry.sol";
import {TreasuryDistributor} from "../contracts/TreasuryDistributor.sol";
import {IContributorRegistry} from "../contracts/interfaces/IContributorRegistry.sol";
import {WadMath} from "../contracts/libraries/WadMath.sol";
import {MockERC20} from "./mocks/MockERC20.sol";

contract TLYTreasuryTest is Test {
    using WadMath for uint256;

    uint64 private constant START = 1_700_000_000;
    uint64 private constant EPOCH = 365 days;
    uint64 private constant MAX_LEGACY_EPOCHS = 25;
    uint64 private constant MAX_EPOCHS_PER_CLAIM = 12;

    uint256 private constant ACCRUAL_SHARE_WAD = 0.01e18;
    uint256 private constant TAPER_FACTOR_WAD = 0.95e18;
    uint256 private constant BASE_PAY = 100_000e6;

    address private daoAdmin = address(this);
    address private podAdmin = address(0xB0D);
    address private lifer = address(0xA11CE);
    address private alumni = address(0xB0B);
    address private active = address(0xC0DE);

    MockERC20 private token;
    ContributorRegistry private registry;
    TreasuryDistributor private treasury;

    function setUp() public {
        vm.warp(START);

        token = new MockERC20("Mock USDC", "mUSDC", 6);
        registry = new ContributorRegistry(daoAdmin, podAdmin);
        treasury = new TreasuryDistributor(
            IERC20(address(token)),
            registry,
            START,
            EPOCH,
            ACCRUAL_SHARE_WAD,
            TAPER_FACTOR_WAD,
            MAX_LEGACY_EPOCHS,
            MAX_EPOCHS_PER_CLAIM,
            daoAdmin
        );

        registry.setTreasuryDistributor(address(treasury));

        token.mint(address(this), 1_000_000_000e6);
        token.approve(address(treasury), type(uint256).max);
        treasury.fund(1_000_000_000e6);
    }

    function testTwentyYearLiferClaimsFirstLegacyEpoch() public {
        _addContributor(lifer);
        _settleActiveEpochs(lifer, 20);

        vm.prank(podAdmin);
        registry.removeContributor(lifer, 20);

        IContributorRegistry.ContributorState memory state =
            registry.contributorState(lifer);

        assertEq(uint8(state.status), uint8(IContributorRegistry.Status.Legacy));
        assertGt(state.initialLegacyAmount, 0);

        vm.warp(START + 21 * EPOCH);

        uint256 expected =
            state.initialLegacyAmount.mulWadDown(TAPER_FACTOR_WAD);

        (
            uint64 claimThroughEpoch,
            uint256 epochsClaimed,
            uint256 claimable
        ) = treasury.previewTrailingYield(lifer);

        assertEq(claimThroughEpoch, 21);
        assertEq(epochsClaimed, 1);
        assertEq(claimable, expected);

        uint256 balanceBefore = token.balanceOf(lifer);

        vm.prank(lifer);
        uint256 paid = treasury.claimTrailingYield();

        assertEq(paid, expected);
        assertEq(token.balanceOf(lifer) - balanceBefore, expected);

        state = registry.contributorState(lifer);
        assertEq(state.lastLegacyClaimEpoch, 21);
    }

    function testAlumniCanClaimThreeSkippedEpochsAtOnce() public {
        _addContributor(alumni);
        _settleActiveEpochs(alumni, 20);

        vm.prank(podAdmin);
        registry.removeContributor(alumni, 20);

        IContributorRegistry.ContributorState memory state =
            registry.contributorState(alumni);

        vm.warp(START + 23 * EPOCH);

        uint256 expected =
            state.initialLegacyAmount.mulWadDown(_pow(TAPER_FACTOR_WAD, 1)) +
            state.initialLegacyAmount.mulWadDown(_pow(TAPER_FACTOR_WAD, 2)) +
            state.initialLegacyAmount.mulWadDown(_pow(TAPER_FACTOR_WAD, 3));

        (
            uint64 claimThroughEpoch,
            uint256 epochsClaimed,
            uint256 claimable
        ) = treasury.previewTrailingYield(alumni);

        assertEq(claimThroughEpoch, 23);
        assertEq(epochsClaimed, 3);
        assertEq(claimable, expected);

        uint256 balanceBefore = token.balanceOf(alumni);

        vm.prank(alumni);
        uint256 paid = treasury.claimTrailingYield();

        assertEq(paid, expected);
        assertEq(token.balanceOf(alumni) - balanceBefore, expected);

        state = registry.contributorState(alumni);
        assertEq(state.lastLegacyClaimEpoch, 23);
    }

    function testPauseLegacyClaimsBlocksAlumniButAllowsActiveClaims() public {
        _addContributor(alumni);
        _settleActiveEpochs(alumni, 2);

        vm.prank(podAdmin);
        registry.removeContributor(alumni, 2);

        _addContributor(active);

        treasury.pauseLegacyClaims();

        vm.warp(START + 3 * EPOCH);

        vm.expectRevert(TreasuryDistributor.LegacyClaimsArePaused.selector);
        vm.prank(alumni);
        treasury.claimTrailingYield();

        uint256 activeBalanceBefore = token.balanceOf(active);

        vm.prank(active);
        uint256 activePaid = treasury.claimActiveComp();

        assertGt(activePaid, 0);
        assertEq(token.balanceOf(active) - activeBalanceBefore, activePaid);
    }

    function _addContributor(address contributor) private {
        uint64 joinedEpoch = treasury.currentEpoch();

        vm.prank(podAdmin);
        registry.addContributor(contributor, contributor, BASE_PAY, joinedEpoch);
    }

    function _settleActiveEpochs(address contributor, uint64 epochs) private {
        for (uint64 epoch = 1; epoch <= epochs; ++epoch) {
            vm.warp(START + epoch * EPOCH);
            vm.prank(contributor);
            treasury.claimActiveComp();
        }
    }

    function _pow(uint256 baseWad, uint256 exponent)
        private
        pure
        returns (uint256)
    {
        return WadMath.rpowWad(baseWad, exponent);
    }
}
