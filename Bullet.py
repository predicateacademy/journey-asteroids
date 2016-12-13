import pygame.mixer
from Ball import Ball

class Bullet(Ball):
    def __init__(self, window_width, window_height, sprite_group, ship, sprite, x, y, radius, speed, angle):
        Ball.__init__(self, window_width, window_height, sprite_group, sprite, x, y, radius, speed, angle)
        self.ship = ship

        self.image = pygame.transform.rotate(self.image, angle - 90)
        self.hit_sound = pygame.mixer.Sound('sounds/' + 'explosion.wav')

    # Update our game state by moving and destroying sprites when hit
    def update(self):
        self.move()

        hit_xbounds, hit_ybounds, hit_ball = self.check_collisions()

        if hit_ybounds or hit_xbounds:
            self.sprites.remove(self)
            self.ship.fired_bullets -= 1
        if hit_ball:
            self.hit_sound.play()
            self.sprites.remove(self)
            self.ship.fired_bullets -= 1

            hit_ball.damage -= 1

            if hit_ball.damage <= 0:
                self.sprites.remove(hit_ball)
