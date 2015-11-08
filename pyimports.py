import re

def parseData(data):
    imports = {}
    dllRegex = re.compile("(.+?):.* Imports from (\w+\.dll)", re.S | re.I)
    bIsExtrnCompiled = False
    while True:
        dllMatch = dllRegex.search(data)
        print dllMatch
        if not bIsExtrnCompiled:
            extrnRegex = re.compile(dllMatch.group()[0] + "(\?{2}\s+){4}(\w+)? (\w+)[:\s]", re.S | re.I)
            bIsExtrnCompiled = True
        nextDll = dllRegex.search(data[dllMatch.span()[1]:])
        if not nextDll:
            break
        currDll = dllMatch.group()[1]
        externals = extrnRegex.findall(data[dllMatch.span()[1]: nextDll.span()[0]])
        print externals
        print dllMatch.group()
        print nextDll.span()
        data = data[dllMatch.span()[1]:]
    externals = extrnRegex.findall(data[dllMatch.span()[1]: ])
    print "last dll: "
    print dllMatch.group()
    print externals
    return "a"
