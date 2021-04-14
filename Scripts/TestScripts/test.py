
# # importing all files  from tkinter 
# from tkinter import * 
# from tkinter import ttk 

# # import only asksaveasfile from filedialog 
# # which is used to save file in any extension 
# from tkinter.filedialog import asksaveasfile 

# files = [('GeoJson', '*.geojson'), 
#     ('Text Document', '*.txt')] 
# file = asksaveasfile(filetypes = files, defaultextension = files) 
# print("###########################################")
# print(file)
# print(type(file))
# print()

# f=open(file.name,"w")
# Text="#####################################################################################################"
# f.write(Text)
# f.close


# import csv
# Path=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.0\SampleData\SampleGTFS\stop_times.txt"



# with open(Path,encoding="utf-8") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     headers = next(csv_reader, None)
#     print(headers)


#     for row in csv_reader:
#         Dict={}
#         # print(row,type(row),len(row))
#         for idx,Element in enumerate(row):
#             Dict[headers[idx]]=Element

#         print(Dict,"\n")


#         print(f'Name{row[5]} and {row[6]}')
#         if len(row) !=9:
#             print(row,type(row),len(row))
#             b=input()
#         if ',' in row[5]:
#             b=input()
#         # b=input()
#         # if line_count == 0:
#         #     print(f'Column names are {", ".join(row)}')
#         #     line_count += 1
#         # else:
#             # print(f'\t{row[5]} works in the {row[6]} department, and was born in {row[7]}.')
#         #     line_count += 1
#     print(f'Processed {6666} lines.')



# f = open('myclone.csv', 'rb')
# reader = csv.reader(f)
# headers = next(reader, None)
# headers
# ['workers', 'constant', 'age']
# column = {}
# for h in headers:
#     column[h] = []

# {'workers': [], 'constant': [], 'age': []}
# for row in reader:
#    for h, v in zip(headers, row):
#      column[h].append(v)


# import networkx as nx


# G = nx.gn_graph(1)

# # G.add_node()
# node="HUI98"
# # G.add_node(node)
# attrs =  {"attr1": 20, "attr2": "nothing"}
# G.add_node(node,attr1="",attr2="")
# Labels=[]
# G.add_node(node,Labels,"labels")
# print(list(G.nodes(data=True)))
# Labels=[1,2,3,4]
# print(list(G.nodes(data=True)))

# # for key in attrs.keys():
# #     G[node][key]=[attrs[key]]
# # G[node]["attr1"]=22

# # attrs

# print(list(G.nodes(data=True)))








# stop_id
# stop_code
# stop_name
# stop_desc
# stop_lat
# stop_lon
# zone_id
# stop_url
# location_type
# parent_station
# stop_timezone
# wheelchair_boarding
# level_id
# platform_code


# "stop_id"
# "stop_code"
# "stop_name"
# "stop_desc"
# "stop_lat"
# "stop_lon"
# "zone_id"
# "stop_url"
# "location_type"
# "parent_station"
# "stop_timezone"
# "wheelchair_boarding"
# "level_id"
# "platform_code"

# if "stop_id" in DataStops[node].keys():
#     stop_id=DataStops[node]['stop_id']
# else: 
#     stop_id=""

# if "stop_code" in DataStops[node].keys():
#     stop_code=DataStops[node]['stop_code']
# else: 
#     stop_code=""

# if "stop_name" in DataStops[node].keys():
#     stop_name=DataStops[node]['stop_name']
# else: 
#     stop_name=""

# if "stop_desc" in DataStops[node].keys():
#     stop_desc=DataStops[node]['stop_desc']
# else: 
#     stop_desc=""

# if "stop_lat" in DataStops[node].keys():
#     stop_lat=DataStops[node]['stop_lat']
# else: 
#     stop_lat=""

# if "stop_lon" in DataStops[node].keys():
#     stop_lon=DataStops[node]['stop_lon']
# else: 
#     stop_id=""

# if "zone_id" in DataStops[node].keys():
#     zone_id=DataStops[node]['zone_id']
# else: 
#     zone_id=""

# if "stop_url" in DataStops[node].keys():
#     stop_url=DataStops[node]['stop_url']
# else: 
#     stop_url=""

# if "location_type" in DataStops[node].keys():
#     location_type=DataStops[node]['location_type']
# else: 
#     location_type=""

# if "parent_station" in DataStops[node].keys():
#     parent_station=DataStops[node]['parent_station']
# else: 
#     parent_station=""

# if "stop_timezone" in DataStops[node].keys():
#     stop_timezone=DataStops[node]['stop_timezone']
# else: 
#     stop_timezone=""

# if "wheelchair_boarding" in DataStops[node].keys():
#     wheelchair_boarding=DataStops[node]['wheelchair_boarding']
# else: 
#     wheelchair_boarding=""

# if "level_id" in DataStops[node].keys():
#     level_id=DataStops[node]['level_id']
# else: 
#     level_id=""

# if "platform_code" in DataStops[node].keys():
#     platform_code=DataStops[node]['platform_code']
# else: 
#     platform_code=""


#         G.add_node(node,location=(x,y),pos=(float(DataStops[node]['stop_lat']),float(DataStops[node]['stop_lon'])),stop_id =stop_id,stop_name =stop_name,stop_code =stop_code,stop_desc=stop_desc,stop_lat=stop_lat,stop_lon=stop_lon,zone_id=zone_id,stop_url=stop_url,location_type=location_type,parent_station=parent_station,stop_timezone=stop_timezone,wheelchair_boarding=wheelchair_boarding,level_id=level_id,platform_code=platform_code)
#         NodePrintProp['Pos'][node]=(x,y)

import zipfile


Path=r"SampleData\GTFS\gtfs_stm.zip"
archive = zipfile.ZipFile(Path, 'r')
with archive as zip: 
    ZipList=zip.namelist()
archive = zipfile.ZipFile(Path, 'r')
for zipfile in ZipList:
    fw=open(r"Operational\\"+zipfile,"w", encoding="utf-8")
    FilePointer=archive.open(zipfile)
    for line in FilePointer.readlines():
        # print(line,type(line))
        text=line.decode("utf-8")
        # print(text,type(text))
        fw.write(text)
    # b=input('Press Enter ...')
    fw.close()

