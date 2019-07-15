from geth.accounts import create_new_account
from geth.chain import write_genesis_file
from geth.chain import initialize_chain
import json
import os
import subprocess
import sys

number = 3
host = ["10.0.80.120", "10.0.80.126", "10.0.80.139"]
accounts = []

subprocess.run(['rm -rf blockchains'], shell=True)
subprocess.run(['mkdir blockchains'], shell=True)

for i in range(number):

	#name and password
	name = "Hospital" + str(i+1)
	account_file_path = "./blockchains/" + name
	password = "123"

	#create password file
	password_file_path = "./blockchains/password.txt"
	file = open(password_file_path, "w")
	file.write(password)
	file.close()

	#create account
	account = create_new_account(account_file_path, "./blockchains/password.txt")
	account = str(account)[4:44]
	print ("Created account:", account)
	accounts.append(account)

#save addresses to a file
file = open("./blockchains/account_addresses.txt", "w")
writeString = ""
for i in accounts:
	writeString += i + "\n"
file.write(writeString)
file.close()

#make a dictionary for alloc portion of genesis.json
account_balance = {}
for i in accounts:
	account_balance[i] = {"balance": "1000000000000000000000000000000"}

#make genesis.json with allocated 1000000000000000000000000000000 gas
genesis_file_path = "./blockchains/genesis.json"
write_genesis_file(
	genesis_file_path, overwrite=True, nonce="0x0000000000000923", timestamp="0x00",
	parentHash="0x0000000000000000000000000000000000000000000000000000000000000000",
	extraData="", gasLimit="0x2fefd8", difficulty = "0x400",
	mixhash="0x0000000000000000000000000000000000000000000000000000000000000000",
	coinbase="0x0000000000000000000000000000000000000000",
	alloc=account_balance,
	config={"chainId": 201906, "homesteadBlock": 0, "eip155Block": 0, "eip158Block": 0}
	)
print ("Created genesis.json")
print ("")

#sort genesis.json (prettify)
json_file = open("./blockchains/genesis.json", "r")
data = json.load(json_file)
json_file = open("./blockchains/genesis.json", "w")
json.dump(data, json_file, sort_keys = True, indent = 2)

enodes = []
for i in range(number):

	name = "Hospital" + str(i+1)
	account_file_path = "./blockchains/" + name

	#init account with created genesis file
	json_file = open(genesis_file_path, "r")
	data = json.load(json_file)
	initialize_chain(data, account_file_path)
	print ("Initialized account", accounts[i], "with created genesis.json")

	#generate nodekey
	subprocess.run(["bootnode --genkey=" + account_file_path + "/geth/nodekey"], shell=True)
	print ("Generated nodekey")

	#get enode
	enode = subprocess.run(["bootnode --nodekey=" + account_file_path + "/geth/nodekey --writeaddress"], shell=True, stdout=subprocess.PIPE)
	enode = enode.stdout.decode('utf-8')
	enode = "enode://" + enode.strip() + "@" + host[i] +":30305?discport=0"
	print ("Enode:", enode)
	enodes.append(enode)

#save enodes to a file
file = open("./blockchains/enode.txt", "w")
writeString = ""
for i in enodes:
	writeString += i + "\n"
file.write(writeString)
file.close()
