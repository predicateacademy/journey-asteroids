import pygame, sys, math
from pygame.locals import *
from random import randrange

from Ball import Ball
from Bullet import Bullet
from Ship import Ship
from Text import Text
from levels import levels
from inputs import keys_down

# Set the window dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Set our target FPS
FPS = 60

# Set our color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create our event variables
KEYDOWN = 2
KEYUP = 3

# Initiate PyGame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroids')

# Create they pygame clock
clock = pygame.time.Clock()

# Initiate the current level
current_level = 0

# Make our sprite group
sprites = pygame.sprite.Group()

# Create our player and add it to the sprite group
player = Ship(WINDOW_WIDTH, WINDOW_HEIGHT, sprites, 'ship.png', 100, 400, 99, 75, 5)
sprites.add(player)

# Create our background surface
background = pygame.image.load('sprites/' + 'background.png').convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Fill the entire window with background when the game starts
DISPLAYSURF.blit(background, background.get_rect())

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Check when a key is pressed and add that key to keys_down
        if event.type == KEYDOWN:
            if not event.key in keys_down:
                keys_down.append(event.key)

        # Check when a key is released and remove that key from keys_down
        if event.type == KEYUP:
            if event.key in keys_down:
                keys_down.remove(event.key)

    # Display the player's lives
    sprites.add(Text(sprites, 'LIVES: ' + str(player.lives), 32, WHITE, 50, 20, 1))

    # Check if there are any balls left
    level_complete = True
    for sprite in sprites:
        if isinstance(sprite, Ball) and not isinstance(sprite, Bullet):
            level_complete = False
            break

    # If the level has been completed
    if level_complete:
        current_level += 1

        # If there are no more levels, you win
        if current_level > len(levels):
            sprites.add(Text(sprites, 'YOU WIN', 72, WHITE, 640, 360, 1))

        # Start the next level
        else:
            level = levels[current_level - 1]

            sprites.add(Text(sprites, 'LEVEL ' + str(level['level']), 72, WHITE, 640, 360, 120))

            # Spawn balls for new level
            for i in range(level['balls']):
                collision = True
                radius = level['radius']
                rand_x = 0
                rand_y = 0

                # Generate random a random position and assume it does not
                # collide with other sprites. If a collision occurs, generate
                # a new position and repeat until there are no collisions.
                while collision:
                    collision = False
                    new_rect = pygame.rect.Rect(0, 0, radius * 2, radius * 2)

                    rand_x = randrange(radius, WINDOW_WIDTH - radius)
                    rand_y = randrange(radius, WINDOW_HEIGHT - radius)

                    new_rect.center = (rand_x, rand_y)

                    for sprite in sprites:
                        if sprite.rect.colliderect(new_rect):
                            collision = True

                # Add the ball to the sprite list
                sprites.add(Ball(WINDOW_WIDTH, WINDOW_HEIGHT, sprites, level['sprite'], rand_x, rand_y, level['radius'], level['speed'], randrange(0, 360), level['damage']))

    # If the player is out of lives, the game ends
    if player.lives <= 0:
        # Draw game over text
        sprites.remove(sprites)
        sprites.add(Text(sprites, 'GAME OVER', 72, WHITE, 640, 360, 120))

    else:
        # Update game state
        sprites.update()

    # Draw screen
    sprites.clear(DISPLAYSURF, background)
    sprites.draw(DISPLAYSURF)

    pygame.display.update()

    # Only output our desired frame rate
    clock.tick(FPS)
