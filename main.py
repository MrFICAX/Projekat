from ast import If
from operator import truediv
from tracemalloc import start
import networkx as nx
import matplotlib.pyplot as plt
import re
from queue import PriorityQueue, Queue
import random
import math


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

# Guards
# https://stackoverflow.com/questions/66159432/how-to-use-values-stored-in-variables-as-case-patterns
# [A] guard is an arbitrary expression attached to a pattern and that must evaluate to a "truthy" value for the pattern to succeed.


def generisiGraf(
    m, n, nizZidova, listaPoz, pobedaA1, pobedaA2, pobedaB1, pobedaB2
):  # veljko
    graf = {}
    tmpM = m
    tmpN = n

    start = (1, 1)
    destinationQueue = Queue()
    visited = set()
    visited.add(f"{start[0]},{start[1]}")
    destinationQueue.put(f"{start[0]},{start[1]}")
    graf[f"{start[0]},{start[1]}"] = (0, [])

    while not destinationQueue.empty():
        node = destinationQueue.get()
        childList = list()
        nodeInt = node.split(",")
        for dx, dy in zip([1, -1, 0, 0, 1, 1, -1, -1], [0, 0, 1, -1, 1, -1, 1, -1]):
            g = (int(nodeInt[0]) + dx, int(nodeInt[1]) + dy)
            if g[0] >= 1 and g[0] <= m and g[1] >= 1 and g[1] <= n:
                childList.append(f"{g[0]},{g[1]}")
                graf[node] = (0, childList)
        for child in graf[node][1]:
            if child not in visited:
                destinationQueue.put(child)
                visited.add(child)

    graf[listaPoz[0]] = ("x", graf[listaPoz[0]][1])
    graf[listaPoz[1]] = ("x", graf[listaPoz[1]][1])
    graf[listaPoz[2]] = ("y", graf[listaPoz[2]][1])
    graf[listaPoz[3]] = ("y", graf[listaPoz[3]][1])

    # graf[pobedaA1] = ("a", graf[pobedaA1][1])
    # graf[pobedaB1] = ("b", graf[pobedaB1][1])

    # graf[pobedaA2] = ("a", graf[pobedaA2][1])
    # graf[pobedaB2] = ("b", graf[pobedaB2][1])

    for edge in nizZidova:
        potege = list()
        for potega in graf[edge[0]][1]:

            if potega != edge[1]:
                potege.append(potega)
        graf[edge[0]] = (graf[edge[0]][0], potege)
        potege = list()
        for potega in graf[edge[1]][1]:
            if potega != edge[0]:
                potege.append(potega)
        graf[edge[1]] = (graf[edge[1]][0], potege)
    return graf


