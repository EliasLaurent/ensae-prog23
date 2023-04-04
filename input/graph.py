class Graph:

    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []


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
        self.edges += [(node1,node2,power_min)]
    

    def comp(self,visité,cc,i):
        if visité[i-1]:
            cc.append(i)
            visité[i-1]=False
            voisins=[a for (a,a2,a3) in self.graph[i]]
            for k in voisins:
                self.comp(visité,cc,k)

#la fonction compco renvoie les composantes connexes sous forme de liste de listes
#et ne sert qu'à petre utilisée dans d'autres fonctions ultérieures
    def compco(self):
        n=self.nb_nodes
        visité=[True for i in range(n)]
        c=[]
        for k in range(1,n+1):
            cc=[]
            self.comp(visité,cc,k)
            if cc!=[]:
                c.append(cc)
        return(c)


#la fonction connected_components_set renvoie les composantes connexes
#au format voulu i.e. en set de frozensets
    def connected_components_set(self):
        n=self.nb_nodes
        visité=[True for i in range(n)]
        c=[]
        for k in range(1,n+1):
            cc=[]
            self.comp(visité,cc,k)
            if cc!=[]:
                c.append(frozenset(cc))
        return(set(c))


    def min_power(self, debut, fin):
        #retourne chemin, puissance minimum
        max_pow=0
        for n in self.nodes:
            for (_, power, _) in self.graph[n]:
                max_pow = max(max_pow, power)
        chemin=None
        a,b=0,max_pow
        while b > a:
            pow=(a+b)//2
            chemin=self.get_path_with_power(debut, fin, pow)
            if chemin is None:
                a=pow+1
            else:
                b=pow
        if chemin is None :
            chemin=self.get_path_with_power(debut, fin, a)
        return(chemin,a)

#autre methode pour avoir les composantes connexes sans recursivite
#ne pas prendre en compte
    """def CCsommet(self,i):
        n=len(self.nodes)
        L=[]
        compconn=[0 for  _ in range(n)]
        compconn[i-1]=1
        L+=self.graph[i]
        while L!=[]:
            voisin = L.pop(0)
            if compconn[voisin[0]-1]==0 :
                compconn[voisin[0]-1]=1
                L+=self.graph[voisin[0]]
        return(compconn)


    def CConnexes(self):
        L=[]
        for i in self.nodes:
            L.append(self.CCsommet(i))
        Lsansdouble = []
        for i in L :
            if i not in Lsansdouble:
                Lsansdouble.append(i)
        liste_compconn=[]
        for compconn in Lsansdouble:
            reelcompconn=[]
            for i in range(len(compconn)):
                if compconn[i]==1:
                    reelcompconn.append(i+1)
            liste_compconn.append(reelcompconn)
        return(liste_compconn)"""

    def get_path_with_power(self,debut,fin,p):
        n=len(self.nodes)
        visit=[0 for _ in range(n)]
        cc=self.CConnexes()
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


    def path_dijkstra(self,p,t):
        debut,fin=t[0],t[1]
        for n in self.nodes:
            gn=[]
            for k in self.graph[n]:
                if k[1]<=p:
                    gn.append(k)
            self.graph[n]=gn
            #on ne prend  que en compte les arete de poid inferieur à p
        cc=self.compco()
        for c in cc:
            #on cherche si une composante conexe avec nos 2 sommets existe
            if c.count(debut)==1:
                if c.count(fin)==0:
                    return None
                else:
                    #on s'inspire de l'algorithme de dijkstra
                    index_d=c.index(debut)
                    index_f=c.index(fin)
                    n=len(c)
                    l1=[float('inf') for i in range(n)]
                    l2=[0 for i in range(n)]
                    l1[index_d]=0
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
                        for arete in self.graph[c[indmin]]:
                            index_noeud=c.index(arete[0])
                            if l2[index_noeud]==0 and l1[index_noeud]>l1[indmin]+arete[2]:
                                l1[index_noeud]=l1[indmin]+arete[2]
                                predecesseur[index_noeud]=indmin
                        l2[indmin]=1
                    chemin=[index_f]
                    while chemin[-1]!=index_d:
                        chemin.append(predecesseur[chemin[-1]])
                    #on réindex par rapport au sommet du vrai graphe et non de la composante 
                    for k in range(len(chemin)):
                        chemin[k]=c[chemin[k]]
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



