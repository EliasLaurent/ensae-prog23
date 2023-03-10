from graph import Graph, graph_from_file
import time
data_path = "input/"
file_name = "network.02.in"
t0=time.perf_counter()
g = graph_from_file(data_path + file_name)
#q10
g.min_power(2,1)
print(time.perf_counter()-t0)
for i in g.nodes():
    print(g.graph[i])