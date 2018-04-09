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
//        require(msg.sender == owner);
        require(bytes(name).length > 0);
        require(token != address(0));
        require(ico != address(0));
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