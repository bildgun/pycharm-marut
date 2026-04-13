import sys, os, json

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem,QMessageBox, QComboBox, QSplitter)
from PyQt5.QtCore import Qt
from klasy import Student, Przedmiot, Rygor, Oceny, OcenyNazwy


JSON_FILE = "Oceny.json"


def ensure_json_file(): #Sprawdz czy istnieje, jak nie to stworz plik
    if not os.path.exists(JSON_FILE):
        data = {
            "student": [],
            "przedmiot": [],
            "rygor": [],
            "oceny": [],
            "ocenyNazwy": []
        }
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def load_data(): #załaduj dane z pliku
    ensure_json_file()
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = {
            "student": [],
            "przedmiot": [],
            "rygor": [],
            "oceny": [],
            "ocenyNazwy": []
        }
    for key in ["student", "przedmiot", "rygor", "oceny", "ocenyNazwy"]:
        if key not in data:
            data[key] = []
    return data


def save_data(data): #zapisz do pliku
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def delete_record(section, id_field, record_id): #usun wiersz z bazy
    data = load_data()
    original_len = len(data.get(section, []))
    data[section] = [item for item in data.get(section, []) if item.get(id_field) != record_id]
    changed = len(data[section]) != original_len
    if changed:
        save_data(data)
    return changed


