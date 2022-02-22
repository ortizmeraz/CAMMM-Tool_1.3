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

def WriteFiles(FILES:list,ExitPath:str,DATA:dict)->None:
    for File in FILES:
        print(File)
        ExitPathFile=ExitPath+File+".txt"
        print(ExitPathFile,len(DATA[File]),type(DATA[File]))
        f = open(ExitPathFile, "w")
        Text=""
        for line in DATA[File]:
            TextLine=','.join(line)
            Text=Text+TextLine+"\n"
        print(Text)
        b=input("Delete")
        f.write("Woops! I have deleted the content!")
        f.close()



def Main_Func(ListFiles:list,WorkPath:str,ExitPath:str)->None:

    FILES=['Agency','Routes','Trips','Stop_times','Stops','Shapes']

    HeaderData={}
    DATA={}
    for file in FILES:
        HeaderData[file]=[]
        DATA[file]=[]
    for workZip in ListFiles:
        CleanFiles(DelPath=WorkPath)
        Decomp(inPath=workZip,OutPath=WorkPath)

        for file in FILES:
            NeedToGetHeaders=CheckHeaders(HeaderData=HeaderData,FileList=FILES)
            if NeedToGetHeaders:
                HeaderData=GetHeaders(Path=WorkPath,FILES=FILES,HeaderData=HeaderData)
            TempData=ReadFile(Path=WorkPath,HeaderData=HeaderData,File=file)
            DATA[file]=DATA[file]+TempData
            # print("file",file)
            # print("workZip",workZip)
            # b=input("Delete")
        CleanFiles(DelPath=WorkPath)
    # CheckDataQuality(FILES=FILES,DATA=DATA)
    WriteFiles(FILES=FILES,ExitPath=ExitPath,DATA=DATA)
    

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
        ExitPath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Data/"
        Main_Func(ListFiles=listPath,WorkPath=OutTemporaryPath,ExitPath=ExitPath)
    else:
        print("Please run in LINUX/UNIX")