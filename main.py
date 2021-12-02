import networkx as nx 
import matplotlib.pyplot as plt
import re
from queue import Queue



# graf = {
#     "1.1": (0, ["1.2", "2.2"...])
#     "1.2": ('A')
# }

# 1. Inicjalni graf
# 2. Pravi bilo koji graf
# 3. Proveri pravila
# 4. Poteze
# 5. Minmax
# 6. Heuristika
# 7. Crta

#
#

#Guards
# https://stackoverflow.com/questions/66159432/how-to-use-values-stored-in-variables-as-case-patterns
# [A] guard is an arbitrary expression attached to a pattern and that must evaluate to a "truthy" value for the pattern to succeed.

def generisiGraf(m, n, nizZidova, listaPoz, pobedaX, pobedaY):
    graf = {}
    tmpM = m
    tmpN = n



    start = (1, 1)
    destinationQueue = Queue()
    visited = set()
    visited.add(f"{start[0]},{start[1]}")
    destinationQueue.put(f"{start[0]},{start[1]}")
    graf[f"{start[0]},{start[1]}"] = (0, [])

    while (not destinationQueue.empty()):
            node = destinationQueue.get()
            childList = list()
            nodeInt = node.split(',')
            for dx, dy in zip([1,-1,0,0, 1,1,-1,-1], [0,0,1,-1,1,-1,1,-1]):
                 g=(int(nodeInt[0]) + dx, int(nodeInt[1]) + dy)
                 if(g[0]>=1 and g[0]<=m and g[1]>=1 and g[1]<=n):
                    childList.append(f"{g[0]},{g[1]}")
                    graf[node]=(0, childList)
            for child in graf[node][1]:
                if child not in visited:
                     destinationQueue.put(child)
                     visited.add(child)


    graf[listaPoz[0]] = ('x', graf[listaPoz[0]][1])
    graf[listaPoz[1]] = ('x', graf[listaPoz[1]][1])
    graf[listaPoz[2]] = ('y', graf[listaPoz[2]][1])
    graf[listaPoz[3]] = ('y',  graf[listaPoz[3]][1])

    graf[pobedaX] = ('a', graf[pobedaX][1])
    graf[pobedaY] = ('b', graf[pobedaY][1])

    for edge in nizZidova:
        potege = list()
        for potega in graf[edge[0]][1]:

            if(potega != edge[1]):
                potege.append(potega)
        graf[edge[0]] = (graf[edge[0]][0], potege)
        potege = list()
        for potega in graf[edge[1]][1]:
            if(potega!=edge[0]):
                potege.append(potega)
        graf[edge[1]] = (graf[edge[1]][0], potege)
    return graf

def unesiZidove(graf, listaZidova, m, n):
    v_h = listaZidova[0][0].split(',')[0] == listaZidova[0][1].split(',')[0]
    
    if(re.search(f"{m},.", listaZidova[0][0]) and v_h):
        return
    if(re.search(f".,{n}", listaZidova[0][0]) and not v_h):
        return
    if(re.search(f"{m},.", listaZidova[0][1]) and v_h):
        return
    if(re.search(f".,{n}", listaZidova[0][1]) and not v_h):
        return

    obrisi(listaZidova,graf)
    print(listaZidova[0][0].split(',')[0])
    print(listaZidova[0][1].split(',')[1])

    if(listaZidova[0][0].split(',')[0]==listaZidova[0][1].split(',')[0]):
        pomocnoBrisanje(1,0,1,0, listaZidova, graf)
        pomocnoBrisanje(0,0,1,0, listaZidova, graf)
        pomocnoBrisanje(1,0,0,0, listaZidova, graf)


    else:
        pomocnoBrisanje(0,1,0,1, listaZidova, graf)
        pomocnoBrisanje(0,0,0,1, listaZidova, graf)
        pomocnoBrisanje(1,0,-1,1, listaZidova, graf)

def pomocnoBrisanje(a, b, c, d, listaZidova, graf):
    x1 = list(listaZidova[0][0].split(','))
    y1 = list(listaZidova[0][1].split(','))
    x1[0] = int(x1[0]) + a
    x1[1] = int(x1[1]) + b
    y1[0] = int(y1[0]) + c
    y1[1] = int(y1[1]) + d
    novaLista = [(str(x1[0]) + ',' + str(x1[1]), str(y1[0]) + ',' + str(y1[1]))]
    obrisi(novaLista, graf)


