from pickletools import uint1
from re import U
from turtle import pos
import networkx as nx
from networkx.algorithms import bipartite as bnx
from networkx.algorithms import node_classification as ncnx
import matplotlib.pyplot as plt
import stmMetro

def UniqueValues(name=str,disct=dict):
    UniqVal=[]
    for data in disct.keys():
        # print(DegCen[data])
        if disct[data] not in UniqVal:
            UniqVal.append(disct[data])
    # for u in UniqVal:
    #     print(u)
    # print("###############################################")
    # print("Name: ",name)
    # print("Length of Unique Values ",len(UniqVal)," of ",len(disct.keys()))
    

def networktest(NodeList:list,EdgeList:list,NodeData:dict,EdgeData:dict):
    G = nx.DiGraph()
    # print("Node list")
    for i,x in enumerate(NodeList):
        # print(i,"-",x,"\t",NodeData[x])
        G.add_node(x,pos=NodeData[x]['Pos'])
    # print("Edge list")
    for i,x in enumerate(EdgeList):
        # print(i,x,type(x))
        # print(x[0], x[1])
        # print(EdgeData[x[0], x[1]])
        G.add_edge(x[0], x[1], weight=EdgeData['time'][x[0], x[1]]) 

    print('###############################################')

    print(dir(nx.clique))
    # b=input('.................................')
    print('###############################################')

    ###################################################
    ####### Algorithms   ##############################
    ###################################################


    ####### Connectivity    ###############################
    # NA

    ####### K-components    ###############################
    # NA

    ####### Clique    ###############################
    # NA


    ####### Clustering    #############################
    AvCl=nx.average_clustering(G)       # Global

    ####### Distance Measures    ######################
    # DistMeas=nx.diameter(G)             #Not Applicable

    ####### Dominating Set    ###############################
    # MinWeigDomSet=nx.min_weighted_dominating_set(G, weight=None)  #Not Applicable

    ####### Matching  ###############################
    # MnMaxMatch=nx.min_maximal_matching(G) #Not Applicable

    ####### Ramsey    ###############################
    # Ramsey=nx.ramsey_R2(G)                  #Not Applicable

    ####### Steiner Tree    ###############################
    # MetClo=nx.metric_closure(G, weight='weight')


    ####### Assortativity    ###############################
    ####### Assortativity    ###############################
    DegAssoCoe=nx.degree_assortativity_coefficient(G, x='out', y='in', weight=None, nodes=None)      # Global

    # AtAssCoe=nx.attribute_assortativity_coefficient(G, 'weight', nodes=None)  #Not Applicable

    # NumAssoCoe=nx.numeric_assortativity_coefficient(G)       #Not Applicable

    DegPearCoe=nx.degree_pearson_correlation_coefficient(G)      # Global


    ####### Average neighbor degree       #################
    # AvNeiDeg=nx.average_neighbor_degree(G, weight="weight")


    ####### Average degree connectivity    ################
    AvDegCon=nx.average_degree_connectivity(G)  # Summmary

    # KNeNeig=nx.k_nearest_neighbors(G, source='in+out', target='in+out', nodes=None, weight=None)  # Summmary  

    ####### Mixing    ###############################
    # Example of Mapping tool for nodes                                                 #Not Applicable
    # mapping = {'male': 0, 'female': 1}                                                #Not Applicable
    # mix_mat = nx.attribute_mixing_matrix(G, 'gender', mapping=mapping)                #Not Applicable
    # NumMixMax=nx.numeric_mixing_matrix(G, 'weight', nodes=None, normalized=True, mapping=None) #Not Applicable
    DegMixDic=nx.degree_mixing_dict(G, x='out', y='in', weight=None, nodes=None, normalized=False)

    ####### Pairs  ###############################
    # nx.node_attribute_xy(G, "color")
    NodeDeg1=nx.node_degree_xy(G, x="in", y="out")
    NodeDeg2=nx.node_degree_xy(G, x="out", y="in")


    ####### Asteroidal    ###############################
    # ISFree=nx.is_at_free(G)
    # FInAsTrip=nx.find_asteroidal_triple(G)

    ###################################################
    ####### Centrality    ###############################
    ###################################################

    DegCen=nx.degree_centrality(G)
    IDegCen=nx.in_degree_centrality(G)
    ODegCen=nx.out_degree_centrality(G)

    ####### Eigenvector    ###############################
    EigenVect=nx.eigenvector_centrality(G, weight='weight') 
    Kats=nx.katz_centrality(G, alpha=0.1, beta=1.0, max_iter=1000, tol=1e-06, nstart=None, normalized=True, weight='weight')
    ####### Closeness    ###############################
    ClossN=nx.closeness_centrality(G,distance='weight')
    # IncClossN=nx.incremental_closeness_centrality(G, EdgeList, prev_cc=None, insertion=True, wf_improved=True) #NA
    # InfoCent=nx.information_centrality(G)

    ####### Current Flow Closeness   ##################
    # CuFlClCe=nx.current_flow_closeness_centrality(G)
    # InfoCent=nx.information_centrality(G)
    ####### Shortest Path| Betweenness    ##############
    BeCen=nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    BeCenSou=nx.betweenness_centrality_source(G, normalized=True, weight=None, sources=None)
    EdBeCen=nx.edge_betweenness_centrality(G, k=None, normalized=True, weight=None, seed=None)          


    ####### Current Flow Betweenness    ###############################
    # CurFloBeCen=nx.current_flow_betweenness_centrality(G,normalized=True, weight=None,  solver='full')
    # CommBeCen=nx.communicability_betweenness_centrality(G)

    # PromGroup=nx.prominent_group(G, 10, weight=None, C=None, endpoints=False, normalized=True, greedy=False)

    ####### Load    ###############################
    LoadCen=nx.load_centrality(G, v=None, cutoff=None, normalized=True, weight=None)
    EdLoadCen=nx.edge_load_centrality(G, cutoff=False)
    # Communicability=nx.communicability(G)

    ####### Harmonic Centrality   ###############################
    HarmCent=nx.harmonic_centrality(G, nbunch=None, distance=None, sources=None)


    Disp=nx.dispersion(G, u=None, v=None, normalized=True, alpha=1.0, b=0.0, c=0.0)

    ####### Reaching    ###############################
    GlobReachCen=nx.global_reaching_centrality(G, weight=None, normalized=True)  # GLobal

    ####### Percolation    ###############################
    # PerCen=nx.percolation_centrality(G, attribute='percolation', states=None, weight=None)

    ####### Second Order Centrality    ###############################
    # SecOrdCen=nx.second_order_centrality(G)

    ####### Trophic    ###############################
    TrophicLev=nx.trophic_levels(G, weight='weight')
    TrophicDif=nx.trophic_differences(G, weight='weight')
    TroIncoPar=nx.trophic_incoherence_parameter(G, weight='weight', cannibalism=False)       # Global

    ####### Chains    ###############################
    # ChainDecom=list(nx.chain_decomposition(G))


    ####### core_number    ###############################
    Cores=nx.core_number(G)
    K_Cores=nx.k_core(G)
    K_Shell=nx.k_shell(G)
    K_crust=nx.k_crust(G)
    K_corona=nx.k_corona(G,1)

    ####### Title H2    ###############################
    DAGancestor=nx.ancestors(G, 2)
    DAGdecendat=nx.descendants(G, 2)
    DAGtopological=list(nx.topological_sort(G))
    # DAGtopoSort=list(nx.all_topological_sorts(G)) # Not applicable

    ####### Distance Measures     #####################
    # barycenter=nx.center(G)
    dominating_set=nx.dominating_set(G)

    FlowHie=nx.flow_hierarchy(G)

    ####### Check for isolated node ###################
    IsIsolated=nx.is_isolate(G, 3)
    # Isolated=list(nx.isolates(G))
    Isolated=nx.number_of_isolates(G)

    ####### Link Analysis    ###############################
    Page=nx.pagerank(G, alpha=0.9)
    GoogleMatrix=nx.google_matrix(G, alpha=0.85, personalization=None, nodelist=None, weight='weight', dangling=None)
    Hits=nx.hits(G)
    AuthMat=nx.authority_matrix(G, nodelist=None)


    ####### Title H2    ###############################
    GGge=list (nx.all_pairs_lowest_common_ancestor(G))

    # Pred=ncnx.harmonic_function(G)
    Comp=nx.complement(G)


    Plannar=nx.check_planarity(G)
    Recep=nx.reciprocity(G, nodes=None)
    Regu=nx.is_regular(G)




    Assort=nx.degree_assortativity_coefficient(G)  # nope
    # EigenVectCent=nx.eigenvector_centrality_numpy(G, weight='weight', max_iter=50, tol=0)   # nope
    IsStrong=nx.is_strongly_connected(G)
    Hirarque=nx.flow_hierarchy(G, weight='weight')
    # ComBeCe=nx.eccentricity(G)
    # Diameter=nx.diameter(G)
    Eccen=nx.node_connectivity(G,s=36,t=97)

    
    AvShortPath=nx.average_shortest_path_length(G)  # Global
    FloydMarshal=nx.floyd_warshall(G, weight='weight')

    # Constrain=nx.constraint(G, nodes=None, weight=None)

    # esize = nx.effective_size(G)
    Wiener=nx.wiener_index(G, weight='weight')


    print('###############################################')
    print('######## End of calculations     ##############')
    print('###############################################')

    # print("TroIncoPar",TroIncoPar,end="\n"*3)
    # print("TrophicDif",list(TrophicDif),end="\n"*3)
    # print("NodeDeg1",list(NodeDeg1),end="\n"*3)
    # print("DegMixDic",DegMixDic,end="\n"*3)
    # print("DAGancestor",DAGancestor,end="\n"*3)
    # print("DAGdecendat",DAGdecendat,end="\n"*3)
    # print("DAGtopological",DAGtopological,end="\n"*3)
    # print("dominating_set",dominating_set,len(dominating_set),end="\n*3")
    # print("Page",Page,end="\n"*3)
    # print("GoogleMatrix",GoogleMatrix,end="\n"*3)
    # print("Hits",Hits,end="\n"*3)
    # print("AuthMat",AuthMat,end="\n"*3)
    # print("Comp",Comp,end="\n"*3)
    # print("Plannar",list(Plannar),end="\n"*3)
    # print("Recep",Recep,end="\n"*3)
    # print("Regu",Regu,end="\n"*3)
    # print("NodeDeg1",NodeDeg1,dir(NodeDeg1))
    # for i in NodeDeg1:
    #     print(i)
    # print("NodeDeg2",NodeDeg2,dir(NodeDeg2))
    # for i in NodeDeg2:
    #     print(i)
    # print("AllPairs",AllPairs,end="\n"*3)
    # print("Assort",Assort,end="\n"*3)
    # print("EigenVect",EigenVect,end="\n"*3)
    # print("Kats",Kats,end="\n"*3)
    # print("IsStrong",IsStrong,end="\n"*3)
    # print("Hirarque",Hirarque,end="\n"*3)
    # print("Eccen",Eccen,end="\n"*3)
    # print("Wiener",Wiener,end="\n"*3)
    # print("FloydMarshal",FloydMarshal,end="\n"*3) 
    # for m in FloydMarshal:
    #     print(m,FloydMarshal[m],type(FloydMarshal[m]),end="\n"*2)
    #     for n in FloydMarshal[m]:
    #         print("\t",n,type(n))


    # print("Wiener",Wiener,end="\n"*3)




    exitvar=False
    if exitvar:
        ExitPath="/mnt/e/GitHub/CAMMM-Tool_1.3/Scripts/Test/Exit/data.txt"
        f=open(ExitPath,"w")
        header=['Node','degree_centrality','in_degree_centrality','out_degree_centrality','eigenvector_centrality','katz_centrality','closeness_centrality','betweenness_centrality','betweenness_centrality_source','load_centrality','harmonic_centrality','dispersion','trophic_levels','core_number','pagerank','Hits']
        Text=",".join(header) +"\n"
        f.write(Text)
        for i,x in enumerate(NodeList):
            # print(x)
            # print(DegCen[x])
            # print(IDegCen[x])
            # print(ODegCen[x])
            # print(EigenVect[x])
            # print(Kats[x])
            # print(ClossN[x])
            # print(BeCen[x])
            # print(BeCenSou[x])
            # print(LoadCen[x])
            # print(HarmCent[x])
            # print(Disp[x])
            # print(TrophicLev[x])
            # print(Cores[x])
            # print(Page[x])
            # print(Hits[0][x])

            row=[x,DegCen[x],IDegCen[x],ODegCen[x],EigenVect[x],Kats[x],ClossN[x],BeCen[x],BeCenSou[x],LoadCen[x],HarmCent[x],Disp[x],TrophicLev[x],Cores[x],Page[x],Hits[0][x]]
            print(row,type(row))
            Text=""
            for i in row:
                Text+=str(i)+","
            Text+="\n"
            f.write(Text)

        #     print(row)
        f.close()
    # print("Kcomponenets",Kcomponenets)



    ###################################################
    ####### Plot graph   ##############################
    ###################################################
    # pos=nx.get_node_attributes(G,'pos')
    # nx.draw(G,pos)
    # plt.show()

if __name__=="__main__":
   

    Nodes,NodeData,Edges,EdgeData=stmMetro.GetMetroSTM()
    networktest(NodeList=Nodes,EdgeList=Edges,NodeData=NodeData,EdgeData=EdgeData)
    # print(dir(nx))


    
