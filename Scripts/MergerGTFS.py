from xmlrpc.client import boolean
import zipfile as zpfl
import pathlib
import os

def Decomp(inPath:str,OutPath:str):
    with zpfl.ZipFile(inPath,"r") as zip_ref:
        zip_ref.extractall(OutPath)
        print("Decompressing:",OutPath)

def CleanFiles(DelPath:str):
    entries = os.listdir(DelPath)	
    for entry in entries:
        FullPath=os.path.abspath(DelPath+entry)
        os.remove(FullPath)

def CheckHeaders(HeaderData:dict,FileList:list)->boolean:
    NeedToGetHeaders=False
    for head in FileList:
        if len(HeaderData[head])==0:
            NeedToGetHeaders=True
    return NeedToGetHeaders

def GetHeaders(Path:str,FILES:list,HeaderData:dict)->dict:
    for file in FILES:
        PathFile=Path+file+".txt"
        print("PathFile",PathFile)
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

    # print(CleanLineH)
    # print(HeaderData[File])
    # # print(LocalKeys)
    # if LocalKeys==HeaderData[File]:
    #         print("I am confused")
    # b=input("Delete")
    
    Lines=f.readlines()
    for line in Lines:
        CleanLine=line.rstrip('\n')
        Elements=CleanLine.split(',')
        ReadyToStore={}
        for idx,key in enumerate(HeaderLocal):
            # print("key:",key)
            # print(HeaderLocal)
            try:
                ReadyToStore[key]=Elements[idx]
            except:
                ReadyToStore[key]="-"
                print("No values for: ",key)
            # if key in HeaderData.keys():
            #     ReadyToStore[key]=Elements[idx]
            # else:
            #     ReadyToStore[key]=Elements[idx]
        # print("Ready To Store Data:",ReadyToStore)
        # b=input("Delete")

        TempLis=[]

        # LocalKeys=list(ReadyToStore.keys())
        for head in HeaderData[File]:

            TempLis.append(ReadyToStore[head])
        ExitList.append(TempLis)
    for line in ExitList:
        print(HeaderData[File])
        print(line)
    print("------------------------------------------------------------------------\n"*2)
    return ExitList





def Main_Func(ListFiles:list,WorkPath:str)->None:

    FILES=['Agency','Routes','Trips','Stop_times','Stops','Shapes']

    HeaderData={}
    for file in FILES:
        HeaderData[file]=[]
    for workZip in ListFiles:
        CleanFiles(DelPath=WorkPath)
        Decomp(inPath=workZip,OutPath=WorkPath)

        for file in FILES:
            NeedToGetHeaders=CheckHeaders(HeaderData=HeaderData,FileList=FILES)
            if NeedToGetHeaders:
                HeaderData=GetHeaders(Path=WorkPath,FILES=FILES,HeaderData=HeaderData)
            ReadFile(Path=WorkPath,HeaderData=HeaderData,File=file)
            print("file",file)
            b=input("Delete")
        CleanFiles(DelPath=WorkPath)
    print("----------------------------------------------------------------------------------------------------------------"*5)




if __name__=="__main__":
    print(os.name)
    if os.name=='posix':
        print("Run")
        listPath=[]
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/opendata_ttc_schedules.zip")
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/burlington.zip")
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/York.zip")
        OutTemporaryPath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/GTFZzip/"
        Main_Func(ListFiles=listPath,WorkPath=OutTemporaryPath)
    else:
        print("Please run in LINUX/UNIX")