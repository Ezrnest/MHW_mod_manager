from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QScrollArea, QMessageBox

from ManagerCore import ManagerCore


def getConfigGeo(core: ManagerCore, *keys):
    t = core.getConfigEntry(*keys)
    if t is None:
        return None
    try:
        return QRect(*(int(x) for x in str(t).split(",")))
    except ValueError:
        return None


def setConfigGeo(core: ManagerCore, geo: QRect, *keys):
    v = f"{geo.x()},{geo.y()},{geo.width()},{geo.height()}"
    core.setConfigEntry(v,*keys)


def information(parent, title, text):
    # Create a QMessageBox
    m = QMessageBox(parent)
    m.setWindowTitle(title)
    m.setText(text)
    m.setIcon(QMessageBox.Information)
    m.setStandardButtons(QMessageBox.Ok)
    m.setDetailedText(text)
    m.exec_()