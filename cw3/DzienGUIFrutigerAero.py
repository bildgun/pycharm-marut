import sys
import os
import json
import random

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QComboBox, QSplitter, QGraphicsDropShadowEffect,
    QFrame, QStackedLayout, QDesktopWidget, QGraphicsOpacityEffect
)
from PyQt5.QtCore import (
    Qt, QTimer, QRect, QEasingCurve, QPropertyAnimation,
    QParallelAnimationGroup, QPoint
)
from PyQt5.QtGui import (
    QColor, QPainter, QLinearGradient, QRadialGradient,
    QBrush, QPen, QFont, QPainterPath
)

from klasy import Student, Przedmiot, Rygor, Oceny, OcenyNazwy


JSON_FILE = "Oceny.json"


def ensure_json_file():
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


def load_data():
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


def save_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def delete_record(section, id_field, record_id):
    data = load_data()
    original_len = len(data.get(section, []))
    data[section] = [item for item in data.get(section, []) if item.get(id_field) != record_id]
    changed = len(data[section]) != original_len
    if changed:
        save_data(data)
    return changed


class Bubble:
    def __init__(self, width, height):
        self.reset(width, height, first=True)

    def reset(self, width, height, first=False):
        self.r = random.randint(20, 80)
        self.x = random.randint(-50, max(50, width + 50))
        self.y = random.randint(-50, max(50, height + 50)) if first else height + random.randint(0, 200)
        self.speed = random.uniform(0.2, 1.2)
        self.alpha = random.randint(35, 90)
        self.dx = random.uniform(-0.3, 0.3)


class AeroBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bubbles = [Bubble(1400, 900) for _ in range(24)]
        self.offset = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_scene)
        self.timer.start(30)

    def animate_scene(self):
        self.offset += 1
        w = max(1, self.width())
        h = max(1, self.height())

        for bubble in self.bubbles:
            bubble.y -= bubble.speed
            bubble.x += bubble.dx
            if bubble.y < -bubble.r * 2:
                bubble.reset(w, h)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Tło bazowe - Frutiger Aero
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor(170, 235, 255))
        grad.setColorAt(0.22, QColor(110, 210, 255))
        grad.setColorAt(0.5, QColor(125, 255, 225))
        grad.setColorAt(0.72, QColor(115, 210, 120))
        grad.setColorAt(1.0, QColor(210, 255, 210))
        painter.fillRect(self.rect(), grad)

        # Świetlna poświata u góry
        glow = QRadialGradient(self.width() * 0.75, self.height() * 0.10, self.width() * 0.55)
        glow.setColorAt(0.0, QColor(255, 255, 255, 155))
        glow.setColorAt(0.4, QColor(255, 255, 255, 65))
        glow.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.fillRect(self.rect(), glow)

        # Delikatne fale
        painter.setPen(Qt.NoPen)
        path = QPainterPath()
        path.moveTo(0, self.height() * 0.66)
        path.cubicTo(self.width() * 0.2, self.height() * 0.57,
                     self.width() * 0.4, self.height() * 0.76,
                     self.width() * 0.6, self.height() * 0.67)
        path.cubicTo(self.width() * 0.76, self.height() * 0.60,
                     self.width() * 0.9, self.height() * 0.73,
                     self.width(), self.height() * 0.62)
        path.lineTo(self.width(), self.height())
        path.lineTo(0, self.height())
        path.closeSubpath()
        painter.fillPath(path, QColor(255, 255, 255, 48))

        path2 = QPainterPath()
        path2.moveTo(0, self.height() * 0.74)
        path2.cubicTo(self.width() * 0.25, self.height() * 0.64,
                      self.width() * 0.48, self.height() * 0.85,
                      self.width() * 0.72, self.height() * 0.74)
        path2.cubicTo(self.width() * 0.83, self.height() * 0.70,
                      self.width() * 0.92, self.height() * 0.79,
                      self.width(), self.height() * 0.72)
        path2.lineTo(self.width(), self.height())
        path2.lineTo(0, self.height())
        path2.closeSubpath()
        painter.fillPath(path2, QColor(120, 255, 255, 35))

        # Bąbelki
        for bubble in self.bubbles:
            rg = QRadialGradient(bubble.x, bubble.y, bubble.r)
            rg.setColorAt(0.0, QColor(255, 255, 255, bubble.alpha))
            rg.setColorAt(0.55, QColor(180, 255, 255, max(10, bubble.alpha - 25)))
            rg.setColorAt(1.0, QColor(255, 255, 255, 0))
            painter.setBrush(QBrush(rg))
            painter.setPen(QPen(QColor(255, 255, 255, 45), 1))
            painter.drawEllipse(int(bubble.x - bubble.r), int(bubble.y - bubble.r), bubble.r * 2, bubble.r * 2)

        # Błysk u góry
        painter.setBrush(QColor(255, 255, 255, 60))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(20, 20, self.width() - 40, 60, 24, 24)


