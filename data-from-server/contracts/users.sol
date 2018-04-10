pragma solidity ^0.4.19;

contract Users {
    // Username mappings are 1-1

    mapping (address=>string) private user_from_addr;
    mapping (string=>address) private addr_from_user;

    function getAddress(string username) public view returns (address) {
        return addr_from_user[username];
    }

    function getUsername(address addr) public view returns (string) {
        return user_from_addr[addr];
    }

    function register(string username) public {
        address prev_a = addr_from_user[username];
        require(prev_a == address(0));
        string storage prev_u = user_from_addr[msg.sender];
        if (bytes(prev_u).length > 0) {
            delete user_from_addr[msg.sender];
        }
        user_from_addr[msg.sender] = username;
        addr_from_user[username] = msg.sender;
    }

    function unregister() public {
        string storage u = user_from_addr[msg.sender];
        require(bytes(u).length > 0);
        address a = addr_from_user[u];
        assert(a == msg.sender);
        delete user_from_addr[a];
        delete addr_from_user[u];
    }
}