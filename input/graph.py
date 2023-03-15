class Graph:

    def __init__(self, nodes=[]):
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
        max_pow=0
        for n in self.nodes:
            for (_, power, _) in self.graph[n]:
                max_pow = max(max_pow, power)
        path=None
        a,b=0,max_pow
        while b > a:
            pow=(a+b)//2
            path=self.get_path_with_power(src, dest, pow)
            if path is None:
                a=pow+1
            else:
                b=pow
        if path is None :
            path=self.get_path_with_power(src, dest, a)
        return(path,a)

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

    def dijkstra(self,p,t):
        debut,fin=t[0],t[1]
        for n in self.nodes:
            gn=[]
            for k in self.graph[n]:
                if k[1]<=p:
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
                    predecesseur=[0 for k in range(n)]
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
                                predecesseur[index_noeud]=k
                        l2[k]=1
                    chemin=[index_f]
                    while chemin[-1]!=index_d:
                        chemin.append(predecesseur[chemin[-1]])
                    for noeud in chemin:
                        noeud=c[noeud]
                    chemin.reverse()
                    return(chemin)



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


import time
def q10():
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
        while s<min(3,g.nb_edges):
            route=routes[i]
            t0=time.perf_counter()
            g.min_power(route[0],route[1])
            s=s+1
            t1=time.perf_counter()
            T.append(t1-t0)
        return(sum(T)/len(T))

    L=[]
    for k in range(1,11):
        data_path = "input/"
        file_name1 = "network."+str(k)+".in"
        file_name2 = "routes."+str(k)+".in"
        g = graph_from_file(data_path + file_name1)
        routes=routes_from_file(data_path + file_name2)
        L.append(temps_trajets(g,routes))
    return(sum(L))
#renvoie RecursionError: maximun recusrion depth exceeded in comparison...
#La méthode m'a l'air pourtant bonne


#on implemente le trifusion pour pouvoir l'utiliser dans kruskal (permet de trier les arete par ordre croissant de puissance)
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
    v=[k for k in range(1,n+1)]
    for a in l:
        print(v)
        if v[a[1]]!=v[a[2]]:
            g2.add_edge(a[1],a[2],a[0])
            b=v[a[2]]
            for k in range(n):
                if v[k]==b:
                    v[k]=v[a[1]]
    return(g2)