class GlassCard(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setObjectName("glassCard")
        self.setFrameShape(QFrame.NoFrame)
        self.setAttribute(Qt.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 85, 120, 70))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(2, 2, -2, -2)

        # szkło
        glass = QLinearGradient(0, 0, 0, self.height())
        glass.setColorAt(0.0, QColor(255, 255, 255, 175))
        glass.setColorAt(0.35, QColor(240, 252, 255, 120))
        glass.setColorAt(1.0, QColor(210, 245, 255, 95))

        painter.setPen(QPen(QColor(255, 255, 255, 160), 1))
        painter.setBrush(glass)
        painter.drawRoundedRect(rect, 22, 22)

        # połysk
        shine_rect = QRect(rect.x() + 4, rect.y() + 4, rect.width() - 8, int(rect.height() * 0.33))
        shine = QLinearGradient(0, shine_rect.top(), 0, shine_rect.bottom())
        shine.setColorAt(0.0, QColor(255, 255, 255, 150))
        shine.setColorAt(1.0, QColor(255, 255, 255, 15))
        painter.setBrush(shine)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(shine_rect, 18, 18)

        super().paintEvent(event)


class HoverButton(QPushButton):
    def __init__(self, text="", accent=False, parent=None):
        super().__init__(text, parent)
        self._shift = 0
        self.accent = accent
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(42)
        self.anim = QPropertyAnimation(self, b"shift", self)
        self.anim.setDuration(180)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(22)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(50, 150, 255, 70 if accent else 45))
        self.setGraphicsEffect(shadow)

        if accent:
            self.setObjectName("accentButton")
        else:
            self.setObjectName("glassButton")

    def getShift(self):
        return self._shift

    def setShift(self, value):
        self._shift = value
        self.update()

    shift = property(getShift, setShift)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._shift)
        self.anim.setEndValue(2)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._shift)
        self.anim.setEndValue(0)
        self.anim.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        r = self.rect().adjusted(1, 1, -1, -1 + self._shift)

        if self.accent:
            grad = QLinearGradient(0, 0, 0, self.height())
            grad.setColorAt(0.0, QColor(255, 255, 255, 230))
            grad.setColorAt(0.08, QColor(220, 250, 255, 235))
            grad.setColorAt(0.5, QColor(95, 220, 255, 235))
            grad.setColorAt(1.0, QColor(50, 160, 255, 240))
            border = QColor(255, 255, 255, 180)
        else:
            grad = QLinearGradient(0, 0, 0, self.height())
            grad.setColorAt(0.0, QColor(255, 255, 255, 195))
            grad.setColorAt(0.45, QColor(220, 245, 255, 145))
            grad.setColorAt(1.0, QColor(170, 230, 255, 120))
            border = QColor(255, 255, 255, 160)

        painter.setBrush(grad)
        painter.setPen(QPen(border, 1))
        painter.drawRoundedRect(r, 16, 16)

        gloss = QRect(r.x() + 3, r.y() + 3, r.width() - 6, int(r.height() * 0.45))
        gloss_grad = QLinearGradient(0, gloss.top(), 0, gloss.bottom())
        gloss_grad.setColorAt(0.0, QColor(255, 255, 255, 160))
        gloss_grad.setColorAt(1.0, QColor(255, 255, 255, 10))
        painter.setBrush(gloss_grad)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(gloss, 14, 14)

        painter.setPen(QColor(15, 70, 90))
        font = self.font()
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(r, Qt.AlignCenter, self.text())


class GlowLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(38)
        self.setObjectName("glowLineEdit")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(255, 255, 255, 60))
        self.setGraphicsEffect(shadow)


class GlowComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(38)
        self.setObjectName("glowComboBox")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(255, 255, 255, 60))
        self.setGraphicsEffect(shadow)


class GlassListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("glassList")
        self.setAlternatingRowColors(False)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 100, 140, 45))
        self.setGraphicsEffect(shadow)


