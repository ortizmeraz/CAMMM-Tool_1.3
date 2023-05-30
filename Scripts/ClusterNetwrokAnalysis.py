## This Calculates 
# #CAMMMM2023
#40
import ast
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import utm
import jenkspy 
import json


def CalculateHubWeight(MetroData,RailData,TramData,BusData,ShowProcess:bool=False)->int:
    ### Description
    ### 
    # Variables 
    # - 
    HubLevel=0
    HubDict=MetroData
    HubDict.update(RailData)
    for station in HubDict.keys():
        HubLevel+=1
        if ShowProcess: print(station)

    ClusterLevel=0
    CLusterDict=BusData
    CLusterDict.update(TramData)
    for stop in CLusterDict.keys():
        ClusterLevel+=1
        if ShowProcess: print(stop)
    #########################################################
    #########################################################
    #########################################################
    if HubLevel>0:
        weigth=(HubLevel*100)+ClusterLevel
    else:
        weigth=ClusterLevel
    #########################################################
    #########################################################
    #########################################################
    return weigth



def ReadLinks(Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 
    ClusterLink=[]
    with open(Path) as f:
        Lines = f.readlines()
        if ShowProcess: print(len(Lines))
        for line in Lines:
            link=ast.literal_eval(line)
            if ShowProcess: print(link,type(link))
            ClusterLink.append(link)
    f.close()
    return ClusterLink

def ReadNodes(Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 
    Data=""
    with open(Path) as f:
        Lines = f.readlines()
        for line in Lines:
            Data+=line
            if ShowProcess: print(line)
    f.close()
    Nodes=ast.literal_eval(Data)
    return Nodes

def CreateNetwork(ListNodes,ListEdges,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 
    Node_Properties={'Pos':{}}
    G = nx.DiGraph()
    Node_Properties['Pos']['99']=[-73.797666, 45.455539]
    Node_Properties['Pos']['98']=[-73.797666, 45.455539]
    for node in ListNodes:
        if ShowProcess: print(node.keys())
        if ShowProcess: print(node['geometry'])
        Xval=float(node['geometry']['coordinates'][0])
        Yval=float(node['geometry']['coordinates'][-1])
        id=node[ 'properties']['Id']
        Node_Properties['Pos'][id]=[Xval,Yval]
        # if ShowProcess: b=input('.................................')
        weigth=CalculateHubWeight(MetroData=node[ 'properties']['MetroData'],
        RailData=node[ 'properties']['RailData'],
        BusData=node[ 'properties']['BusData'],
        TramData=node[ 'properties']['TramData'])

        if ShowProcess: print("id      :",id)
        if ShowProcess: print("weigth  :",weigth)
        if ShowProcess: print("Coords  :",Node_Properties['Pos'][id])
        if ShowProcess: print("\n"*3,node[ 'properties'].keys())
        if id != '99':
            G.add_node(id,weigth=weigth,pos=(Xval,Yval))

    G.add_edges_from(ListEdges)

    # nx.draw_networkx_nodes(G)
    # nx.nx.draw_networkx_edges(G)
    print(list(G.nodes))
    # if ShowProcess: b=input('.................................')
    # print("###\n"*5)
    # print("Graphiing")
    # nx.draw(G,pos=Node_Properties['Pos'])
    # plt.show()
    # if ShowProcess: b=input('.................................')

    return G


def ClassifyData(CollectionOfValues:dict,Breaks:dict,KeyList:list,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 


    Data={"features": []}
    # if ShowProcess: print("............................................")
    for key in KeyList:
        # if ShowProcess: print(key)
        keys = list(CollectionOfValues.keys())
        tempDict = {key: 0 for key in keys}
        tempDict["Id"]=key
        for analysis in CollectionOfValues.keys():
            # if ShowProcess: print("\t",analysis,"type",type(analysis))
            #  The breaks and value are stored in a shorter variable for ease of use
            lb=Breaks[analysis]
            vl=CollectionOfValues[analysis][key]
            if ShowProcess: print("\t"*2,lb,len(lb))
            tempDict[analysis]=0
            # if ShowProcess: print("\t\t Value:",vl)
            for r in range(1,11):
                if lb[r-1]<=vl and vl<=lb[r]:
                    # if ShowProcess: print(r,lb[r-1],"-",lb[r],"|",end="\t")
                    # if ShowProcess: print("type r:",r,type(r))
                    tempDict[str(analysis)]=r
                    # if ShowProcess: print("\t"*2,r)

            # if ShowProcess: print()
            # if ShowProcess: print(tempDict)
        Data["features"].append(tempDict)


    print(".........FORMATED DATA...................................")
    # print(Data)
    json_formatted_str = json.dumps(Data, indent=4)
    if ShowProcess: print(json_formatted_str)
    return json_formatted_str,Data



def Calculations(Graph,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 
    print("start....")
    degree_centrality = nx.degree_centrality(Graph)
    closeness_centrality = nx.closeness_centrality(Graph)
    eigenvector_centrality = nx.betweenness_centrality(Graph, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    betweeness_centrality = nx.betweenness_centrality(Graph)


    ListKeys=list(eigenvector_centrality.keys())
    col_degree_centrality=[]
    col_closeness_centrality=[]
    col_eigenvector_centrality=[]
    col_betweeness_centrality=[]
    dict_cen={}
    dict_clo={}
    dict_bet={}
    for keys in ListKeys:
        col_degree_centrality.append(int(degree_centrality[keys]*10000000))
        dict_cen[keys]=int(degree_centrality[keys]*10000000)
        col_closeness_centrality.append(int(closeness_centrality[keys]*10000000))
        dict_clo[keys]=int(closeness_centrality[keys]*10000000)
        col_betweeness_centrality.append(int(betweeness_centrality[keys]*10000000))
        dict_bet[keys]=int(betweeness_centrality[keys]*10000000)
    
    UnVal_degree_centrality=list(set(col_degree_centrality))
    UnVal_closeness_centrality=list(set(col_closeness_centrality))
    UnVal_eigenvector_centrality=list(set(col_eigenvector_centrality))
    UnVal_betweeness_centrality=list(set(col_betweeness_centrality))

    ClasesCentrality=jenkspy.jenks_breaks(UnVal_degree_centrality, n_classes=10)
    ClasesCloseness=jenkspy.jenks_breaks(UnVal_closeness_centrality, n_classes=10)
    # ClasesEigenvector=jenkspy.jenks_breaks(UnVal_eigenvector_centrality, n_classes=10)
    ClasesBetweeness=jenkspy.jenks_breaks(UnVal_betweeness_centrality, n_classes=10)

    CollectionOfAnalysis={"Centrality":dict_cen,"Closeness":dict_clo,"Betweeness":dict_bet}
    BreakOfCollections={"Centrality":ClasesCentrality,"Closeness":ClasesCloseness,"Betweeness":ClasesBetweeness}

    if ShowProcess: print("\n"*10)
    if ShowProcess: print("ClasesCentrality",ClasesCentrality)
    if ShowProcess: print("ClasesCloseness",ClasesCloseness)
    if ShowProcess: print("ClasesBetweeness",ClasesBetweeness)
    if ShowProcess: b=input('.................................')
    Text,Data=ClassifyData(CollectionOfValues=CollectionOfAnalysis,Breaks=BreakOfCollections,KeyList=ListKeys,ShowProcess=False)
    return Text,Data


def WriteFile(Data:dict,Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # -
    f = open(Path, 'w')
    json_formatted_str = json.dumps(Data, indent=4)
    f.write(json_formatted_str)
    f.close()
    return None
    
    print("end......")

if __name__=="__main__":
    PathLinks="/mnt/e/Github/CAMMM-Tool_1.3/Output/Links.txt"
    PathNodes="/mnt/e/GitHub/CAMMM-Tool_1.3/Output/general.json"

    ExitPath="/mnt/e/GitHub/CAMMM-Tool_1.3/Output/connectivity.geojson"

    ClusterLink=ReadLinks(Path=PathLinks)
    ClusterNodes=ReadNodes(Path=PathNodes)
    # print(type(ClusterNodes['features']))
    # print(len(ClusterNodes['features']))
    # print(ClusterNodes['features'][0][ 'properties'])
    Graph=CreateNetwork(ListNodes=ClusterNodes['features'],ListEdges=ClusterLink,ShowProcess=False)
    Text,Data=Calculations(Graph=Graph,ShowProcess=False)
    WriteFile(Data=Data,Path=ExitPath)
    # print(type(ClusterLink))
    # print(len(ClusterLink))
    # print(ClusterLink[0])






#{
#   "features": [
#     {
#         "Id": "10",  
#         "Centrality": 0.0050335570469798654,
#         "Closeness" : 0.02029144279570403,
#         "EigenVect" : 0.15799053829758186
#     },
#     {
#         "Id": "21",  
#         "Centrality": 0.0028763183125599234,
#         "Closeness" : 0.023267285305485334,
#         "EigenVect" : 0.012695822176745454
#     },{
#      }
#  ]
# }






# Closness

#####5____

# The higher value indicates better relative position inside the transit network. 



#  ¿Orto?-NORMALIZED 
# {
#   "features": [
#     {
#         "Id": "1",  
#         "Centrality": 5,
#         "Closeness" : 8,
#         "EigenVect" : 2
#     },
#     {
#         "Id": "21",  
#         "Centrality": 7,
#         "Closeness" : 5,
#         "EigenVect" : 3
#     },{
#      }
#  ]
# }