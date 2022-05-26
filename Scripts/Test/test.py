import networkx as nx
import matplotlib.pyplot as plt



def networktest(NodeList=list,EdgeList=list,NodeData=dict,EdgeData=dict):
    G = nx.DiGraph()
    for i,x in enumerate(NodeList):
        print(i,"-",x,"\t",NodeData[x])
        G.add_node(x)
    print("Edge list")
    for i,x in enumerate(EdgeList):
        print(i,x)
        G.add_edge(x[0], x[1], weight=EdgeData[i]['weight']) 


    DegCen=nx.degree_centrality(G)
    print(DegCen)
    nx.draw(G)
    plt.show()

if __name__=="__main__":
    List=[1,2,3,4,5,6,7,8,
    11,12,13,14,15,16,17,
    21,22,23,25,27
    ]
    Edges=[[1,2],
    [2,3],
    [3,4],
    [4,5],
    [5,6],
    [6,7],
    [7,8],
    [11,12],
    [12,13],
    [13,14],
    [14,15],
    [15,16],
    [16,17],
    [21,22],
    [22,23],
    [23,4],
    [4,25],
    [25,16],
    [16,27],
    ]
    DataDict={}
    DataDict[1]={"num":9}
    DataDict[2]={"num":9}
    DataDict[3]={"num":9}
    DataDict[4]={"num":9}
    DataDict[5]={"num":9}
    DataDict[6]={"num":9}
    DataDict[7]={"num":9}
    DataDict[8]={"num":9}
    DataDict[11]={"num":9}
    DataDict[12]={"num":9}
    DataDict[13]={"num":9}
    DataDict[14]={"num":9}
    DataDict[15]={"num":9}
    DataDict[16]={"num":9}
    DataDict[17]={"num":9}
    DataDict[21]={"num":9}
    DataDict[22]={"num":9}
    DataDict[23]={"num":9}
    DataDict[24]={"num":9}
    DataDict[25]={"num":9}
    DataDict[27]={"num":9}

    EdgeData={}
    EdgeData[0]={'weight':112}
    EdgeData[1]={'weight':90}
    EdgeData[2]={'weight':150}
    EdgeData[3]={'weight':105}
    EdgeData[4]={'weight':128}
    EdgeData[5]={'weight':190}
    EdgeData[6]={'weight':50}
    EdgeData[7]={'weight':75}
    EdgeData[8]={'weight':125}
    EdgeData[9]={'weight':175}
    EdgeData[10]={'weight':85}
    EdgeData[11]={'weight':56}
    EdgeData[12]={'weight':110}
    EdgeData[13]={'weight':185}
    EdgeData[14]={'weight':68}
    EdgeData[15]={'weight':95}
    EdgeData[16]={'weight':143}
    EdgeData[17]={'weight':256}
    EdgeData[18]={'weight':210}
    EdgeData[19]={'weight':215}
    EdgeData[20]={'weight':168}
    EdgeData[21]={'weight':195}
    EdgeData[22]={'weight':55}
    EdgeData[23]={'weight':145}
    networktest(NodeList=List,EdgeList=Edges,NodeData=DataDict,EdgeData=EdgeData)
    # print(dir(nx))


    
