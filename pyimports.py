import re

def parseData(data):
    imports = {}
    dllRegex = re.compile("(\w+):.*?Imports from (\w+\.dll)", re.I)
    bIsExtrnCompiled = False
    importsFull = {}
    while True:
        dllMatch = dllRegex.search(data)
        if not bIsExtrnCompiled:
            extrnRegex = re.compile(dllMatch.group(1) + ".+(\?{2}\s+){4}\s+(extrn )?(\w+)[:\s]", re.I)
            bIsExtrnCompiled = True
        nextDll = dllRegex.search(data[dllMatch.span(2)[1]:])
        if not nextDll:
            break
        externals = extrnRegex.findall(data[dllMatch.span(2)[1]:dllMatch.span(2)[1] + nextDll.span(2)[0]])
        
        data = data[dllMatch.span(2)[1]:]
        imports = []
        for i in externals:
            imports.append(i[2])
        importsFull[dllMatch.group(2)] = imports
    externals = extrnRegex.findall(data[dllMatch.span(2)[1]:])
##    print "last dll: "
##    print dllMatch.group()
##    print importsFull
##    raw_input()
    return importsFull
