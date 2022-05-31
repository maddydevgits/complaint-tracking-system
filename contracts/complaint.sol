// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract complaint {

  uint[] _ids;
  string[] _complaints;
  address[] _users;
  uint[] _statuses;

  function addComplaint(address user,uint id,string memory comp) public {

    _users.push(user);
    _ids.push(id);
    _complaints.push(comp);
    _statuses.push(0);
  }

  function listComplaints() public view returns (address[] memory, uint[] memory, string[] memory, uint[] memory) {

    return (_users,_ids,_complaints,_statuses);
  }

  function updateComplaint(uint id, uint status) public {
    uint i=0;
    for(i=0;i<_ids.length;i++) {
      if(_ids[i]==id) {
        _statuses[i]=status;
      }
    }
  }
}
