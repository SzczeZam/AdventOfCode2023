import sys
import re

line="""_____________________________________________"""
data= sys.argv[1]
flag= sys.argv[2]

cap_digits= r'(\d+)'
cap_sym= r'([^\.\d\n])'
cap_gear= r'(\*)'

def parseData(path):
    print("-in line parser-")
    storageList= []
    with open(path, "r") as input:
        for line in input:
            storageList.append(line)
    return storageList

def findIndicies(obs_list):
    re_t_dig = re.finditer(cap_digits, obs_list[0])
    re_digits =  re.finditer(cap_digits, obs_list[1])
    re_b_dig = re.finditer(cap_digits, obs_list[2])
    

    re_top_symbols = re.finditer(cap_sym, obs_list[0])
    re_current_symbols = re.finditer(cap_sym, obs_list[1], flags=re.MULTILINE)
    re_bottom_symbols = re.finditer(cap_sym, obs_list[2])
    
    re_gears = re.finditer(cap_gear, obs_list[1])

    ## place holders (have mercy on my soul)
    # digits
    tdigs = []
    tdigLOCs =[]

    dig_list = []
    digLOCs = []

    bdigs= []
    bdigLOCs = []

    # gears
    cgLOC = []

    # symbols
    tLOC = []
    t_list = []
    
    cLOC = []
    c_list = []
    
    bLOC = []
    b_list = []

    for g in re_gears:
        cgLOC.append(g.span()[0])

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
        digLOCs.append(m.span())

    for n in re_t_dig:
        tdigs.append(n.group())
        tdigLOCs.append(n.span())
     
    for n in re_b_dig:
        bdigs.append(n.group())
        bdigLOCs.append(n.span())
            
    return [[tLOC, cLOC, bLOC], [tdigs,tdigLOCs], [dig_list, digLOCs, cgLOC], [bdigs,bdigLOCs]]

def isGearRatio(gear, LOCs, digits):
    isGR = False
    center_values = False


    
    def hasAdjVal(index, loc_list, dlist):
        isAdjacent = False
        res = [False]
        for i in range(0,len(loc_list)):
            loc = loc_list[i]
            lVal = loc[0]
            hVal = loc[1]
            if lVal-1 <= index  and index <= hVal:
                isAdjacent = True
                res= [True, dlist[i]]
        return res

    def centerAdj(index, center_locs, center_dig):
        numbers = []
        hasRightValue = False
        hasLeftValue = False
        for i in range(0, len(center_locs)):
            lItem = center_locs[i][1]
            rItem = 0 if i == len(center_locs)-1 else center_locs[i+1][0]
            if int(lItem) == int(index):
                hasLeftValue = True
                numbers.append(center_dig[i])
            if int(rItem) == index+1:
                hasRightValue = True
                numbers.append(center_dig[i+1])
            if hasLeftValue and hasRightValue:
                nonlocal center_values
                center_values = True
                   
        return numbers

    topCheck= hasAdjVal(gear,LOCs[0],digits[0])
    centerCheck= centerAdj(gear, LOCs[1], digits[1])
    bottomCheck= hasAdjVal(gear,LOCs[2], digits[2])
    LCheck= [False]
    tb_out = [] 
    
    if topCheck[0]:
        tb_out.append(topCheck[1])
    if bottomCheck[0]:
        tb_out.append(bottomCheck[1])
    if topCheck[0] and bottomCheck[0]:
        isGR = True
    tb = topCheck[0] or bottomCheck[0]
    if not isGR and not center_values:
        print("************************************************************")
        if len(centerCheck) > 0:
            if tb:
                print(line+line+line)
                print(tb_out)
                LCheck= [True, [centerCheck[0],tb_out[0]]]

                
    return [isGR, center_values, centerCheck, tb_out, LCheck]

def isValid(currentLOC, LOCs):
    lC = currentLOC[0]
    hC = currentLOC[1]-1
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
    gearLOCs = parts[2]
    matchedNumbers = []

    for i in range(0, len(partNumbers)):
        curIndex = parts[1][i]
        #loop through symbol matches to see if indicies are in range
        validCheck=isValid(curIndex,LOCs)
        if validCheck[0]:
            matchedNumbers.append(int(partNumbers[i]))
    return matchedNumbers

def findGearRatios(top, center, bottom):
    gearLOCs = center[2]
    validRatios = []
    srcRatios= []
    #for each gear location
    print(gearLOCs)
    for i in range(0,len(gearLOCs)):
        gear = gearLOCs[i]
        gearCheck = isGearRatio(gear, [ top[1], center[1], bottom[1] ], [top[0], center[0], bottom[0]])
        print(gearCheck)
        print(f"gear index: {gear}")

        if gearCheck[0]:
            tg=int(gearCheck[3][0])
            bg=int(gearCheck[3][1])
            validRatios.append(tg*bg)
            srcRatios.append([tg,bg])
            print(f"top value {tg} * bottom value {bg}")

        if gearCheck[1]:
            lValue=int(gearCheck[2][0])
            rValue=int(gearCheck[2][1])
            validRatios.append(lValue*rValue)
            srcRatios.append([lValue,rValue])
            print(f"left value {lValue} * right value {rValue}")

        if gearCheck[4][0]:
            print("found L")
            xN = int(gearCheck[4][1][0])
            yN = int(gearCheck[4][1][1])
            validRatios.append(xN*yN)
            srcRatios.append([xN,yN])
            print(f"x{xN} y{yN}")
        if gearCheck[0] or gearCheck[1]:
            print("!VALID!")
        print(line)

    return [validRatios,srcRatios]




def findPartNumbers(schemaLines):
    # loop through supplied lines
    totalValidParts = []
    src = []
    for i in range(0, len(schemaLines)):
        # store relevant lines (above and below) for each line
        lineData = [
            "" if i == 0 else schemaLines[i-1],
            schemaLines[i],
            "" if i == len(schemaLines)-1 else schemaLines[i+1]
            ]
        dataArr = findIndicies(lineData)

        print(f"""
        -- KEY- -- 
        ln {format(i, '03d')}: >> {lineData[0]}
        ln {format(i+1, '03d')}: >> {lineData[1]}
        ln {format(i+2, '03d')}: >> {lineData[2]}
        """)

        match flag:
            case "p":
                partNums = findAdjacent(dataArr[0], dataArr[2])
                totalValidParts += partNums
            case "g":
                gearRatios = findGearRatios(dataArr[1],dataArr[2],dataArr[3])
                totalValidParts += gearRatios[0]
                src += gearRatios[1]
        print(line)
    return [totalValidParts, src]



def main():
    print("✨running script✨")
    lines = parseData(data)
    sample= []
    for i in range(0,5):
        sample.append(lines[i])
    # sample for testing
    
    validNumbers = findPartNumbers(lines)
    print(f"{len(lines)} lines parsed")
    print(f"{len(validNumbers[0])} {'gear ratios' if flag == 'g' else 'valid numbers'} found")
    print(sum(validNumbers[0]))


main() 

