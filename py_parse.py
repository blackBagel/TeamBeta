import os
import pyImports

CSV_DELIM = ","

asmDir = "C:\Users\Jbt\Desktop\samples\\"
asms = os.listdir(asmDir)

outputCsv = "out.csv"
outFile = open(outputCsv, "w+")

for asm in asms:
    if asm.endswith(".asm"):
        outFile.write(asm + CSV_DELIM)
        asmData = open(asmDir + asm, "rb").read()
        print "in " + asm
        # run regex
        print pyImports.parseData(asmData)
