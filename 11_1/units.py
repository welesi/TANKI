import os
from hitbox import Hitbox
from tkinter import NW, PhotoImage
from random import randint

import missiles_collection
import world
import  texture as skin

img_dir = os.path.abspath(os.path.dirname(__file__))  # Текущая директория файла
img_dir = os.path.join(img_dir, "img")  # Путь к папке с изображениями
class Unit:
    def __init__(self, canvas, x,y, speed, padding,
                 bot, default_image):
        self._speed = speed
        self._x = x
        self._y = y
        self._vx = 0
        self._vy = 0
        self._canvas = canvas
        self._hp = 100
        self._dx = 0
        self._dy = 0
        self._bot = bot
        self._hitbox = Hitbox(x,y,world.BLOCK_SIZE,world.BLOCK_SIZE,
                              padding=padding)

        self._destroyed = False

        self._default_image = default_image
        self._left_image = default_image
        self._right_image = default_image
        self._forward_image = default_image
        self._backward_image = default_image
        self._destroy_image = default_image

        # img_dir = os.path.abspath(os.path.dirname(__file__))  # Текущая директория файла
        # img_dir = os.path.join(img_dir, "img")  # Путь к папке с изображениями

        # Загрузка изображений HP с указанием пути
        # self.hp_100 = PhotoImage(file=os.path.join(img_dir, "100.png"))
        # self.hp_75 = PhotoImage(file=os.path.join(img_dir, "75.png"))
        # self.hp_50 = PhotoImage(file=os.path.join(img_dir, "50.png"))
        # self.hp_25 = PhotoImage(file=os.path.join(img_dir, "25.png"))
        # self.hp_0 = PhotoImage(file=os.path.join(img_dir, "0.png"))

        self._hp_id = None
        #
        self._create()
        # self.current_texture = self.textures[100]
        # self.rect = self.current_texture.get_rect()
        # self.update_position(parent_rect)

    def _create(self):
        self._id = self._canvas.create_image(self._x, self._y, image=skin.get(self._default_image), anchor=NW)
        # self._hp_id = self._canvas.create_image(self._x, self._y - 20, image=self.hp_100, anchor=NW)

    def _update_hp_display(self):
        """Обновляет изображение HP в зависимости от текущего здоровья."""
        if self._hp_id is not None:
            if self._hp > 75:
                hp_image = self.hp_100
            elif self._hp > 50:
                hp_image = self.hp_75
            elif self._hp > 25:
                hp_image = self.hp_50
            elif self._hp > 0:
                hp_image = self.hp_25
            else:
                hp_image = self.hp_0

            screen_x = world.get_screen_x(self._x)
            screen_y = world.get_screen_y(self._y - 20)
            self._canvas.moveto(self._hp_id, x=screen_x, y=screen_y)
            self._canvas.itemconfig(self._hp_id, image=hp_image)


    def __del__(self):
        try:
            self._canvas.delete(self._id)
        except Exception:
            pass


    def forward(self):
        self._vx = 0
        self._vy = -1
        self._canvas.itemconfig(self._id, image=skin.get(self._forward_image))


    def backward(self):
        self._vx = 0
        self._vy = 1
        self._canvas.itemconfig(self._id, image=skin.get(self._backward_image))


    def left(self):
        self._vx = -1
        self._vy = 0
        self._canvas.itemconfig(self._id, image=skin.get(self._left_image))


    def right(self):
        self._vx = 1
        self._vy = 0
        self._canvas.itemconfig(self._id, image=skin.get(self._right_image))


    def get_destroy_image(self):
        return self._destroy_image


    def stop(self):
        self._vx = 0
        self._vy = 0


    def update(self):
        if self._bot:
            self._AI()
        self._dx = self._vx * self._speed
        self._dy = self._vy * self._speed
        self._x += self._dx
        self._y += self._dy
        self._update_hitbox()
        self._check_map_collision()
        self._repaint()
        self._update_hp_display()


    def _AI(self):
        pass


    def _update_hitbox(self):
        self._hitbox.moveto(self._x, self._y)


    def _check_map_collision(self):
        details = {}
        result = self._hitbox.check_map_collision(details)
        if result:
            self._on_map_collision(details)
        else:
            self._no_map_collision()


    def _no_map_collision(self):
        pass


    def _on_map_collision(self, details):
        pass


    def _repaint(self):
        screen_x = world.get_screen_x(self._x)
        screen_y = world.get_screen_y(self._y)
        self._canvas.moveto(self._id, x=screen_x, y=screen_y)


    def _undo_move(self):
        if self._dx == 0 and self._dy == 0:
            return
        self._x -= self._dx
        self._y -= self._dy
        self._update_hitbox()
        self._repaint()
        self._dx = 0
        self._dy = 0


    def intersects(self, other_unit):
        value = self._hitbox.intersects(other_unit._hitbox)
        if value:
            self._on_intersects(other_unit)
        return value


    def _on_intersects(self, other_unit):
        self._undo_move()


    def _change_orientation(self):
        rand = randint(0, 3)
        if rand == 0:
            self.left()
        elif rand == 1:
            self.forward()
        elif rand == 2:
            self.right()
        elif rand == 3:
            self.backward()


    def get_hp(self):
        return self._hp


    def get_speed(self):
        return self._speed


    def get_x(self):
        return self._x


    def get_y(self):
        return self._y


    def get_vx(self):
        return self._vx


    def get_vy(self):
        return self._vy


    def get_size(self):
        return world.BLOCK_SIZE


    def is_bot(self):
        return self._bot


    def damage(self, value):
        self._hp -= value
        if self._hp <= 0:
            self.destroy()
        self._update_hp_display()


    def is_destroyed(self):
        return self._destroyed


    def destroy(self):
        self._destroyed = True
        self.stop()
        self._speed = 0

        if not self._bot:
            self._canvas.itemconfig(self._id, image=skin.get(self._destroy_image))


