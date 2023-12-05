import sys
import re


line="""_____________________________________________"""
data= sys.argv[1]
flag= sys.argv[2]

def parseData(path):
    print("-in line parser-")
    storageList= []
    with open(path, "r") as input:
        for line in input:
            storageList.append(line)
    return storageList

# returns [ above, current, below ]
def findIndicies(obs_dict):
    regEx = [
        r'(\d+)',
        r'([^\.\d\n])',
        r'(\*)'
     ]
    
    ## returns [ readable digits {value, location}, all symbols {value, location}, gears (*) {value, location} ]

    def getValues(expression, line):
        return [{"value":m.group(),"location":m.span()}for m in re.finditer(expression, line)]
    data_matrix = [[
        getValues(regEx[option], observed_line) for option in range(0,len(regEx))
        ] for observed_line in obs_dict]   
    return data_matrix
            

def findRatios(data):
    try: 
        digits = [
            [ tnumber for tnumber in data[0][0] ],
            [ cnumber for cnumber in data[1][0] ],
            [ bnumber for bnumber in data[2][0] ]
            ]
    
        gear_indicie_list = [ gear["location"][0] for gear in data[1][2] ]

        ratio_list = []
        for gear in gear_indicie_list:
            matches = []
            for row in digits:
                for number in row:
                    if len(matches) < 2:
                        if number["location"][0]-1 <= gear and gear <= number["location"][1]:
                            matches.append(int(number["value"]))
            if len(matches) >= 2:
                ratio = matches[0]*matches[1]
                ratio_list.append(ratio)
                print(f"ratio found for index: {gear}")
                print(f"{matches[0]} * {matches[1]} = {ratio}")

        return ratio_list

    except IndexError as e:
        print(f"An index error occurred: {e}")

def findPartNumbers(schema_lines):
    # loop through supplied lines
    total_ratios = []
    for i in range(0, len(schema_lines)):
        lineData = [
            "" if i == 0 else schema_lines[i-1],
            schema_lines[i],
            "" if i == len(schema_lines)-1 else schema_lines[i+1]
            ]
        print("line",i,"\n") 
        matrix = findIndicies(lineData)
        ratio_list_per_line = findRatios(matrix)
        for ratio in ratio_list_per_line:
            total_ratios.append(ratio)
    return total_ratios





def main():
    print("✨running script✨")
    lines = parseData(data)
    sample= []
    for i in range(0,35):
        sample.append(lines[i])
    # sample for testing
    
    valid_numbers = findPartNumbers(lines)
    total = sum(valid_numbers)
    for ratio in valid_numbers:
        print(ratio) 
    print(f"total: {total}")
    return total

#last try: 84403435
#refactor attempt: 21663788 ! oh I'm stupid that was only 1/4 of the data
#try 89471771 when limit is up

main() 

