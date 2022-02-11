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


def ReadFile(Path:str,HeaderData:dict,FileList:str)->list:
    ExitList=[]
    NeedToGetHeaders=CheckHeaders(HeaderData=HeaderData,FileList=FileList)

    for file in FileList:
        PathFile=Path+file+".txt"
        print("PathFile",PathFile)
        f=open(PathFile,"r",encoding="utf-8")
        Headerstr=f.readline()
        HeaderLocal=Headerstr.split(',')
        if NeedToGetHeaders:
            HeaderData[file]=HeaderLocal
        # print("HeaderData",file,HeaderData[file],type(HeaderData[file]))
        
        Lines=f.readlines()
        for line in Lines:
            Elements=line.split(',')
            ReadyToStore={}
            for idx,key in enumerate(HeaderLocal):
                print(key)
                ReadyToStore[key]=Elements[idx]
            # print("Ready To Store Data:",ReadyToStore)
            # b=input("Delete")


            TempLis=[]
            for head in HeaderData[file]:
                TempLis.append(ReadyToStore[head])
            ExitList.append(TempLis)
        for line in ExitList:
            print(line)
        # print("Header",Header)

        # JuggleDict={}
        # # print(Lines)
        # ExitList=[]
        # for line in Lines:
        #     print(line)
        #     Tempo=[]
        #     # for head in Header:




def Main_Func(ListFiles:list,WorkPath:str)->None:
    CleanFiles(DelPath=WorkPath)

    Files=['Agency','Routes','Trips','Stop_times','Stops','Shapes']

    HeaderData={}
    HeaderData['Agency']=[]
    HeaderData['Routes']=[]
    HeaderData['Trips']=[]
    HeaderData['Stop_times']=[]
    HeaderData['Stops']=[]
    HeaderData['Shapes']=[]

    Decomp(inPath=listPath[0],OutPath=OutTemporaryPath)

    ReadFile(Path=OutTemporaryPath,HeaderData=HeaderData,FileList=Files)


    b=input("Delete")
    CleanFiles(DelPath=WorkPath)




if __name__=="__main__":
    print(os.name)
    if os.name=='posix':
        print("Run")
        listPath=[]
        listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/opendata_ttc_schedules.zip")
        OutTemporaryPath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/GTFZzip/"
        Main_Func(ListFiles=listPath,WorkPath=OutTemporaryPath)
    else:
        print("Please run in LINUX/UNIX")