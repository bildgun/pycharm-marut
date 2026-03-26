flag = False
liczby = input("Podaj ciąg liczb oddzielonych spacjami: ").strip()
tup = tuple(map(int,liczby.split(' ')))
print("Największa liczba: ",max(tup))
print("Najmniejsza liczba: ",min(tup))
print("Suma: ",sum(tup))
lista = {}
for i in tup:
    lista[i] = 0
for i in tup:
    if i in tup:
        lista[i] += 1
for i in lista:
    if lista[i] > 1:
        flag = True
        print("Czy są duplikaty? Tak")
        break
if flag == False:
    print("Czy są duplikaty? Nie")
