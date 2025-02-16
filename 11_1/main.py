from tkinter import *
import missiles_collection
import world
import tanks_collection
import texture
import pause_menu

KEY_UP, KEY_DOWN = 38, 40
KEY_W, KEY_S, KEY_A, KEY_D = 87, 83, 65, 68
SPACE = 32
PLUS = 187
ESC = 27
TAB = 9

FPS = 60


def key_press(event):
    player = tanks_collection.get_player()

    if player.is_destroyed() or pause_menu.menu_active:
        pause_menu.menu_key_press(event, w)
        return

    if not pause_menu.menu_active:
        if event.keycode == KEY_W:
            player.forward()
        elif event.keycode == KEY_S:
            player.backward()
        elif event.keycode == KEY_A:
            player.left()
        elif event.keycode == KEY_D:
            player.right()
        elif event.keycode == SPACE:
            player.fire()
        elif event.keycode == PLUS:
            tanks_collection.spawn()
        elif event.keycode == ESC:
            pause_menu.show_menu(w)
        elif event.keycode == TAB:
            pause_menu.toggle_pause()


def update():
    player = tanks_collection.get_player()
    if player.is_destroyed():
        pause_menu.show_menu(w)
        return

    if not pause_menu.game_paused and not pause_menu.menu_active:
        tanks_collection.update()
        missiles_collection.update()
        world.set_camera_xy(player.get_x() - world.SCREEN_WIDTH // 2 + player.get_size() // 2,
                            player.get_y() - world.SCREEN_HEIGHT // 2 + player.get_size() // 2)
        world.update_map()
    w.after(1000 // FPS, update)


def load_textures():
    texture.load('tank_down', '../img/tank_down.png')
    texture.load('tank_up', '../img/tank_up.png')
    texture.load('tank_left', '../img/tank_left.png')
    texture.load('tank_right', '../img/tank_right.png')
    texture.load('tank_down_player', '../img/tank_down_player.png')
    texture.load('tank_up_player', '../img/tank_up_player.png')
    texture.load('tank_left_player', '../img/tank_left_player.png')
    texture.load('tank_right_player', '../img/tank_right_player.png')

    texture.load(world.BRICK, '../img/brick.png')
    texture.load(world.WATER, '../img/water.png')
    texture.load(world.CONCRETE, '../img/wall.png')
    texture.load(world.MISSILE, '../img/bonus.png')

    texture.load('missile_up', '../img/missile_up.png')
    texture.load('missile_down', '../img/missile_down.png')
    texture.load('missile_left', '../img/missile_left.png')
    texture.load('missile_right', '../img/missile_right.png')
    texture.load('tank_destroy', '../img/tank_destroy.png')

w = Tk()
load_textures()
w.title('Танки на минималках 2.0')
canv = Canvas(w, width=world.SCREEN_WIDTH, height=world.SCREEN_HEIGHT, bg='#8ccb5e')
canv.pack()

world.initialize(canv)
tanks_collection.initialize(canv)
missiles_collection.initialize(canv)

w.bind('<KeyPress>', key_press)
update()
w.mainloop()