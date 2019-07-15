import blockchain	#blockchain.py

n = 25

for i in range(1, n+1):
	patientId = open("ids&keys/" + str(i) + "_id.pem", "r")
	patientId = patientId.read().strip()
	print("Init:", patientId)
	result = blockchain.blockchainInterface("register", patientId, write=False);
