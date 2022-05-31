// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {
  
  address[] _users;
  string[] _names;
  uint[] _passwords;
  string[] _emails;

  mapping(address=>bool) _customers;

  function registerUser(address user, string memory name, uint password, string memory email) public {

    require(!_customers[user]);
    _users.push(user);
    _names.push(name);
    _passwords.push(password);
    _emails.push(email);
  }

  function viewUsers() public view returns (address[] memory, string[] memory, uint[] memory, string[] memory) {
    return (_users,_names,_passwords,_emails);
  }

  function loginUser(address user, uint password) public view returns(bool) {

    uint i;

    for(i=0;i<_users.length;i++) {
      if(_users[i]==user && _passwords[i]==password)
        return true;
    }
    return false;
  }
}
