import networkx as nx
import matplotlib.pyplot as plt



G=nx.DiGraph()

# NodeList=['N1',"N2","N3","N4","N5","N6","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18"]

Pos={}
Pos["N1"]=(1,5)
Pos["N2"]=(2,5)
Pos["N3"]=(3,5)
Pos["N4"]=(4,5)
Pos["N5"]=(1,4)
Pos["N6"]=(2,4)
Pos["N7"]=(3,4)
Pos["N8"]=(1,3)
Pos["N9"]=(2,3)
Pos["N10"]=(3,3)
Pos["N11"]=(1,2)
Pos["N12"]=(2,2)
Pos["N13"]=(3,2)
Pos["N14"]=(4,2)
Pos["N15"]=(1,1)
Pos["N16"]=(2,1)
Pos["N17"]=(3,1)
Pos["N18"]=(4,1)

G.add_nodes_from(Pos.keys())

G.add_edge("N1","N5", weight=1)
G.add_edge("N5","N8", weight=1)
G.add_edge("N8","N11", weight=1)
G.add_edge("N11","N15", weight=1)
G.add_edge("N1","N6", weight=1)
G.add_edge("N8","N9", weight=1)
G.add_edge("N15","N16", weight=1)
G.add_edge("N2","N1", weight=1)
G.add_edge("N2","N6", weight=1)
G.add_edge("N6","N2", weight=1)
G.add_edge("N6","N9", weight=2)
G.add_edge("N9","N6", weight=1)
G.add_edge("N9","N10", weight=1)
G.add_edge("N12","N9", weight=1)
G.add_edge("N12","N15", weight=1)
G.add_edge("N12","N16", weight=3)
G.add_edge("N16","N12", weight=1)
G.add_edge("N16","N15", weight=1)
G.add_edge("N16","N17", weight=1)
G.add_edge("N3","N2", weight=1)
G.add_edge("N3","N4", weight=1)
G.add_edge("N7","N3", weight=1)
G.add_edge("N10","N7", weight=1)
G.add_edge("N10","N13", weight=1)
G.add_edge("N13","N12", weight=1)
G.add_edge("N13","N17", weight=1)
G.add_edge("N17","N18", weight=1)
G.add_edge("N4","N3", weight=1)
G.add_edge("N14","N13", weight=1)
G.add_edge("N18","N14", weight=1)




print(Pos)

# nx.draw_networkx_nodes(G,pos=Pos,with_labels=True)
        # nx.draw_networkx_edges(Gr['G'],pos=Gr['Node_Properties']['Pos'],edge_color=Gr['Edge_Color'])
        # ###############################################################################
        # plt.tick_params(axis='both',labelcolor='white')
        # Coords=GetcXcY(List_Coords=Gr['Node_Properties']['Pos'])
        # print(Coords)
        # # b=input()
        # Info=nx.info(Gr['G'])+"\nNetwork Density: "+str(nx.density(Gr['G']))
        # print(Info,type(Info))
        # plt.text(Coords['AvgX'], Coords['MaxY']+1300, Gr['Node_Properties']['FileName'])
        # plt.text(Coords['MinX'], Coords['MinY'],Info)


# print(G.neighbors("N9"))
print(G.degree())
print("degree_centrality",nx.degree_centrality(G))
print("betweenness_centrality",nx.betweenness_centrality(G))
print("closeness_centrality",nx.closeness_centrality(G))
print("eigenvector_centrality",nx.eigenvector_centrality(G))

nx.draw(G, with_labels=True,pos=Pos)
plt.show()

Dc=nx.degree_centrality(G)
Bc=nx.betweenness_centrality(G)
nx.closeness_centrality(G)
nx.eigenvector_centrality(G)