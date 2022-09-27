import readline
import Calculations

import utm
import os
import csv
import pyproj
import zipfile
import math
import sqlite3
import decimal
decimal.getcontext().prec = 10


from FeatureOperations import ConvertToUTM
from FeatureOperations import Agregate

from NetworkAnalisys import GtfsToNetwork
from Databases import TransportNames
from NetworkAnalisys import AgregatedGTFSStopsToNetwork
from NetworkAnalisys import NetWorkToGeoJson
from AggregationTools import CreateNodes

from Clasification import TransformStopsCsvToGeoJson
from Clasification import GetStopDensity

from ClassCollection import BusStop

import networkx




def AnalyzeFareData(Data):
    ExitDict={"Av.Fare":0,"Farrelist":[],"Currency":"","Multimodality":""}
    keys=Data.keys()
    # print("KEys ###############################")
    # for key in keys:
    #     print("\t",key)
    # print("Data ###############################")
    # for key in keys:
    #     print(key)
    #     print("\t",Data[key],type(Data[key]))

    ListOfPrices=[]
    for x in Data["price"]:
        ListOfPrices.append(float(x))
    ExitDict["Av.Fare"]=(sum(ListOfPrices)/len(ListOfPrices))
    for x in range(0,len(Data["price"])):
        # print("--------",x,Data["fare_id"][x],Data["price"][x])
        ExitDict["Farrelist"].append([Data["fare_id"][x],Data["price"][x]])
    # print(Data["currency_type"],type(Data["currency_type"]))
    ExitDict["Currency"]=list(set(Data["currency_type"]))
    ExitDict["Multimodality"]=[]
    for x in Data["transfers"]:
        if x=='':
            ExitDict["Multimodality"].append(True)
        else:
            ExitDict["Multimodality"].append(False)

    # print("ExitDict[Currency]",ExitDict["Currency"],type(ExitDict["Currency"]))
    print(ExitDict)
    return ExitDict

def WriteFareData(Data,CityKey):
    BasePath="Results/_FareInfo/"
    Text=str(Data) 
    ExitPath=BasePath+CityKey+".json"
    # print("ExitPath",ExitPath)
    # print("Text:",Text)
    fw=open(ExitPath,'w')
    fw.write(Text)
    fw.write('\n')
    fw.close()



def GetFareDate(path):
    with open(path,encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        Dict={}
        for head in headers:
            Dict[head]=[]
        for id,row in enumerate(csv_reader):
            print(id,row,type(row),len(row))
            for idx,Element in enumerate(row):
                Dict[headers[idx]].append(Element)

        # print(Dict)
    return Dict




def GetInfoData(List,NameOfCity):
    Files=[]
    CompleteList=["agency.txt", "stops.txt", "routes.txt", "trips.txt", "stop_times.txt", "calendar.txt", "calendar_dates.txt", "fare_attributes.txt", "fare_rules.txt", "shapes.txt", "frequencies.txt", "transfers.txt", "pathways.txt", "levels.txt","feed_info.txt", "translations.txt", "attributions.txt"]
    for Path in List:
        FullSplitPath=Path.split("/")
        File=FullSplitPath[-1]
        print(File)
        if File == "fare_attributes.txt":
            print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY","fare_attributes.txt")
            FareData=GetFareDate(path=Path)
            FareProcData=AnalyzeFareData(Data=FareData)
            WriteFareData(Data=FareProcData,CityKey=NameOfCity)
            # b=input("Delete")