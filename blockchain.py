import web3
from web3 import Web3
from web3.contract import ConciseContract
import sys
import datetime

def blockchainInterface(command, patientId, parameter=None, write=True):

	#get abi of contract
	contractAbi = open("Deployment/artifacts/HealthRecordManagement.abi", "r")
	contractAddress = open("Deployment/contractAddress.txt", "r")
	contractAbi = contractAbi.read()
	contractAddress = contractAddress.read().strip()
	contractAddress = Web3.toChecksumAddress(contractAddress)

	#connect to ethereum through http endpoint and set account to be used
	web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
	web3.eth.defaultAccount = web3.eth.accounts[0]

	#instantiate contract
	HealthRecordManagement = web3.eth.contract(abi=contractAbi, address=contractAddress)
	HRM_reader = ConciseContract(HealthRecordManagement)
	
	###############################################################################################
	
	#we will return these to test.py
	toWrite = ""
	tx_hash = None
	count = None
	healthRecord = None

	if command == "register": #checked

		try:
			tx_hash = HealthRecordManagement.functions.registerPatient(patientId).transact({'from': web3.eth.accounts[0], 'gas': 3000000})
			web3.eth.waitForTransactionReceipt(tx_hash)
			toWrite += "registerPatient: SUCCESS"

		except ValueError as e:
			toWrite += e.args[0]['message'] + "\n"
			toWrite += "registerPatient: FAIL"

		except Exception as e:
			print(e)
			toWrite += "Unexpected Error"

		if write == True:
			print(toWrite)

		return([toWrite, tx_hash])

	elif command == "count": #checked

		try:
			count = HRM_reader.getHealthRecordCount(patientId)
			toWrite += "Number of health records for this patient: " + str(count) + "\n"
			toWrite += "getHealthRecordCount: SUCCESS"

		except Exception as e:
			print(e)
			toWrite += "Unexpected Error"

		if write == True:
			print(toWrite)

		return([toWrite, count])

	elif command == "add": #checked

		hash = parameter

		try:
			tx_hash = HealthRecordManagement.functions.addHealthRecord(patientId, hash).transact({'from': web3.eth.accounts[0], 'gas': 3000000})
			web3.eth.waitForTransactionReceipt(tx_hash)
			toWrite += "addHealthRecord: SUCCESS"

		except ValueError as e:
			toWrite += e.args[0]['message'] + "\n"
			toWrite += "addHealthRecord: FAIL"
		
		except Exception as e:
			print(e)
			toWrite += "Unexpected Error"

		if write == True:
			print(toWrite)
		return([toWrite, tx_hash])

	elif command == "get": #checked

		try:
			index = int(parameter)
		
		except:
			toWrite += "Not an integer."
			print(toWrite)
			return(toWrite)


		try:
			healthRecord = HRM_reader.getHealthRecord(patientId, index)
			toWrite += "Hash:" + healthRecord[0] + "\n"
			toWrite += "Timestamp:" + str(datetime.datetime.fromtimestamp(healthRecord[1])) + "\n"
			toWrite += "getHealthRecord: SUCCESS"

		except ValueError as e:
			toWrite += e.args[0]['message'] + "\n"
			toWrite += "getHealthRecord: FAIL"
		
		except Exception as e:
			print(e)
			toWrite += "Unexpected Error"

		if write == True:
			print(toWrite)
		return([toWrite, healthRecord])

	else:
		if write == True:
			print("Unknown command.")
		return([None, None])

#if runned directly
if len(sys.argv) > 1:
	
	#all
	if len(sys.argv) > 2:
		command = sys.argv[1]
		patientId = sys.argv[2]
	
	else:
		print("Need at least (command, patientId).")

	#register only needs 2
	if command in ["register", "count"]:
		blockchainInterface(command, patientId)

	#add/get needs 3
	elif command in ["add", "get"]:

		if len(sys.argv) > 3:
			parameter = sys.argv[3]
			blockchainInterface(command, patientId, parameter=parameter)

		else:
			print("Need (command, patientId, <parameter>) for add/get.")

	else:
		print("Unknown command.")