def unesiZidove(graf, listaZidova, m, n):  # zeljko

    if listaZidova[0][0].split(",")[0] == listaZidova[0][1].split(",")[0] and listaZidova[0][0].split(",")[1] == listaZidova[0][1].split(",")[1]:
        return False

    v_h = listaZidova[0][0].split(",")[0] == listaZidova[0][1].split(",")[0]
    if listaZidova[0][1] not in graf[listaZidova[0][0]][1]:
        if listaZidova[0][0] not in graf[listaZidova[0][1]][1]:
            return False
    if v_h:
        if (
            str(
                str((int(listaZidova[0][0].split(",")[0]) + 1))
                + ","
                + listaZidova[0][0].split(",")[1]
            )
            not in graf[str(
                str((int(listaZidova[0][1].split(",")[0]) + 1))
                + ","
                + listaZidova[0][1].split(",")[1]
            )][1]
        ):
            return False
    else:
        if (
            str(
                listaZidova[0][0].split(",")[0]
                + ","
                + str(int(listaZidova[0][0].split(",")[1]) + 1)
            )
            not in graf[str(listaZidova[0][1].split(",")[0]
                + ","
                + str(int(listaZidova[0][1].split(",")[1]) + 1)
            )][1]
        ):
            return False

        # if(str((str((int(listaZidova[0][0].split(',')[0])+1)))+',' + str(int(listaZidova[0][0].split(',')[1]))) not in graf[listaZidova[0][0]][1]):
        #     if(str(listaZidova[0][1].split(',')[0]+','+str(int(listaZidova[0][1].split(',')[1])+1)) not in graf[listaZidova[0][1]][1]):
        #         return False

    if re.search(f"{m},.", listaZidova[0][0]) and v_h:
        return False
    if re.search(f".,{n}", listaZidova[0][0]) and not v_h:
        return False
    if re.search(f"{m},.", listaZidova[0][1]) and v_h:
        return False
    if re.search(f".,{n}", listaZidova[0][1]) and not v_h:
        return False
    if v_h:
        #AKO JE VERTIKALNI ZID UKRSTEN SA POSTOJECIM HORIZONTALNIM
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0])
        x12 = int(x1[1])
        y11 = int(y1[0]) + 1
        y12 = int(y1[1]) - 1
        novaListaZidova1 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        x11 = int(x1[0]) + 1
        x12 = int(x1[1]) + 1
        y11 = int(y1[0]) 
        y12 = int(y1[1]) 
        novaListaZidova2 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # NOT zato sto proveravamo da li ne postoji veza, ukoliko ne postoji veza, znaci da postoji zid i da nije moguce kretati se po dijagonali
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova1, m, n) and not ProveriDaLiPostojiVeza(graf, novaListaZidova2, m, n):
            return False
    else:
        #AKO JE VERTIKALNI ZID UKRSTEN SA POSTOJECIM HORIZONTALNIM
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0])
        x12 = int(x1[1])
        y11 = int(y1[0]) - 1
        y12 = int(y1[1]) + 1
        novaListaZidova1 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        x11 = int(x1[0]) + 1
        x12 = int(x1[1]) + 1
        y11 = int(y1[0])
        y12 = int(y1[1])
        novaListaZidova2 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]


        # NOT zato sto proveravamo da li ne postoji veza, ukoliko ne postoji veza, znaci da postoji zid i da nije moguce kretati se po dijagonali
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova1, m, n) and not ProveriDaLiPostojiVeza(graf, novaListaZidova2, m, n):
            return False

    obrisi(listaZidova, graf, m, n)
    # print(listaZidova[0][0].split(',')[0])
    # print(listaZidova[0][1].split(',')[1])

    if v_h:
        pomocnoBrisanje(1, 0, 1, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(0, 0, 1, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(1, 0, 0, 0, listaZidova, graf, m, n)

        # OVAJ NAREDNI DEO PROVERAVA DA LI JE MOGUCE ICI DIJAGONALOM PORED ZIDA KOJE SE DODAJE SA NOVOM LISTOM ZIDOVA
        # PORED POSTOJECEG ZIDA JE MOGUCE PROCI SAMO AKO NE POSTOJI DRUGI ZID IZNAD ILI ISPOD NOVOG KOJI SE DODAJE (PO KOLONI)

        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0]) - 1
        x12 = int(x1[1])
        y11 = int(y1[0]) - 1
        y12 = int(y1[1])
        novaListaZidova1 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # NOT zato sto proveravamo da li ne postoji veza, ukoliko ne postoji veza, znaci da postoji zid i da nije moguce kretati se po dijagonali
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova1, m, n):
            pomocnoBrisanje(0, 0, -1, 0, listaZidova, graf, m, n)
            pomocnoBrisanje(-1, 0, 0, 0, listaZidova, graf, m, n)

        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0]) + 2
        x12 = int(x1[1])
        y11 = int(y1[0]) + 2
        y12 = int(y1[1])
        novaListaZidova2 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        if not ProveriDaLiPostojiVeza(graf, novaListaZidova2, m, n):
            pomocnoBrisanje(1, 0, 2, 0, listaZidova, graf, m, n)
            pomocnoBrisanje(2, 0, 1, 0, listaZidova, graf, m, n)

        #Provera za ukrstanje vertikalnog i horizontalnog
            #DA LI POSTOJI LEVI GORNJI ZID
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0])
        x12 = int(x1[1])
        y11 = int(y1[0]) - 1
        y12 = int(y1[1]) - 1
        novaListaZidova3 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        if not ProveriDaLiPostojiVeza(graf, novaListaZidova3, m, n): #AKO NE POSTOJI VEZA
            pomocnoBrisanje(0, 0, -1, 0, listaZidova, graf, m, n)
            
            #DA LI POSTOJI DESNI GORNJI ZID
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0])
        x12 = int(x1[1]) + 1
        y11 = int(y1[0]) - 1
        y12 = int(y1[1])
        novaListaZidova4 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # AKO NE POSTOJI VEZA
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova4, m, n):
            pomocnoBrisanje(-1, 0, 0, 0, listaZidova, graf, m, n)

            #DA LI POSTOJI DONJI LEVI ZID
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0]) + 1
        x12 = int(x1[1]) 
        y11 = int(y1[0]) + 2
        y12 = int(y1[1]) - 1
        novaListaZidova4 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # AKO NE POSTOJI VEZA
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova4, m, n):
            pomocnoBrisanje(+1, 0, +2, 0, listaZidova, graf, m, n)

            #DA LI POSTOJI DONJI DESNI ZID
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0]) + 1
        x12 = int(x1[1]) + 1
        y11 = int(y1[0]) + 2
        y12 = int(y1[1])
        novaListaZidova4 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # AKO NE POSTOJI VEZA
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova4, m, n):
            pomocnoBrisanje(+2, 0, +1, 0, listaZidova, graf, m, n)


    else:
        pomocnoBrisanje(0, 1, 0, 1, listaZidova, graf, m, n)
        pomocnoBrisanje(0, 0, 0, 1, listaZidova, graf, m, n)
        pomocnoBrisanje(1, 0, -1, 1, listaZidova, graf, m, n)

        # OVAJ NAREDNI DEO PROVERAVA DA LI JE MOGUCE ICI DIJAGONALOM PORED ZIDA KOJE SE DODAJE SA NOVOM LISTOM ZIDOVA
        # PORED POSTOJECEG ZIDA JE MOGUCE PROCI SAMO AKO NE POSTOJI DRUGI ZID ISPRED ILI IZA NOVOG KOJI SE DODAJE (PO VRSTI)

        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0])
        x12 = int(x1[1]) - 1
        y11 = int(y1[0])
        y12 = int(y1[1]) - 1
        novaListaZidova1 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        if not ProveriDaLiPostojiVeza(graf, novaListaZidova1, m, n):
            pomocnoBrisanje(0, 0, 0, -1, listaZidova, graf, m, n)
            pomocnoBrisanje(0, -1, 0, 0, listaZidova, graf, m, n)

        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0])
        x12 = int(x1[1]) + 2
        y11 = int(y1[0])
        y12 = int(y1[1]) + 2
        novaListaZidova2 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        if not ProveriDaLiPostojiVeza(graf, novaListaZidova2, m, n):
            pomocnoBrisanje(0, 1, 0, 2, listaZidova, graf, m, n)
            pomocnoBrisanje(0, 2, 0, 1, listaZidova, graf, m, n)

            #DA LI POSTOJI GORNJI LEVI ZID
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0])
        x12 = int(x1[1])
        y11 = int(y1[0]) - 1
        y12 = int(y1[1]) - 1
        novaListaZidova4 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # AKO NE POSTOJI VEZA
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova4, m, n):
            pomocnoBrisanje(0, 0, 0, -1, listaZidova, graf, m, n)

            #DA LI POSTOJI GORNJI DESNI ZID
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0])
        x12 = int(x1[1]) + 1
        y11 = int(y1[0]) - 1
        y12 = int(y1[1]) + 2
        novaListaZidova4 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # AKO NE POSTOJI VEZA
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova4, m, n):
            pomocnoBrisanje(0, +1, 0, +2, listaZidova, graf, m, n)

            #DA LI POSTOJI DONJI LEVI ZID
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0]) + 1
        x12 = int(x1[1]) - 1
        y11 = int(y1[0]) 
        y12 = int(y1[1])
        novaListaZidova4 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # AKO NE POSTOJI VEZA
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova4, m, n):
            pomocnoBrisanje(0, -1, 0, 0, listaZidova, graf, m, n)

            #DA LI POSTOJI DONJI DESNI ZID
        x1 = list(listaZidova[0][0].split(","))
        y1 = list(listaZidova[0][1].split(","))
        x11 = int(x1[0]) + 1
        x12 = int(x1[1]) + 2
        y11 = int(y1[0])
        y12 = int(y1[1]) + 1
        novaListaZidova4 = [(str(x11)+","+str(x12), str(y11)+","+str(y12))]

        # AKO NE POSTOJI VEZA
        if not ProveriDaLiPostojiVeza(graf, novaListaZidova4, m, n):
            pomocnoBrisanje(0, +2, 0, +1, listaZidova, graf, m, n)

    return True


def ProveriDaLiPostojiVeza(graf, listaZidova, m, n):
    x1 = list(listaZidova[0][0].split(","))
    y1 = list(listaZidova[0][1].split(","))
    if (
        0 == int(x1[0])
        or 0 == int(x1[1])
        or 0 == int(y1[0])
        or 0 == int(y1[1])
    ):
        return False
    if (
       n+1 == int(x1[0])
        or m+1 == int(x1[1])
        or n+1 == int(y1[0])
        or m+1 == int(y1[1])
       ):
        return False
    # if graf[x1].contains(y1)
    if listaZidova[0][0] in graf[listaZidova[0][1]][1]:
        return True
    else:
        return False


def pomocnoBrisanje(a, b, c, d, listaZidova, graf, m, n):  # zeljko
    x1 = list(listaZidova[0][0].split(","))
    y1 = list(listaZidova[0][1].split(","))
    x1[0] = int(x1[0]) + a
    x1[1] = int(x1[1]) + b
    y1[0] = int(y1[0]) + c
    y1[1] = int(y1[1]) + d
    novaLista = (str(x1[0]) + "," + str(x1[1]), str(y1[0]) + "," + str(y1[1]))
    if (
        0 == int(novaLista[0].split(",")[0])
        or 0 == int(novaLista[0].split(",")[1])
        or 0 == int(novaLista[1].split(",")[0])
        or 0 == int(novaLista[1].split(",")[1])
    ):
        return
    if (
        n + 1 == int(novaLista[0].split(",")[0])
        or m + 1 == int(novaLista[0].split(",")[1])
        or n + 1 == int(novaLista[1].split(",")[0])
        or m + 1 == int(novaLista[1].split(",")[1])
    ):
        return
    obrisi([novaLista], graf, m, n)