#met 15 ans à s'executer, trop long...
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
        while s<min(5,g.nb_edges):
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
    l=trifus(l)
    c=[]
    g2=Graph(range(1,n+1))
    v=[k for k in range(1,n+1)]
    #les sommets n1 et n2 sont reliés si v[n1]=v[n2], au debut aucun est relié
    for a in l:
        if v[a[1]-1]!=v[a[2]-1]:
            g2.add_edge(a[1],a[2],a[0])
            b=v[a[2]-1]
            for k in range(n):
                if v[k]==b:
                    v[k]=v[a[1]-1]
    return(g2)

"""test : import time
data_path = "input/"
file_name = "network.05.in"
#t0=time.perf_counter()
g = graph_from_file(data_path + file_name)"""
 
def Q14(graph,n1,n2):
    g=kruskal(graph)
    parents={}#dictionnaire qui a un noeud associe le noeud antérieur et le puissance necessaire
    profondeurs={1:0}#associe a un noeud sa profondeur par rapport a la racine
    def remplissage_dictonnaire(n):
        if not(n1 in parents and n2 in parents):
            for arete in g.graph[n]:
                if not(arete[0] in parents):
                    parents[arete[0]]=(n,arete[1])
                    profondeurs[arete[0]]=profondeurs[n]+1
                    remplissage_dictonnaire(arete[0])
    remplissage_dictonnaire(1)
    #on prend le sommet 1 comme la racine de l'arbre
    chemin=[n1,n2]
    poids=[]
    #on veut se ramener a un probleme ou nos 2 noeuds sont a la meme profondeur
    while profondeurs[n1]!=profondeurs[n2]:
        if profondeurs[n1]<profondeurs[n2]:
            if parents[n2][0]!=n1:
                chemin.insert(1,parents[n2][0])
            poids.append(parents[n2][1])
            n2=parents[n2][0]
        elif profondeurs[n1]>profondeurs[n2]:
            if parents[n1][0]!=n2:
                chemin.insert(-1,parents[n1][0])
            poids.append(parents[n1][1])
            n1=parents[n1][0]
    #une fois que nos deux noeuds sont a la meme profondeur on a juste a remonter simultanément dans l'arbre jusqu'a trouver un ancetre commun
    while n1!=n2:
        k=chemin.index(n1)
        if parents[n2][0]!= parents[n1][0]:
            chemin.insert(k+1,parents[n2][0])
            chemin.insert(k+1,parents[n1][0])
        else:
            chemin.insert(k+1,parents[n1][0])
        poids.append(parents[n2][1])
        poids.append(parents[n1][1])
        n1=parents[n1][0]
        n2=parents[n2][0]
    p=max(poids)
    return(p,chemin)

#test : print(Q14(g, 2, 1))

#Q18
def routes_from_file(x):
    with open("input/routes."+str(x)+".in", "r") as file:
        n = int(file.readline())
        L=[]
        for k in range(n):
            route = list(map(int, file.readline().split()))
            debut,fin,profit = route
            L.append([debut,fin,profit])
    g=graph_from_file("input/network."+str(x)+".in")
    for route in L:
        for arete in g.edges:
            if (debut==arete[0] and fin==arete[1]) or (debut==arete[1] and fin==arete[0]):
                route.append(arete[2])
    return(L)

g=graph_from_file("input/network.1.in")
"""print(routes_from_file(1))
print(g.edges[1][1])"""
def trucks_from_file(filename):
    with open(filename, "r") as file:
        n = int(file.readline())
        L=[]
        for k in range(n):
            truck = list(map(int, file.readline().split()))
            pow,cout = truck
            L.append([pow,cout])
    return(L)

#test : print(trucks_from_file("input/trucks.2.in"))

"""def cout_route(route):
    pow=route[2]"""
#q18 a chauque trajet ona ssocie le prix min du camion qui peut le faire puis on resoud programmation dynamique

