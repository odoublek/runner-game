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

# Create a list or dictionary of enemy types
enemy_types = ["type1", "type2", "type3", "type4"]

# Create a dictionary to get data of the enemies
enemy_data = {
    "type1": {"image": pygame.image.load("images/enemy.png"), "damage": 20, "xp": 5},
    "type2": {"image": pygame.image.load("images/enemy2.png"), "damage": 20, "xp": 10},
    "type3": {"image": pygame.image.load("images/enemy3.png"), "damage": 30, "xp": 15},
    "type4": {"image": pygame.image.load("images/enemy4.png"), "damage": 40, "xp": 20}
}


# Create a list to store the enemies
enemies = []

# Set number of enemies for each type
enemies_count = {
    "type1": 2,
    "type2": 0,
    "type3": 0,
    "type4": 1
}

# Use a for loop to create instances of each enemy type
for enemy_type in enemy_types:
    for i in range(enemies_count[enemy_type]):
        enemy_image = enemy_data[enemy_type]["image"]
        enemy_rect = enemy_image.get_rect()
        enemy_rect.x = screen_size[0]-enemy_rect.width
        enemy_rect.y = random.randrange(0, screen_size[1]-enemy_rect.height)

        # check for collision with other enemies
        collision = False
        for e in enemies:
            if enemy_rect.colliderect(e["rect"]):
                collision = True
                break
        if collision:
            # randomly move the rectangle if it collides with another enemy
            enemy_rect.y = random.randrange(screen_size[1]-enemy_rect.height)
        enemies.append(
            {"type": enemy_type, "image": enemy_image, "rect": enemy_rect})


# Player's level and XP
player_level = 1
player_xp = 0

# XP required to level up
level_up_xp = 100

# Set player and enemy speed
player_speed = 4
enemy_speed = 4

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
game_over_font = pygame.font.Font('freesansbold.ttf', 60)
game_over_text = game_over_font.render(game_over_message, True, (255, 0, 0))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (screen_size[0]/2, screen_size[1]/2)

# # Create play again button
# play_again_image = pygame.image.load("Images/play-again-button.png")
# play_again_rect = play_again_image.get_rect()
# play_again_rect.center = (screen_size[0]/2, screen_size[1]/2 + 100)

# # Set player health
player_health = 200

# Set clock
clock = pygame.time.Clock()

# Game loop
while running:

    # # Get the background image
    # game_surface = Surface((screen_size[0], screen_size[1]))
    # screen.blit(rescaled, (0, 0))while player_health <= 0:

    # # Play again button
    # while player_health <= 0:
    #     screen.blit(game_over_text, game_over_rect)
    #     screen.blit(play_again_image, play_again_rect)
    #     pygame.display.update()

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

    # Movement of enemies
    for enemy_rect in enemies:
        enemy_rect["rect"].x -= enemy_speed
    for enemy in enemies:
        screen.blit(enemy_data[enemy["type"]]["image"], enemy["rect"])
        pygame.display.update()
        clock.tick(60)

    # Create new enemies and add them to list
    if player_level == 4:
        wave_size = 4
    elif player_level >= 6:
        wave_size = 5
    if len(enemies) < wave_size:
        for i in range(wave_size - len(enemies)):
            # Select a random enemy type
            enemy_type = random.choice(enemy_types)
            # Load the corresponding image for the selected type
            enemy_image = enemy_data[enemy_type]
            enemy_rect = enemy_data[enemy_type]["image"].get_rect().copy()
            enemy_rect.x = screen_size[0]-enemy_rect.width
            enemy_rect.y = random.randint(
                0, screen_size[1] - enemy_rect.height)
            collision = False
            for existing_enemy in enemies:
                if enemy_rect.colliderect(existing_enemy["rect"]):
                    collision = True
                    break
            if not collision:
                enemies.append(
                    {"type": enemy_type, "image": enemy_data[enemy_type]["image"], "rect": enemy_rect, "damage": enemy_data[enemy_type]["damage"]})

                wave_counter += 1

    # Check the enemies
    for enemy in enemies:
        if enemy["rect"].x <= 0:
            print("You have defeated an enemy!")
            player_xp += enemy_data[enemy["type"]]["xp"]
            enemies.remove(enemy)
            enemies_defeated += 1
            wave_counter -= 1
            if wave_counter == 0:
                wave += 1
                wave_counter = wave_size

    # Check collision between player and enemies
    for enemy in enemies:
        if player_rect.colliderect(enemy["rect"]):
            player_health -= enemy_data[enemy["type"]]["damage"]
            print("Player took damage! Current hp is:", player_health)
            screen.blit(enemy_data[enemy["type"]]["image"], enemy["rect"])
            if player_health == 0:
                print("Game Over")
                enemies_defeated += len(enemies)
                game_over_message = "Game Over\nLevel: {}\nEnemies Defeated: {}".format(
                    player_level, enemies_defeated)
                game_over_text = font.render(
                    game_over_message, True, (255, 0, 0))
                game_over_rect = game_over_text.get_rect()
                game_over_rect.center = (screen_size[0]/2, screen_size[1]/2)
                screen.blit(game_over_text, game_over_rect)
                pygame.display.update()
                pygame.time.wait(5000)
                pygame.quit()

    # Check if player has enough XP to level up
    health_increment = 10
    level_up_increment = 100
    if player_xp >= level_up_xp:
        player_level += 1
        player_health += player_level * health_increment
        player_xp = 0
        level_up_xp += level_up_increment
        level_up_xp += 50
        player_speed += 2  # increase player speed
        enemy_speed += 0.3  # increase enemy speed
        print("You have leveled up! Your level is now",
              player_level, "\n Your total hp is =", player_health)
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
    screen.blit(enemy["image"], enemy["rect"])

    for enemy in enemies:
        screen.blit(enemy["image"], enemy["rect"])

    # Update the display
    pygame.display.update()

# Clean up
pygame.quit()
