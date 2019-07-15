import csv 						#output ro file
import datetime					#create now timestamp
import os 						#get file size for get
from pymongo import MongoClient #connect to mongo
from pymongo import collection 	#mongo collection commands
import random 					#randomizer
import subprocess 				#run openssl
import time 					#timer

host = "10.0.80.135"
port = 27017

#number of patients
n = 25

#available commands
commands = ["register", "add", "get"]
patients = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
fileSize = ["10kB", "100kB", "1000kB"]

dictionary = {10000: "10kB", 100000: "100kB", 1000000: "1000kB"}

#output results
csvfile = open("results_centralized.csv", "w")
output = csv.writer(csvfile, delimiter=',')
output.writerow(["TIMESTAMP", "COMMAND", "PATIENT", "ADD'L INPUT", "FILE SIZE", "OUTPUT 1", "OUTPUT 2", "TIME 1", "TIME 2"])

totalTime0 = time.time()
for i in range(5000):

	#randomize commandNum
	commandNum = random.randint(0, 2)
	patientIdNum = random.randint(0, n-1)
	fileSizeNum = random.randint(0, 2)

	#set variables from randomizer
	command = commands[commandNum]
	patient = patients[patientIdNum]

	client = MongoClient(host, port)
	db = client['test-database']

	if command == "register":

		#create key and id so that it will always succeed
		t0 = time.time()
		publicKeyName = "ids&keys/Z_id.pem"
		genkey = subprocess.call(['openssl', 'rand', '-out', publicKeyName, '-base64', '32'])
		symmetricKeyName = "ids&keys/Z_key.pem"
		genkey = subprocess.call(['openssl', 'rand', '-out', symmetricKeyName, '-base64', '32'])
		t1 = time.time()
		time1 = t1 - t0

		#read from the newly created id and create collection in mongodb
		t0 = time.time()
		patientId = open("ids&keys/Z_id.pem", "r")
		patientId = patientId.read().strip()
		collection.Collection(db, patientId, create=True)
		t1 = time.time()
		time2 = t1 - t0

		print(i, "REGISTER", "Z")
		timestamp = int(datetime.datetime.now().timestamp())
		output.writerow([timestamp, "Register", "Z", "", "", "", "", time1, time2])

	elif command == "add":

		#OpenSSL encrypt
		t0 = time.time()
		fileName = "files/" + fileSize[fileSizeNum]
		fileName_encrypted = fileName + "_encrypted"
		keyName = "ids&keys/" + str(patientIdNum+1) + "_key.pem"
		encrypt = subprocess.run(['openssl', 'enc', '-aes256', '-base64', '-pbkdf2', '-in', fileName, '-out', fileName_encrypted, '-pass', 'file:' + keyName])
		t1 = time.time()
		time1 = t1 - t0

		#MongoDB add
		t0 = time.time()

		file = open(fileName_encrypted, "r")
		file = file.read()
		
		patientId = open("ids&keys/" + str(patientIdNum+1) + "_id.pem", "r")
		patientId = patientId.read().strip()
		
		healthrecord = {
			"healthrecord": file,
			"timestamp": int(datetime.datetime.now().timestamp())
		}

		currentPatient = collection.Collection(db, patientId)
		currentPatient.insert_one(healthrecord)
		t1 = time.time()
		time2 = t1 - t0
		
		data = db.command("collstats", patientId)["size"]
		print (data)

		print(i, "ADD", patient, fileSize[fileSizeNum])
		timestamp = int(datetime.datetime.now().timestamp())
		output.writerow([timestamp, "Add", patient, "unencrypted file", fileSize[fileSizeNum], "", "", time1, time2])

	elif command == "get":

		#Get id and call count
		t0 = time.time()
		patientId = open("ids&keys/" + str(patientIdNum+1) + "_id.pem", "r")
		patientId = patientId.read().strip()
		
		currentPatient = collection.Collection(db, patientId)
		count = currentPatient.count_documents({})
		t1 = time.time()
		time1 = t1 - t0

		print(i, "COUNT", patient, count)
		timestamp = int(datetime.datetime.now().timestamp())
		output.writerow([timestamp, "Count", patient, "", "", count, "", time1])

		if (count == 0):
			continue

		index = random.randint(0, count-1)

		#MongoDB get
		t0 = time.time()
		patientId = open("ids&keys/" + str(patientIdNum+1) + "_id.pem", "r")
		patientId = patientId.read().strip()
		currentPatient = collection.Collection(db, patientId)
		currentHealthRecord = currentPatient.find()[index]
		actualHealthRecord = currentHealthRecord["healthrecord"]
		timestamp = currentHealthRecord["timestamp"]
		file = open("files/" + patient + "_" + str(index), "w")
		file.write(currentHealthRecord["healthrecord"])
		file.close()
		t1 = time.time()
		time1 = t1 - t0

		#OpenSSL decrypt
		t0 = time.time()
		fileName_encrypted = "files/" + patient + "_" + str(index)
		fileName = fileName_encrypted + "_decrypted"
		keyName = "ids&keys/" + str(patientIdNum+1) + "_key.pem"
		decrypt = subprocess.run(['openssl', 'enc', '-d', '-aes256', '-base64', '-pbkdf2', '-in', fileName_encrypted, '-out', fileName, '-pass', 'file:' + keyName])
		t1 = time.time()
		time2 = t1 - t0

		#getFileSize of decrypted file
		get_size = dictionary[os.stat(fileName).st_size]
		
		print(i, "GET", patient, index, get_size)
		timestamp = int(datetime.datetime.now().timestamp())
		output.writerow([timestamp, "Get", patient, index, get_size, "encrypted file", timestamp, time1, time2])

		os.remove("files/" + patient + "_" + str(index))
		os.remove(fileName)

	else:
		print("NANI?")

	client.close()

totalTime1 = time.time()
print(totalTime1 - totalTime0)
