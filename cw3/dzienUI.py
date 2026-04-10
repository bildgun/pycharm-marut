from PyQt5.QtWidgets import QApplication, QWidget
import sys, klasy

app = QApplication(sys.argv)
window = QWidget()
window.show()
app.exec_()

oceny = klasy.Oceny()