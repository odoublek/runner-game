import pygame
import random
from pygame.locals import *
from pygame.surface import Surface

# Initialize pygame
pygame.init()

# Declare color
# black = pygame.color.Color('#000000')
# white = pygame.color.Color('#ffffff')

# Set screen size
screen_size = (1400, 600)

# Create the screen
screen = pygame.display.set_mode(screen_size)

# Set background
background = pygame.image.load('Images/bg-image.jpg')
rescaled = pygame.transform.scale(background, (1400, 600))
screen.blit(rescaled, (0, 0))

# Set title
pygame.display.set_caption("My RPG")

# Setting up fonts
# game_over_font = pygame.font.SysFont('Verdana', 60)

# Create the player
player_image = pygame.image.load("Images/player.png")
player_rect = player_image.get_rect()
player_rect.x = 0
player_rect.y = screen_size[1]/2

# Create multiple enemies
enemies = []
for i in range(3):
    enemy_image = pygame.image.load("Images/enemy.png")
    enemy_rect = enemy_image.get_rect()
    enemy_rect.x = screen_size[0]-enemy_rect.width
    enemy_rect.y = random.randrange(0, screen_size[1]-enemy_rect.height)
    while any(enemy_rect.colliderect(other_rect) for other_rect in enemies):
        enemy_rect.y = random.randrange(0, screen_size[1]-enemy_rect.height)
    enemies.append(enemy_rect)

# Player's level and XP
player_level = 1
player_xp = 0

# XP required to level up
level_up_xp = 1950

# Set player and enemy speed
player_speed = 1
enemy_speed = 0.05

# Set game loop flag
running = True

# Create font
font = pygame.font.SysFont(None, 30)

# Create level up message
level_up_message = "LEVEL UP!"
level_up_text = font.render(level_up_message, True, (255, 0, 0))
level_up_rect = level_up_text.get_rect()
level_up_rect.center = (screen_size[0]/2, screen_size[1]/2)

# Create waves
wave = 1
wave_size = 3
wave_counter = 0

# Create variable to keep track of enemies defeated
enemies_defeated = 0
if enemies_defeated <= 0:
    enemies_defeated == 0

# Create game over message
game_over_message = "Game Over\nLevel: {}\nEnemies Defeated: {}".format(
    player_level, enemies_defeated)
game_over_text = font.render(game_over_message, True, (255, 0, 0))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (screen_size[0]/2, screen_size[1]/2)

# Set player health
player_health = 100

# Displaying game over with font
# game_over = game_over_font.render("Game Over", True, (255, 0, 0))

# Set clock
clock = pygame.time.Clock()

# Game loop
while running:

    # Get the background image
    game_surface = Surface((screen_size[0], screen_size[1]))
    screen.blit(rescaled, (0, 0))
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Handle player key presses
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        if player_rect.y > 0:
            player_rect.y -= player_speed
    if keys[K_DOWN]:
        if player_rect.y < screen_size[1] - player_rect.height:
            player_rect.y += player_speed

    for enemy_rect in enemies:
        enemy_rect.x -= enemy_speed
        game_surface.blit(enemy_image, enemy_rect)
    screen.blit(player_image, player_rect)
    pygame.display.update()
    clock.tick(60)

    # Create new enemies and add them to list
    if len(enemies) < wave_size:
        for i in range(wave_size - len(enemies)):
            enemy_image = pygame.image.load("Images/enemy.png")
            enemy_rect = enemy_image.get_rect().copy()
            enemy_rect.x = screen_size[0]-enemy_rect.width
            enemy_rect.y = random.randint(
                0, screen_size[1] - enemy_rect.height)
            collision = False
            for existing_enemy in enemies:
                if enemy_rect.colliderect(existing_enemy):
                    collision = True
                    break
            if not collision:
                enemies.append(enemy_rect)
                wave_counter += 1

    # Move the enemies
    for enemy in enemies:
        if enemy.x <= 0:
            print("You have defeated an enemy!")
            player_xp += 5
            enemies.remove(enemy)
            enemies_defeated += 1
            wave_counter -= 1
            if wave_counter == 0:
                wave += 1
                wave_size = 3
                wave_counter = 0

    # Check collision between player and enemies
    for enemy in enemies:
        enemy.x -= enemy_speed
        if player_rect.colliderect(enemy):
            print("Game Over")
            enemies_defeated += len(enemies)
            game_over_message = "GAME OVER  Level: {}\nEnemies Defeated: {}".format(
                player_level, enemies_defeated)
            game_over_text = font.render(game_over_message, True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect()
            game_over_rect.center = (screen_size[0]/2, screen_size[1]/2)
            screen.blit(game_over_text, game_over_rect)
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()

    # Creating game over screen
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            print("Game Over")
            screen.blit(game_over_text, game_over_rect)
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()

    # Check if player has enough XP to level up
    if player_xp >= level_up_xp:
        player_level += 1
        player_xp = 0
        level_up_xp += 50
        player_speed += 2  # increase player speed
        enemy_speed += 0.3  # increase enemy speed
        print("You have leveled up! Your level is now", player_level)
        # Show level up message
        screen.blit(level_up_text, level_up_rect)
        pygame.display.update()
        # Wait for 2 seconds
        pygame.time.wait(1000)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the player
    screen.blit(player_image, player_rect)
    # Draw the enemy
    screen.blit(enemy_image, enemy_rect)

    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Update the display
    pygame.display.update()

# Clean up
pygame.quit()