def q18(graph,camions,trajets,budjet):
    #camions est une liste de doublet(puissance,prix)
    #trajet est une liste de triplet(debut,fin,profit)
    l=[]
    for t in trajets:
        pmin,chemin=Q14(graph,t[0],t[1])
        l.append((pmin,chemin,t[2]))
    l2=[]
    for chemin in l:
        prixmin=np.inf
        indice=np.inf
        for k in range(len(camions)):
            if camions[k][0]>=chemin[0]:
                if camions[k][1]<prixmin:
                    prixmin=camions[k][1]
                    indice=k
        l2.append(prixmin,chemin[2],k,chemin[1])
    return(l2)
    #l2 est une liste de quadruplet de la forme(prix,profit,camion,chemin)
    #on doit maintenant resoudre le probleme du sac a dos sur les 2 premier element de chaque quadruplet​
print(q18(g,trucks_from_file("input/trucks.1.in"),routes_from_file(1),25000000))

import numpy as np

#q18 a chaque trajet on associe le prix min du camion qui peut le faire puis on resoud programmation dynamique
def q18progdynamique(graph,camions,trajets,budjet):
    #camions est une liste de doublet(puissance,prix)
    #trajets est une liste de triplet(debut,fin,profit)
    l=[]
    for t in trajets:
        pmin,chemin=Q14(graph,t[0],t[1])
        l.append((pmin,chemin,t[2]))
    l2=[]
    for chemin in l:
        prixmin=np.inf
        indice=np.inf
        for k in range(len(camions)):
            if camions[k][0]>=chemin[0]:
                if camions[k][1]<prixmin:
                    prixmin=camions[k][1]
                    indice=k
        l2.append(prixmin,chemin[2],indice,chemin[1])
    #l2 est une liste de quadruplet de la forme (prix,profit,camion,chemin) de chaque trajet
    #on doit maintenant resoudre le probleme du sac a dos sur les 2 premiers elements de chaque quadruplet
    #je suppose que le budjet, les prix et les profits sont des entiers
    T=[[(0,[]) for i in range(budjet+1)] for i in range(len(l2)+1)]
    """"T[i][j] represente le profit optimum et la liste des trajets a prendre
    si on peut faire que les i premiers trajets avec un budjet de j"""
    for i in range(1,len(l2)+1):
        for b in range(budjet+1):
            #on utilise la formule de recurrence
            if b>l2[i][0]:
                if T[i-1][b][0]>=T[i-1][b-l2[i][0]][0]+l2[i][1]:
                    T[i][b]=T[i-1][b]
                else:
                    T[i][b]=(T[i-1][b-l2[i][0]][0]+l2[i][1],T[i-1][b-l2[i][0]][1]+[i])
            else:
                T[i][b]=T[i-1][b]
    opti=T[len(l2)+1][budjet+1][1]
    sol=[]
    for trajet in opti:
        sol.append(l2[trajet][2],trajets[trajet])
    return(sol)

def q18greedy(graph,camions,trajets,budjet):#la solution retournée n'est pas forcement optimale
    l=[]
    for t in trajets:
        pmin,chemin=Q14(graph,t[0],t[1])
        l.append((pmin,chemin,t[2]))
    l2=[]
    for chemin in l:
        prixmin=np.inf
        indice=np.inf
        for k in range(len(camions)):
            if camions[k][0]>=chemin[0]:
                if camions[k][1]<prixmin:
                    prixmin=camions[k][1]
                    indice=k
        l2.append(prixmin,chemin[2],indice,chemin[1])
    #l2 est une liste de quadruplet de la forme (prix,profit,camion,chemin) de chaque trajet
    #on va maintenant trier les trajet de maniere decroissante en fonction de leur rapport profit/prix
    lefficacite=[]
    for i in range(len(l2)):
        lefficacite.append((i,l2[i][1]/l2[i][0]))
    #on tri l'efficacite en fonction de son 2eme parametre
    def triFusion(L):
        if len(L) == 1:
            return L
        else:
            return fusion( triFusion(L[:len(L)//2]) , triFusion(L[len(L)//2:]) )

    def fusion(A,B):
        if len(A) == 0:
            return B
        elif len(B) == 0:
            return A
        elif A[0][1]>= B[0][1]:
            return [A[0]] + fusion( A[1:] , B )
        else:
            return [B[0]] + fusion( A , B[1:] )
    lefficacite=triFusion(lefficacite)
    #on fait en priorite les trajets avec le meilleur rapport profit/cout
    b=budjet
    sol=[]
    for trajet in lefficacite:
        if l2[trajet[0]][0]<=b:
            sol.append(l2[trajet][2],trajets[trajet])
            b-=l2[trajet[0]][0]
    return(sol)