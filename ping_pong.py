from pygame import *
from random import randint
from time import time as timer
#подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.Font(None, 80)
winl = font1.render('LEFT PLAYER WIN!', True, (255, 255, 255))
winr = font1.render('RIGHT PLAYER WIN!', True, (255, 255, 255))
losel = font1.render('LEFT PLAYER LOSE!', True, (180, 0, 0))
loser = font1.render('RIGHT PLAYER LOSE!', True, (180, 0, 0))

#нам нужны такие картинки:
img_hero = "rocket.png" #герой
img_enemy = "ufo.png" #враг
img_racket = "racket.png"
img_tennis_ball = "tenis_ball.png"

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

win_width = 700
win_height = 500
display.set_caption("Ping-pong")
window = display.set_mode((win_width, win_height))
speed_x = 3
speed_y = 3

class RacketLeft(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 95:
            self.rect.y += self.speed

class RacketRight(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 95:
            self.rect.y += self.speed

racket_left = RacketLeft(img_racket, 75, 100, 25, 100, 10)
racket_right = RacketRight(img_racket, 625, 100, 25, 100, 10)
tennis_ball = GameSprite(img_tennis_ball, 200, 200, 50, 50, 10)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
clock = time.Clock()
while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:

        tennis_ball.rect.x += speed_x
        tennis_ball.rect.y += speed_y

        if tennis_ball.rect.y >= win_height - 50 or tennis_ball.rect.y <= 0:
            speed_y *= -1

        if sprite.collide_rect(tennis_ball, racket_left) or sprite.collide_rect(tennis_ball, racket_right):
            speed_x *= -1

        window.fill((255, 0, 70))
        racket_left.update_l()
        racket_right.update_r()
        racket_left.reset()
        racket_right.reset()
        tennis_ball.reset()

        if tennis_ball.rect.x <= 0:
            window.blit(losel, (70, 200))
            finish = True

        if tennis_ball.rect.x >= win_width - 25:
            window.blit(loser, (70, 200))
            finish = True

    clock.tick(40)
    display.update()
