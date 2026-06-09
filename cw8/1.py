import PyQt5, openpyxl, jmespath
import numpy as np
wbname = 'budgetmanager.xlsx'

class Wydatek:
    def __init__(self, data,kategoria,kwota,opis):
        self.data = data
        self.kategoria = kategoria
        self.kwota = kwota
        self.opis = opis
        pass

class BudgetManager:
    def __init__(self):
        self.wydatki = []
        wb = openpyxl.load_workbook(wbname)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
            data = row[0].value
            kategoria = row[1].value
            kwota = row[2].value
            opis = row[3].value
            self.wydatki.append(Wydatek(data,kategoria,kwota,opis))
        wb.save(wbname)
        pass

    def dodaj_wydatek(self, Wydatek):
        data = Wydatek.data
        kategoria = Wydatek.kategoria
        kwota = Wydatek.kwota
        opis = Wydatek.opis
        self.wydatki.append(Wydatek(data,kategoria,kwota,opis))
        pass

    def oblicz_sume_kategorii(self, kategoriaSzukana):
        suma = 0
        for konkretnywydatek in self.wydatki:
            if konkretnywydatek.kategoria == kategoriaSzukana:
                suma += int(konkretnywydatek.kwota)
        return suma

    def wczytaj_z_excela(self, nazwaexcela):
        self.wydatki = []
        wb = openpyxl.load_workbook(nazwaexcela)
        ws = wb.active
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
            data = row[0].value
            kategoria = row[1].value
            kwota = row[2].value
            opis = row[3].value
            self.wydatki.append(Wydatek(data, kategoria, kwota, opis))
        wb.save(nazwaexcela)
        pass

    def czysc_dane(self):
        self.wydatki = []
        pass

    





# wydatek = Wydatek('12 lipca', 'Jedzenie', '100', 'blablabalo')
# #BudgetManager().dodaj_wydatek(wydatek)
# a = BudgetManager()
# print(a.oblicz_sume_kategorii('Jedzenie'))


