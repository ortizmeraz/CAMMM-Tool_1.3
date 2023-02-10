import json
import utm

def ReadFile(Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 

    with open(Path, encoding='utf-8') as fh:
        data = json.load(fh)
    fh.close()
    # print(data['data'])
    # print(len(data['data']))
    # print(len(data['data']['stations']))
    # print(type(data['data']['stations']))
    # print(data['data'].keys())
    return data['data']['stations']

Path=r''
f = open(Path, 'w')
for t in List:
    text=t
    f.write(text)
f.close()


def WriteToCSV(Data,Headers,Path,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 
    f = open(Path, 'w',encoding='utf-8')
    t=",".join(Headers)+"\n"
    f.write(t)
    for s in Data:
        print(s)
        text=",".join(s)+"\n"
        f.write(text)
    f.close()
    return None

def ReadStations(Stations:list,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 
    Complete=[]
    Headers=['station_id','lat','lon','name','short_name','capacity','X','Y']
    NumStations=0
    for station in Stations:
        if ShowProcess: print(station['station_id'],station['lat'],station['lon'])
        if ShowProcess: print(station['name']," vs ",station['short_name'])
        if ShowProcess: print(station.keys())
        if station['lat'] != 0 and station['lon']!= 0:
            NumStations+=1
            UTM=utm.from_latlon(station['lat'],station['lon'])
            CoordX=str(UTM[0])
            CoordY=str(UTM[1])
            print("CoordX",CoordX)
            print("CoordY",CoordY)
            data=[str(station['station_id']),str(station['lat']),str(station['lon']),str(station['name']),str(station['short_name']),str(station['capacity']),CoordX,CoordY]
            Complete.append(data)
    if ShowProcess: print("NumStations",NumStations)
    return Complete,Headers
if __name__=="__main__":
    Path="/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/station_information.json"
    PathOut="/mnt/e/GitHub/CAMMM-Tool_1.3/Output/Bikes_MTL.csv"
    Stations=ReadFile(Path=Path)
    Data,Headers=ReadStations(Stations=Stations,ShowProcess=False)
    WriteToCSV(Data=Data,Headers=Headers,Path=PathOut)
     
