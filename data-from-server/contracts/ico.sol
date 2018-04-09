pragma solidity ^0.4.19;

/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {

  /**
  * @dev Multiplies two numbers, throws on overflow.
  */
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        assert(c / a == b);
        return c;
    }

    /**
    * @dev Integer division of two numbers, truncating the quotient.
    */
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        // assert(b > 0); // Solidity automatically throws when dividing by 0
        uint256 c = a / b;
        // assert(a == b * c + a % b); // There is no case in which this doesn't hold
        return c;
    }

    /**
    * @dev Subtracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    */
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }

    /**
    * @dev Adds two numbers, throws on overflow.
    */
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}

contract ERC20Basic {
    function totalSupply() public view returns (uint256);
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}

contract ICO {
    using SafeMath for uint256;

    address public tokenAddress;
    uint256 public tokenPriceInWei;
    address private owner;

    function ICO() public {
        owner = msg.sender;
    }

    function init(address token, uint256 priceInWei) public {
        require(msg.sender == owner);
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
        require(numTokens <= token.totalSupply());
        require(numTokens <= token.balanceOf(this));

        require(token.transfer(msg.sender, numTokens));
    }

    function cashOut() public {
        require(msg.sender == owner);
        owner.transfer(address(this).balance);
    }
}