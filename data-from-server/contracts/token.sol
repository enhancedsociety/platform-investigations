pragma solidity ^0.4.19;

import "./common.sol";

/**
 * Quilt from Zeppelin contract patches
 */


/**
 * @title Basic token
 * @dev Basic version of StandardToken, with no allowances.
 */
contract BasicToken is ERC20Basic {
    using SafeMath for uint256;

    mapping(address => uint256) balances;

    uint256 totalSupply_;

    /**
    * @dev total number of tokens in existence
    */
    function totalSupply() public view returns (uint256) {
        return totalSupply_;
    }

    /**
    * @dev transfer token for a specified address
    * @param _to The address to transfer to.
    * @param _value The amount to be transferred.
    */
    function transfer(address _to, uint256 _value) public returns (bool) {
        require(_to != address(0));
        require(_value <= balances[msg.sender]);

        // SafeMath.sub will throw if there is not enough balance.
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    /**
    * @dev Gets the balance of the specified address.
    * @param _owner The address to query the the balance of.
    * @return An uint256 representing the amount owned by the passed address.
    */
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

}


contract PlatformToken is BasicToken {

    string public name; // solium-disable-line uppercase
    string public symbol; // solium-disable-line uppercase
    uint8 public constant decimals = 0; // solium-disable-line uppercase

    uint256 public constant INITIAL_SUPPLY = 10000000000;

    /**
    * @dev Constructor that gives an ICO contract all of the supply.
    */
    function PlatformToken(address ico, string _name, string _symbol) public {
        totalSupply_ = INITIAL_SUPPLY;
        balances[ico] = INITIAL_SUPPLY;
        name = _name;
        symbol = _symbol;
        emit Transfer(0x0, ico, INITIAL_SUPPLY);
    }

}