import json, os, jmespath

def write_json(dane, filename, typ):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({typ: []}, f)

    with open(filename, 'r+') as outfile:
        try:
            file_dane = json.load(outfile)
        except json.JSONDecodeError:
            file_dane = {typ: []}

        if typ not in file_dane:
            file_dane[typ] = []

        file_dane[typ].append(dane)

        outfile.seek(0)
        json.dump(file_dane, outfile, indent=4)
        outfile.truncate()

def get_next_id(filename, typ):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        if typ not in data:
            return 0
        last_Id = max(item[typ+"Id"] for item in data[typ])
        return last_Id+1
    except:
        return 0

class Student:
    def __init__(self, imie_i_nazwisko, wiek, grupa):
        self.studentId = get_next_id("Oceny.json", "student")
        self.imie_i_nazwisko = imie_i_nazwisko
        self.wiek = wiek
        self.grupa = grupa
    def dodawanie_student(self):
        write_json(
            {"studentId": self.studentId, "imie_i_nazwisko": self.imie_i_nazwisko, "wiek": self.wiek, "grupa": self.grupa},
            "Oceny.json",
            "student"
        )


class OcenyNazwy: #TEST JMESPath - lepszy od bilb
    def __init__(self, przedmiotId, rygorId, studentId, termin, ocena):
        with open('Oceny.json', 'r') as f:
            data = json.load(f)
        self.ocenyNazwyId = get_next_id("Oceny.json", "ocenyNazwy")
        self.przedmiot = jmespath.search(f"przedmiot[?przedmiotId==`{przedmiotId}`] | [0].nazwa", data)
        self.rygor = jmespath.search(f"rygor[?rygorId==`{rygorId}`] | [0].nazwa", data)
        self.student = jmespath.search(f"student[?studentId==`{studentId}`] | [0].imie_i_nazwisko", data)
        self.termin = termin
        self.ocena = ocena
    def dodawanie_oceny(self):
        write_json(
            {"ocenyNazwyId": self.ocenyNazwyId, "student": self.student, "przedmiot": self.przedmiot, "rygor": self.rygor,
             "termin": self.termin, "ocena": self.ocena},
            "Oceny.json",
            "ocenyNazwy"
        )

class Oceny:
    def __init__(self, przedmiotId, rygorId, studentId, termin, ocena):
        self.ocenyId = get_next_id("Oceny.json", "oceny")
        self.przedmiotId = przedmiotId
        self.rygorId = rygorId
        self.studentId = studentId
        self.termin = termin
        self.ocena = ocena
    def dodawanie_oceny(self):
        write_json(
            {"ocenyId": self.ocenyId, "studentId": self.studentId, "przedmiotId": self.przedmiotId, "rygorId": self.rygorId,
             "termin": self.termin, "ocena": self.ocena},
            "Oceny.json",
            "oceny"
        )

class Przedmiot:
    def __init__(self, nazwa):
        self.przedmiotId = get_next_id("Oceny.json", "przedmiot")
        self.nazwa = nazwa
    def dodawanie_przedmiot(self):
        write_json(
            {"przedmiotId": self.przedmiotId, "nazwa": self.nazwa},
            "Oceny.json",
            "przedmiot"
        )

class Rygor:
    def __init__(self, nazwa):
        self.rygorId = get_next_id("Oceny.json", "rygor")
        self.nazwa = nazwa
    def dodawanie_rygor(self):
        write_json(
            {"rygorId": self.rygorId, "nazwa": self.nazwa},
            "Oceny.json",
            "rygor"
        )


# TEST:

# rygor = Rygor("Cwiczenia")
# rygor.dodawanie_rygor()

# student1 = Student("Jan Kowalski", 21, "A1")
# student1.dodawanie_student()
#
# student2 = Student("Anna Nowak", 22, "B2")
# student2.dodawanie_student()
#
# przedmiot1 = Przedmiot("Matematyka")
# przedmiot1.dodawanie_przedmiot()
#
# przedmiot2 = Przedmiot("Fizyka")
# przedmiot2.dodawanie_przedmiot()
# #
# # rygor1 = Rygor("Wyklad")
# # rygor1.dodawanie_rygor()
# # #
# # rygor2 = Rygor("Laboratorium")
# # rygor2.dodawanie_rygor()
#
#
# ocena = Oceny(0, 0, 0, "2026-04-09", 4.5)
# ocena.dodawanie_oceny()
#
# ocena_nazwa = OcenyNazwy(0, 0, 0, "2026-04-09", 4.5)
# ocena_nazwa.dodawanie_oceny()