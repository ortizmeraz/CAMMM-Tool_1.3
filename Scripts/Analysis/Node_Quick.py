import json
import os
import numpy as np
from jenkspy import JenksNaturalBreaks

import matplotlib.pyplot as plt



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
        # for key in i["properties"].keys():
        #     print(key)
        # b=input('.................................')


    dtype=[("StopCode", np.int32), ("weight", np.int32), ("Routes", (np.str_, 100)), ("ContainedStops", (np.str_, 100)), ("SuperNode", (np.str_, 100)), ("CenDeg", np.float64), ("CatCenDeg", np.float64), ("Clossnes", np.float64), ("CatClossnes", np.float64), ("Eigen", np.float64), ("CatEigen", np.float64)]

    # print(dir(Array))
    # if showOutput: print(Array)
    ArrayFeeder=[]
    for idx,i in enumerate(DataDict["features"]):
        if showOutput: print(type(i))
        if showOutput:print(i["properties"]['weight'])
        ArrayFeeder.append(i["properties"]['weight'])
    Array=np.array(ArrayFeeder)
    if showOutput: print(Array)

    return Array


if __name__=="__main__":
    PathFolder="/mnt/e/GitHub/CAMMM-Tool_1.3/Results/SuperNode"
    Files=readFiles(PathFolder=PathFolder,showOutput=False)

    Xstops=list(range(0,45,5))
    jnb = JenksNaturalBreaks(4)

    for File in Files:
        ExitName=File+".jpg"
        f1 = plt.figure()
        Array = Csv2Array(FileName=File,BasePath=PathFolder,showOutput=False)
        SortedArray=np.sort(Array)
        classes = jnb.fit(Array) 
        print(classes)
        plt.plot(SortedArray[::-1])
        plt.title(File)
        plt.yticks(Xstops)
        # plt.show()
        plt.savefig(ExitName)
        plt.clf()