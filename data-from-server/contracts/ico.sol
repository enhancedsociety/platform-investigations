pragma solidity ^0.4.19;

import "./common.sol";

contract ICO {
    using SafeMath for uint256;

    address public tokenAddress;
    uint256 public tokenPriceInWei;
    address private creator;
    address public owner;

    function ICO(address owner_) public {
        owner = owner_;
        creator = msg.sender;
    }

    function init(address token, uint256 priceInWei) public {
        require(msg.sender == creator);
        require(tokenAddress == address(0));
        require(token != address(0));
        require(priceInWei > 0);
        tokenAddress = token;
        tokenPriceInWei = priceInWei;
    }

    function () payable public {
        require(tokenAddress != address(0));
        require(tokenPriceInWei > 0 wei);
        uint256 numTokens = msg.value.div(tokenPriceInWei);
        ERC20Basic token = ERC20Basic(tokenAddress);
        require(numTokens > 0);
        require(numTokens <= token.totalSupply());
        require(numTokens <= token.balanceOf(this));

        require(token.transfer(msg.sender, numTokens));
    }

    function cashOut() public {
        require(msg.sender == owner);
        owner.transfer(address(this).balance);
    }
}