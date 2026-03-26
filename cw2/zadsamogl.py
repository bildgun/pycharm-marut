samogloski = ['a','e','i','o','u','y']
lista = {}
for i in samogloski:
    lista[i] = 0
slowo = input('Podaj słowo: ')
slowo = slowo.lower()
for i in slowo:
    if i in samogloski:
        lista[i] += 1
print(f"Ilość wystąpień samogłosków w słowie {slowo}:")
for i in lista:
    print(f"Ilość wystąpień '{i}': {lista[i]}")
