import sys
import re
data= sys.argv[1]

cap_digits= r'(\d+)'
cap_sym= r'([^\.\d\n])'

def parseData(path):
    print("-in line parser-")
    storageList= []
    with open(path, "r") as input:
        for line in input:
            storageList.append(line)
    return storageList

def findIndicies(obs_list):
    re_digits =  re.finditer(cap_digits, obs_list[1])
    re_top_symbols = re.finditer(cap_sym, obs_list[0])
    re_current_symbols = re.finditer(cap_sym, obs_list[1])
    re_bottom_symbols = re.finditer(cap_sym, obs_list[2])
    
    dig_list = []
    digLOC = []

    tLOC = []
    t_list = []
    cLOC = []
    c_list = []
    bLOC = []
    b_list = []

    
    for s in re_top_symbols:
        t_list.append(s.group())
        tLOC.append(s.span()[0])
         
    for s in re_current_symbols:
        c_list.append(s.group())
        cLOC.append(s.span()[0])

    for s in re_bottom_symbols:
        b_list.append(s.group())
        bLOC.append(s.span()[0])

    for m in re_digits:
        dig_list.append(m.group())
        digLOC.append(m.span())

    return [[tLOC, cLOC, bLOC], [dig_list, digLOC]]

def isValid(currentLOC, LOCs):
    lC = currentLOC[0]
    hC = currentLOC[1]
    valid = False
    matchIndex = 0

    def loopThruLOC(locLs):
        for value in locLs:
            if value >= lC-1 and value <= hC+1:
                nonlocal valid
                nonlocal matchIndex
                valid = True
                matchIndex= value
                

    loopThruLOC(LOCs[0])
    loopThruLOC(LOCs[1])
    loopThruLOC(LOCs[2])
    return [valid,matchIndex]
    
    # if value is >= lC-1 and value is <= hC +1 
    # then it is within range of the number

def findAdjacent(LOCs, parts):
    partNumbers = parts[0]
    partLOCs = parts[1]
    matchedNumbers = []
    for i in range(0, len(partNumbers)):
        curIndex = parts[1][i]
        #loop through symbol matches to see if indicies are in range
        check=isValid(curIndex,LOCs)
        print(check)
        if check[0]:
            matchedNumbers.append(partNumbers[i])
    print(matchedNumbers)




def findPartNumbers(schemaLines):
    # loop through supplied lines
    for i in range(0, len(schemaLines)):
        # store relevant lines (above and below) for each line
        lineData = [
            "" if i == 0 else schemaLines[i-1],
            schemaLines[i],
            "" if i == len(schemaLines)-1 else schemaLines[i+1]
            ]
        dataArr = findIndicies(lineData)
        partNums = findAdjacent(dataArr[0], dataArr[1])






def main():
    print("✨running script✨")
    lines = parseData(data)
    sample= []
    for i in range(0,3):
        sample.append(lines[i])

    # sample for testing
    validNumbers = findPartNumbers(sample)

main() 

