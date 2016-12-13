import pygame.image, pygame.transform, math

from Bullet import Bullet
from Ball import Ball
from inputs import keys_down

class Ship(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height, sprite_group, sprite, x, y, width, height, speed):
        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)
        self.window_width = window_width
        self.window_height = window_height
        self.sprites = sprite_group

        # Setup our sprite surface
        self.image = pygame.image.load('sprites/' + sprite)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image = self.image.convert_alpha()

        # Set the source image
        self.source_image = self.image.copy()

        # Get our rectangle and set the position
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Set other classs variables
        self.is_shooting = False
        self.total_bullets = 5
        self.fired_bullets = 0
        self.speed = speed
        self.lives = 5
        self.angle = 90

        # Set all class sounds
        self.shooting_sound = pygame.mixer.Sound('sounds/' + 'shot.wav')
        self.damage_sound = pygame.mixer.Sound('sounds/' + 'damage.wav')

    def update(self):
        # If up arrow pressed
        if 273 in keys_down:
            self.move(1)

        # If down arrow pressed
        if 274 in keys_down:
            self.move(-1)

        # If right arrow pressed
        if 275 in keys_down:
            self.turn(-0.65)

        # If left arrow pressed
        if 276 in keys_down:
            self.turn(0.65)

        # If spacebar pressed
        if 32 in keys_down:
            if not self.is_shooting and self.fired_bullets < self.total_bullets:
                self.fired_bullets += 1
                self.is_shooting = True
                self.shooting_sound.play()

                x, y = self.rect.center
                self.sprites.add(Bullet(self.window_width, self.window_height, self.sprites, self, 'bullet.png', x, y, 10, 12, self.angle))
        else:
            self.is_shooting = False

        for sprite in self.sprites:
            if not sprite is self and type(sprite) is Ball and self.rect.colliderect(sprite.rect):
                self.damage_sound.play()
                self.lives -= sprite.damage

                self.sprites.remove(sprite)
                break

    def turn(self, multiplier):
        center = self.rect.center
        self.angle += float(self.speed) * multiplier

        self.image = pygame.transform.rotate(self.source_image, self.angle - 90)

        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, multiplier):
        angle = math.radians(-self.angle)
        prev_x = self.rect.x
        prev_y = self.rect.y

        delta_x = float(self.speed) * multiplier * math.cos(angle)
        delta_y = float(self.speed) * multiplier * math.sin(angle)
        self.rect = self.rect.move(delta_x, delta_y)

        if self.rect.right >= self.window_width or self.rect.left <= 0:
            self.rect.x = prev_x

        if self.rect.top <= 0 or self.rect.bottom >= self.window_height:
            self.rect.y = prev_y
