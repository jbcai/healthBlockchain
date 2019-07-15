import subprocess
import sys

hospitalNum = sys.argv[1]

"""
print('geth --datadir ./blockchains/Hospital' + hospitalNum +
	' --networkid 201906 --nodiscover --rpc --rpcport 854' + portNum +
	' --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" --port 3030' + portNum +
	' console')
"""
subprocess.run(['geth --datadir ./blockchains/Hospital' + hospitalNum +
	' --networkid 201906 --nodiscover --rpc --rpcport 8545' +
	' --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" --port 30305' +
	' console'], shell=True)