def obrisi(listaZidova, graf, m, n):  # zeljko
    for edge in listaZidova:
        potege = list()
        for potega in graf[edge[0]][1]:
            if potega != edge[1]:
                potege.append(potega)
        graf[edge[0]] = (graf[edge[0]][0], potege)
        potege = list()
        for potega in graf[edge[1]][1]:
            if potega != edge[0]:
                potege.append(potega)
        graf[edge[1]] = (graf[edge[1]][0], potege)


def SetujPocetnoStanje(
    velicinaX, velicinaY, listaIgraca, pobedaA1, pobedaA2, pobedaB1, pobedaB2
):  # veljko
    return generisiGraf(
        velicinaX, velicinaY, [], listaIgraca, pobedaA1, pobedaA2, pobedaB1, pobedaB2
    )


def pomeriIGraca(
    graf, m, n, startPoz, endPoz, naPotezu, pobeda, px1, px2, py1, py2
):  # veljko
    igrac = graf[startPoz][0]
    if igrac != naPotezu:
        return (False, False)

    endPozInt = (int(endPoz.split(",")[0]), int(endPoz.split(",")[1]))
    startPozInt = (int(startPoz.split(",")[0]), int(startPoz.split(",")[1]))
    if (
        endPozInt[0] >= 1
        and endPozInt[0] <= m
        and endPozInt[1] >= 1
        and endPozInt[1] <= n
    ):
        ValidiranPokret = validacijaPokreta(
            graf, startPozInt, endPozInt, endPoz, startPoz, px1, px2, py1, py2
        )
        if ValidiranPokret:
            if (endPoz == px1 or endPoz == px2) and naPotezu == "x":
                pobeda = True
            elif (endPoz == py1 or endPoz == py2) and naPotezu == "y":
                pobeda = True
            graf[startPoz] = (0, graf[startPoz][1])
            graf[endPoz] = (igrac, graf[endPoz][1])
    else:
        ValidiranPokret = False
    ret = (pobeda, ValidiranPokret)
    return ret


def validacijaPokreta(graf, trenutno, ciljno, endpoz, startPoz, px1, px2, py1, py2):  # filip

    # naPotezu = graf[startPoz][0]
    # MogucePobednickoPolje = graf[endpoz][0]

    if graf[endpoz][0] == "x" or graf[endpoz][0] == "y":
        if not (endpoz == px1 or endpoz == px2 or endpoz == py1 or endpoz == py2):
            return False

    for tx, ty in zip([1, 0, -1, 0], [0, 1, 0, -1]):
        p = (trenutno[0] + tx, trenutno[1] + ty)

        if p == ciljno:
            for node in graf[startPoz][1]:
                if node == endpoz: #Ako ne postoji zid, proverava se da li postoji veza izmedju startPoz i endPoz
                    if endpoz == px1 or endpoz == px2 or endpoz == py1 or endpoz == py2:
                        return True


    for dx, dy in zip([2, -2, 0, 0], [0, 0, 2, -2]):
        g = (trenutno[0] + dx, trenutno[1] + dy)
        if g == (10, 8):
            a = 3
        if g == ciljno:
            for node in graf[startPoz][1]:
                if (
                    node.split(",")[0] != startPoz.split(",")[0]
                    and node.split(",")[1] != startPoz.split(",")[1]
                ):
                    continue
                for child in graf[node][1]:
                    if (
                        child.split(",")[0] != node.split(",")[0]
                        and child.split(",")[1] != node.split(",")[1]
                    ):
                        continue
                    else:
                        if (
                            child.split(",")[0] == node.split(",")[0]
                            or child.split(",")[1] == node.split(",")[1]
                        ):
                            if child == endpoz:
                                return True

    for tx, ty in zip([1, -1, 1, -1], [1, -1, -1, 1]):
        p = (trenutno[0] + tx, trenutno[1] + ty)
        if p == ciljno:
            for node in graf[startPoz][1]:
                if node == endpoz:
                    return True
    # print("Nije moguce pomeriti igraca na ovo polje! Postoji zid ili ste uneli nevalidnu vrednost")
    return False


def stampajGraf(graf, M, N):  # filip
    print("TABLA:")
    brojevi = "  | "
    okvirHorizontalni = "----"
    for j in range(1, N + 1):
        if j > 9:
            brojevi += str(j) + "   "
            okvirHorizontalni += "-----"
        else:
            brojevi += str(j) + "    "
            okvirHorizontalni += "-----"
    print(brojevi)
    print(okvirHorizontalni)
    vrsta = ""
    for i in range(1, M + 1):
        horizontalniZidovi = "    "
        if i < 10:
            vrsta = str(i) + " | "
        else:
            vrsta = str(i) + "| "

        for j in range(1, N + 1):
            zid = ""

            if f"{i},{j+1}" in graf[f"{i},{j}"][1]:
                zid = "  "
            elif j != N:
                zid = "||"
            if f"{i+1},{j}" in graf[f"{i},{j}"][1]:
                horizontalniZidovi += "     "
            elif i != M:
                horizontalniZidovi += "=    "
            vrsta += str("" + str(graf[f"{i},{j}"][0]) + " " + zid + " ")

        print(vrsta)
        print(horizontalniZidovi)
    print("-----------------------------------------")


def NotClosedPath(pobedaPozicije, graph):
    igracCounterX = 0
    igracCounterY = 0

    ciljniCvorovi = list()
    start = pobedaPozicije[0]
    destinationQueue = Queue(len(graph))
    visited = set()

    for i in range(0, 2):
        if pobedaPozicije[i] not in ciljniCvorovi:
            visited.add(pobedaPozicije[i])
            destinationQueue.put(pobedaPozicije[i])
            ciljniCvorovi.append(pobedaPozicije[i])
            while not destinationQueue.empty():
                node = destinationQueue.get()
                if graph[node][0] == "x":
                    igracCounterX += 1
                if node == pobedaPozicije[i + 1]:
                    ciljniCvorovi.append(node)
                for child in graph[node][1]:
                    if child not in visited:
                        destinationQueue.put(child)
                        visited.add(child)
        if igracCounterX < 2:
            return False

    visited = set()

    for i in range(2, 4):
        if pobedaPozicije[i] not in ciljniCvorovi:
            visited.add(pobedaPozicije[i])
            destinationQueue.put(pobedaPozicije[i])
            ciljniCvorovi.append(pobedaPozicije[i])
            while not destinationQueue.empty():
                node = destinationQueue.get()
                if graph[node][0] == "y":
                    igracCounterY += 1
                if node == pobedaPozicije[i + 1]:
                    ciljniCvorovi.append(node)
                for child in graph[node][1]:
                    if child not in visited:
                        destinationQueue.put(child)
                        visited.add(child)
        if igracCounterY < 2:
            return False
    return True


def proveriPobednika(pobedaPravilnoTuple):  # filip
    return pobedaPravilnoTuple[0]


