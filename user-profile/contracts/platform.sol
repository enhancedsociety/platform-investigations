pragma solidity ^0.4.19;

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

    function addProject(string name, address token, address ico) public {
        require(msg.sender == owner);
        projects.push(Project(token, ico, name));
    }

}