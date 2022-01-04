#! python3.7

import sqlite3

def Dictionary():
    RowPaths={'SampleData':1,
    'Importance1':2,
    'Importance2':3,
    'NetworkSimple1':4,
    'NetworkSimple2':5,
    'NetworkNodeLine1':6,
    'NetworkBusStops1':7,
    'NetworkNodeLine2':8,
    'NetworkBusStops2':9,
    'EPSGIN':10,
    'PathSingleGTFS':11,
    'end':0}
    return RowPaths

def RearPaths(Key):
    PathDB="Scripts/Database.db"
    RowPaths=Dictionary()
    db = sqlite3.connect(PathDB)
    cursor = db.cursor()
    Comand='SELECT * FROM ListPaths WHERE "_rowid_"=\'2\';'
    Data=cursor.execute('SELECT * FROM ListPaths WHERE "_rowid_"=\''+str(RowPaths[Key])+'\';')
    List=list(Data)
    # print("Key: ",Key)
    # print("Path:",List[0][2])
    # b=input()
    return List[0][2]

def UpdatePath(Key,NewPath):
    # print("NewPath",NewPath)
    RowPaths=Dictionary()
    # PathDB="E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\Scripts\Database.db"
    PathDB="Scripts/Database.db"
    db = sqlite3.connect(PathDB)
    cursor = db.cursor()
    Comand='UPDATE "main"."ListPaths" SET "Path"=\''+NewPath+'\' WHERE "_rowid_"=\''+str(RowPaths[Key])+'\';'
    print("Comand",Comand)
    cursor.execute(Comand)
    db.commit()

# def AgregarRegistro(db,Tabla,NombresColumnas,ColumnasValores):
#     db = sqlite3.connect(Path)
#     cursor = db.cursor()
#     Comand='INSERT INTO "main"."'+Tabla+'"('+NombresColumnas+') VALUES ('+ColumnasValores+');'
#     cursor.execute(Comand)
#     db.commit()

