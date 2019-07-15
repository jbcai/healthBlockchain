import subprocess
import sys

subprocess.call(['rm', '-rf', 'files'])
subprocess.call(['mkdir', 'files'])

fileSizes = [10, 100, 1000]

for index, i in enumerate(fileSizes):

	fileName = "files/" + str(i) + "kB"

	subprocess.call(['dd', 'if=/dev/zero', 'of='+fileName, 'count='+str(i), 'bs=1000'])