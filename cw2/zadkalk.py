# Kalkulator
from math import isnan
def kalk(a:float,b:float,operator:str):
    if operator == '+':
        return a+b
    elif operator == '-':
        return a-b
    elif operator == '*':
        return a*b
    elif operator == '/':
        if b != 0:
            return a / b
        return "Nie można dzielić przez 0"
    else:
        return "Podałeś zły operator"

try:
    a = float(input('Podaj a: '))
    b = float(input('Podaj b: '))
except ValueError:
    print("To nie liczby/a")
    exit(1)

op = input('Podaj operator: ')

print(kalk(a,b,op))
