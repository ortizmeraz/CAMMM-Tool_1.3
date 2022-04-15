from xmlrpc.client import boolean
import zipfile as zpfl
from zipfile import ZipFile

import pathlib
import os
import Calculations


# Decompression function
def Decomp(inPath:str,OutPath:str):
    with zpfl.ZipFile(inPath,"r") as zip_ref:
        zip_ref.extractall(OutPath)
        print("Decompressing:",OutPath)
# Clean working directory
def CleanFiles(DelPath:str):
    entries = os.listdir(DelPath)	
    for entry in entries:
        FullPath=os.path.abspath(DelPath+entry)
        os.remove(FullPath)
# Function to check if there are headers stored in the Header dict
def CheckHeaders(HeaderData:dict,FileList:list)->boolean:
    NeedToGetHeaders=False
    for head in FileList:
        if len(HeaderData[head])==0:
            NeedToGetHeaders=True
    return NeedToGetHeaders

def GetHeaders(Path:str,FILES:list,HeaderData:dict)->dict:
    for file in FILES:
        PathFile=Path+file+".txt"
        # print("PathFile",PathFile)
        f=open(PathFile,"r",encoding="utf-8")
        Headerstr=f.readline()
        CleanLineH=Headerstr.rstrip()
        HeaderLocal=CleanLineH.split(',')
        HeaderData[file]=HeaderLocal

    return HeaderData

def ReadFile(Path:str,HeaderData:dict,File:str)->list:
    ExitList=[]

    PathFile=Path+File+".txt"
    print("PathFile",PathFile)
    f=open(PathFile,"r",encoding="utf-8")
    Headerstr=f.readline()
    CleanLineH=Headerstr.rstrip()
    HeaderLocal=CleanLineH.split(',')

    # print("HeaderLocal     ",HeaderLocal)
    # print("HeaderData[File]",HeaderData[File])

    Lines=f.readlines()
    for line in Lines:
        CleanLine=line.rstrip('\n')
        Elements=CleanLine.split(',')
        ReadyToStore={}
        for idx,key in enumerate(HeaderLocal):
            ReadyToStore[key]=Elements[idx]
  
        TempLis=[]
        # LocalKeys=list(ReadyToStore.keys())
        for head in HeaderData[File]:
            try:
                # print("Key found")
                TempLis.append(ReadyToStore[head])
            except:
                # print("head",head)
                # print("Key found")
                TempLis.append("-")
            # if key in HeaderLocal:
            #     print("Key found")
            #     TempLis.append(ReadyToStore[head])
            # else:
            #     print("Key found")

            #     TempLis.append("-")
        ExitList.append(TempLis)
    # for line in ExitList:
        # print(HeaderData[File])
        # print(line)
    # print("------------------------------------------------------------------------\n"*2)
    return ExitList


def CheckDataQuality(FILES:list,DATA:dict)->None:
    for file in FILES:
        Change=False
        print("file:",file)
        for idx,i in enumerate(DATA[file]):
            print(len(i),end=",")
            if len(i)!=len(DATA[file][idx-1]):
                Change=True
                print("-----\n"*3)
        print("CheckDataQuality")
        print("Status of change",Change)
        b=input("Delete")
        print("\n"*5)

def WriteFiles(FILES:list,ExitPath:str,DATA:dict,HeaderData:dict)->None:
    for File in FILES:
        print(File)
        ExitPathFile=ExitPath+File+".txt"
        print(ExitPathFile,len(DATA[File]),type(DATA[File]))
        f = open(ExitPathFile, "w")
        print("type DATA[File]: ",type(DATA[File]))
        TextLine=','.join(HeaderData[File])
        Text=TextLine+"\n"
        f.write(Text)
        for line in DATA[File]:
            TextLine=','.join(line)
            Text=TextLine+"\n"
            f.write(Text)
        print(Text)
        # b=input("Delete")
        f.close()

def CompressFiles(FILES:list,ExitPath:str,ExitZip:str)->None:
    with ZipFile(ExitZip, mode='w') as zf:
        for File in FILES:
            ExitPathFile=ExitPath+File+".txt"
            zf.write(ExitPathFile)

def Main_Func(ListFiles:list,WorkPath:str,ExitPath:str)->None:
    # This is the main function. It needs:
    # A) List of GTFS files.
    # B) working path to uncompress
    # C) Exit path 
    FILES=['Agency','Routes','Trips','Stop_times','Stops','Shapes']
    # a dictionary to store all the header data of the first GTFS and use it as a guide for the rest of files
    HeaderData={}
    # a dictionary to store the data BY FILE TYPE(see 'FILES')
    DATA={}
    # The headers for the files are used to create the containers for the FILES
    for file in FILES:
        HeaderData[file]=[]
        DATA[file]=[]
    # The main cilce starts here
    for workZip in ListFiles:
        # The woking file directory is cleaned
        CleanFiles(DelPath=WorkPath)
        # The files of the GTFS are decompressed
        Decomp(inPath=workZip,OutPath=WorkPath)
        # The loop for each of the files in the GTFS
        for file in FILES:
            # Header function is excecuted, a boolean value returns, True is there are no headers stored 
            NeedToGetHeaders=CheckHeaders(HeaderData=HeaderData,FileList=FILES)
            if NeedToGetHeaders: # if there are no headers stored, excecute the GetHeaders function 
                HeaderData=GetHeaders(Path=WorkPath,FILES=FILES,HeaderData=HeaderData)
            # The data of the working file is stored in a temporary file using ReadFile
            TempData=ReadFile(Path=WorkPath,HeaderData=HeaderData,File=file)
            # Data is stored in the correct list in the DATA dictornay pool
            DATA[file]=DATA[file]+TempData
            # print("file",file)
            # print("workZip",workZip)
            # b=input("Delete")
        # The woking file directory is cleaned
        CleanFiles(DelPath=WorkPath)
    # Check data is properly stored function
    # CheckDataQuality(FILES=FILES,DATA=DATA)
    # Files are stored in files to be compressed
    WriteFiles(FILES=FILES,ExitPath=ExitPath,DATA=DATA,HeaderData=HeaderData)
    CompressFiles(FILES=FILES,ExitPath=ExitPath,ExitZip=str)
    

    print("----------------------------------------------------------------------------------------------------------------"*5)




if __name__=="__main__":
    print(os.name)
    if os.name=='posix':
        print("Run")
        listPath=[]
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/opendata_ttc_schedules.zip")
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/hamilton.zip")
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/burlington.zip")
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/York.zip")
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/Mississauga.zip")
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/GTFS_Durham_TXT.zip")

        OutTemporaryPath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/GTFZzip/"
        ExitPath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Data/"
        ExitZip=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Data/new_gtfs.zip"
        Main_Func(ListFiles=listPath,WorkPath=OutTemporaryPath,ExitPath=ExitPath)
    else:
        print("Please run in LINUX/UNIX")