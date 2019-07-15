# healthBlockchain
CS 198-199 Requirement 2018-2019

## Installation Requirements

1. OpenSSL: https://websiteforstudents.com/manually-install-the-latest-openssl-toolkit-on-ubuntu-16-04-18-04-lts/
2. Python3.7 : https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/

### Blockchain
3. IPFS: https://docs.ipfs.io/guides/guides/install/
4. Go-Ethereum: https://github.com/ethereum/go-ethereum/wiki/Installation-Instructions-for-Ubuntu
5. Node and Npm: https://tecadmin.net/install-latest-nodejs-npm-on-linux-mint/
6. Truffle: sudo npm install truffle@4.1.15
7. Py-Geth: sudo python3.7 -m pip install py-geth
8. Web3.py: sudo python3.7 -m pip install web3

### Baseline
9. MongoDB: https://docs.mongodb.com/v3.6/tutorial/install-mongodb-on-linux/
10. PyMongo: sudo python3.7 -m pip install pymongo

## How to Use:
- Each computer (except MongoDB database) should have a copy of this github repo.
- If a step is only a python file, run it with python3.7 filename.py
- The initial 25 id-key pairs should be the same across all three computers.
- Unless stated, run all the commands on all computers.

### Blockchain Setup
1. 0_genFile.py: creates 10kB, 100kB, 1000kB files
2. (only 1 needed) 0_genKey.py: creates 25 id-key pairs
3. (only 1 needed) Set the list host of 0_makeBlockchain.py to the ip addresses of the computers.
4. (only 1 needed) 0_makeBlockchain.py: creates a folder named blockchains. The blockchains folder has the following: 3 blockchains account, the genesis.json, and enode addresses of those accounts in a .txt file
5. Distribute the id-key pairs and blockchains folder across 3 computers
6. 1_startBlockchain.py: start Hospital n (please add parameter: 1,2,3)
7. For PC1, Geth: admin.addPeer(enode of PC2 & PC3). For PC2, Geth: admin.addPeer(enode of PC3). The three computers are now all connected.
8. Geth: personal.unlockAccount(eth.accounts[0], "123", 0)
9. Geth: miner.start()
10. (only 1 needed) Go to Deployment folder and do truffle migrate. This will return contract address of HealthRecordManagement
11. Create a contractAddress.txt in the Deployment folder, and save the contract address of HealthRecordManagement there
12. Start IPFS daemon
13. (only 1 needed) 3_addInitBlockchain.py: create 25 empty collections with the ids
14. 4_blockchainRandom.py: the actual 5000 random transactions in the blockchain setup of thesis

### Baseline Setup
1. 0_genFile.py: creates 10kB, 100kB, 1000kB files
2. (only 1 needed) 0_genKey.py: creates 25 id-key pairs
3. Start the mongoDB database in the 4th computer (make sure to bind all ips)
4. Change the ip and port of 5_addInitCentralized.py & 6_centralizedRandom.py according to the ip and port of the 4th computer's mongoDB instance
5. Distribute the id-key pairs across 3 computers
6. (only 1 needed) 5_addInitCentralized.py: create 25 empty collections with the ids
7. 6_centralizedRandom.py: the actual 5000 random transactions in the baseline setup of thesis