def generisiNovoStanjeZaUlazniPotez(
    graf, m, n, startPoz, endPoz, naPotezu, pobeda, px1, px2, py1, py2
):
    if endPoz == "3,6":
        a = 10
    if naPotezu == "y":
        a = 10
    igrac = graf[startPoz][0]
    if igrac != naPotezu:
        return (False, False, False)
    noviGraf = graf.copy()
    endPozInt = (int(endPoz.split(",")[0]), int(endPoz.split(",")[1]))
    startPozInt = (int(startPoz.split(",")[0]), int(startPoz.split(",")[1]))
    if (
        endPozInt[0] >= 1
        and endPozInt[0] <= m
        and endPozInt[1] >= 1
        and endPozInt[1] <= n
    ):
        ValidiranPokret = validacijaPokreta(
            noviGraf, startPozInt, endPozInt, endPoz, startPoz, px1, px2, py1, py2
        )
        if ValidiranPokret:
            if (endPoz == px1 or endPoz == px2) and naPotezu == "x":
                pobeda = True
            elif (endPoz == py1 or endPoz == py2) and naPotezu == "y":
                pobeda = True
            noviGraf[startPoz] = (0, noviGraf[startPoz][1])
            noviGraf[endPoz] = (igrac, noviGraf[endPoz][1])
    else:
        ValidiranPokret = False
        return pobeda, [], ValidiranPokret

    listaGrafova = []

    # horizontalni zidovi
    for i in range(1, m):
        for j in range(1, n):
            novinoviGraf = noviGraf.copy()
            if unesiZidove(
                novinoviGraf, [
                    (str(i) + "," + str(j), str(i + 1) + "," + str(j))], m, n
            ):
                # stampajGraf(novinoviGraf, m, n)
                if NotClosedPath([px1, px2, py1, py2], novinoviGraf):
                    listaGrafova.append(novinoviGraf)
                else:
                    a = 10
    # vertikalni zidovi
    for i in range(1, m):
        for j in range(1, n):
            novinoviGraf = noviGraf.copy()
            if unesiZidove(
                novinoviGraf, [
                    (str(i) + "," + str(j), str(i) + "," + str(j + 1))], m, n
            ):
                # stampajGraf(novinoviGraf, m, n)
                if NotClosedPath([px1, px2, py1, py2], novinoviGraf):
                    listaGrafova.append(novinoviGraf)
                else:
                    a = 10

    ret = (pobeda, listaGrafova, ValidiranPokret)

    return ret


def generisiSvaMogucaStanja(graf, m, n, startPoz, naPotezu, pobeda, px1, px2, py1, py2):

    if graf[startPoz][0] != naPotezu:
        print(
            "Na prosledjenoj startnoj poziciji se ne nalazi igrac koji treba da bude na potezu"
        )
        return []
    listaStanja = []
    
    startPozInt = (int(startPoz.split(",")[0]), int(startPoz.split(",")[1]))
    for dx, dy in zip([2, -2, 0, 0], [0, 0, 2, -2]):
        g = (startPozInt[0] + dx, startPozInt[1] + dy)
        stringG = f"{g[0]},{g[1]}"
        tmpStanje = generisiNovoStanjeZaUlazniPotez(
            graf, m, n, startPoz, stringG, naPotezu, pobeda, px1, px2, py1, py2
        )
        if tmpStanje[2]:
            listaStanja = listaStanja + tmpStanje[1]

    for tx, ty in zip([1, -1, 1, -1], [1, -1, -1, 1]):
        p = (startPozInt[0] + tx, startPozInt[1] + ty)
        stringP = f"{p[0]},{p[1]}"
        tmpStanje = generisiNovoStanjeZaUlazniPotez(
            graf, m, n, startPoz, stringP, naPotezu, pobeda, px1, px2, py1, py2
        )
        if tmpStanje[2]:
            listaStanja = listaStanja + tmpStanje[1]
    return listaStanja