class Tank(Unit):
    def __init__(self, canvas, row, col, bot=True):
        super().__init__(canvas,
                         col*world.BLOCK_SIZE,
                         row*world.BLOCK_SIZE,
                         2,
                         8,
                         bot,'tank_up')
        if bot:
            self._forward_image = 'tank_up'
            self._backward_image = 'tank_down'
            self._left_image = 'tank_left'
            self._right_image = 'tank_right'
        else:
            self._forward_image = 'tank_up_player'
            self._backward_image = 'tank_down_player'
            self._left_image = 'tank_left_player'
            self._right_image = 'tank_right_player'

            self._destroy_image = 'tank_destroy'



        self.forward()
        self._ammo = 80
        self._usual_speed = self._speed
        self._water_speed = self._speed//2
        self._target = None


    def set_target(self, target):
        self._target = target


    def _AI_goto_target(self):
        if randint(1,2) == 1:
            if self._target.get_x() < self.get_x():
                self.left()
            else:
                self.right()
        else:
            if self._target.get_y() < self.get_y():
                self.forward()
            else:
                self.backward()


    def _AI(self):
        if randint(1,30) ==1:
            if randint(1,10) < 9 and self._target is not None:
                self._AI_goto_target()
            else:
                self._change_orientation()
        elif randint(1,30) == 1:
            self._AI_fire()
        elif randint(1,100) == 1:
            self.fire()


    def _AI_fire(self):
        if self._target is None:
            return

        center_x = self.get_x() + self.get_size()//2
        center_y = self.get_y() + self.get_size() // 2

        target_center_x = self._target.get_x() + self._target.get_size()//2
        target_center_y = self._target.get_y() + self._target.get_size() // 2

        row = world.get_row(center_y)
        col = world.get_col(center_x)

        row_target = world.get_row(target_center_y)
        col_target = world.get_col(target_center_x)

        if row == row_target:
            if col_target < col:
                self.left()
                self.fire()
            else:
                self.right()
                self.fire()

        elif col == col_target:
            if row_target < row:
                self.forward()
                self.fire()
            else:
                self.backward()
                self.fire()


    def fire(self):
        if self._ammo > 0:
            self._ammo -= 1
            missiles_collection.fire(self)


    def _take_ammo(self):
        self._ammo += 10
        if self._ammo > 100:
            self._ammo = 100


    def get_ammo(self):
        return self._ammo


    def _set_usual_speed(self):
        self._speed = self._usual_speed


    def _set_water_speed(self):
        self._speed = self._water_speed


    def _on_map_collision(self, details):
        if world.WATER in details and len(details) == 1:
            self._set_water_speed()
        elif world.MISSILE in details:
            pos = details[world.MISSILE]
            if world.take(pos['row'], pos['col'])!= world.AIR:
                self._take_ammo()
        else:
            self._undo_move()
            if self._bot:
                self._change_orientation()


    def _no_map_collision(self):
        self._set_usual_speed()


    def _on_intersects(self, other_unit):
        super()._on_intersects(other_unit)
        if self._bot:
            self._change_orientation()


class Missile(Unit):
    def __init__(self, canvas, owner):
        super().__init__(canvas, owner.get_x(), owner.get_y(), 6, 20, False, 'missile_up')


        self._forward_image = 'missile_up'
        self._backward_image = 'missile_down'
        self._left_image = 'missile_left'
        self._right_image = 'missile_right'
        self._owner = owner

        self.__black_list = [world.CONCRETE, world.BRICK, world.WATER, world.MISSILE]


        if owner.get_vx() == 1 and owner.get_vy() == 0:
            self.right()
        elif owner.get_vx() == -1 and owner.get_vy() == 0:
            self.left()

        elif owner.get_vx() == 0 and owner.get_vy() == -1:
            self.forward()
        elif owner.get_vx() == 0 and owner.get_vy() == 1:
            self.backward()


        self._x += owner.get_vx() * self.get_size() // 2
        self._y += owner.get_vy() * self.get_size() // 2


    def _create(self):
        # Переопределяем метод, чтобы не создавать _hp_id для снарядов
        self._id = self._canvas.create_image(self._x, self._y, image=skin.get(self._default_image), anchor=NW)


    def get_owner(self):
        return self._owner


    def _on_map_collision(self, details):
        if world.BRICK in details:
            row = details[world.BRICK]['row']
            col = details[world.BRICK]['col']
            world.destroy(row, col)
            self.destroy()

        if world.CONCRETE in details:
            self.destroy()
















