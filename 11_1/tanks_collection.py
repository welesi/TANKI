from random import randint
from units import Tank
import world
import missiles_collection
from tkinter import NW

_tanks = []
_canvas = None

id_screen_text = 0

FPS = 60

_game_paused = False
_menu_active = False

_game_loop_id = None  # Глобальная переменная для хранения идентификатора цикла


def initialize(canv):
    global _canvas, id_screen_text
    _canvas = canv

    player = spawn(False)
    enemy = spawn(True).set_target(player)


    for _ in range(3):
        enemy = spawn(True)
        enemy.set_target(player)

    id_screen_text = _canvas.create_text(10, 10, text=_get_screen_text(), font=('TkDefaultFont', 20), fill='white',
                                         anchor=NW)


def _get_screen_text():
    if get_player().is_destroyed():
        return 'Game Over!'
    if len(_tanks) == 1:
        return 'You Win!'
    return 'Осталось: {}'.format(len(_tanks) - 1)


def _update_screen_text():
    _canvas.itemconfig(id_screen_text, text=_get_screen_text())


def get_player():
    return _tanks[0]


def update():
    _update_screen_text()

    start = len(_tanks) - 1

    for i in range(start, -1, -1):
        if _tanks[i].is_destroyed() and i != 0:
            del _tanks[i]
        else:
            _tanks[i].update()
            check_collision(_tanks[i])
            missiles_collection.check_missiles_collision(_tanks[i])

    missiles_collection.update()


def check_collision(tank):
    for other_tank in _tanks:
        if tank == other_tank:
            continue
        if tank.intersects(other_tank):
            return True
    return False


def spawn(is_bot=True):
    cols = world.get_cols()
    rows = world.get_rows()

    while True:
        col = randint(1, cols - 1)
        row = randint(1, rows - 1)

        if world.get_block(row, col) != world.GROUND:
            continue

        t = Tank(_canvas, row, col, bot=is_bot)
        if not check_collision(t):
            _tanks.append(t)
            return t


def pause_game():
    global _game_paused
    _game_paused = True


def resume_game():
    global _game_paused
    _game_paused = False
    start_update_loop()


def set_game_paused(paused):
    global _game_paused
    _game_paused = paused


def set_menu_active(active):
    global _menu_active
    _menu_active = active


def start_update_loop(): # Запуск игрового цикла (продолжает игру)
    global _game_loop_id

    if _game_loop_id is not None:  # Если цикл уже идёт, остановить его
        _canvas.after_cancel(_game_loop_id)
        _game_loop_id = None

    def loop(): # Функция одного кадра игры
        global _game_loop_id
        if _game_paused or _menu_active or get_player().is_destroyed():
            return
        update()
        _game_loop_id = _canvas.after(1000 // FPS, loop)


    _game_loop_id = _canvas.after(1000 // FPS, loop)  # Запускаем основной цикл


def reset(): # Перезапуск всей игры (удаляет старые объекты и создаёт новые)
    global _tanks, id_screen_text, _menu_active, _game_paused, _game_loop_id

    _menu_active = False
    _game_paused = False

    if _game_loop_id is not None: # Если игровой процесс уже запущен
        _canvas.after_cancel(_game_loop_id)
        _game_loop_id = None

    _tanks = []

    if id_screen_text is not None:
        _canvas.delete(id_screen_text)
        id_screen_text = None

    initialize(_canvas)
    start_update_loop()  # Возвращаем нормальную скорость