def generisiLogicnaStanjaZaUlazniPotezPijuna(
    graf, m, n, startPoz, endPoz, naPotezu, pobeda, px1, px2, py1, py2, BrojZidova
):
    igrac = graf[startPoz][0]
    if igrac != naPotezu:
        return (False, False, False)
    minBrKorakaDoCilja = VratiBrojKorakaDoCilja(
        graf, m, n, naPotezu, px1, px2, py1, py2)
    noviGraf = graf.copy()
    endPozInt = (int(endPoz.split(",")[0]), int(endPoz.split(",")[1]))
    startPozInt = (int(startPoz.split(",")[0]), int(startPoz.split(",")[1]))
    if (
        endPozInt[0] >= 1
        and endPozInt[0] <= m
        and endPozInt[1] >= 1
        and endPozInt[1] <= n
    ):
        ValidiranPokret = validacijaPokreta(
            noviGraf, startPozInt, endPozInt, endPoz, startPoz, px1, px2, py1, py2
        )
        if ValidiranPokret:
            if (endPoz == px1 or endPoz == px2) and naPotezu == "x":
                pobeda = True
            elif (endPoz == py1 or endPoz == py2) and naPotezu == "y":
                pobeda = True
            noviGraf[startPoz] = (0, noviGraf[startPoz][1])
            noviGraf[endPoz] = (igrac, noviGraf[endPoz][1])

            if( minBrKorakaDoCilja == 1 and pobeda):
                return (pobeda, [noviGraf], ValidiranPokret)
            minBrKorakaDoCiljaNovogGrafa = VratiBrojKorakaDoCilja(
                noviGraf, m, n, naPotezu, px1, px2, py1, py2)
            if(minBrKorakaDoCilja < minBrKorakaDoCiljaNovogGrafa):
                ValidiranPokret = False
                return pobeda, [], ValidiranPokret

    else:
        ValidiranPokret = False
        return pobeda, [], ValidiranPokret

    if pobeda == True:
        return (pobeda, [noviGraf], ValidiranPokret)
    listaGrafova = []

    if BrojZidova <= 0:
        return (pobeda, [noviGraf], ValidiranPokret)


    pozicijeXiY = pozicijePijuna(noviGraf)
    listaNajkracihPuteva = []
    minPovratnaVrednost = 100
    tmpMin = 300
    IzabranaY = ""
    IzabranoCiljno = ""
    minX = 0
    minY = 0
    maxX = 0
    maxY = 0
    brKorakaDoCiljaNovogNovogGrafa = 0
    tmpNaPotezu = ""
    if naPotezu == "x":
        tmpNaPotezu = "y"
        # poziv za protivnikove figure
        tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[2], py1)
        if tmpMin > 0:
            if tmpMin < minPovratnaVrednost:
                minPovratnaVrednost = tmpMin
                IzabranaY = pozicijeXiY[2]
                IzabranoCiljno = py1
                # listaNajkracihPuteva.append(povratnaVr)
        tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[3], py1)
        if tmpMin > 0:
            if tmpMin < minPovratnaVrednost:
                minPovratnaVrednost = tmpMin
                IzabranaY = pozicijeXiY[3]
                IzabranoCiljno = py1
                # listaNajkracihPuteva.append(povratnaVr)
        tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[2], py2)
        if tmpMin > 0:
            if tmpMin < minPovratnaVrednost:
                minPovratnaVrednost = tmpMin
                IzabranaY = pozicijeXiY[3]
                IzabranoCiljno = py2
                # listaNajkracihPuteva.append(povratnaVr)
        tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[3], py2)
        if tmpMin > 0:
            if tmpMin < minPovratnaVrednost:
                minPovratnaVrednost = tmpMin
                IzabranaY = pozicijeXiY[3]
                IzabranoCiljno = py2
                # listaNajkracihPuteva.append(povratnaVr)
        # minBrKorakaDoCiljaProtivnika = list(sorted(listaNajkracihPuteva))[0]
        IzabranaYx = IzabranaY.split(",")[0]
        IzabranaYy = IzabranaY.split(",")[1]
        IzabranoCiljnox = IzabranoCiljno.split(",")[0]
        IzabranoCiljnoy = IzabranoCiljno.split(",")[1]

        minX = IzabranaYx if IzabranaYx < IzabranoCiljnox else IzabranoCiljnox
        minY = IzabranaYy if IzabranaYy < IzabranoCiljnoy else IzabranoCiljnoy
        maxX = IzabranaYx if IzabranaYx > IzabranoCiljnox else IzabranoCiljnox
        maxY = IzabranaYy if IzabranaYy > IzabranoCiljnoy else IzabranoCiljnoy

    else:
        IzabranaX = ""
        tmpNaPotezu = "x"
        # poziv za protivnikove figure
        tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[0], px1)
        if tmpMin > 0:
            if tmpMin < minPovratnaVrednost:
                minPovratnaVrednost = tmpMin
                IzabranaX = pozicijeXiY[0]
                IzabranoCiljno = px1
                # listaNajkracihPuteva.append(povratnaVr)
        tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[1], px1)
        if tmpMin > 0:
            if tmpMin < minPovratnaVrednost:
                minPovratnaVrednost = tmpMin
                IzabranaX = pozicijeXiY[1]
                IzabranoCiljno = px1
                # listaNajkracihPuteva.append(povratnaVr)
        tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[0], px2)
        if tmpMin > 0:
            if tmpMin < minPovratnaVrednost:
                minPovratnaVrednost = tmpMin
                IzabranaX = pozicijeXiY[0]
                IzabranoCiljno = px2
                # listaNajkracihPuteva.append(povratnaVr)
        tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[1], px2)
        if tmpMin > 0:
            if tmpMin < minPovratnaVrednost:
                minPovratnaVrednost = tmpMin
                IzabranaX = pozicijeXiY[1]
                IzabranoCiljno = px2
                # listaNajkracihPuteva.append(povratnaVr)
            # minBrKorakaDoCiljaProtivnika = list(sorted(listaNajkracihPuteva))[0]
        if IzabranaX == "":
            a = 10
            tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[0], px1)
            if tmpMin > 0:
                if tmpMin < minPovratnaVrednost:
                    minPovratnaVrednost = tmpMin
                    IzabranaX = pozicijeXiY[0]
                    IzabranoCiljno = px1
                    # listaNajkracihPuteva.append(povratnaVr)
            tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[1], px1)
            if tmpMin > 0:
                if tmpMin < minPovratnaVrednost:
                    minPovratnaVrednost = tmpMin
                    IzabranaX = pozicijeXiY[1]
                    IzabranoCiljno = px1
                    # listaNajkracihPuteva.append(povratnaVr)
            tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[0], px2)
            if tmpMin > 0:
                if tmpMin < minPovratnaVrednost:
                    minPovratnaVrednost = tmpMin
                    IzabranaX = pozicijeXiY[0]
                    IzabranoCiljno = px2
                    # listaNajkracihPuteva.append(povratnaVr)
            tmpMin = bestSearch(noviGraf, m, n, pozicijeXiY[1], px2)
            if tmpMin > 0:
                if tmpMin < minPovratnaVrednost:
                    minPovratnaVrednost = tmpMin
                    IzabranaX = pozicijeXiY[1]
                    IzabranoCiljno = px2

        IzabranaXx = IzabranaX.split(",")[0]
        IzabranaXy = IzabranaX.split(",")[1]
        IzabranoCiljnox = IzabranoCiljno.split(",")[0]
        IzabranoCiljnoy = IzabranoCiljno.split(",")[1]

        minX = int(IzabranaXx if IzabranaXx < IzabranoCiljnox else IzabranoCiljnox)
        minY = int(IzabranaXy if IzabranaXy < IzabranoCiljnoy else IzabranoCiljnoy)
        maxX = int(IzabranaXx if IzabranaXx > IzabranoCiljnox else IzabranoCiljnox)
        maxY = int(IzabranaXy if IzabranaXy > IzabranoCiljnoy else IzabranoCiljnoy)
    dodatak = 1
    if minX > 2:
        minX = minX - dodatak
    if minY > 2:
        minY = minY - dodatak
    if maxX < m - 1:
        maxX = maxX + dodatak
    if minY < n - 1:
        maxY = maxY + dodatak

    # horizontalni zidovi
    # Ove int() sam dodao jer je bacalo gresku, po meni su nepotrebni - Filip
    for i in range(int(minX), int(maxX)):
        for j in range(int(minY), int(maxY)):
            novinoviGraf = noviGraf.copy()
            if unesiZidove(
                novinoviGraf, [
                    (str(i) + "," + str(j), str(i + 1) + "," + str(j))], m, n
            ):
                if NotClosedPath([px1, px2, py1, py2], novinoviGraf):
                    brKorakaDoCiljaNovogNovogGrafa = VratiBrojKorakaDoCilja(
                        novinoviGraf, m, n, tmpNaPotezu, px1, px2, py1, py2)
                    if(minPovratnaVrednost < brKorakaDoCiljaNovogNovogGrafa):
                        #stampajGraf(novinoviGraf,m,n)
                        listaGrafova.append(novinoviGraf)

    # vertikalni zidovi
    for i in range(int(minX), int(maxX)):
        for j in range(int(minY), int(maxY)):
            novinoviGraf = noviGraf.copy()
            if unesiZidove(
                novinoviGraf, [
                    (str(i) + "," + str(j), str(i) + "," + str(j + 1))], m, n
            ):
                # stampajGraf(novinoviGraf, m, n)
                if NotClosedPath([px1, px2, py1, py2], novinoviGraf):
                    brKorakaDoCiljaNovogNovogGrafa = VratiBrojKorakaDoCilja(
                        novinoviGraf, m, n, tmpNaPotezu, px1, px2, py1, py2)
                    if(minPovratnaVrednost < brKorakaDoCiljaNovogNovogGrafa):
                        # stampajGraf(novinoviGraf,m,n)
                        listaGrafova.append(novinoviGraf)

    if len(listaGrafova) == 0:  # Ukoliko nije generisano stanje sa zidom koji povecava broj koraka do cilja protivnika, generisemo sva stanja unutar pravougaonika
        # izmedju izabranogPolja i izabranogCiljnog
        # Ove int() sam dodao jer je bacalo gresku, po meni su nepotrebni - Filip
        # minX = minX -  3 * dodatak
        # minY = minY - 3 * dodatak
        # maxX = maxX + 3 * dodatak
        # maxY = maxY + 3 * dodatak
        # for i in range(int(minX), int(maxX)):
        #     for j in range(int(minY), int(maxY)):
        #         novinoviGraf = noviGraf.copy()
        #         if unesiZidove(
        #             novinoviGraf, [
        #                 (str(i) + "," + str(j), str(i + 1) + "," + str(j))], m, n
        #         ):
        #             # stampajGraf(novinoviGraf, m, n)
        #             if NotClosedPath([px1, px2, py1, py2], novinoviGraf):
        #                 listaGrafova.append(novinoviGraf)

        # # vertikalni zidovi
        # for i in range(int(minX), int(maxX)):
        #     for j in range(int(minY), int(maxY)):
        #         novinoviGraf = noviGraf.copy()
        #         if unesiZidove(
        #             novinoviGraf, [
        #                 (str(i) + "," + str(j), str(i) + "," + str(j + 1))], m, n
        #         ):
        #             # stampajGraf(novinoviGraf, m, n)
        #             if NotClosedPath([px1, px2, py1, py2], novinoviGraf):
        #                 listaGrafova.append(novinoviGraf)
        flag = True
        while flag:
            i = int(random.randint(1, m - 1))
            j = int(random.randint(1, n - 1))
            novinoviGraf = noviGraf.copy()
            listaZidova = [(str(i) + "," + str(j), str(i) + "," + str(j + 1))]
            if unesiZidove(novinoviGraf, listaZidova, m, n):
                            # stampajGraf(novinoviGraf, m, n)
                            if NotClosedPath([px1, px2, py1, py2], novinoviGraf):
                                listaGrafova.append(novinoviGraf)
                                pobeda = True   
                                flag = False 
            else:
                listaZidova = [(str(i) + "," + str(j), str(i + 1) + "," + str(j))]
                if unesiZidove(novinoviGraf, listaZidova, m, n):
                            # stampajGraf(novinoviGraf, m, n)
                            if NotClosedPath([px1, px2, py1, py2], novinoviGraf):
                                listaGrafova.append(novinoviGraf)
                                pobeda = True
                                flag = False 


    ret = (pobeda, listaGrafova, ValidiranPokret)
    return ret


