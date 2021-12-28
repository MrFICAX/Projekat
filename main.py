import networkx as nx
import matplotlib.pyplot as plt
import re
from queue import Queue
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

def generisiGraf(m, n, nizZidova, listaPoz, pobedaA1, pobedaA2, pobedaB1, pobedaB2):  # veljko
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
        for dx, dy in zip([1, -1, 0, 0, 1, 1, -1, -1], [0, 0, 1, -1, 1, -1, 1, -1]):
            g = (int(nodeInt[0]) + dx, int(nodeInt[1]) + dy)
            if(g[0] >= 1 and g[0] <= m and g[1] >= 1 and g[1] <= n):
                childList.append(f"{g[0]},{g[1]}")
                graf[node] = (0, childList)
        for child in graf[node][1]:
            if child not in visited:
                destinationQueue.put(child)
                visited.add(child)

    graf[listaPoz[0]] = ('x', graf[listaPoz[0]][1])
    graf[listaPoz[1]] = ('x', graf[listaPoz[1]][1])
    graf[listaPoz[2]] = ('y', graf[listaPoz[2]][1])
    graf[listaPoz[3]] = ('y',  graf[listaPoz[3]][1])

    graf[pobedaA1] = ('a', graf[pobedaA1][1])
    graf[pobedaB1] = ('b', graf[pobedaB1][1])

    graf[pobedaA2] = ('a', graf[pobedaA2][1])
    graf[pobedaB2] = ('b', graf[pobedaB2][1])

    for edge in nizZidova:
        potege = list()
        for potega in graf[edge[0]][1]:

            if(potega != edge[1]):
                potege.append(potega)
        graf[edge[0]] = (graf[edge[0]][0], potege)
        potege = list()
        for potega in graf[edge[1]][1]:
            if(potega != edge[0]):
                potege.append(potega)
        graf[edge[1]] = (graf[edge[1]][0], potege)
    return graf