def obrisi(listaZidova, graf):
    for edge in listaZidova:
        potege = list()
        for potega in graf[edge[0]][1]:

            if(potega != edge[1]):
                potege.append(potega)
        graf[edge[0]] = (graf[edge[0]][0], potege)
        potege = list()
        for potega in graf[edge[1]][1]:
            if(potega!=edge[0]):
                potege.append(potega)
        graf[edge[1]] = (graf[edge[1]][0], potege)

def SetujPocetnoStanje(velicinaX, velicinaY, listaIgraca, pobedaX, pobedaY):
    return generisiGraf(velicinaX, velicinaY, [], listaIgraca, pobedaX, pobedaY)

def pomeriIGraca(graf,m,n, startPoz, endPoz, naPotezu, pobeda, px, py):
    igrac = graf[startPoz][0]
    if(igrac!=naPotezu):
        return

    endPozInt = (int(endPoz.split(',')[0]), int(endPoz.split(',')[1]))
    startPozInt = (int(startPoz.split(',')[0]), int(startPoz.split(',')[1]))
    if(endPozInt[0]>=1 and endPozInt[0]<=m and endPozInt[1]>=0 and endPozInt[1]<=n):
        if validacijaPokreta(graf, startPozInt, endPozInt, endPoz):
                if endPoz==px and naPotezu == "x":
                    pobeda = True
                elif endPoz == py and naPotezu=='y':
                    pobeda = True
                graf[startPoz] = (0, graf[startPoz][1])
                graf[endPoz] = (igrac, graf[endPoz][1])
    return pobeda

def validacijaPokreta(graf, trenutno, ciljno, endpoz):

    if(graf[endpoz][0] == "x" or graf[endpoz][0] == "y"):
            return False


    for dx, dy in zip([2, -2, 0, 0], [0, 0, 2, -2]):
        g = (trenutno[0] + dx, trenutno[1] + dy)
        if (g == ciljno):
            return True

    for tx, ty in zip([1, -1, 1, -1], [1, -1, -1 , 1]):
        p = (trenutno[0] + tx, trenutno[1] + ty)
        if(p==ciljno):
            return True

    return False

def gameLoop():
    pobeda = False
    pobenik = None
    trenutniIgrac = "x"
    startnaPoz = None
    pobedaX = "3,4"
    pobedaY = "5,5"
    graf = SetujPocetnoStanje(6, 6, ["1,1","2,2", "3,3", "4,4"], "3,4", "5,5")

    while not pobeda:
        print("Selektujte polje sa igracem koga pomerate: ")
        startnaPoz = input()

        print("Na koje polje: ")
        destinacija = input()

        print("Unesite gde postavljate zid: ")
        zid1 = input()
        zid2 = input()

        if not re.search(f"[1-6],[1-6]", zid1):
            print("Unesite pravilno polje!")
            continue

        if not re.search(f"[1-6],[1-6]", zid2):
            print("Unesite pravilno polje!")
            continue

        if not re.search(f"[1-6],[1-6]", startnaPoz):
            print("Unesite pravilno polje!")
            continue

        if not re.search(f"[1-6],[1-6]", destinacija):
            print("Unesite pravilno polje!")
            continue

        pobeda = pomeriIGraca(graf, 6,6, startnaPoz, destinacija, trenutniIgrac, pobeda , pobedaX, pobedaY)
        unesiZidove(graf, [(zid1, zid2)] , 6, 6)
        trenutniIgrac = "x" if trenutniIgrac=="y" else "y"

        lista = {}
        for i in graf:
            lista[i] = (graf[i][1])
        g = nx.Graph(lista)
        nx.draw(g, with_labels=True)
        plt.show()
        print("nesto")

    print("Pobednik je : "  + "x" if trenutniIgrac=="y" else "x")


# listaIgraca = ["1,1","2,2", "3,3", "4,4"]
# listaZidova = []
# pobedaX = "3,1"
# pobedaY = "4,2"
# gra = generisiGraf(4, 4, listaZidova, listaIgraca, pobedaX, pobedaY)


gameLoop()


print("Kraj!")