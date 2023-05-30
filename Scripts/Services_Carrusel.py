## 5001
# #CAMMMM2023

## Obtain the carrousel of services per  node
# This script needs the following:
#   - The shapefiles of services per each node, check the results of the geospatial analysis.
#   - The node file 'general.json'
# The script outputs a json, the example is the bottom

import sys,os
import csv
import json


def ReadFiles(Pathin,ShowProcess:bool=False)->list:
    ### Description
    ### this function reads all the files in a folder 
    # Variables 
    # - Pathin :the folder
    # - dir_list :the list of files in the folder 
    dir_list = os.listdir(Pathin)
    if ShowProcess: print(dir_list)
    if ShowProcess: print(len(dir_list))
    return dir_list

def ReadDataNode(PathIn:str,Category:dict,IdProp:str,ShowProcess:bool=False)->list:
    ### Description
    ### 
    # Variables 
    # - 
    CategoryData={"Primary":{},"Secondary":{},"Tertiary":{}}
    DistData={"Primary":{},"Secondary":{},"Tertiary":{}}
    Groups=[]
    Classes=[]
    with open(PathIn,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        if ShowProcess: print(headers)
        # ['fid', 'osm_id', 'code', 'fclass', 'name', 'Categories', 'Categori_1', 'Categori_2', 'start', 'end', 'cost', 'Distance']
            # 0          1     2       3         4         5                6        7            8         9       10      11

        for idx,row in enumerate(csv_reader):
            # print(row)
            # the elemtens of interest are stored in temp vars for ease of use
            fclass=row[3]
            group=row[6]
            dist=row[11]
            # if the class in a category of interest the following happens 
            if fclass in Category.keys():
                # Store the Category in variable for ease of use
                AgregatedCat=Category[fclass]
                # If the category has not being registered 
                if AgregatedCat not in CategoryData[group].keys():
                    CategoryData[group][AgregatedCat]={"Count": 0,"minDist": 0,"avgDist": 1}
                    DistData[group][AgregatedCat]=[]
                # The data is stored for procesing
                CategoryData[group][AgregatedCat]["Count"]+=1
                DistData[group][AgregatedCat].append(float(dist))
        # Calculations for distances happen, to get min and average 
        for lkey in CategoryData.keys():
            for skey in CategoryData[lkey].keys():
                CategoryData[lkey][skey]["minDist"]=int(min(DistData[lkey][skey]))
                CategoryData[lkey][skey]["avgDist"]=int(sum(DistData[lkey][skey])/len(DistData[lkey][skey]))
                # 
                        
        Data={"Id": IdProp,"CategoryData":CategoryData}
        json_formatted_str = json.dumps(Data, indent=4)
        if ShowProcess: print(json_formatted_str)   
        if ShowProcess: b=input('.................................')

    return Data
    
def GetIdProperty(Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### The function retrieves the Properties Id and matches it to the sequential id
    # Variables 
    # - PayLoad is the dictionary that containes the matching 
    # - data, the data from the json file
    PayLoad={}
    # open the file and store the data in data var
    with open(Path, encoding='utf-8') as fh:
        data = json.load(fh)
    fh.close()
    # if ShowProcess: print(data)
    # A Loop that runs across all the features in the data and matches the Properties Id to the sequential id
    for feature in data["features"]:
        # if ShowProcess: print(feature['id'],"-",feature['properties']['Id'])
        PayLoad[feature['id']]=feature['properties']['Id']
        if ShowProcess: print(feature['id'],PayLoad[feature['id']])
    # return the data
    return PayLoad

def NewCat(ShowProcess:bool=False)->dict:
    ### Description
    ### This is just a dictionary that matches the classes to the categories
    # Variables 
    # - NewCat : the diccionary
    NewCat={}
    NewCat["atm"]="Finance"
    NewCat["bakery"]="Food"
    NewCat["bank"]="Finance"
    NewCat["butcher"]="Food"
    NewCat["chemist"]="Health"
    NewCat["clinic"]="Health"
    NewCat["college"]="Education"
    NewCat["convenience"]="Store"
    NewCat["dentist"]="Health"
    NewCat["department_store"]="Store"
    NewCat["doctors"]="Health"
    NewCat["hospital"]="Health"
    NewCat["kindergarten"]="Education"
    NewCat["laundry"]="Laundry"
    NewCat["library"]="Education"
    NewCat["market_place"]="Store"
    NewCat["nursing_home"]="Shelter"
    NewCat["optician"]="Health"
    NewCat["pharmacy"]="Health"
    NewCat["police"]="Government"
    NewCat["restaurant"]="Food"
    NewCat["school"]="Education"
    NewCat["shelter"]="Shelter"
    NewCat["supermarket"]="Store"
    NewCat["toilet"]="Sanitation"
    NewCat["university"]="Education"
    NewCat["veterinary"]="Health"
    NewCat["bar"]="Food"
    NewCat["beauty_shop"]="Beauty & Fashion"
    NewCat["beverages"]="Food"
    NewCat["bookshop"]="Education"
    NewCat["cafe"]="Food"
    NewCat["car_dealership"]="Store"
    NewCat["car_wash"]="Store"
    NewCat["clothes"]="Beauty & Fashion"
    NewCat["community_centre"]="Government"
    NewCat["computer_shop"]="Electronics"
    NewCat["courthouse"]="Government"
    NewCat["doityourself"]="Store"
    NewCat["embassy"]="Government"
    NewCat["fast_food"]="Food"
    NewCat["fire_station"]="Government"
    NewCat["food_court"]="Food"
    NewCat["furniture_shop"]="Store"
    NewCat["garden_centre"]="Store"
    NewCat["greengrocer"]="Food"
    NewCat["hairdresser"]="Beauty & Fashion"
    NewCat["hostel"]="Shelter"
    NewCat["mall"]="Store"
    NewCat["mobile_phone_shop"]="Electronics"
    NewCat["park"]="Recreation"
    NewCat["post_office"]="Government"
    NewCat["pub"]="Food"
    NewCat["public_building"]="Government"
    NewCat["recycling"]="Government"
    NewCat["recycling_clothes"]="Government"
    NewCat["recycling_glass"]="Government"
    NewCat["recycling_metal"]="Government"
    NewCat["recycling_paper"]="Government"
    NewCat["shoe_shop"]="Beauty & Fashion"
    NewCat["sports_centre"]="Recreation"
    NewCat["sports_shop"]="Store"
    NewCat["stationery"]="Store"
    NewCat["swimming_pool"]="Recreation"
    NewCat["town_hall"]="Government"
    NewCat["toy_shop"]="Store"
    NewCat["vending_any"]="Food"
    NewCat["vending_machine"]="Food"
    NewCat["video_shop"]="Store"
    NewCat["wastewater_plant"]="Government"
    NewCat["water_mill"]="Government"
    NewCat["water_works"]="Government"
    NewCat["alpine_hut"]="Shelter"
    NewCat["arts_centre"]="Culture"
    NewCat["attraction"]="Recreation"
    NewCat["biergarten"]="Recreation"
    NewCat["camp_site"]="Recreation"
    NewCat["caravan_site"]="Shelter"
    NewCat["chalet"]="Shelter"
    NewCat["cinema"]="Recreation"
    NewCat["dog_park"]="Recreation"
    NewCat["florist"]="Store"
    NewCat["gift_shop"]="Store"
    NewCat["golf_course"]="Recreation"
    NewCat["guesthouse"]="Shelter"
    NewCat["hotel"]="Shelter"
    NewCat["ice_rink"]="Recreation"
    NewCat["jeweller"]="Beauty & Fashion"
    NewCat["motel"]="Shelter"
    NewCat["museum"]="Culture"
    NewCat["nightclub"]="Recreation"
    NewCat["outdoor_shop"]="Store"
    NewCat["picnic_site"]="Recreation"
    NewCat["playground"]="Recreation"
    NewCat["stadium"]="Recreation"
    NewCat["theatre"]="Culture"
    NewCat["theme_park"]="Recreation"
    NewCat["tourist_info"]="Recreation"
    NewCat["track"]="Recreation"
    NewCat["zoo"]="Government"

    return NewCat

def WriteFile(Data:dict,Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # -
    f = open(Path, 'w')
    json_formatted_str = json.dumps(DataForFile, indent=4)
    f.write(json_formatted_str)
    f.close()
    return None

if __name__=="__main__":
    # input Path 
    PathFolder=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Service Procesing\Processing\Distances_Table"
    PathGeneral=r"E:\GitHub\CAMMM-Tool_1.3\Output\general.json"
    # outpath
    PathExit=r"E:\GitHub\CAMMM-Tool_1.3\Output\Carrousel.json"
    # Create the data object to be exported
    DataForFile={"features": []}
    # Get the list of files that contain all the node-service data 
    Files=ReadFiles(Pathin=PathFolder,ShowProcess=False)
    #Read the asociation of classes into the categories
    Cat=NewCat()
    # print(len(Cat))

    # The Propertie Id is obtained, the gis processing is done with the sequential 'id' for ease of management of files
    NewId=GetIdProperty(Path=PathGeneral,ShowProcess=False)
    count=0

    for file in Files:
        SmallId=int(file[-9:-4])
        FilePath=PathFolder+"\\"+file
        if str(SmallId) in NewId.keys():
            # print(FilePath,"                           ",SmallId,NewId[str(SmallId)])
            NodeData=ReadDataNode(PathIn=FilePath,Category=Cat,IdProp=NewId[str(SmallId)],ShowProcess=False)
            DataForFile["features"].append(NodeData)
        else:
            count=1+count
    print(count)
    # json_formatted_str = json.dumps(DataForFile, indent=4)
    # print(type(json_formatted_str))   
    WriteFile(Data=DataForFile,Path=PathExit)


# Example of the output 

#{
#   "features": [
#     {
#         "id": "1",  
#         "CategoryData": {
#             "Primary": {
#                 "Finance": {
#                     "Count": 6,
#                     "minDist": 666,
#                     "avgDist": 666
#                 },
#                 "Food": {
#                     "Count": 7,
#                     "minDist": 77,
#                     "avgDist": 77
#                 },
#                 "Store": {
#                     "Count": 8,
#                     "minDist": 88,
#                     "avgDist": 88
#                 },
#             },
#             "Secondary": {
#                 "Food"{
#                     "Count": 5,
#                     "minDist": 545,
#                     "avgDist": 545
#                 },
#                 "Store"{
#                     "Count": 61,
#                     "minDist": 45,
#                     "avgDist": 65
#                 },
#                 "Beauty-Fashion"{
#                     "Count": 26,
#                     "minDist": 34,
#                     "avgDist": 43
#                 }
#             },
#             "Tertiary": {
#                 "Electronics": {
#                     "Count": 98,
#                     "minDist": 78,
#                     "avgDist": 78
#                 },
#                 "Recreation": {
#                     "Count": 9,
#                     "minDist": 56,
#                     "avgDist": 78
#                 },
#                 "Culture": {
#                     "Count": 398,
#                     "minDist": 6345,
#                     "avgDist": 6665
#                 }
#             }
#         }
#     }
# ]
# }