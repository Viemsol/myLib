import sys
import os
import subprocess
def cliEx(cmd):
	resp = os.system(cmd)
	return resp
def batchEx(batchPath):
	subprocess.call([batchPath])