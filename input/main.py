from graph import Graph, graph_from_file, kruskal, q10
import time
data_path = "input/"
file_name = "network.02.in"
t0=time.perf_counter()
g = graph_from_file(data_path + file_name)
#q10
"""i=1
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
            s=s+1
        t1=time.perf_counter()
        T.append((t1-t0)/k)
print(sum(T)/len(T))"""
#print(q10())
"""def test():
    def routes_from_file(filename):
        with open(filename, "r") as file:
            n = int(file.readline())
            L=[]
            for k in range(n):
                route = list(map(int, file.readline().split()))
                debut,fin,power_min = route
                L.append([debut,fin,power_min]) # will add dist=1 by default
        return(L)

    def temps_trajets(g,routes):
        i=0
        s=0
        T=[]
        while s<min(5,g.nb_edges):
            route=routes[s]
            t0=time.perf_counter()
            g.min_power(route[0],route[1])
            s=s+1
            t1=time.perf_counter()
            T.append(t1-t0)
        return(sum(T)/len(T))
    routes=routes_from_file(data_path+"routes.2.in")
    print(temps_trajets(g,routes))
test()"""
#print(g.compco())
print(g.path_dijkstra(5, [1,2]))
print(g.compco())