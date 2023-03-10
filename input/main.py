from graph import Graph, graph_from_file#, temps_trajets
import time
data_path = "input/"
file_name = "network.02.in"
#t0=time.perf_counter()
g = graph_from_file(data_path + file_name)
#q10
"""g.min_power(2,1)
print(time.perf_counter()-t0)
print(g.graph[1])
i=1
s=0
T=[]
while s<min(3,g.nb_edges):
    if len(g.graph[i])==0:
        i=i+1
    else:
        t0=time.perf_counter()
        k=0
        for lien in g.graph[i]:
            g.min_power(i,lien[0])
            k=k+1
        t1=time.perf_counter()
        T.append((t1-t0)/k)
print(sum(T)/len(T))
print(T)"""
v=range(1,10+1)
print(v[4])