class Student:
    def __init__(self, imie_i_nazwisko, wiek, grupa):
        self.imie_i_nazwisko = imie_i_nazwisko
        self.wiek = wiek
        self.grupa = grupa

class Oceny:
    def __init__(self, przedmiot, rygor, student):
        self.przedmiot = Przedmiot(nazwa=przedmiot)
class Przedmiot:
    def __init__(self, nazwa):
        self.nazwa = nazwa
class Rygor:
    def __init__(self, nazwa):
        self.nazwa = nazwa