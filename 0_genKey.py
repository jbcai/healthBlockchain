import subprocess
import sys

#number of patients
keyNum = 25

subprocess.call(['rm', '-rf', 'ids&keys'])
subprocess.call(['mkdir', 'ids&keys'])

for i in range(1, keyNum+1):

	patient = str(i)

	publicKeyName = "ids&keys/" + patient + "_id.pem"
	genkey = subprocess.call(['openssl', 'rand', '-out', publicKeyName, '-base64', '32'])
	symmetricKeyName = "ids&keys/" + patient + "_key.pem"
	genkey = subprocess.call(['openssl', 'rand', '-out', symmetricKeyName, '-base64', '32'])
