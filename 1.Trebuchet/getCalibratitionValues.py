import re
import sys
edgecases= ["twone","threeight","fiveight","sevenine","oneight", "eightwo", "nineight","eighthree"]
digits= ["zero","one","two","three","four","five","six","seven","eight","nine"]
edge= {
        "twone": "twoone",
        "threeight": "threeeight",
        "fiveight": "fiveeight",
        "sevenine": "sevennine",
        "oneight": "oneeight",
        "eightwo": "eighttwo",
        "nineight":"nineeight",
        "eighthree": "eightthree"
        }
cap= f"({"|".join(digits)}|\\d)"   
sub= f"({"|".join(edgecases)})" 

found= 0
ln= 0
sum= 0
dict = {}
i= 0
for x in digits:
    dict[x]=i
    i += 1
    
with open(sys.argv[1], "r") as f:
    for line in f:
        for i in range(0, len(edgecases)):
        #for f_d in edgecases:
            subres=re.sub(list(edge)[i], list(edge.values())[i], line)
            print(subres)
            #line = subres
        values = re.findall(cap, line)
        print(line)
        if (len(values) > 0): #ensure non-emmpty list
            print(f"matches: {values}")
            found += 1
            captured = (values[0], values[-1])
            comp =""
            prev =""
            print(captured)
            for item in captured:
                print(item)
                if item in digits:
                    item = dict[item]
                comp += str(item)
            sum += int(comp)
            print([values[0], comp])
            print(f"total: {sum}")
            print("-----------------------------------------------")
print("calibration complete.")
print(found)
print(sum)