def generisiSvaLogicnaStanja(
    graf, m, n, startPoz, naPotezu, pobeda, px1, px2, py1, py2, BrojZidova
):

    if graf[startPoz][0] != naPotezu:
        print(
            "Na prosledjenoj startnoj poziciji se ne nalazi igrac koji treba da bude na potezu"
        )
        return []

    startPozInt = (int(startPoz.split(",")[0]), int(startPoz.split(",")[1]))
    for tx, ty in zip([1, 0, -1, 0], [0, 1, 0, -1]):
        g = (startPozInt[0] + tx, startPozInt[1] + ty)
        stringG = f"{g[0]},{g[1]}"
        noviGraf = graf.copy()

        endPozInt = (int(stringG.split(",")[0]), int(stringG.split(",")[1]))
        if (
            endPozInt[0] >= 1
            and endPozInt[0] <= m
            and endPozInt[1] >= 1
            and endPozInt[1] <= n
        ):
            ValidiranPokret = validacijaPokreta(
                noviGraf, startPozInt, endPozInt, stringG, startPoz, px1, px2, py1, py2
            )
            if ValidiranPokret:
                for mogucPotez in graf[startPoz][1]:
                    if stringG == mogucPotez: #Ako ne postoji zid, proverava se da li postoji veza izmedju startPoz i endPoz
                        if stringG == px1 or stringG == px2 or stringG == py1 or stringG == py2:
                            if (stringG == px1 or stringG == px2) and naPotezu == "x":
                                pobeda = True
                            elif (stringG == py1 or stringG == py2) and naPotezu == "y":
                                pobeda = True
                            noviGraf[startPoz] = (0, noviGraf[startPoz][1])
                            noviGraf[stringG] = (
                                naPotezu, noviGraf[stringG][1])
                            return [noviGraf]
    listaStanja = []
    startPozInt = (int(startPoz.split(",")[0]), int(startPoz.split(",")[1]))
    for dx, dy in zip([2, -2, 0, 0], [0, 0, 2, -2]):
        g = (startPozInt[0] + dx, startPozInt[1] + dy)
        stringG = f"{g[0]},{g[1]}"
        tmpStanje = generisiLogicnaStanjaZaUlazniPotezPijuna(
            graf, m, n, startPoz, stringG, naPotezu, pobeda, px1, px2, py1, py2, BrojZidova
        )
        if tmpStanje[2]:
            listaStanja = listaStanja + tmpStanje[1]
            if tmpStanje[0] == True:
                return listaStanja

    for tx, ty in zip([1, -1, 1, -1], [1, -1, -1, 1]):
        p = (startPozInt[0] + tx, startPozInt[1] + ty)
        stringP = f"{p[0]},{p[1]}"
        tmpStanje = generisiLogicnaStanjaZaUlazniPotezPijuna(
            graf, m, n, startPoz, stringP, naPotezu, pobeda, px1, px2, py1, py2, BrojZidova
        )
        if tmpStanje[2]:
            listaStanja = listaStanja + tmpStanje[1]
            if tmpStanje[0] == True:
                return listaStanja
    return listaStanja


# covek
# x1, x2

# mahina POINTOFVIEW
# y1, y2

# move, evaluation = minimax(graph, 8, -math.inf, math.inf, True, )


def pozicijePijuna(graph):
    sp = []
    for i in graph:
        if graph[i][0] == "x":
            sp = [i] + sp
        if graph[i][0] == "y":
            sp = sp + [i]

    return sp


def pozicijePobednickihPolja():
    global M
    global N
    A1x = int(M / 3)
    A1y = int(N / 3)
    A2x = int(2 * M / 3)
    A2y = int(N / 3)
    B1x = int(M / 3)
    B1y = int(2 * N / 3)
    B2x = int(2 * M / 3)
    B2y = int(2 * N / 3)
    pobedaA1 = f"{A1x},{A1y}"
    pobedaA2 = f"{A2x},{A2y}"
    pobedaB1 = f"{B1x},{B1y}"
    pobedaB2 = f"{B2x},{B2y}"
    sp = [pobedaA1, pobedaA2, pobedaB1, pobedaB2]
    return sp
    # for i in graph:
    #     if graph[i][0] == "a":
    #         sp = [i] + sp
    #     if graph[i][0] == "b":
    #         sp = sp + [i]



