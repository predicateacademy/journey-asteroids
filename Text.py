import pygame.font

class Text(pygame.sprite.Sprite):
    # Initiate this text object
    def __init__(self, sprite_group, text, size, color, x, y, duration):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprite_group

        font = pygame.font.SysFont('Sans', size)

        self.image = font.render(str(text), True, color)

        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.ticks = 0
        self.duration = duration

    # If a non-zero duration was set, destroy this text after the given duration
    def update(self):
        if self.duration:
            self.ticks += 1
            if self.ticks > self.duration:
                self.sprites.remove(self)
