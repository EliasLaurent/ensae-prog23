class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented.
    Attributes:
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor2, p2, d2), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges.
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges.
        Parameters:
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0


    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes.

        Parameters:
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1



    def comp(self,l,lb,lv):
        if lv==[]:
            return(l,lb)
        else:
            i=lv.pop()
            if lb[i-1]:
                lb[i-1]=False
                b=[a for (a,a2,a3) in self.graph[i]]
                l.append(i)
                lv+=b
            return(self.comp(l,lb,lv))

    def compco(self):
        n=self.nb_nodes
        lb=[True for i in range(n)]
        c=[]
        for k in range(1,n+1):
            l1,l2=self.comp([],lb,[k])
            lb=l2
            if l1!=[]:
                c.append(l1)
        return(c)

    def connected_components_set(self):
        n=self.nb_nodes
        lb=[True for i in range(n)]
        c=[]
        for k in range(1,n+1):
            l1,l2=self.comp([],lb,[k])
            lb=l2
            if l1!=[]:
                c.append(frozenset(l1))
        return(set(c))

    def min_power(self, src, dest):
        """
        Should return path, min_power.
        """
        max_pow = 0
        for n in self.nodes:
            for (_, power, _) in self.graph[n]:
                max_pow = max(max_pow, power)

        path = None
        a, b = 0, max_pow

        while b > a:
            pow = (a + b)//2
            path = self.get_path_with_power(src, dest, pow)
            if path is None:
                a = pow + 1
            else:
                b = pow
        if path is None :
            path=self.get_path_with_power(src, dest, a)
        return path, a

    def CCsommet(self,i):
        n=len(self.nodes)
        L=[]
        compconn=[0 for  _ in range(n)]
        compconn[i-1]=1
        L+=self.graph[i]
        while L!=[]:
            voisin = L.pop(0)
            if compconn[voisin[0]-1]==0 :
                compconn[voisin[0]-1]=1
                L+=self.graph[voisin[0]] #ajout dans L des voisins de voisin
        return(compconn)

    def CConnexes(self):
        L=[]
        for i in self.nodes:
            L.append(self.CCsommet(i))
        Lsansdouble = []
        for i in L :
            if i not in Lsansdouble:
                Lsansdouble.append(i)
        return(Lsansdouble)
#3
    def get_path_with_power(self,debut,fin,p):
        n=len(self.nodes)
        visit=[0 for _ in range(n)]
        cc=self.compco()
        for c in cc:
            if c.count(debut)==1:
                if c.count(fin)==0:
                    return None
        n=self.nb_nodes
        M=[[debut]]
        L=[debut]
        visit[debut-1]=1
        voisin=self.graph[debut]
        while L!=[]:
            m=[]
            L.pop(0)
            for trouple in voisin :
                if visit[trouple[0]-1]==0 and trouple[1]<=p:
                    m.append(trouple[0])
                    visit[trouple[0]-1]=1
                    L.append(trouple[0])
            if m!=[]:
                M.append(m)
            if L!=[]:
                voisin=self.graph[L[0]]
        chemin=[]
        ind=0
        for k in M:
            if fin in k:
                ind=M.index(k)
        b=fin
        for l in range(ind,-1,-1):
            if l==ind:
                chemin.append(fin)
            else:
                b=M[l][0]
                chemin.append(b)
        if len(chemin)>1:
            chemin.reverse()
            return(chemin)
        else:
            return(None)
    
    def get_path_with_powerQ5(self,p,t):
        debut,fin=t[0],t[1]
        for n in self.nodes:
            gn=[]
            for k in self.graph[n]:
                if k[1]<p:
                    gn.append(k)
            self.graph[n]=gn
        cc=self.compco()
        for c in cc:
            if c.count(debut)==1:
                if c.count(fin)==0:
                    return None
                else:
                    index_d=c.index(debut)
                    index_f=c.index(fin)
                    n=len(c)
                    l1=[float('inf') for i in range(n)]
                    l2=[0 for i in range(n)]
                    l1[index_d]=0
                    l2[index_d]=1
                    P=[debut]
                    prédécesseur=[0 for k in range(n)]
                    a=index_d
                    while l2!=[1 for i in range(n)]:
                        mind=float('inf')
                        indmin=n+1
                        for k in range(n):
                            if l2[k]==0 and l1[k]<mind:
                                mind=l1[k]
                                indmin=k
                        for arret in self.graph[c[k]]:
                            index_noeud=c.index(arret[0])
                            if l2[index_noeud]==0 and l1[index_noeud]>l1[k]+arret[2]:
                                l1[index_noeud]=l1[k]+arret[2]
                                prédécesseur[index_noeud]=k
                        l2[k]=1
                    chemin=[index_f]
                    while chemin[-1]!=index_d:
                        chemin.append(prédécesseur[chemin[-1]])
                    for noeud in chemin:
                        noeud=c[noeud]
                    return(chemin)

    def get_path_with_powerQ5_2(self,p,t):
    #pour que ce soit plus compréensible on construit le chemin de debut à fin mais le chemin renvoyé est de fin à debut
    #si on veut le vrai chemin on a juste a inverser debut et fin
        a=t[0]
        t[0]=t[1]
        t[1]=a
        print(self.get_path_with_powerQ5(p, t))


def graph_from_file(filename):
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g

"""g = graph_from_file("work/network.01.in")
print(g)
print(g.compco())"""
"""import time
#TD2
def temps_trajets(g):
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
    print(sum(T)/len(T))"""
def fus(l1,l2):
    l=[]
    k1=0
    k2=0
    n=len(l1)
    m=len(l2)
    while k1<n and k2<m:
        if l1[k1][0]<l2[k2][0]:
            l.append(l1[k1])
            k1=k1+1
        else:
            l.append(l2[k2])
            k2=k2+1
    while k1<n:
        l.append(l1[k1])
        k1=k1+1
    while k2<m:
        l.append(l2[k2])
        k2=k2+1   
    return(l)

def trifus(l):
    n=len(l)
    if n<2:
        return(l)
    else:
        m=n//2
        return(fus(trifus(l[m:]),trifus(l[:m])))

def kruskal(g):
    n=g.nb_nodes
    l=[]
    for n in g.nodes:
        for k in g.graph[n]:
            l.append([k[1],n,k[0]])
    print(l)
    l=trifus(l)
    print(l)
    c=[]
    g2=Graph(range(1,n+1))
    v=range(1,n+1)
    for a in l:
        if v[a[1]]!=v[a[2]]:
            g2.add_edge(a[1],a[2],a[0])
            g2.nb_edges+=1
            b=v[a[2]]
            for k in v:
                if k==b:
                    k=v[a[1]]
    return(g2)


"""from graph import Graph, graph_from_file#, temps_trajets
import time
data_path = "input/"
file_name = "network.02.in"
#t0=time.perf_counter()
g = graph_from_file(data_path + file_name)
print(kruskal(g))
print(g)"""