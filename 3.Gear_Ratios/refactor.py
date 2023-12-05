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
        r'(\d+)',           # match all digits
        r'([^\.\d\n])',     # match all NOT .,digits,newline
        r'(\*)'             # match all *
     ]
    
    ## returns [ readable digits {value, location}, all symbols {value, location}, gears (*) {value, location} ]

    # function takes regex and string, returns array containing dicts {value, location} of every match
    def getValues(expression, line):
        return [{"value":m.group(),"location":m.span()}for m in re.finditer(expression, line)]

    # create matrix to store necessary data
    # for top,current, and bottom lines (3)
    # run getValues function for each regex query option (3)
    data_matrix = [[
        getValues(regEx[option], observed_line) for option in range(0,len(regEx))
        ] for observed_line in obs_dict]   
    return data_matrix
            

def findRatios(data):
    try: 
        # each item contains [numbers{value, location}]
        digits = [
            [ tnumber for tnumber in data[0][0] ],
            [ cnumber for cnumber in data[1][0] ],
            [ bnumber for bnumber in data[2][0] ]
            ]

        # list of all gear indecies
        gear_indicie_list = [ gear["location"][0] for gear in data[1][2] ]
        
        # ratio storage
        ratio_list = []
        # check all gear locations
        for gear in gear_indicie_list:

            matches = []
            # check above, current, and below rows
            for row in digits:
                for number in row:
                    
                    # need 2 numbers (AND ONLY 2) for a valid ratio
                    if len(matches) < 2:
                        if number["location"][0]-1 <= gear and gear <= number["location"][1]:
                            matches.append(int(number["value"]))

            # only adds matches to ratio storage if 2 matches have been found
            if len(matches) >= 2:
                ratio = matches[0]*matches[1]
                ratio_list.append(ratio)
                print(f"ratio found for index: {gear}")
                print(f"{matches[0]} * {matches[1]} = {ratio}")

        return ratio_list

    except IndexError as e:
        print(f"An index error occurred: {e}")

def findPartNumbers(schema_lines):
    # setup list to hold total ratios across all lines
    total_ratios = []

    #run checks for each line in input
    for i in range(0, len(schema_lines)):
        # each line requires the line above and below
        # here we create a package of required lines
        lineData = [
            "" if i == 0 else schema_lines[i-1],
            schema_lines[i],
            "" if i == len(schema_lines)-1 else schema_lines[i+1]
            ]

        print("line",i,"\n") 
        # [[above data][current data][below data]]
        # ...data = [[{number, location}],[{symbol, location],[{gear, location}? only in current]] 
        matrix = findIndicies(lineData)

        # list of valid ratio's per line
        ratio_list_per_line = findRatios(matrix)
        for ratio in ratio_list_per_line:
            #append to total
            total_ratios.append(ratio)

    #return total
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
#that worked... nice.

main() 

