from PyQt5.QtCore import QRect

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
