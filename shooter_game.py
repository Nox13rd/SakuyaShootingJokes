#Create your own shooter
from pygame import *
from random import randint
# create screen object (window)
_WIDTH = 800
_HEIGHT = 640
font.init()
mixer.init()
window = display.set_mode((_WIDTH, _HEIGHT))
# create clock object
clock = time.Clock()
# create any element of the game
class ImageSprite(sprite.Sprite):
    def __init__(self, image_file, position, size, speed=(0,0)):
        super().__init__()
        self.speed = Vector2(speed)
        self.rect = Rect(position, size)
        self.initial_position = position
        self.image = image.load(image_file)
        self.image = transform.scale(self.image, size)
    def reset(self):
        self.rect.topleft = self.initial_position
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)



class Player(ImageSprite):
    def set_lives(self, lives):
        self.lives = lives
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed.x
        if keys[K_d]:
            self.rect.x += self.speed.x
        if self.rect.right < 0:
            self.rect.left = _WIDTH
        if self.rect.left > _WIDTH:
            self.rect.right = 0
    def is_touching(self, target):
        return sprite.collide_rect(self, target)
    def shoot(self, Projectile):
        fire_sound.play() 
        p = Projectile()
        p.rect.center = self.rect.midtop
        projectiles.add(p)

class Knife(ImageSprite):
    def __init__(self):
        super().__init__("knife.png", (0,0), (25, 45), (0, -30))
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Fairy(ImageSprite):
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.top > _HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, _WIDTH - self.rect.width)

class Boss(ImageSprite):
    def __init__(self, image_file, position, size, speed = (0,0)):
        super().__init__(image_file, position, size, speed)
        self.respawn = 35
        self.incarnate = 1
        self.hitpoints = 5
        self.status = "ALIVE"
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.left < 0 or self.rect.right > _WIDTH:
            self.speed.x *=  -1
    def shoot(self):
        if self.status == "ALIVE":
            p = BallProjecile(self.rect.center, (0, 4))
            boss_projectiles.add(p)
    def reincarnate(self):
        self.incarnate += 1
        self.hitpoins = 5 * (self.incarnate+1)
        self.respawn = 30
        self.status = "ALIVE"
        


class BallProjecile(ImageSprite):
    def __init__(self, position, speed):
        super().__init__("bullet.png", position, (30,30), (0, randint(15, 25)))
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.bottom > _HEIGHT or self.rect.left > _WIDTH or self.rect.right < 0:
            self.kill()


class TxTSprite(sprite.Sprite):
    def __init__(self, words, color, position, font_size):
        super().__init__()
        self.font = font.Font(None, font_size)
        self.image = self.font.render(words, True, color)
        self.rect = self.image.get_rect()
        self.initial_position = position
        self.color = color
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def update_txt(self, new_txt):
        self.image = self.font.render(new_txt, True, self.color)



points = 0
finale = TxTSprite( words ="Your score : "+str(points), color = "black", position =(300, 600), font_size = 100 )
background = ImageSprite(image_file="background.png", position=(0, 0), size=(_WIDTH, _HEIGHT)) 
player = Player(image_file="playersakuya.png", position=(300, 535), size=(80, 100), speed=(10, 10))
boss = Boss(image_file="ufo.png", position=(250, 0), size =(80, 100), speed= (10, 0))
player.rect.bottom = _HEIGHT - 15
player.set_lives(5)
projectiles = sprite.Group()
boss_projectiles = sprite.Group()
enemies = sprite.Group()
fire_sound = mixer.Sound("fire.ogg")
points = 0


game_state = "PLAY"

for i in range(20):
    enemy = Fairy("fairy.png", ( randint(0, _WIDTH-75), -65), (75, 65), (0, randint(1, 10)))
    enemies.add(enemy)


while not event.peek(QUIT):
    if game_state == "PLAY":

        for e in event.get():
            if e.type == KEYDOWN and e.key == K_SPACE:
                player.shoot(Knife)
        background.draw(window)

        hits = sprite.groupcollide(projectiles, enemies, True, True)
        for  hit in hits:
            enemy = Fairy("fairy.png", ( randint(0, _WIDTH-75), -65), (75, 65), (0, randint(1, 10)))
            enemies.add(enemy)
            points += 150

        boss_hits = sprite.spritecollide(boss, projectiles, True)
        if boss_hits:
            boss.hitpoints -= len(boss_hits)
            if boss.hitpoints <= 0:
                boss.status = "DECEASED"
                points += 1000

        player_hits = sprite.spritecollide(player, boss_projectiles, True)
        if player_hits:
            player.lives -= 1
            if player.lives <= 0:
                finale.update_txt("Your score : "+str(points))
                game_state = "GAME OVER"

        if 0 <= (time.get_ticks() % 0.5 )<= 5:
            boss.shoot()


#Do Current score on screen # Homework
#anywhere
#Respawn on the boss -> 
#If touch fairy = lose life
#Show life value / hit points
#research about git + create github account??
#Finish the game finally -> Saturday 


        projectiles.update()
        projectiles.draw(window)
        player.update()
        player.draw(window)
        boss_projectiles.update()
        boss_projectiles.draw(window)

        if boss.hitpoints > 0:
            boss.update()
            boss.draw(window)
        enemies.update()
        enemies.draw(window)
    elif game_state == "GAME OVER":
        window.fill("darkorange")
        finale.draw(window)
    # update the display EVERYTIME a change happens
    display.update()
    # set the FPS
    clock.tick(60)


    