def unesiZidove(graf, listaZidova, m, n):  # zeljko

    if '9' in listaZidova[0][0] or '9' in listaZidova[0][1]:
        a=10
    if '10' in listaZidova[0][0] or '10' in listaZidova[0][1]:
        a = 10
    v_h = listaZidova[0][0].split(',')[0] == listaZidova[0][1].split(',')[0]

    if v_h:
        if(str(str((int(listaZidova[0][0].split(',')[0])+1))+','+listaZidova[0][0].split(',')[1]) not in graf[listaZidova[0][0]][1]):
            if(str(str(int(listaZidova[0][1].split(',')[0])+1)+','+listaZidova[0][1].split(',')[1]) not in graf[listaZidova[0][1]][1]):
                return False
    else:
       if listaZidova[0][1] not in graf[listaZidova[0][0]][1]:
           if listaZidova[0][0] not in graf[listaZidova[0][1]][1]:
               return False

        # if(str((str((int(listaZidova[0][0].split(',')[0])+1)))+',' + str(int(listaZidova[0][0].split(',')[1]))) not in graf[listaZidova[0][0]][1]):
        #     if(str(listaZidova[0][1].split(',')[0]+','+str(int(listaZidova[0][1].split(',')[1])+1)) not in graf[listaZidova[0][1]][1]):
        #         return False

    if(re.search(f"{m},.", listaZidova[0][0]) and v_h):
        return False
    if(re.search(f".,{n}", listaZidova[0][0]) and not v_h):
        return False
    if(re.search(f"{m},.", listaZidova[0][1]) and v_h):
        return False
    if(re.search(f".,{n}", listaZidova[0][1]) and not v_h):
        return False

    obrisi(listaZidova, graf, m, n)
    print(listaZidova[0][0].split(',')[0])
    print(listaZidova[0][1].split(',')[1])

    if(listaZidova[0][0].split(',')[0] == listaZidova[0][1].split(',')[0]):
        pomocnoBrisanje(1, 0, 1, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(0, 0, 1, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(1, 0, 0, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(0, 0, -1, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(-1, 0, 0, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(1, 0, 2, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(2, 0, 1, 0, listaZidova, graf, m, n)

    else:
        pomocnoBrisanje(0, 1, 0, 1, listaZidova, graf, m, n)
        pomocnoBrisanje(0, 0, 0, 1, listaZidova, graf, m, n)
        pomocnoBrisanje(1, 0, -1, 1, listaZidova, graf, m, n)
        pomocnoBrisanje(0, 0, 0, -1, listaZidova, graf, m, n)
        pomocnoBrisanje(0, -1, 0, 0, listaZidova, graf, m, n)
        pomocnoBrisanje(0, 1, 0, 2, listaZidova, graf, m, n)
        pomocnoBrisanje(0, 2, 0, 1, listaZidova, graf, m, n)

    return True


def pomocnoBrisanje(a, b, c, d, listaZidova, graf, m, n):  # zeljko
    x1 = list(listaZidova[0][0].split(','))
    y1 = list(listaZidova[0][1].split(','))
    x1[0] = int(x1[0]) + a
    x1[1] = int(x1[1]) + b
    y1[0] = int(y1[0]) + c
    y1[1] = int(y1[1]) + d
    novaLista = (str(x1[0]) + ',' + str(x1[1]),
                  str(y1[0]) + ',' + str(y1[1]))
    if 0 == int(novaLista[0].split(",")[0]) or 0 == int(novaLista[0].split(",")[1]) or 0 == int(novaLista[1].split(",")[0]) or 0 == int(novaLista[1].split(",")[1]):
        return
    if n+1 == int(novaLista[0].split(",")[0]) or m+1 == int(novaLista[0].split(",")[1]) or n+1 == int(novaLista[1].split(",")[0]) or m+1 == int(novaLista[1].split(",")[1]):
        return
    obrisi([novaLista], graf, m, n)


def obrisi(listaZidova, graf, m, n):  # zeljko
    for edge in listaZidova:
        potege = list()
        for potega in graf[edge[0]][1]:
            if(potega != edge[1]):
                potege.append(potega)
        graf[edge[0]] = (graf[edge[0]][0], potege)
        potege = list()
        for potega in graf[edge[1]][1]:
            if(potega != edge[0]):
                potege.append(potega)
        graf[edge[1]] = (graf[edge[1]][0], potege)


def SetujPocetnoStanje(velicinaX, velicinaY, listaIgraca, pobedaA1, pobedaA2, pobedaB1, pobedaB2):  # veljko
    return generisiGraf(velicinaX, velicinaY, [], listaIgraca, pobedaA1, pobedaA2, pobedaB1, pobedaB2)


def pomeriIGraca(graf, m, n, startPoz, endPoz, naPotezu, pobeda, px1, px2, py1, py2):  # veljko
    igrac = graf[startPoz][0]
    if(igrac != naPotezu):
        return (False, False)

    endPozInt = (int(endPoz.split(',')[0]), int(endPoz.split(',')[1]))
    startPozInt = (int(startPoz.split(',')[0]), int(startPoz.split(',')[1]))
    if(endPozInt[0] >= 1 and endPozInt[0] <= m and endPozInt[1] >= 1 and endPozInt[1] <= n):
        ValidiranPokret = validacijaPokreta(
            graf, startPozInt, endPozInt, endPoz, startPoz)
        if ValidiranPokret:
            if (endPoz == px1 or endPoz == px2) and naPotezu == "x":
                pobeda = True
            elif (endPoz == py1 or endPoz == py2) and naPotezu == 'y':
                pobeda = True
            graf[startPoz] = (0, graf[startPoz][1])
            graf[endPoz] = (igrac, graf[endPoz][1])
    else:
        ValidiranPokret = False
    ret = (pobeda, ValidiranPokret)
    return ret


def validacijaPokreta(graf, trenutno, ciljno, endpoz, startPoz):  # filip

    if(graf[endpoz][0] == "x" or graf[endpoz][0] == "y"):
        return False

    for dx, dy in zip([2, -2, 0, 0], [0, 0, 2, -2]):
        g = (trenutno[0] + dx, trenutno[1] + dy)
        if g == (10,8):
            a=3
        if (g == ciljno):
            for node in graf[startPoz][1]:
                if(node.split(",")[0] != startPoz.split(",")[0] and node.split(",")[1] != startPoz.split(",")[1]):
                    continue
                for child in graf[node][1]:
                    if(child.split(",")[0] != node.split(",")[0] and child.split(",")[1] != node.split(",")[1]):
                        continue
                    else:
                        if child.split(",")[0] == node.split(",")[0] or child.split(",")[1] == node.split(",")[1]:
                            if(child == endpoz):
                                return True

    for tx, ty in zip([1, -1, 1, -1], [1, -1, -1, 1]):
        p = (trenutno[0] + tx, trenutno[1] + ty)
        if(p == ciljno):
            for node in graf[startPoz][1]:
                if(node == endpoz):
                    return True
    #print("Nije moguce pomeriti igraca na ovo polje! Postoji zid ili ste uneli nevalidnu vrednost")
    return False


def stampajGraf(graf, M, N):  # filip
    print("TABLA:")
    brojevi = "  | "
    okvirHorizontalni = "----"
    for j in range(1, N+1):
        if(j > 9):
            brojevi += str(j) + "   "
            okvirHorizontalni += "-----"
        else:
            brojevi += str(j) + "    "
            okvirHorizontalni += "-----"
    print(brojevi)
    print(okvirHorizontalni)
    vrsta = ""
    for i in range(1, M+1):
        horizontalniZidovi = "    "
        if(i < 10):
            vrsta = str(i) + " | "
        else:
            vrsta = str(i) + "| "

        for j in range(1, N+1):
            zid = ""

            if(f"{i},{j+1}" in graf[f"{i},{j}"][1]):
                zid = "  "
            elif j != N:
                zid = "||"
            if(f"{i+1},{j}" in graf[f"{i},{j}"][1]):
                horizontalniZidovi += "     "
            elif i != M:
                horizontalniZidovi += "=    "
            vrsta += str(""+str(graf[f"{i},{j}"][0])+" "+zid+" ")

        print(vrsta)
        print(horizontalniZidovi)
    print("-----------------------------------------")


def isClosedPath(pobedaPozicije, graph):
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
            while (not destinationQueue.empty()):
                node = destinationQueue.get()
                if(graph[node][0] == 'x'):
                    igracCounterX += 1
                if(node == pobedaPozicije[i+1]):
                    ciljniCvorovi.append(node)
                for child in graph[node][1]:
                    if child not in visited:
                        destinationQueue.put(child)
                        visited.add(child)
        if(igracCounterX < 2):
            return False

    visited = set()

    for i in range(2, 4):
        if pobedaPozicije[i] not in ciljniCvorovi:
            visited.add(pobedaPozicije[i])
            destinationQueue.put(pobedaPozicije[i])
            ciljniCvorovi.append(pobedaPozicije[i])
            while (not destinationQueue.empty()):
                node = destinationQueue.get()
                if(graph[node][0] == 'y'):
                    igracCounterY += 1
                if(node == pobedaPozicije[i+1]):
                    ciljniCvorovi.append(node)
                for child in graph[node][1]:
                    if child not in visited:
                        destinationQueue.put(child)
                        visited.add(child)
        if(igracCounterY < 2):
            return False
    return True


def proveriPobednika(pobedaPravilnoTuple):  # filip
    return pobedaPravilnoTuple[0]


def generisiNovoStanjeZaUlazniPotez(graf, m, n, startPoz, endPoz, naPotezu, pobeda, px1, px2, py1, py2):
    if endPoz == "3,6":
        a=10
    if naPotezu == 'y':
        a=10
    igrac = graf[startPoz][0]
    if(igrac != naPotezu):
        return (False, False, False)
    noviGraf = graf.copy()
    endPozInt = (int(endPoz.split(',')[0]), int(endPoz.split(',')[1]))
    startPozInt = (int(startPoz.split(',')[0]), int(startPoz.split(',')[1]))
    if(endPozInt[0] >= 1 and endPozInt[0] <= m and endPozInt[1] >= 1 and endPozInt[1] <= n):
        ValidiranPokret = validacijaPokreta(
            noviGraf, startPozInt, endPozInt, endPoz, startPoz)
        if ValidiranPokret:
            if (endPoz == px1 or endPoz == px2) and naPotezu == "x":
                pobeda = True
            elif (endPoz == py1 or endPoz == py2) and naPotezu == 'y':
                pobeda = True
            noviGraf[startPoz] = (0, noviGraf[startPoz][1])
            noviGraf[endPoz] = (igrac, noviGraf[endPoz][1])
    else:
        ValidiranPokret = False
        return pobeda, [], ValidiranPokret

    listaGrafova = []

    #horizontalni zidovi
    for i in range(1, m):
        for j in range(1, n):
            novinoviGraf = noviGraf.copy()
            if unesiZidove(novinoviGraf, [(str(i)+','+str(j), str(i+1)+','+str(j))], m, n):
                stampajGraf(novinoviGraf, m, n)
                if isClosedPath([px1, px2, py1, py2], novinoviGraf):
                    listaGrafova.append(novinoviGraf)
                else:
                    a = 10
    #vertikalni zidovi
    for i in range(1, m):
        for j in range(1, n):
            novinoviGraf = noviGraf.copy()
            if unesiZidove(novinoviGraf, [(str(i)+','+str(j), str(i)+','+str(j+1))], m, n):
                stampajGraf(novinoviGraf, m, n)
                if isClosedPath([px1, px2, py1, py2], novinoviGraf):
                    listaGrafova.append(novinoviGraf)
                else:
                    a = 10

    ret = (pobeda, listaGrafova, ValidiranPokret)

    return ret


def generisiSvaMogucaStanja(graf, m, n, startPoz, naPotezu, pobeda, px1, px2, py1, py2):

    if graf[startPoz][0] != naPotezu:
        print("Na prosledjenoj startnoj poziciji se ne nalazi igrac koji treba da bude na potezu")
        return []
    listaStanja = []
    startPozInt = (int(startPoz.split(',')[0]), int(startPoz.split(',')[1]))
    for dx, dy in zip([2, -2, 0, 0], [0, 0, 2, -2]):
        g = (startPozInt[0] + dx, startPozInt[1] + dy)
        stringG = f"{g[0]},{g[1]}"
        tmpStanje = generisiNovoStanjeZaUlazniPotez(
            graf, m, n, startPoz, stringG, naPotezu, pobeda, px1, px2, py1, py2)
        if tmpStanje[2]:
            listaStanja = listaStanja+tmpStanje[1]

    for tx, ty in zip([1, -1, 1, -1], [1, -1, -1, 1]):
        p = (startPozInt[0] + tx, startPozInt[1] + ty)
        stringP = f"{p[0]},{p[1]}"
        tmpStanje = generisiNovoStanjeZaUlazniPotez(
            graf, m, n, startPoz, stringP, naPotezu, pobeda, px1, px2, py1, py2)
        if tmpStanje[2]:
            listaStanja = listaStanja+tmpStanje[1]
    return listaStanja

# covek
#x1, x2

# mahina POINTOFVIEW
#y1, y2

#move, evaluation = minimax(graph, 8, -math.inf, math.inf, True, )


def pozicijePijuna(graph):
    sp = []
    countx = 0
    county = 0
    for i in graph:
        if graph[i][0] == 'x':
            sp = [i]+sp
        if graph[i][0] == 'y':
            sp = sp+[i]

    return sp


def minimax(graph, depth, alpha, beta, maximizing_player, naPotezu, m, n, pobeda, px1, px2, py1, py2):

    if depth == 0:
        return None,  random.randint(-100, 100)

    children = list()

    startPoz = pozicijePijuna(graph)

    if maximizing_player:
        children.append(generisiSvaMogucaStanja(
            graph, m, n, startPoz[0], naPotezu, pobeda, px1, px2, py1, py2))
        children.append(generisiSvaMogucaStanja(
            graph, m, n, startPoz[1], naPotezu, pobeda, px1, px2, py1, py2))
    else:
        children.append(generisiSvaMogucaStanja(
            graph, m, n, startPoz[2], naPotezu, pobeda, px1, px2, py1, py2))
        children.append(generisiSvaMogucaStanja(
            graph, m, n, startPoz[3], naPotezu, pobeda, px1, px2, py1, py2))

    children = children[0]+children[1]
    best_move = children[0]

    if maximizing_player:  # pov->robot      najbolji potez za robota
        max_eval = -math.inf
        for child in children:

            naPotezuu = 'x' if naPotezu == 'y' else 'y'
            current_eval = minimax(child, depth - 1, alpha, beta,
                                   False, naPotezuu, m, n, pobeda, px1, px2, py1, py2)[1]
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

            naPotezuu = 'x' if naPotezu == 'y' else 'y'
            current_eval = minimax(child, depth - 1, alpha, beta,
                                   True, naPotezuu, m, n, pobeda, px1, px2, py1, py2)[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = child
            beta = min(beta, current_eval)
            if beta <= alpha:
                break

        return best_move, min_eval


def gameLoop():  # filip

    print("Unesite M velicinu table (broj vrsta): ")
    M = int(input())
    print("Unesite N velicinu table (broj kolona): ")
    N = int(input())

    print("Unesite broj zidova koje poseduje svaki igrac: ")
    BrojZidova = 2 * int(input())

    pobeda = False
    pattern = "[1-{M}|10],[1-{N}|10]"
    pobenik = None
    trenutniIgrac = "x"
    startnaPoz = None
    A1x = int(M/3)
    A1y = int(N/3)
    A2x = int(2*M/3)
    A2y = int(N/3)
    B1x = int(M/3)
    B1y = int(2*N/3)
    B2x = int(2*M/3)
    B2y = int(2*N/3)
    pobedaA1 = f"{A1x},{A1y}"
    pobedaB1 = f"{A2x},{A2y}"
    pobedaA2 = f"{B1x},{B1y}"
    pobedaB2 = f"{B2x},{B2y}"
    # M = 12
    # N = 14
    graf = SetujPocetnoStanje(
        M, N, ["1,1", "4,5", "8,8", "2,5"], pobedaA1, pobedaB1, pobedaA2, pobedaB2)
    stampajGraf(graf, M, N)

    pommmmm = minimax(graf, 2, -math.inf, math.inf, True, 'x',
                      M, N, False, pobedaA1, pobedaA2, pobedaB1, pobedaB2)
    print(pommmmm)

    while True:
        print(f"NA POTEZU JE IGRAC {trenutniIgrac}: ")
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

        # Testiranje metode generisiSvaMogucaStanja
        # lista = generisiSvaMogucaStanja(graf, M, N, "10,14", "y",
        #                           pobeda, pobedaA1, pobedaB1, pobedaA2, pobedaB2)

        grafCopy = graf.copy()

        pobedaPravilnoTuple = pomeriIGraca(
            graf, M, N, startnaPoz, destinacija, trenutniIgrac, pobeda, pobedaA1, pobedaB1, pobedaA2, pobedaB2)
        if(not pobedaPravilnoTuple[1]):
            graf = grafCopy
            print(f"Nepravilno kretanje, na potezu je {trenutniIgrac}!")
            continue
        if BrojZidova > 0:
            validanZid = unesiZidove(graf, [(zid1, zid2)], M, N)
            if not validanZid:
                graf = grafCopy
                print("Nepravilno unesen zid")
                continue
            if not isClosedPath((pobedaA1, pobedaA2, pobedaB1, pobedaB2), graf):
                graf = grafCopy
                print(
                    "Unosenje ovog zida dovodi do zatvaranja cilja, unesite pravilan zid")
                continue

        trenutniIgrac = "x" if trenutniIgrac == "y" else "y"
        BrojZidova -= 1
        #pobeda = pobedaPravilnoTuple[0]
        if proveriPobednika(pobedaPravilnoTuple):
            break
        # lista = {}
        # for i in graf:
        #     lista[i] = (graf[i][1])
        # g = nx.Graph(lista)
        # nx.draw(g, with_labels=True)
        # plt.show()
        stampajGraf(graf, M, N)

    print("Pobednik je : " + "x" if trenutniIgrac == "y" else "y")


gameLoop()