def minMax(
    graph,
    depth,
    alpha,
    beta,
    maximizing_player,
    naPotezu,
    m,
    n,
    pobeda,
    px1,
    px2,
    py1,
    py2,
    BrojZidova
):

    if depth == 0:
        return None, heuristika(graph, m, n, naPotezu, px1, px2, py1, py2)

    children = list()

    startPoz = pozicijePijuna(graph)

    if maximizing_player:
        children.append(
            generisiSvaLogicnaStanja(
                graph, m, n, startPoz[0], naPotezu, pobeda, px1, px2, py1, py2, BrojZidova
            )
        )
        children.append(
            generisiSvaLogicnaStanja(
                graph, m, n, startPoz[1], naPotezu, pobeda, px1, px2, py1, py2, BrojZidova
            )
        )
    else:
        children.append(
            generisiSvaLogicnaStanja(
                graph, m, n, startPoz[2], naPotezu, pobeda, px1, px2, py1, py2, BrojZidova
            )
        )
        children.append(
            generisiSvaLogicnaStanja(
                graph, m, n, startPoz[3], naPotezu, pobeda, px1, px2, py1, py2, BrojZidova
            )
        )

    children = children[0] + children[1]
    best_move = children[0]

    if maximizing_player:  # pov->robot      najbolji potez za robota
        max_eval = -math.inf
        for child in children:

            naPotezuu = "x" if naPotezu == "y" else "y"
            current_eval = minMax(
                child,
                depth - 1,
                alpha,
                beta,
                False,
                naPotezuu,
                m,
                n,
                pobeda,
                px1,
                px2,
                py1,
                py2,
                BrojZidova
            )[1]
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = child
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval

    else:
        min_eval = math.inf
        for child in children:

            naPotezuu = "x" if naPotezu == "y" else "y"
            current_eval = minMax(
                child,
                depth - 1,
                alpha,
                beta,
                True,
                naPotezuu,
                m,
                n,
                pobeda,
                px1,
                px2,
                py1,
                py2,
                BrojZidova
            )[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = child
            beta = min(beta, current_eval)
            if beta <= alpha:
                break

        return best_move, min_eval


def gameLoop():  # filip

    global M
    global N
    print("Unesite broj zidova koje poseduje svaki igrac: ")
    BrojZidova = 2 * int(input())

    pobeda = False
    pattern = "[1-{M}|10],[1-{N}|10]"
    pobenik = None
    trenutniIgrac = "x"
    startnaPoz = None
    A1x = int(M / 3)
    A1y = int(N / 3)
    A2x = int(2 * M / 3)
    A2y = int(N / 3)
    B1x = int(M / 3)
    B1y = int(2 * N / 3)
    B2x = int(2 * M / 3)
    B2y = int(2 * N / 3)
    pobedaA1 = f"{A1x},{A1y}"
    pobedaA2 = f"{A2x},{A2y}"
    pobedaB1 = f"{B1x},{B1y}"
    pobedaB2 = f"{B2x},{B2y}"
    # M = 12
    # N = 14
    
    graf = SetujPocetnoStanje(
        M, N, [pobedaB1, pobedaB2, pobedaA1, pobedaA2], pobedaA1, pobedaA2, pobedaB1, pobedaB2
    )
    stampajGraf(graf, M, N)

    # DEO KODA ZA TESTIRANJE FUNKCIJA
    # ------------------------------
    # heuristika(graf, M, N, 'x', pobedaA1, pobedaB1, pobedaA2, pobedaB2)
    # bestSearch(graf, M, N, pozicijePijuna(graf)[0], pobedaA1)
    # pommmmm = minMax(graf, 2, -math.inf, math.inf, True, 'x', M, N, False, pobedaA1, pobedaA2, pobedaB1, pobedaB2)
    # print(pommmmm)
    # stampajGraf(pommmmm[0], M, N)

    # stampajGraf(pommmmm[0], M, N)
    # KRAJ DELA ZA TESTIRANJE

    while True:
        print(f"NA POTEZU JE IGRAC {trenutniIgrac}: ")
        if trenutniIgrac == "x":

            print("Selektujte polje sa igracem koga pomerate: ")
            startnaPoz = input()

            print("Na koje polje: ")
            destinacija = input()

            if BrojZidova > 0:
                print("Unesite gde postavljate zid: ")
                zid1 = input()
                zid2 = input()

                if not re.search(pattern, zid1):
                    print("Unesite pravilno polje za zid1!")
                    continue

                if not re.search(pattern, zid2):
                    print("Unesite pravilno polje za zid2!")
                    continue

            if not re.search(pattern, startnaPoz):
                print("Unesite pravilno polje za startnu poziciju!")
                continue

            if not re.search(pattern, destinacija):
                print("Unesite pravilno polje za krajnju poziciju!")
                continue

            grafCopy = graf.copy()

            pobedaPravilnoTuple = pomeriIGraca(
                graf,
                M,
                N,
                startnaPoz,
                destinacija,
                trenutniIgrac,
                pobeda,
                pobedaA1,
                pobedaA2,
                pobedaB1,
                pobedaB2,
            )
            if not pobedaPravilnoTuple[1]:
                graf = grafCopy
                print(f"Nepravilno kretanje, na potezu je {trenutniIgrac}!")
                continue
            if BrojZidova > 0:
                validanZid = unesiZidove(graf, [(zid1, zid2)], M, N)
                if not validanZid:
                    graf = grafCopy
                    print("Nepravilno unesen zid")
                    continue
                if not NotClosedPath((pobedaA1, pobedaA2, pobedaB1, pobedaB2), graf):
                    graf = grafCopy
                    print(
                        "Unosenje ovog zida dovodi do zatvaranja cilja, unesite pravilan zid"
                    )
                    continue

            if proveriPobednika(pobedaPravilnoTuple):
                break
    
            trenutniIgrac = "x" if trenutniIgrac == "y" else "y"
            BrojZidova -= 1
        else:
            graf = minMax(
                graf,
                1,
                -math.inf,
                math.inf,
                False,
                "y",
                M,
                N,
                pobeda,
                pobedaA1,
                pobedaA2,
                pobedaB1,
                pobedaB2,
                BrojZidova
            )[0]

            if graf[pobedaA1][0] != 0:
                if graf[pobedaA1][0] == "x":
                    break
            if graf[pobedaA2][0] != 0:
                if graf[pobedaA2][0] == "x":
                    break
            if graf[pobedaB1][0] != 0:
                if graf[pobedaB1][0] == "y":
                    break
            if graf[pobedaB2][0] != 0:
                if graf[pobedaB2][0] == "y":
                    break

            trenutniIgrac = "x" if trenutniIgrac == "y" else "y"
            BrojZidova -= 1

        proveriPrelazakPrekoPobednickePozicije(graf, pobedaA1, pobedaA2, pobedaB1, pobedaB2)     
        stampajGraf(graf, M, N)

    print("Pobednik je : x" if trenutniIgrac == "x" else "Pobednik je : y")
    stampajGraf(graf, M, N)


def proveriPrelazakPrekoPobednickePozicije(graf, pobedaA1, pobedaA2, pobedaB1, pobedaB2):
        if(graf[pobedaA1][0] == 0):
            graf[pobedaA1] = ('a', graf[pobedaA1][1])
        if(graf[pobedaA2][0] == 0):
            graf[pobedaA2] = ('a', graf[pobedaA2][1])
        if(graf[pobedaB1][0] == 0):
            graf[pobedaB1] = ('b', graf[pobedaB1][1])
        if(graf[pobedaB2][0] == 0):
            graf[pobedaB2] = ('b', graf[pobedaB2][1])

def VratiBrojKorakaDoCilja(graf, m, n, naPotezu, pobedaA1, pobedaA2, pobedaB1, pobedaB2):
    # stampajGraf(graf,m,n)
    startPoz = pozicijePijuna(graf)
    minBrKorakaDoCilja = 0
    listaNajkracihPuteva = []
    if naPotezu == "x":
        if startPoz[2] == pobedaB1 or startPoz[2] == pobedaB2 or startPoz[3] == pobedaB1 or startPoz[3] == pobedaB2:
            return 1
        povratnaVr = bestSearch(graf, m, n, startPoz[0], pobedaA1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[1], pobedaA1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[0], pobedaA2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[1], pobedaA2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        minBrKorakaDoCilja = list(sorted(listaNajkracihPuteva))[0]

    else:
        if startPoz[0] == pobedaA1 or startPoz[0] == pobedaA2 or startPoz[1] == pobedaA1 or startPoz[1] == pobedaA2:
            return 1
        povratnaVr = bestSearch(graf, m, n, startPoz[2], pobedaB1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[3], pobedaB1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[2], pobedaB2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[3], pobedaB2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        minBrKorakaDoCilja = list(sorted(listaNajkracihPuteva))[0]

    return minBrKorakaDoCilja


def heuristika(graf, m, n, naPotezu, pobedaA1, pobedaA2, pobedaB1, pobedaB2):
    startPoz = pozicijePijuna(graf)
    minBrKorakaDoCilja = 0
    minBrKorakaDoCiljaProtivnika = 0
    GranicnaHeuristika = 500
    listaNajkracihPuteva = []
    if naPotezu == "x":
        if startPoz[2] == pobedaB1 or startPoz[2] == pobedaB2 or startPoz[3] == pobedaB1 or startPoz[3] == pobedaB2:
            return -GranicnaHeuristika
        povratnaVr = bestSearch(graf, m, n, startPoz[0], pobedaA1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[1], pobedaA1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[0], pobedaA2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[1], pobedaA2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        minBrKorakaDoCilja = list(sorted(listaNajkracihPuteva))[0]
        listaNajkracihPuteva = []
        # poziv za protivnikove figure
        povratnaVr = bestSearch(graf, m, n, startPoz[2], pobedaB1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[3], pobedaB1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[2], pobedaB2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[3], pobedaB2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        minBrKorakaDoCiljaProtivnika = list(sorted(listaNajkracihPuteva))[0]
        konacnaVrednost = 1/minBrKorakaDoCilja * 100
        konacnaVrednost = konacnaVrednost - 1/minBrKorakaDoCiljaProtivnika * 100

        # if(minBrKorakaDoCiljaProtivnika == 1):
        #     a = 10
        # print("ODREDJUJEM HEURISTIKU:")
        # stampajGraf(graf, m, n)
        # print("vrednost heuristike je " + str(konacnaVrednost))
        return konacnaVrednost
    else:
        if startPoz[0] == pobedaA1 or startPoz[0] == pobedaA2 or startPoz[1] == pobedaA1 or startPoz[1] == pobedaA2:
            return GranicnaHeuristika
        povratnaVr = bestSearch(graf, m, n, startPoz[2], pobedaB1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[3], pobedaB1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[2], pobedaB2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[3], pobedaB2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        minBrKorakaDoCilja = list(sorted(listaNajkracihPuteva))[0]
        listaNajkracihPuteva = []
        # provera za protivnika
        povratnaVr = bestSearch(graf, m, n, startPoz[0], pobedaA1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[1], pobedaA1)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[0], pobedaA2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        povratnaVr = bestSearch(graf, m, n, startPoz[1], pobedaA2)
        if povratnaVr > 0:
            listaNajkracihPuteva.append(povratnaVr)
        minBrKorakaDoCiljaProtivnika = list(sorted(listaNajkracihPuteva))[0]

    konacnaVrednost = 1/minBrKorakaDoCilja * 100
    konacnaVrednost = konacnaVrednost - 1/minBrKorakaDoCiljaProtivnika * 100
    return - konacnaVrednost


def bestSearch(graf, m, n, start, goal):
    if start == goal:
        path = PriorityQueue(1)
        path.put(start)
        return 0

    pobedaPozicije = pozicijePobednickihPolja()
    destinationStack = PriorityQueue(len(graf))
    visited = set()
    found = False
    visited.add(start)
    destinationStack.put((heuristikaZaTrazenjeputa(start, goal), start))
    previous = {}
    previous[start] = None

    while not found and not destinationStack.empty():
        node = destinationStack.get()

        startPozInt = (int(node[1].split(",")[0]), int(node[1].split(",")[1]))
        for tx, ty in zip([1, 0, -1, 0], [0, 1, 0, -1]):
            g = (startPozInt[0] + tx, startPozInt[1] + ty)
            stringG = f"{g[0]},{g[1]}"

            endPozInt = (int(stringG.split(",")[0]), int(
                stringG.split(",")[1]))
            startPozInt = (int(node[1].split(",")[0]),
                           int(node[1].split(",")[1]))
            if (
                endPozInt[0] >= 1
                and endPozInt[0] <= m
                and endPozInt[1] >= 1
                and endPozInt[1] <= n
            ):
                if stringG == goal:
                    a = 10
                ValidiranPokret = validacijaPokreta(
                    graf, startPozInt, endPozInt, stringG, node[1], pobedaPozicije[
                        0], pobedaPozicije[1], pobedaPozicije[2], pobedaPozicije[3]
                )
                if ValidiranPokret:
                    for mogucPotez in graf[node[1]][1]:
                        if stringG == mogucPotez: #Ako ne postoji zid, proverava se da li postoji veza izmedju startPoz i endPoz
                            if stringG == pobedaPozicije[0] or stringG == pobedaPozicije[1] or stringG == pobedaPozicije[2] or stringG == pobedaPozicije[3]:                            
                                if goal == stringG:
                                    previous[stringG] = node[1]
                                    found = True
                                    break
            if found:
                break
        if found:
           break
        listaPoteza = []
        startPozInt = (int(node[1].split(",")[0]), int(node[1].split(",")[1]))
        for dx, dy in zip([2, -2, 0, 0], [0, 0, 2, -2]):
            g = (startPozInt[0] + dx, startPozInt[1] + dy)
            stringG = f"{g[0]},{g[1]}"

            noviGraf = graf.copy()
            endPozInt = (int(stringG.split(",")[0]), int(
                stringG.split(",")[1]))
            startPozInt = (int(node[1].split(",")[0]),
                           int(node[1].split(",")[1]))
            if (
                endPozInt[0] >= 1
                and endPozInt[0] <= m
                and endPozInt[1] >= 1
                and endPozInt[1] <= n
            ):
                if stringG == goal:
                    a = 10
                ValidiranPokret = validacijaPokreta(
                    noviGraf, startPozInt, endPozInt, stringG, node[1], pobedaPozicije[0], pobedaPozicije[1], pobedaPozicije[2], pobedaPozicije[3]
                )
                if ValidiranPokret:
                    listaPoteza.append(stringG)
        for tx, ty in zip([1, -1, 1, -1], [1, -1, -1, 1]):
            p = (startPozInt[0] + tx, startPozInt[1] + ty)
            stringP = f"{p[0]},{p[1]}"
            noviGraf = graf.copy()
            endPozInt = (int(stringP.split(",")[0]), int(
                stringP.split(",")[1]))
            startPozInt = (int(node[1].split(",")[0]),
                           int(node[1].split(",")[1]))
            if (
                endPozInt[0] >= 1
                and endPozInt[0] <= m
                and endPozInt[1] >= 1
                and endPozInt[1] <= n
            ):
                ValidiranPokret = validacijaPokreta(
                    noviGraf, startPozInt, endPozInt, stringP, node[1], pobedaPozicije[
                        0], pobedaPozicije[1], pobedaPozicije[2], pobedaPozicije[3]
                )
                if ValidiranPokret:
                    listaPoteza.append(stringP)

        for child in listaPoteza:
            if child not in visited:
                destinationStack.put(
                    (heuristikaZaTrazenjeputa(child, goal), child))
                previous[child] = node[1]
                if child == goal:
                    found = True
                    break
                visited.add(child)

    path = list()

    if found:
        path.append(goal)
        prev = previous[goal]
        while prev is not None:
            path.append(prev)
            prev = previous[prev]
    path.reverse()
    # if len(path) == 1:
    #     return 1
    # else:
    return len(path) - 1  # Oduzimamo pocetnu i krajnju tacku


def heuristikaZaTrazenjeputa(tacka1, tacka2):
    x1 = int(tacka1.split(",")[0])
    y1 = int(tacka1.split(",")[1])
    x2 = int(tacka2.split(",")[0])
    y2 = int(tacka2.split(",")[1])

    return math.sqrt(
        pow(x1 - x2, 2) + pow(y1 - y2, 2)
    )  # Ovo vraca udaljenost dva cvora i koristi se kao heuristika u trazenju najkraceg puta


print("Unesite M velicinu table (broj vrsta): ")
M = int(input())
print("Unesite N velicinu table (broj kolona): ")
N = int(input())


gameLoop()
