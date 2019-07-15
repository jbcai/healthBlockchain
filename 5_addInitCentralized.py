from pymongo import MongoClient #connect to mongo
from pymongo import collection 	#mongo collection commands

n = 25

client = MongoClient('10.0.80.135', 27017)
client.drop_database('test-database')
db = client['test-database']

#register all initial patients
for i in range(1, n+1):
	patientId = open("ids&keys/" + str(i) + "_id.pem", "r")
	patientId = patientId.read().strip()
	collection.Collection(db, patientId, create=True)
	data = db.command("collstats", patientId)["size"]
	print(data)
