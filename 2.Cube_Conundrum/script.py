import re
import sys

data = sys.argv[1]
limits={
"r": int(sys.argv[2]),
"g": int(sys.argv[3]),
"b": int(sys.argv[4]),
}




def getValues(arr):
    red = 0
    green = 0
    blue = 0
    isValid= True
    for item in arr:
        cNu = int(re.findall("(\d+)\s", item)[0])
        val= item[-1]
        match val:
            case "r":
               red = cNu
               if cNu > limits["r"]:
                   #print(f"red value ({cNu}) over {limits['r']}")
                   isValid= False
            case "g":
               green = cNu
               if cNu > limits["g"]:
                   #print(f"green value ({cNu}) over {limits['g']}")
                   isValid= False
            case "b":
               blue = cNu
               if cNu > limits["b"]:
                   #print(f"blue value ({cNu}) over {limits['b']}")
                   isValid= False
    return [red,green,blue,isValid]

def getGameData(gameStr):
    vars = re.split(":",gameStr)
    id = re.findall("(\d+):",gameStr)[0]
    throws = re.split(";",vars[1])
    gameObj = {
        "id":id,
        "throw_amount" : len(throws),
        "throw_list" : [],
        "isValid" : True 
    }

    for i in range(0, len(throws)):
        values = re.findall("(\d+\s\w)", throws[i])
        valueArr = getValues(values)
        gameObj["throw_list"].append(valueArr)
        if (valueArr[-1] == False):
               gameObj["isValid"]= False
    return gameObj

def parseData():

    with open(data, "r") as input:
        invalid_ids = []
        valid_ids = []
        for line in input:
           gameData = getGameData(line)
           if (gameData["isValid"] == False):
               invalid_ids.append(int(gameData["id"]))
           elif (gameData["isValid"] == True):
               valid_ids.append(int(gameData["id"]))

        print(f"{len(invalid_ids)} invalid games.")
        print(f"{len(valid_ids)} valid games.")

        valid_sum = sum(valid_ids)
        invalid_sum = sum(invalid_ids)
        
        print("sum of valid ids")
        print(valid_sum)




def run():
    print(f"current resources: {limits['r']} red, {limits['g']} green, {limits['b']} blue.")
    parseData()

run()
