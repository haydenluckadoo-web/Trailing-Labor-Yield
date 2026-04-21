// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

library WadMath {
    uint256 internal constant WAD = 1e18;

    error WadMulOverflow();

    function mulWadDown(uint256 x, uint256 y) internal pure returns (uint256) {
        if (x != 0 && y > type(uint256).max / x) {
            revert WadMulOverflow();
        }

        return (x * y) / WAD;
    }

    function rpowWad(uint256 baseWad, uint256 exponent)
        internal
        pure
        returns (uint256 resultWad)
    {
        resultWad = WAD;

        while (exponent > 0) {
            if ((exponent & 1) == 1) {
                resultWad = mulWadDown(resultWad, baseWad);
            }

            exponent >>= 1;

            if (exponent > 0) {
                baseWad = mulWadDown(baseWad, baseWad);
            }
        }
    }
}
