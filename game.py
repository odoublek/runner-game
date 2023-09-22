import pygame
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen settings
screen_size = (1400, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("My RPG")

# Player settings
player_image = pygame.image.load("Images/player.png")
player_rect = player_image.get_rect()
player_rect.topleft = (0, screen_size[1] // 2)
player_speed = 4
player_health = 200

# Enemy constructor
class Enemy:
    def __init__(self, image, damage, xp):
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = screen_size[0]
        self.rect.y = random.randint(0, screen_size[1] - self.rect.height)
        self.damage = damage
        self.xp = xp
        self.speed = 2

    def move(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right < 0

# Define different enemy types and their attributes
enemy_types = [
    {"image": pygame.image.load("images/enemy.png"), "damage": 20, "xp": 5},
    {"image": pygame.image.load("images/enemy2.png"), "damage": 30, "xp": 10},
    {"image": pygame.image.load("images/enemy3.png"), "damage": 40, "xp": 15},
    {"image": pygame.image.load("images/enemy4.png"), "damage": 50, "xp": 20}
]

# Create a list to store enemies
enemies = []

# Game state variables
dodged_enemies = 0
game_over = False

# Fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font('freesansbold.ttf', 60)

# Game loop flag
running = True

# Set clock
clock = pygame.time.Clock()

# Function to reset the game
def reset_game():
    global dodged_enemies, game_over, player_health, player_rect, enemies
    dodged_enemies = 0
    game_over = False
    player_health = 200
    player_rect.topleft = (0, screen_size[1] // 2)
    enemies = []

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[K_DOWN] and player_rect.bottom < screen_size[1]:
            player_rect.y += player_speed

        # Generate enemies
        if len(enemies) < 3:
            enemy_data = random.choice(enemy_types)
            enemy_image = enemy_data["image"]
            enemy_damage = enemy_data["damage"]
            enemy_xp = enemy_data["xp"]
            enemy = Enemy(enemy_image, enemy_damage, enemy_xp)
            enemies.append(enemy)

        # Update enemy positions and remove offscreen enemies
        for enemy in enemies:
            enemy.move()
            if enemy.is_offscreen():
                enemies.remove(enemy)
                dodged_enemies += 1

        # Check for collisions between player and enemies
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                player_health -= enemy.damage
                enemies.remove(enemy)
                if player_health <= 0:
                    game_over = True

        # Clear the screen and draw everything
        screen.fill((255, 255, 255))

        # Draw the enemies
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)

        # Draw the player
        screen.blit(player_image, player_rect)

        # Display dodged enemies count
        dodged_text = font.render("You dodged: {} enemies".format(dodged_enemies), True, (0, 0, 0))
        screen.blit(dodged_text, (20, 20))

        pygame.display.update()

        # Display player's remaining health at the top right corner
        health_text = font.render("Life: {}".format(player_health), True, (255, 0, 0))
        health_text_rect = health_text.get_rect(topleft=(screen_size[0] - 150, 20))
        screen.blit(health_text, health_text_rect)

        pygame.display.update()

    else:
        # Game over screen
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        restart_button = pygame.Rect(screen_size[0] // 2 - 100, screen_size[1] // 2 + 50, 200, 50)
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        restart_text = font.render("Try Again", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        screen.blit(restart_text, restart_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    reset_game()

# Clean up
pygame.quit()
