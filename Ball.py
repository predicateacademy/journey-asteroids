import pygame.image, pygame.transform, math

class Ball(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height, sprite_group, sprite, x, y, radius, speed, angle, damage=1):
        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)
        self.window_width = window_width
        self.window_height = window_height
        self.sprites = sprite_group

        # Setup our sprite surface
        self.image = pygame.image.load('sprites/' + sprite)
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        self.image = self.image.convert_alpha()

        # Get our rectangle and set the position
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Create our vector variables
        self.speed = speed
        self.angle = math.radians(-angle)

        # Set the damage the ball receives and gives
        self.damage = damage

    # Update our game state by checking for collisions, moving, and bouncing
    def update(self):
        self.move()

        hit_xbounds, hit_ybounds, hit_ball = self.check_collisions()

        if hit_xbounds:
            self.angle = math.pi - self.angle
        if hit_ybounds:
            self.angle = -self.angle
        if hit_ball and not (hit_xbounds or hit_ybounds):
            self.angle = self.angle - math.pi

    # Calculate x/y movement and move
    def move(self):
        delta_x = self.speed*math.cos(self.angle)
        delta_y = self.speed*math.sin(self.angle)
        self.rect = self.rect.move(delta_x, delta_y)

    # Check for any boundary or ball collisions
    def check_collisions(self):
        hit_xbounds = False
        hit_ybounds = False
        hit_ball = None

        if self.rect.right >= self.window_width or self.rect.left <= 0:
            hit_xbounds = True

        if self.rect.top <= 0 or self.rect.bottom >= self.window_height:
            hit_ybounds = True

        for sprite in self.sprites:
            if not sprite is self and self.rect.colliderect(sprite.rect) and type(sprite) is Ball:
                hit_ball = sprite
                break

        return hit_xbounds, hit_ybounds, hit_ball