class MainWindow(QMainWindow): #Klasa - Okno główne
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dziennik - Bohdan Susulovskyi")
        self.setMinimumSize(1000, 700)

        ensure_json_file()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_students = QWidget()
        self.tab_przedmioty = QWidget()
        self.tab_rygory = QWidget()
        self.tab_oceny = QWidget()

        self.tabs.addTab(self.tab_students, "Studenci")
        self.tabs.addTab(self.tab_przedmioty, "Przedmioty")
        self.tabs.addTab(self.tab_rygory, "Rygory")
        self.tabs.addTab(self.tab_oceny, "Oceny")

        self.build_students_tab()
        self.build_przedmioty_tab()
        self.build_rygory_tab()
        self.build_oceny_tab()

        self.refresh_all()

    def show_error(self, text):
        QMessageBox.critical(self, "Błąd", text)

    def show_info(self, text):
        QMessageBox.information(self, "Informacja", text)

    def refresh_all(self):
        self.refresh_students()
        self.refresh_przedmioty()
        self.refresh_rygory()
        self.refresh_oceny_combo()
        self.refresh_oceny_lista()

    # STUDENCI

    def build_students_tab(self):
        layout = QHBoxLayout()

        left_widget = QWidget()
        left_layout = QFormLayout()

        self.student_name_input = QLineEdit()
        self.student_wiek_input = QLineEdit()
        self.student_grupa_input = QLineEdit()

        add_student_btn = QPushButton("Dodaj studenta")
        add_student_btn.clicked.connect(self.add_student)

        left_layout.addRow("Imię i nazwisko:", self.student_name_input)
        left_layout.addRow("Wiek:", self.student_wiek_input)
        left_layout.addRow("Grupa:", self.student_grupa_input)
        left_layout.addRow(add_student_btn)

        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()

        self.student_list = QListWidget()

        delete_student_btn = QPushButton("Usuń zaznaczonego studenta")
        delete_student_btn.clicked.connect(self.delete_student)

        right_layout.addWidget(QLabel("Lista studentów"))
        right_layout.addWidget(self.student_list)
        right_layout.addWidget(delete_student_btn)

        right_widget.setLayout(right_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([350, 650])

        layout.addWidget(splitter)
        self.tab_students.setLayout(layout)

    def add_student(self):
        name = self.student_name_input.text().strip()
        age_text = self.student_wiek_input.text().strip()
        group = self.student_grupa_input.text().strip()

        if not name or not age_text or not group:
            self.show_error("Wypełnij wszystkie pola studenta.")
            return

        try:
            age = int(age_text)
        except ValueError:
            self.show_error("Wiek musi być liczbą całkowitą.")
            return

        student = Student(name, age, group)
        student.dodawanie_student()

        self.student_name_input.clear()
        self.student_wiek_input.clear()
        self.student_grupa_input.clear()

        self.refresh_all()
        self.show_info("Dodano studenta.")

    def refresh_students(self):
        self.student_list.clear()
        data = load_data()

        for student in data["student"]:
            text = (
                f'ID: {student["studentId"]} | '
                f'{student["imie_i_nazwisko"]} | '
                f'Wiek: {student["wiek"]} | '
                f'Grupa: {student["grupa"]}'
            )
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, student["studentId"])
            self.student_list.addItem(item)

    def delete_student(self):
        item = self.student_list.currentItem()
        if not item:
            self.show_error("Wybierz studenta do usunięcia.")
            return

        student_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz usunąć wybranego studenta?"
        )
        if reply == QMessageBox.Yes:
            if delete_record("student", "studentId", student_id):
                self.refresh_all()
                self.show_info("Usunięto studenta.")
            else:
                self.show_error("Nie udało się usunąć studenta.")


    # PRZEDMIOTY

    def build_przedmioty_tab(self):
        layout = QHBoxLayout()

        left_widget = QWidget()
        left_layout = QFormLayout()

        self.przedmiot_input = QLineEdit()

        add_subject_btn = QPushButton("Dodaj przedmiot")
        add_subject_btn.clicked.connect(self.add_subject)

        left_layout.addRow("Nazwa przedmiotu:", self.przedmiot_input)
        left_layout.addRow(add_subject_btn)

        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()

        self.przedmiot_lista = QListWidget()

        delete_subject_btn = QPushButton("Usuń zaznaczony przedmiot")
        delete_subject_btn.clicked.connect(self.delete_subject)

        right_layout.addWidget(QLabel("Lista przedmiotów"))
        right_layout.addWidget(self.przedmiot_lista)
        right_layout.addWidget(delete_subject_btn)

        right_widget.setLayout(right_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([350, 650])

        layout.addWidget(splitter)
        self.tab_przedmioty.setLayout(layout)

    def add_subject(self):
        name = self.przedmiot_input.text().strip()

        if not name:
            self.show_error("Podaj nazwę przedmiotu.")
            return

        subject = Przedmiot(name)
        subject.dodawanie_przedmiot()

        self.przedmiot_input.clear()
        self.refresh_all()
        self.show_info("Dodano przedmiot.")

    def refresh_przedmioty(self):
        self.przedmiot_lista.clear()
        data = load_data()

        for przed in data["przedmiot"]:
            text = f'ID: {przed["przedmiotId"]} | {przed["nazwa"]}'
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, przed["przedmiotId"])
            self.przedmiot_lista.addItem(item)

    def delete_subject(self):
        item = self.przedmiot_lista.currentItem()
        if not item:
            self.show_error("Wybierz przedmiot do usunięcia.")
            return

        subject_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz usunąć wybrany przedmiot?"
        )
        if reply == QMessageBox.Yes:
            if delete_record("przedmiot", "przedmiotId", subject_id):
                self.refresh_all()
                self.show_info("Usunięto przedmiot.")
            else:
                self.show_error("Nie udało się usunąć przedmiotu.")


    # RYGORY

    def build_rygory_tab(self):
        layout = QHBoxLayout()

        left_widget = QWidget()
        left_layout = QFormLayout()

        self.nazwa_rygoru = QLineEdit()

        add_rygor_btn = QPushButton("Dodaj rygor")
        add_rygor_btn.clicked.connect(self.add_rygor)

        left_layout.addRow("Nazwa rygoru:", self.nazwa_rygoru)
        left_layout.addRow(add_rygor_btn)

        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()

        self.rygor_list = QListWidget()

        delete_rygor_btn = QPushButton("Usuń zaznaczony rygor")
        delete_rygor_btn.clicked.connect(self.delete_rygor)

        right_layout.addWidget(QLabel("Lista rygorów"))
        right_layout.addWidget(self.rygor_list)
        right_layout.addWidget(delete_rygor_btn)

        right_widget.setLayout(right_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([350, 650])

        layout.addWidget(splitter)
        self.tab_rygory.setLayout(layout)

    def add_rygor(self):
        name = self.nazwa_rygoru.text().strip()

        if not name:
            self.show_error("Podaj nazwę rygoru.")
            return

        rygor = Rygor(name)
        rygor.dodawanie_rygor()

        self.nazwa_rygoru.clear()
        self.refresh_all()
        self.show_info("Dodano rygor.")

    def refresh_rygory(self):
        self.rygor_list.clear()
        data = load_data()

        for rygor in data["rygor"]:
            text = f'ID: {rygor["rygorId"]} | {rygor["nazwa"]}'
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, rygor["rygorId"])
            self.rygor_list.addItem(item)

    def delete_rygor(self):
        item = self.rygor_list.currentItem()
        if not item:
            self.show_error("Wybierz rygor do usunięcia.")
            return

        rygor_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz usunąć wybrany rygor?"
        )
        if reply == QMessageBox.Yes:
            if delete_record("rygor", "rygorId", rygor_id):
                self.refresh_all()
                self.show_info("Usunięto rygor.")
            else:
                self.show_error("Nie udało się usunąć rygoru.")


    # OCENY

    def build_oceny_tab(self):
        layout = QHBoxLayout()

        left_widget = QWidget()
        left_layout = QFormLayout()

        self.ocena_studentcombo = QComboBox()
        self.ocena_przedmiotcombo = QComboBox()
        self.ocena_rygorcombo = QComboBox()
        self.ocena_termincombo = QComboBox()
        self.ocena_ocena = QComboBox()

        add_grade_btn = QPushButton("Dodaj ocenę")
        add_grade_btn.clicked.connect(self.add_grade)

        left_layout.addRow("Student:", self.ocena_studentcombo)
        left_layout.addRow("Przedmiot:", self.ocena_przedmiotcombo)
        left_layout.addRow("Rygor:", self.ocena_rygorcombo)
        left_layout.addRow("Termin (1,2,3):", self.ocena_termincombo)
        left_layout.addRow("Ocena:", self.ocena_ocena)
        left_layout.addRow(add_grade_btn)

        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()

        self.lista_ocen = QListWidget()

        usun_ocene = QPushButton("Usuń zaznaczoną ocenę")
        usun_ocene.clicked.connect(self.usun_ocene)

        right_layout.addWidget(QLabel("Lista ocen"))
        right_layout.addWidget(self.lista_ocen)
        right_layout.addWidget(usun_ocene)

        right_widget.setLayout(right_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])

        layout.addWidget(splitter)
        self.tab_oceny.setLayout(layout)

    def refresh_oceny_combo(self):
        data = load_data()

        self.ocena_studentcombo.clear()
        self.ocena_przedmiotcombo.clear()
        self.ocena_rygorcombo.clear()
        self.ocena_termincombo.clear()
        for student in data["student"]:
            self.ocena_studentcombo.addItem(
                f'{student["imie_i_nazwisko"]} (ID: {student["studentId"]})',
                student["studentId"]
            )

        for przed in data["przedmiot"]:
            self.ocena_przedmiotcombo.addItem(
                f'{przed["nazwa"]} (ID: {przed["przedmiotId"]})',
                przed["przedmiotId"]
            )

        for rygor in data["rygor"]:
            self.ocena_rygorcombo.addItem(
                f'{rygor["nazwa"]} (ID: {rygor["rygorId"]})',
                rygor["rygorId"]
            )
        for termin in range(1,3):
            self.ocena_termincombo.addItem(termin)

        self.ocena_ocena.addItem('2')
        self.ocena_ocena.addItem('3')
        self.ocena_ocena.addItem('3.5')
        self.ocena_ocena.addItem('4')
        self.ocena_ocena.addItem('5')
    def add_grade(self):
        if self.ocena_studentcombo.count() == 0:
            self.show_error("Brak studentów. Dodaj studenta.")
            return
        if self.ocena_przedmiotcombo.count() == 0:
            self.show_error("Brak przedmiotów. Dodaj przedmiot.")
            return
        if self.ocena_rygorcombo.count() == 0:
            self.show_error("Brak rygorów. Dodaj rygor.")
            return

        student_id = self.ocena_studentcombo.currentData()
        subject_id = self.ocena_przedmiotcombo.currentData()
        rygor_id = self.ocena_rygorcombo.currentData()
        term = self.ocena_termincombo.text().strip()
        grade_text = self.ocena_ocena.text().strip()

        if not term or not grade_text:
            self.show_error("Podaj termin i ocenę.")
            return

        try:
            grade_value = float(grade_text)
        except ValueError:
            self.show_error("Ocena musi być liczbą, np. 4 lub 4.5")
            return

        # zapis ID (Jak do SQL)
        oceny = Oceny(subject_id, rygor_id, student_id, term, grade_value)
        oceny.dodawanie_oceny()

        # zapis nazw (Bez powiązania z innymi danymi z bazy)
        ocenyNazwy = OcenyNazwy(subject_id, rygor_id, student_id, term, grade_value)
        ocenyNazwy.dodawanie_oceny()

        self.ocena_termincombo.clear()
        self.ocena_ocena.clear()

        self.refresh_all()
        self.show_info("Dodano ocenę.")

    def refresh_oceny_lista(self):
        self.lista_ocen.clear()
        data = load_data()

        for oceny in data["ocenyNazwy"]:
            text = (
                f'ID: {oceny["ocenyNazwyId"]} | '
                f'Student: {oceny["student"]} | '
                f'Przedmiot: {oceny["przedmiot"]} | '
                f'Rygor: {oceny["rygor"]} | '
                f'Termin: {oceny["termin"]} | '
                f'Ocena: {oceny["ocena"]}'
            )
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, oceny["ocenyNazwyId"])
            self.lista_ocen.addItem(item)

    def usun_ocene(self):
        item = self.lista_ocen.currentItem()
        if not item:
            self.show_error("Wybierz ocenę do usunięcia.")
            return

        ocenanazwy_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz usunąć wybraną ocenę?"
        )
        if reply != QMessageBox.Yes:
            return

        data = load_data()

        # znajdź odpowiedni rekord w ocenyNazwy
        target = None
        for g in data["ocenyNazwy"]:
            if g.get("ocenyNazwyId") == ocenanazwy_id:
                target = g
                break

        if target is None:
            self.show_error("Nie znaleziono oceny.")
            return

        # usuń z ocenyNazwy po ID
        data["ocenyNazwy"] = [
            g for g in data["ocenyNazwy"]
            if g.get("ocenyNazwyId") != ocenanazwy_id
        ]

        # usuń odpowiadający rekord z oceny na podstawie zgodnych danych
        removed = False
        new_oceny = []
        for g in data["oceny"]:
            if (
                not removed
                and g.get("termin") == target.get("termin")
                and float(g.get("ocena")) == float(target.get("ocena"))
            ):
                removed = True
                continue
            new_oceny.append(g)

        data["oceny"] = new_oceny
        save_data(data)

        self.refresh_all()
        self.show_info("Usunięto ocenę.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()