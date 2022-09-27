import json
import os
import numpy as np




def readFiles(PathFolder,showOutput):
    Files=os.listdir(PathFolder)
    if showOutput: print(Files) 
    return Files


def Csv2Array(FileName,BasePath,showOutput):
    Path=BasePath+"/"+FileName
    file = open(Path)
    DataDict=json.load(file)
    # if showOutput: print(type(DataDict))
    if showOutput: print("DataDict len",len(DataDict))
    # if showOutput: print(DataDict)

    if showOutput: print("DataDict[features] type",type(DataDict["features"]))
    if showOutput: print("DataDict[features] len ",len(DataDict["features"]))
    
    for i in DataDict["features"][:10]:
        if showOutput : print(i["properties"],"\n"*2)
        for key in i["properties"].keys():
            print(key)
        # b=input('.................................')


    dtype=[("StopCode", np.int32), ("weight", np.int32), ("Routes", (np.str_, 100)), ("ContainedStops", (np.str_, 100)), ("SuperNode", (np.str_, 100)), ("CenDeg", np.float64), ("CatCenDeg", np.float64), ("Clossnes", np.float64), ("CatClossnes", np.float64), ("Eigen", np.float64), ("CatEigen", np.float64)]

    Array=np.array(i["properties"],dtype=dtype)
    print(dir(Array))
    if showOutput: print(Array)
    for i in DataDict["features"][:10]:
        Array.insert(i["properties"])


if __name__=="__main__":
    PathFolder="/mnt/e/GitHub/CAMMM-Tool_1.3/Results/SuperNode"
    Files=readFiles(PathFolder=PathFolder,showOutput=False)

    Csv2Array(FileName=Files[0],BasePath=PathFolder,showOutput=True)