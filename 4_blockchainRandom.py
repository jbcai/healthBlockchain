import blockchain	#blockchain.py
import csv 			#output to file
import os 			#get file size for get
import random 		#randomizer
import re 			#get Qm_code from ipfs add 
import subprocess 	#run openssl and ipfs
import time 		#timer
import datetime

#number of patients
n = 25

#available commands
commands = ["register", "add", "get"]
patients = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
fileSize = ["10kB", "100kB", "1000kB"]

dictionary = {10000: "10kB", 100000: "100kB", 1000000: "1000kB"}

#output results
csvfile = open("results_blockchain.csv", "w")
output = csv.writer(csvfile, delimiter=',')
output.writerow(["TIMESTAMP", "COMMAND", "PATIENT", "ADD'L INPUT", "FILE SIZE", "TXN HASH", "OUTPUT 1", "OUTPUT 2", "TIME 1", "TIME 2", "TIME3"])

totalTime0 = time.time()
for i in range(5000):

	#randomize commandNum
	commandNum = random.randint(0, 2)
	patientIdNum = random.randint(0, n-1)
	fileSizeNum = random.randint(0, 2)

	#set variables from randomizer
	command = commands[commandNum]
	patient = patients[patientIdNum]

	if command == "register":

		#create key and id so that it will always succeed
		t0 = time.time()
		publicKeyName = "ids&keys/Z_id.pem"
		genkey = subprocess.call(['openssl', 'rand', '-out', publicKeyName, '-base64', '32'])
		symmetricKeyName = "ids&keys/Z_key.pem"
		genkey = subprocess.call(['openssl', 'rand', '-out', symmetricKeyName, '-base64', '32'])
		t1 = time.time()
		time1 = t1 - t0

		#read from the newly created id and register it to the blockchain
		t0 = time.time()
		patientId = open("ids&keys/Z_id.pem", "r")
		patientId = patientId.read().strip()
		result = blockchain.blockchainInterface(command, patientId, write=False);
		t1 = time.time()
		time2 = t1 - t0
		#print(result)

		print(i, "REGISTER", "Z")
		timestamp = int(datetime.datetime.now().timestamp())
		output.writerow([timestamp, "Register", "Z", "", "", result[1].hex(), "", "", time1, time2])

	elif command == "add":

		#OpenSSL encrypt
		t0 = time.time()
		fileName = "files/" + fileSize[fileSizeNum]
		fileName_encrypted = fileName + "_encrypted"
		keyName = "ids&keys/" + str(patientIdNum+1) + "_key.pem"
		encrypt = subprocess.run(['openssl', 'enc', '-aes256', '-base64', '-pbkdf2', '-in', fileName, '-out', fileName_encrypted, '-pass', 'file:' + keyName])
		t1 = time.time()
		time1 = t1 - t0

		#IPFS add
		t0 = time.time()
		p = re.compile(r'Qm\w+')
		add = subprocess.run(['ipfs', 'add', fileName_encrypted], stdout=subprocess.PIPE)
		Qm_code = p.findall(add.stdout.decode('utf-8'))[0]
		t1 = time.time()
		time2 = t1 - t0

		#Ethereum add
		t0 = time.time()
		patientId = open("ids&keys/" + str(patientIdNum+1) + "_id.pem", "r")
		patientId = patientId.read().strip()
		result = blockchain.blockchainInterface(command, patientId, parameter=Qm_code, write=False);
		t1 = time.time()
		time3 = t1 - t0
		#print(result)

		print(i, "ADD", patient, fileSize[fileSizeNum])
		timestamp = int(datetime.datetime.now().timestamp())
		output.writerow([timestamp, "Add", patient, Qm_code, fileSize[fileSizeNum], result[1].hex(), "", "", time1, time2, time3])

	elif command == "get":
		#count first before

		#Get id and call count
		t0 = time.time()
		patientId = open("ids&keys/" + str(patientIdNum+1) + "_id.pem", "r")
		patientId = patientId.read().strip()
		#print(patientId)
		result = blockchain.blockchainInterface("count", patientId, write=False);
		t1 = time.time()
		time1 = t1 - t0
		#print(result)

		count = result[1]

		print(i, "COUNT", patient, count)
		timestamp = int(datetime.datetime.now().timestamp())
		output.writerow([timestamp, "Count", patient, "", "", "", count, "", time1])

		#you cannot get anything from this patient
		if (count == 0):
			continue

		index = random.randint(0, count-1)

		#Ethereum get
		t0 = time.time()
		patientId = open("ids&keys/" + str(patientIdNum+1) + "_id.pem", "r")
		patientId = patientId.read().strip()
		result = blockchain.blockchainInterface(command, patientId, parameter=index, write=False);
		t1 = time.time()
		time1 = t1 - t0
		#print(result)

		Qm_code = result[1][0]
		#print(Qm_code)

		#IPFS get
		t0 = time.time()
		get = subprocess.run(['ipfs', 'get', '-o=files/', Qm_code], stdout=subprocess.PIPE)
		t1 = time.time()
		time2 = t1 - t0

		#OpenSSL decrypt
		t0 = time.time()
		fileName_encrypted = "files/" + Qm_code
		fileName = fileName_encrypted + "_decrypted"
		keyName = "ids&keys/" + str(patientIdNum+1) + "_key.pem"
		decrypt = subprocess.run(['openssl', 'enc', '-d', '-aes256', '-base64', '-pbkdf2', '-in', fileName_encrypted, '-out', fileName, '-pass', 'file:' + keyName])
		t1 = time.time()
		time3 = t1 - t0
		
		#print(result)

		#getFileSize of decrypted file
		get_size = dictionary[os.stat(fileName).st_size]
		
		print(i, "GET", patient, index, get_size)
		timestamp = int(datetime.datetime.now().timestamp())
		output.writerow([timestamp, "Get", patient, index, get_size, "", result[1][0], result[1][1], time1, time2, time3])

		os.remove(fileName_encrypted)
		os.remove(fileName)

	else:
		print("NANI?")

totalTime1 = time.time()
totalTime = totalTime1 - totalTime0
print(totalTime)
