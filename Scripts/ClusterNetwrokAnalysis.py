## This Calculates 
# #CAMMMM2023
#40
import ast
import networkx as nx
import matplotlib.pyplot as plt

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

    G = nx.DiGraph()

    for node in ListNodes:
        if ShowProcess: print(node[ 'properties']['Id'])
        id=node[ 'properties']['Id']
        weigth=CalculateHubWeight(MetroData=node[ 'properties']['MetroData'],
        RailData=node[ 'properties']['RailData'],
        BusData=node[ 'properties']['BusData'],
        TramData=node[ 'properties']['TramData'])

        if ShowProcess: print("id",id)
        if ShowProcess: print("weigth",weigth)
        if ShowProcess: print("\n"*3,node[ 'properties'].keys())
        G.add_node(id,weigth=weigth)
        # if ShowProcess: b=input('.................................')

    G.add_edges_from(ListEdges)

    # nx.draw_networkx_nodes(G)
    # nx.nx.draw_networkx_edges(G)
    print(list(G.edges))
    if ShowProcess: b=input('.................................')

    nx.draw(G)
    plt.show()
    if ShowProcess: b=input('.................................')

    return None

if __name__=="__main__":
    PathLinks="/mnt/e/Github/CAMMM-Tool_1.3/Output/Links.txt"
    PathNodes="/mnt/e/Github/CAMMM-Tool_1.3/Salida3_5.json"

    ClusterLink=ReadLinks(Path=PathLinks)
    ClusterNodes=ReadNodes(Path=PathNodes)
    # print(type(ClusterNodes['features']))
    # print(len(ClusterNodes['features']))
    # print(ClusterNodes['features'][0][ 'properties'])
    CreateNetwork(ListNodes=ClusterNodes['features'],ListEdges=ClusterLink,ShowProcess=True)

    # print(type(ClusterLink))
    # print(len(ClusterLink))
    # print(ClusterLink[0])
