from units import Missile

_missiles = []
_canvas = None


def initialize(canvas):
    global _canvas
    _canvas = canvas


def fire(owner):
    m = Missile(_canvas, owner)
    _missiles.append(m)


def update():
    start = len(_missiles) - 1
    for i in range(start, -1, -1):
        if _missiles[i].is_destroyed():
            del _missiles[i]
        else:
            _missiles[i].update()