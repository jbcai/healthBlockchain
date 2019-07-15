pragma solidity ^0.4.25;

contract HealthRecordManagement
{
  struct HealthRecord {
      string ipfsHash;
      uint timestamp;
  }
  
  //remove loop from function exists
  mapping(string => bool) patientExists;
  mapping(string => bool) hashExists;
  mapping(string => HealthRecord[]) allHealthRecords;
  
  constructor() public {
      
    //prevent blank hash inputs
    hashExists[""] = true;
  }
  
  function registerPatient(string memory patientId) public {
    
    //require patient's non-existence and non-blank patientId
    require(patientExists[patientId] == false, "This patient is already registered.");
    require(keccak256(abi.encodePacked(patientId)) != keccak256(abi.encodePacked("")), "Input patientId is blank.");
    patientExists[patientId] = true;
  }
  
  function addHealthRecord(string memory patientId, string memory hash) public {
    
    //require patient's existence and hash's non-existence
    require(patientExists[patientId] == true, "Patient must be registered first.");
    require(hashExists[hash] == false, "Hash must not exist inside the blockchain.");

    //after passing all checks the put it in the array
    allHealthRecords[patientId].push(HealthRecord(hash, now));
    hashExists[hash] = true;
  }

  function getHealthRecordCount(string memory patientId) public view returns (uint){
      
    //don't check for patient's existence for added security
    return allHealthRecords[patientId].length;
  }

  function getHealthRecord(string memory patientId, uint index) public view returns (string memory, uint) {

    //don't check for patient's existence for added security
    //require that the index inside the array actually exists
    require(index < getHealthRecordCount(patientId), "Index must be less than number of health records of this patient inside the blockchain.");

    //save the struct to separate variables
    HealthRecord storage healthrecord = allHealthRecords[patientId][index];
    string memory a = healthrecord.ipfsHash;
    uint b = healthrecord.timestamp;
    
    //return variables
    return (a, b);
  }
  
}
