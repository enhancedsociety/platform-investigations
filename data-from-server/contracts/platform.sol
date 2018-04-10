pragma solidity ^0.4.19;

import "./token.sol";

import "./ico.sol";

contract Platform {
    struct Project {
        address token;
        address ico;
        string name;
    }

    Project[] private projects;
    address private owner;

    function Platform() public {
        owner = msg.sender;
    }

    function addProject(string name, string symbol, uint256 priceInWei) public returns (address, address){
        address project_owner = msg.sender;
        ICO ico = new ICO(project_owner);
        require(ico != address(0));
        PlatformToken token = new PlatformToken(ico, name, symbol);
        require(token != address(0));
        ico.init(token, priceInWei);
        projects.push(Project(token, ico, name));
    }

    function numProjects() public view returns(uint) {
        return projects.length;
    }

    function getProject(uint i) public view returns(string, address, address) {
        require(i < projects.length);
        require(i >= 0);
        Project memory result = projects[i];
        return (result.name, result.token, result.ico);
    }

}