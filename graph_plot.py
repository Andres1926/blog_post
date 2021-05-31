from pulp import *
import pandas as pd
import numpy as np
import  networkx as nx
import matplotlib.pyplot as plt
import csv
from tqdm import tqdm_gui
from tqdm import tqdm

import sys 
import time


start_time = time.time()

# path of the folder containing the edlist files
inPath ="/test-files"

# path of the folder that will contain the results 
outPath ="/test-files/ILP-output"

for root,dirs,files in os.walk(inPath):
    for file in files:
        if file.endswith(".edgelist"):
            inputPath = os.path.join(inPath, file)
            pr=inputPath
            name=os.path.splitext(file)[0]
            print(name)

            #G = nx.read_edgelist(pr+'.edgelist')
            G = nx.read_adjlist(pr)
            #G = nx.read_edgelist("test"+str(i)+".edgelist") # load graph

            #graph = nx.random_tree(tr, seed=1)
            #nx.write_edgelist(graph, "test"+str(tr)+".edgelist")
            #G = nx.read_edgelist("test"+str(tr)+".edgelist")
            #create a list of node items
            Nodes_l = nx.nodes(G)

            # define the problem 

            prob = LpProblem("MDS_problem",LpMinimize)

            #create variables

            Node_vars = LpVariable.dicts("nd", Nodes_l,cat='Binary')

            # sum of all nodes cat='Binary' 0,None,LpInteger

            prob += lpSum([Node_vars])

            # Create constrains
            for i in Nodes_l:
                prob += lpSum([Node_vars[f] for f in list(G.adj[i])]) >= 1.0 - Node_vars[i]
                
            #print(prob) if need to evaluate the constraints 

            #sove the problem 

            prob.solve()

            # The status of the solution is printed to the screen

            print("Status:", LpStatus[prob.status])

            # Organizing the MDS set

            MDS_set=[]
            non_MDS=[]



            for v in prob.variables():
                if v.varValue>0:
                    vlist=v.name[3:30]
                    MDS_set.append(vlist)
                    
                elif v.varValue==0:
                    hlist=v.name[3:30]
                    non_MDS.append(hlist)
                            

            # Deterministic solution lengths
            mds_o = value(prob.objective)
            Tnd = len(Nodes_l)
            Dnd = len(MDS_set)
            
            print('Total nodes : ', Tnd)
            print('Minimum dominating nodes : ', Dnd)
            

            # print sets if requiere probing

            print('MDS set : ', MDS_set)
            #nx.write_edgelist(G.subgraph(MDS_set), "test"+pr+".edgelist")
            #print('Critical Set ILP:',C_MDS_ILP)
            #print('Redundant Set ILP:',R_MDS)
            #print('Intermiten Set ILP:',I_MDS)
            
            pos = nx.spring_layout(G)
            options = {'node_color': 'blue','node_size': 20,'width': 0.5}
            plt.subplot(111)
            nx.draw(G,pos=pos, **options)
            #nx.draw(G.subgraph(MDS_set), pos=pos, node_size = 12, node_color='orange')
            
            plt.savefig(outPath+'/MDS_02'+name+'.pdf')
            #plt.show()
            #plt.close()

            with open(outPath+'/MDS_'+name+'.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter =' ')
                writer.writerow(['MDS Protein'])
                writer.writerows([i for i in MDS_set])


            print("Running time: --- %s seconds ---" % (time.time() - start_time))
