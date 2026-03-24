from operator import indexOf

fraza = "Lotnictwo i Kosmonautyka"
lista_fraza = list(fraza)
print(fraza)
print(lista_fraza)

for i in list("Lotnict"):
    lista_fraza.remove(i)
print(lista_fraza)
w = lista_fraza.pop(0)

for i in list("o i Kosmon"):
    lista_fraza.remove(i)
print(lista_fraza)
a = lista_fraza.pop(0)

lista_fraza.remove("u")
t = lista_fraza.pop(0)

wat = [w,a,t]
nowa_fraza = "".join(wat)
print(nowa_fraza)