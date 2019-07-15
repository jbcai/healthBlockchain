const HealthRecordManagement = artifacts.require("HealthRecordManagement");

module.exports = function(deployer) {
  deployer.deploy(HealthRecordManagement);
};
