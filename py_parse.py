import os
import pyIPs
#import multiprocessing
import pp
import sys

CSV_DELIM = ","

asmDir = "C:\Users\Jbt\Desktop\malware stuff\TeamBeta\TeamBeta-git\samples\\"
asms = os.listdir(asmDir)

def runRegexes(filePath):
    if filePath.endswith(".asm"):
        print filePath
        asmData = open(filePath, "rb").read()
    
        imports = pyIPs.parseData(asmData)
        
    
        out = open(filePath + ".csv", "w+")
        out.write(str(imports))
        out.close()


# tuple of all parallel python servers to connect with
ppservers = ()
#ppservers = ("10.0.0.1",)

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

jobs = [(asm, job_server.submit(func=runRegexes, args=((asmDir + asm),), depfuncs=(), modules=("pyIPs",))) for asm in asms]
for asm,job in jobs:
    job()

job_server.print_stats()
