import networkx as nx 
import matplotlib.pyplot as plt



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
    for i in range(1, m+1):
        for j in range(1, n+1):
            potegList = []
            match (i, j):
                case (1, 1):
                    potegList.extend([ str(i + 1) + "," + str(j),
                              str(i) + "," + str(j + 1),
                              str(i + 1) + "," + str(j + 1)])
                    graf[str(i) + "," + str(j)] = (0, potegList)

                case (i, j) if (i, j) == (m,n):
                    potegList.extend([str(i - 1) + "," + str(j), str(i) + "," + str(j - 1),
                              str(i - 1) + "," + str(j - 1)])
                    graf[str(i) + "," + str(j)] = (0, potegList)                              

                case (1, tmpN) if (1, tmpN) == (1, n):
                    potegList.extend([str(i ) + "," + str(j - 1),
                              str(i + 1) + "," + str(j - 1), str(i + 1) + "," + str(j)])
                    graf[str(i) + "," + str(j)] = (0, potegList)                              

                case (tmpM, 1) if (tmpM, 1) == (m, 1):
                    potegList.extend([str(i - 1) + "," + str(j),
                              str(i - 1) + "," + str(j + 1), str(i) + "," + str(j + 1)])
                    graf[str(i) + "," + str(j)] = (0, potegList)                              

                case (1, j) if (1, j) == (1, j):
                    potegList.extend([str(i) + "," + str(j - 1), str(i + 1) + "," + str(j),
                                      str(i) + "," + str(j + 1), str(i + 1) + "," + str(j - 1),
                                      str(i + 1) + "," + str(j + 1) ])
                    graf[str(i) + "," + str(j)] = (0, potegList)                                      

                case (i, 1) if (i, 1) == (i, 1):
                    potegList.extend([str(i + 1) + "," + str(j), str(i - 1) + "," + str(j),
                                      str(i) + "," + str(j+1), str(i+1) + "," + str(j+1), str(i - 1) + "," + str(j + 1)])
                    graf[str(i) + "," + str(j)] = (0, potegList)                                      

                case (tmpM, j) if (tmpM, j) == (m, j):
                    potegList.extend([str(i - 1) + "," + str(j), str(i - 1) + "," + str(j - 1), str(i) + "," + str(j - 1),
                                      str(i - 1) + "," + str(j + 1),
                                      str(i) + "," + str(j + 1)])
                    graf[str(i) + "," + str(j)] = (0, potegList)                                      

                case (i, tmpN) if (i, tmpN) == (i, n):
                    potegList.extend([str(i - 1) + "," + str(j), str(i + 1) + "," + str(j - 1),
                                      str(i - 1) + "," + str(j - 1), str(i - 1) + "," + str(j),
                                     str(i + 1) + ',' + str(j)])
                    graf[str(i) + "," + str(j)] = (0, potegList)                                     
                case _:
                    potegList.extend([str(i-1) + "," + str(j - 1), str(i - 1) + "," + str(j), str(i - 1) + "," + str(j + 1), str(i) + "," + str(j+1), str(i) + "," + str(j-1), str(i + 1) + "," + str(j - 1), str(i+1) + "," + str(j), str(i+1) + "," + str(j+1)])
                    graf[str(i) + "," + str(j)] = (0, potegList)                    

            #graf[str(i) + "." + str(j)] = (0, potegList)

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


listaIgraca = ["1,1","2,2", "3,3", "4,4"]
listaZidova = [("2,1", "2,2")] 
pobedaX = "3,1"
pobedaY = "4,2"
gra = generisiGraf(4, 4, listaZidova, listaIgraca, pobedaX, pobedaY)

lista = {}
for i in gra:
    lista[i] = (gra[i][1])
g = nx.Graph(lista)
nx.draw(g, with_labels = True)
plt.show()
