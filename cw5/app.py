import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure


class SimpleGraph(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wykresy")

        # UI Setup
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Menu boczne
        menu = QVBoxLayout()
        self.btns = {"sin": np.sin, "cos": np.cos, "tg": np.tan, "ctg": lambda x: 1 / np.tan(x)}
        self.radios = {}

        for name in self.btns:
            self.radios[name] = QRadioButton(name)
            menu.addWidget(self.radios[name])

        btn = QPushButton("Rysuj")
        btn.clicked.connect(self.plot)
        menu.addWidget(btn)
        layout.addLayout(menu)

        # Wykres
        self.canvas = Canvas(Figure(figsize=(5, 4)))
        self.ax = self.canvas.figure.add_subplot(111)
        layout.addWidget(self.canvas)

    def plot(self):
        self.ax.cla()
        x = np.linspace(-2 * np.pi, 2 * np.pi, 400)

        for name, func in self.btns.items():
            if self.radios[name].isChecked():
                self.ax.plot(x, func(x))
                self.ax.set_ylim(-5, 5)  # Stabilizacja dla tg/ctg

        self.canvas.draw()


app = QApplication(sys.argv)
win = SimpleGraph()
win.show()
app.exec_()