samogloski = ['o','e','i','a','u','y']
lista = {}
for i in samogloski:
    lista[i] = 0
slowo = input('Podaj słowo: ')
slowo = slowo.lower()
for i in slowo:
    if i in samogloski:
        lista[i] += 1
print(f"Ilość wystąpień samogłosków w słowie {slowo}:")
for i,v in sorted(lista.items()):
    print(f"Ilość wystąpień '{i}': {v}")
