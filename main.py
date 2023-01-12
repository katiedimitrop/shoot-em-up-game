import pygame

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOURS, FPS
from sprites import Player, Enemy, Cloud

pygame.mixer.init()
pygame.init()

running = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

ENEMYEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMYEVENT, millis=250)
CLOUDEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(CLOUDEVENT, 1000)

player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("assets/audio/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("assets/audio/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("assets/audio/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("assets/audio/Collision.ogg")


def process_events():
    global running

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        running = False

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ENEMYEVENT:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == CLOUDEVENT:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


def update_objects():
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, pygame)
    enemies.update()
    clouds.update()


def draw_objects():
    screen.fill(COLOURS.SKY_BLUE)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

    # Set game FPS
    clock.tick(FPS)


# Main loop
while running:
    process_events()
    update_objects()
    draw_objects()

# Done! Time to quit.
pygame.quit()