def TransportNames():
    TypeOfSystemName={}
    TypeOfSystemName["0"] = " Tram, Streetcar, Light rail. Any light rail or street level system within a metropolitan area."
    TypeOfSystemName["1"] = " Subway, Metro. Any underground rail system within a metropolitan area."
    TypeOfSystemName["2"] = " Rail. Used for intercity or long distance travel."
    TypeOfSystemName["3"] = " Bus. Used for short and long distance bus routes."
    TypeOfSystemName["4"] = " Ferry. Used for short and long distance boat service."
    TypeOfSystemName["5"] = " Cable tram. Used for street level rail cars where the cable runs beneath the vehicle."
    TypeOfSystemName["6"] = " Aerial lift, Suspended cable car, Cable transport where cabins, cars, gondolas or open chairs are suspended by means of one or more cables."
    TypeOfSystemName["7"] = " Funicular. Any rail system designed for steep inclines."
    TypeOfSystemName["11"] = " Trolleybus. Electric buses that draw power from overhead wires using poles."
    TypeOfSystemName["12"] = " Monorail. Railway in which the track consists of a single rail or a beam."
    TypeOfSystemName["100"] = "Railway Service"
    TypeOfSystemName["101"] = "High Speed Rail Service"
    TypeOfSystemName["102"] = "Long Distance Trains"
    TypeOfSystemName["103"] = "Inter Regional Rail Service"
    TypeOfSystemName["104"] = "Car Transport Rail Service"
    TypeOfSystemName["105"] = "Sleeper Rail Service"
    TypeOfSystemName["106"] = "Regional Rail Service"
    TypeOfSystemName["107"] = "Tourist Railway Service"
    TypeOfSystemName["108"] = "Rail Shuttle (Within Complex)"
    TypeOfSystemName["109"] = "Suburban Railway"
    TypeOfSystemName["110"] = "Replacement Rail Service"
    TypeOfSystemName["111"] = "Special Rail Service"
    TypeOfSystemName["112"] = "Lorry Transport Rail Service"
    TypeOfSystemName["113"] = "All Rail Services"
    TypeOfSystemName["114"] = "Cross-Country Rail Service"
    TypeOfSystemName["115"] = "Vehicle Transport Rail Service"
    TypeOfSystemName["116"] = "Rack and Pinion Railway"
    TypeOfSystemName["117"] = "Additional Rail Service"
    TypeOfSystemName["200"] = "Coach Service"
    TypeOfSystemName["201"] = "International Coach Service"
    TypeOfSystemName["202"] = "National Coach Service"
    TypeOfSystemName["203"] = "Shuttle Coach Service"
    TypeOfSystemName["204"] = "Regional Coach Service"
    TypeOfSystemName["205"] = "Special Coach Service"
    TypeOfSystemName["206"] = "Sightseeing Coach Service"
    TypeOfSystemName["207"] = "Tourist Coach Service"
    TypeOfSystemName["208"] = "Commuter Coach Service"
    TypeOfSystemName["209"] = "All Coach Services"
    TypeOfSystemName["400"] = "Urban Railway Service"
    TypeOfSystemName["401"] = "Metro Service"
    TypeOfSystemName["402"] = "Underground Service"
    TypeOfSystemName["403"] = "Urban Railway Service"
    TypeOfSystemName["404"] = "All Urban Railway Services"
    TypeOfSystemName["405"] = "Monorail"
    TypeOfSystemName["700"] = "Bus Service"
    TypeOfSystemName["701"] = "Regional Bus Service"
    TypeOfSystemName["702"] = "Express Bus Service"
    TypeOfSystemName["703"] = "Stopping Bus Service"
    TypeOfSystemName["704"] = "Local Bus Service"
    TypeOfSystemName["705"] = "Night Bus Service"
    TypeOfSystemName["706"] = "Post Bus Service"
    TypeOfSystemName["707"] = "Special Needs Bus"
    TypeOfSystemName["708"] = "Mobility Bus Service"
    TypeOfSystemName["709"] = "Mobility Bus for Registered Disabled"
    TypeOfSystemName["710"] = "Sightseeing Bus"
    TypeOfSystemName["711"] = "Shuttle Bus"
    TypeOfSystemName["712"] = "School Bus"
    TypeOfSystemName["713"] = "School and Public Service Bus"
    TypeOfSystemName["714"] = "Rail Replacement Bus Service"
    TypeOfSystemName["715"] = "Demand and Response Bus Service"
    TypeOfSystemName["716"] = "All Bus Services"
    TypeOfSystemName["800"] = "Trolleybus Service"
    TypeOfSystemName["900"] = "Tram Service"
    TypeOfSystemName["901"] = "City Tram Service"
    TypeOfSystemName["902"] = "Local Tram Service"
    TypeOfSystemName["903"] = "Regional Tram Service"
    TypeOfSystemName["904"] = "Sightseeing Tram Service"
    TypeOfSystemName["905"] = "Shuttle Tram Service"
    TypeOfSystemName["906"] = "All Tram Services"
    TypeOfSystemName["1000"] = "Water Transport Service"
    TypeOfSystemName["1100"] = "Air Service"
    TypeOfSystemName["1200"] = "Ferry Service"
    TypeOfSystemName["1300"] = "Aerial Lift Service"
    TypeOfSystemName["1400"] = "Funicular Service"
    TypeOfSystemName["1500"] = "Taxi Service"
    TypeOfSystemName["1501"] = "Communal Taxi Service"
    TypeOfSystemName["1502"] = "Water Taxi Service"
    TypeOfSystemName["1503"] = "Rail Taxi Service"
    TypeOfSystemName["1504"] = "Bike Taxi Service"
    TypeOfSystemName["1505"] = "Licensed Taxi Service"
    TypeOfSystemName["1506"] = "Private Hire Service Vehicle"
    TypeOfSystemName["1507"] = "All Taxi Services"
    TypeOfSystemName["1700"] = "Miscellaneous Service"
    TypeOfSystemName["1702"] = "Horse-drawn Carriage"
    return TypeOfSystemName



def TextSqLite(idx):
    Text=[]
    Text[0]="INSERT INTO CityData "
    Text[1]="(Id,FirstAgency,name,AreaSqKm,PopulationMillion,DensityPersonSqKm,NumBoroughs,NumTransitSystems,Type0,NumStops0,NumLines0,AvgDisStops0,Type1,NumStops1,NumLines1,AvgDisStops1,Type2,NumStops2,NumLines2,AvgDisStops2,Type3,NumStops3,NumLines3,AvgDisStops3,Type4,NumStops4,NumLines4,AvgDisStops4)"
    Text[2]=" VALUES "
    return idx



if __name__ == "__main__":
    # print("New ...............Text")
    # # New=input()
    # # UpdatePath(Key='Importance1',NewPath=New)
    # L=RearPaths(Key='Importance1')
    # print(L)
    # b=input()
    UpdatePath(Key="Importance1",NewPath="test")


