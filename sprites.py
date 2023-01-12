import pygame
import random

from settings import COLOURS, STEP, SCREEN_WIDTH, SCREEN_HEIGHT, MIN_ENEMY_SPEED, MAX_ENEMY_SPEED
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL
)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/image/jet.png").convert()
        self.surf.set_colorkey(COLOURS.WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys, py_game):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -STEP)
            py_game.mixer.Sound("assets/audio/Rising_putter.ogg").play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, STEP)
            py_game.mixer.Sound("assets/audio/Falling_putter.ogg").play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-STEP, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(STEP, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill(COLOURS.WHITE)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(MIN_ENEMY_SPEED, MAX_ENEMY_SPEED)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("assets/image/cloud.png").convert()
        self.surf.set_colorkey(COLOURS.BLACK, RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-STEP, 0)
        if self.rect.right < 0:
            self.kill()