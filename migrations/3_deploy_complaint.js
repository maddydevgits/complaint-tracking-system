const complaint = artifacts.require("complaint");

module.exports = function (deployer) {
  deployer.deploy(complaint);
};
