import re

def parseData(data):
    dllRegex = re.compile("(\d{1,3}\.){3}\d{1,3}", re.I)
    importsFull = ()
    nextDll = True
    while nextDll:
        dllMatch = dllRegex.search(data)
        data = data[dllMatch.span(2)[1]:]
        importsFull.append(dllMatch.group(0))
        nextDll = dllRegex.search(data[dllMatch.span(2)[1]:])
##    print "last dll: "
##    print dllMatch.group()
##    print importsFull
##    raw_input()
    return importsFull
