from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

   

class Musuh(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, musuh_speed, musuh_jarak_x):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = musuh_speed
        self.x = musuh_jarak_x

    side = "left"

    def update(self):
        if self.rect.x <= self.x:
            self.side = "right"
        if self.rect.x >= win_width - 80:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, bullet_image, x, y, width, height, bullet_speed):
        GameSprite.__init__(self, bullet_image, x, y, width, height)
        self.speed = bullet_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()
    

win_height = 500
win_width = 700

window = display.set_mode((win_width, win_height))
display.set_caption("The Maze")

backround_color = (130, 143, 148)

class player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed_x, speed_y):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = speed_x
        self.y_speed = speed_y
    
    def update(self):
        if hero.rect.x <= win_width - 80 and hero.x_speed > 0 or hero.rect.x >= 0 and hero.x_speed < 0:
            self.rect.x += self.x_speed
        platform_touched = sprite.spritecollide(self, wall, False)
        if self.x_speed > 0:
            for p in platform_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if hero.rect.y <= win_height - 80 and hero.y_speed > 0 or hero.rect.y >= 0 and hero.y_speed < 0:
            self.rect.y += self.y_speed

        platform_touched = sprite.spritecollide(self, wall, False)
        if self.y_speed > 0:
            for i in platform_touched:
                self.rect.bottom = min(self.rect.bottom, i.rect.top)
        elif self.y_speed < 0:
                for i in platform_touched:
                    self.rect.top = max(self.rect.top, i.rect.bottom)
    def fire(self):
        bullet  = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
        

wall = sprite.Group()
w1 = GameSprite("platform2.png", 80, 220, 300, 50)
w2 = GameSprite("platform2_v.png", 370, 100, 50, 400)
w3 = GameSprite("platform2_v.png", 100, -260, 50, 400)
w4 = GameSprite("platform2.png", -70, 365, 350, 50)
#w2 = GameSprite("platform2_v.png", 370, 100, 50, 400)
#w2 = GameSprite("platform2_v.png", 370, 100, 50, 400)
#w2 = GameSprite("platform2_v.png", 370, 100, 50, 400)
#w2 = GameSprite("platform2_v.png", 370, 100, 50, 400)


wall.add(w1)
wall.add(w2)
wall.add(w3, w4)

monsters = sprite.Group()

enemy1 = Musuh('cyborg.png', win_width -80, 10, 80, 80, 5, 140)
enemy2 = Musuh('cyborg.png', win_width -80, 230, 80, 80, 5, 420)

monsters.add(enemy1)
monsters.add(enemy2)

bullets = sprite.Group()

hero = player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
#enemy = GameSprite("cyborg.png", win_width - 85, 100, 80, 80)
final_sprite = GameSprite("pac-1.png", win_width - 85, win_height - 85, 80, 80)

run = True
finish = False

while run:
    time.delay(50)

    

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                hero.x_speed = -5
            elif e.key == K_RIGHT:
                hero.x_speed = 5
            elif e.key == K_UP:
                hero.y_speed = -5
            elif e.key == K_DOWN:
                hero.y_speed = 5
            elif e.key == K_SPACE:
                hero.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                hero.x_speed = 0
            elif e.key == K_RIGHT:
                hero.x_speed = 0
            elif e.key == K_UP:
                hero.y_speed = 0
            elif e.key == K_DOWN:
                hero.y_speed = 0

    if not finish:
        window.fill(backround_color)

        
        final_sprite.reset()
        wall.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        monsters.update()
        hero.update()

        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(wall, bullets, False, True)

        hero.reset()
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            img = image.load("game-over_1.png")
            window.fill((255, 255, 255))
            window.blit(transform.scale(img,(win_width, win_height)), (0,0))
        
        if sprite.collide_rect(hero, final_sprite):
            finish = True
            img2 = image.load("thumb.jpg")
            window.fill((255, 255, 255))
            window.blit(transform.scale(img2,(win_width, win_height)), (0,0))



    display.update()