class SectionTitle(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("sectionTitle")
        font = QFont("Segoe UI", 12)
        font.setBold(True)
        self.setFont(font)


class AnimatedMessageBox(QMessageBox):
    def __init__(self, icon_type, title, text, parent=None):
        super().__init__(parent)
        self.setIcon(icon_type)
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Ok)
        self.setStyleSheet("""
            QMessageBox {
                background: rgba(220, 248, 255, 235);
            }
            QMessageBox QLabel {
                color: rgb(20, 70, 90);
                font-size: 14px;
            }
            QMessageBox QPushButton {
                min-width: 90px;
                min-height: 34px;
                border-radius: 12px;
                padding: 6px 12px;
                border: 1px solid rgba(255,255,255,170);
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 rgba(255,255,255,220),
                    stop:1 rgba(90,210,255,210));
                color: rgb(20,60,80);
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 rgba(255,255,255,235),
                    stop:1 rgba(60,190,255,230));
            }
        """)

    def showEvent(self, event):
        super().showEvent(event)
        self.setWindowOpacity(0.0)
        self.anim = QPropertyAnimation(self, b"windowOpacity", self)
        self.anim.setDuration(250)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dziennik • Bohdan Susulovskyi • Frutiger Aero Edition")
        self.setMinimumSize(1180, 760)
        ensure_json_file()

        self.bg = AeroBackground(self)
        self.setCentralWidget(self.bg)

        self.root_layout = QVBoxLayout(self.bg)
        self.root_layout.setContentsMargins(26, 22, 26, 22)
        self.root_layout.setSpacing(18)

        self.build_header()
        self.build_tabs_area()
        self.apply_global_style()
        self.center_on_screen()

        self.refresh_all()
        #self.start_opening_animation()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bg.setGeometry(self.rect())

    def center_on_screen(self):
        screen = QDesktopWidget().availableGeometry().center()
        geo = self.frameGeometry()
        geo.moveCenter(screen)
        self.move(geo.topLeft())

    def build_header(self):
        header = GlassCard()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        header_layout.setSpacing(2)

        title = QLabel("Dziennik ocen")
        title.setObjectName("mainTitle")

        subtitle = QLabel("PyQt5 • JSON • Frutiger Aero • szkło, światło, gradienty i animacje")
        subtitle.setObjectName("subTitle")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        self.root_layout.addWidget(header)

    def build_tabs_area(self):
        outer = GlassCard()
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(14, 14, 14, 14)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(False)

        self.tab_students = QWidget()
        self.tab_przedmioty = QWidget()
        self.tab_rygory = QWidget()
        self.tab_oceny = QWidget()

        self.tabs.addTab(self.tab_students, "Studenci")
        self.tabs.addTab(self.tab_przedmioty, "Przedmioty")
        self.tabs.addTab(self.tab_rygory, "Rygory")
        self.tabs.addTab(self.tab_oceny, "Oceny")

        outer_layout.addWidget(self.tabs)
        self.root_layout.addWidget(outer, 1)

        self.build_students_tab()
        self.build_przedmioty_tab()
        self.build_rygory_tab()
        self.build_oceny_tab()

    def apply_global_style(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                font-family: "Segoe UI";
                color: rgb(18, 67, 84);
            }

            QLabel#mainTitle {
                font-size: 28px;
                font-weight: 700;
                color: rgb(15, 86, 112);
            }

            QLabel#subTitle {
                font-size: 12px;
                color: rgba(20, 75, 90, 190);
            }

            QLabel#sectionTitle {
                font-size: 18px;
                font-weight: 700;
                color: rgb(20, 82, 100);
                padding: 4px 2px 10px 2px;
            }

            QTabWidget::pane {
                border: 1px solid rgba(255,255,255,120);
                background: rgba(255,255,255,55);
                border-radius: 18px;
                top: -1px;
            }

            QTabBar::tab {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 rgba(255,255,255,180),
                    stop:1 rgba(190,245,255,110));
                border: 1px solid rgba(255,255,255,130);
                padding: 12px 18px;
                margin-right: 8px;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                color: rgb(20, 74, 92);
                font-weight: bold;
                min-width: 120px;
            }

            QTabBar::tab:selected {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 rgba(255,255,255,235),
                    stop:1 rgba(110,220,255,160));
                color: rgb(12, 76, 102);
            }

            QTabBar::tab:hover {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 rgba(255,255,255,215),
                    stop:1 rgba(140,230,255,145));
            }

            QLabel {
                background: transparent;
            }

            QFrame#glassCard {
                background: transparent;
                border-radius: 22px;
            }

            QLineEdit#glowLineEdit, QComboBox#glowComboBox {
                background: rgba(255,255,255,180);
                border: 1px solid rgba(255,255,255,165);
                border-radius: 14px;
                padding: 8px 12px;
                color: rgb(15, 68, 85);
                selection-background-color: rgba(80, 200, 255, 140);
                font-size: 13px;
            }

            QLineEdit#glowLineEdit:focus, QComboBox#glowComboBox:focus {
                background: rgba(255,255,255,220);
                border: 1px solid rgba(60, 205, 255, 180);
            }

            QComboBox::drop-down {
                border: none;
                width: 28px;
                background: transparent;
            }

            QComboBox QAbstractItemView {
                border: 1px solid rgba(255,255,255,150);
                border-radius: 12px;
                background: rgba(225,248,255,240);
                selection-background-color: rgba(105,220,255,150);
                color: rgb(15, 70, 88);
                padding: 6px;
            }

            QListWidget#glassList {
                background: rgba(255,255,255,145);
                border: 1px solid rgba(255,255,255,140);
                border-radius: 18px;
                padding: 8px;
                outline: none;
                font-size: 13px;
            }

            QListWidget#glassList::item {
                background: rgba(255,255,255,95);
                border: 1px solid rgba(255,255,255,70);
                border-radius: 12px;
                margin: 5px 3px;
                padding: 12px;
                color: rgb(16, 72, 90);
            }

            QListWidget#glassList::item:selected {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 rgba(255,255,255,210),
                    stop:1 rgba(120,240,255,160));
                border: 1px solid rgba(90,220,255,120);
                color: rgb(10, 70, 95);
            }

            QListWidget#glassList::item:hover {
                background: rgba(240,255,255,150);
            }

            QSplitter::handle {
                background: rgba(255,255,255,80);
                border-radius: 4px;
                margin: 8px 0;
            }
        """)

    def create_form_card(self, title_text):
        card = GlassCard()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(SectionTitle(title_text))
        return card, layout

    def create_list_card(self, title_text):
        card = GlassCard()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(SectionTitle(title_text))
        return card, layout

    def animated_splitter(self, left_widget, right_widget):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([380, 700])
        return splitter

    def show_error(self, text):
        msg = AnimatedMessageBox(QMessageBox.Critical, "Błąd", text, self)
        msg.exec_()

    def show_info(self, text):
        msg = AnimatedMessageBox(QMessageBox.Information, "Informacja", text, self)
        msg.exec_()

    def start_opening_animation(self):
        self.opacity_effect = QGraphicsOpacityEffect(self.overlay)
        self.overlay.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

        start_geo = self.overlay.geometry()
        moved_geo = QRect(
            start_geo.x(),
            start_geo.y() + 25,
            start_geo.width(),
            start_geo.height()
        )

        self.anim_opacity = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        self.anim_opacity.setDuration(700)
        self.anim_opacity.setStartValue(0.0)
        self.anim_opacity.setEndValue(1.0)
        self.anim_opacity.setEasingCurve(QEasingCurve.OutCubic)

        self.anim_geo = QPropertyAnimation(self.overlay, b"geometry", self)
        self.anim_geo.setDuration(700)
        self.anim_geo.setStartValue(moved_geo)
        self.anim_geo.setEndValue(start_geo)
        self.anim_geo.setEasingCurve(QEasingCurve.OutCubic)

        self.open_group = QParallelAnimationGroup(self)
        self.open_group.addAnimation(self.anim_opacity)
        self.open_group.addAnimation(self.anim_geo)
        self.open_group.start()

    def refresh_all(self):
        self.refresh_students()
        self.refresh_przedmioty()
        self.refresh_rygory()
        self.refresh_oceny_combo()
        self.refresh_oceny_lista()

    # =========================
    # STUDENCI
    # =========================
    def build_students_tab(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)

        left_card, left_outer = self.create_form_card("Dodawanie studenta")
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setSpacing(12)

        self.student_name_input = GlowLineEdit()
        self.student_wiek_input = GlowLineEdit()
        self.student_grupa_input = GlowLineEdit()

        add_student_btn = HoverButton("Dodaj studenta", accent=True)
        add_student_btn.clicked.connect(self.add_student)

        form.addRow("Imię i nazwisko:", self.student_name_input)
        form.addRow("Wiek:", self.student_wiek_input)
        form.addRow("Grupa:", self.student_grupa_input)
        left_outer.addLayout(form)
        left_outer.addWidget(add_student_btn)

        right_card, right_outer = self.create_list_card("Lista studentów")
        self.student_list = GlassListWidget()

        delete_student_btn = HoverButton("Usuń zaznaczonego studenta")
        delete_student_btn.clicked.connect(self.delete_student)

        right_outer.addWidget(self.student_list)
        right_outer.addWidget(delete_student_btn)

        splitter = self.animated_splitter(left_card, right_card)
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

    # =========================
    # PRZEDMIOTY
    # =========================
    def build_przedmioty_tab(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)

        left_card, left_outer = self.create_form_card("Dodawanie przedmiotu")
        form = QFormLayout()
        form.setSpacing(12)

        self.przedmiot_input = GlowLineEdit()

        add_subject_btn = HoverButton("Dodaj przedmiot", accent=True)
        add_subject_btn.clicked.connect(self.add_subject)

        form.addRow("Nazwa przedmiotu:", self.przedmiot_input)
        left_outer.addLayout(form)
        left_outer.addWidget(add_subject_btn)

        right_card, right_outer = self.create_list_card("Lista przedmiotów")
        self.przedmiot_lista = GlassListWidget()

        delete_subject_btn = HoverButton("Usuń zaznaczony przedmiot")
        delete_subject_btn.clicked.connect(self.delete_subject)

        right_outer.addWidget(self.przedmiot_lista)
        right_outer.addWidget(delete_subject_btn)

        splitter = self.animated_splitter(left_card, right_card)
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

    # =========================
    # RYGORY
    # =========================
    def build_rygory_tab(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)

        left_card, left_outer = self.create_form_card("Dodawanie rygoru")
        form = QFormLayout()
        form.setSpacing(12)

        self.nazwa_rygoru = GlowLineEdit()

        add_rygor_btn = HoverButton("Dodaj rygor", accent=True)
        add_rygor_btn.clicked.connect(self.add_rygor)

        form.addRow("Nazwa rygoru:", self.nazwa_rygoru)
        left_outer.addLayout(form)
        left_outer.addWidget(add_rygor_btn)

        right_card, right_outer = self.create_list_card("Lista rygorów")
        self.rygor_list = GlassListWidget()

        delete_rygor_btn = HoverButton("Usuń zaznaczony rygor")
        delete_rygor_btn.clicked.connect(self.delete_rygor)

        right_outer.addWidget(self.rygor_list)
        right_outer.addWidget(delete_rygor_btn)

        splitter = self.animated_splitter(left_card, right_card)
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

    # =========================
    # OCENY
    # =========================
    def build_oceny_tab(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)

        left_card, left_outer = self.create_form_card("Dodawanie oceny")
        form = QFormLayout()
        form.setSpacing(12)

        self.ocena_studentcombo = GlowComboBox()
        self.ocena_przedmiotcombo = GlowComboBox()
        self.ocena_rygorcombo = GlowComboBox()
        self.ocena_termincombo = GlowLineEdit()
        self.ocena_ocena = GlowLineEdit()

        add_grade_btn = HoverButton("Dodaj ocenę", accent=True)
        add_grade_btn.clicked.connect(self.add_grade)

        form.addRow("Student:", self.ocena_studentcombo)
        form.addRow("Przedmiot:", self.ocena_przedmiotcombo)
        form.addRow("Rygor:", self.ocena_rygorcombo)
        form.addRow("Termin (YYYY-MM-DD):", self.ocena_termincombo)
        form.addRow("Ocena:", self.ocena_ocena)

        left_outer.addLayout(form)
        left_outer.addWidget(add_grade_btn)

        right_card, right_outer = self.create_list_card("Lista ocen")
        self.lista_ocen = GlassListWidget()

        usun_ocene = HoverButton("Usuń zaznaczoną ocenę")
        usun_ocene.clicked.connect(self.usun_ocene)

        right_outer.addWidget(self.lista_ocen)
        right_outer.addWidget(usun_ocene)

        splitter = self.animated_splitter(left_card, right_card)
        layout.addWidget(splitter)
        self.tab_oceny.setLayout(layout)

    def refresh_oceny_combo(self):
        data = load_data()

        self.ocena_studentcombo.clear()
        self.ocena_przedmiotcombo.clear()
        self.ocena_rygorcombo.clear()

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

        oceny = Oceny(subject_id, rygor_id, student_id, term, grade_value)
        oceny.dodawanie_oceny()

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

        target = None
        for g in data["ocenyNazwy"]:
            if g.get("ocenyNazwyId") == ocenanazwy_id:
                target = g
                break

        if target is None:
            self.show_error("Nie znaleziono oceny.")
            return

        data["ocenyNazwy"] = [
            g for g in data["ocenyNazwy"]
            if g.get("ocenyNazwyId") != ocenanazwy_id
        ]

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
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()