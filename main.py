import pygame
import sys
from player import draw_player
from collisions import check_collision

pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
RED = (255, 0, 0)
BLACK = (0, 0, 0)
INITIAL_JUMP_FORCE = -15
GRAVITY = 0.8
PLAYER_SPEED = 5
SPAWN_X_OFFSET = 10
SPAWN_Y_OFFSET = -50

time = 0
jump_force = 0
is_jumping = False
player_x = 100
player_y = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Molasses Mike")

# Player variables
START_X = (SCREEN_WIDTH // 2) - 650  # Store starting X position
START_Y = SCREEN_HEIGHT - 300  # Store starting Y position
player_x = START_X
player_y = START_Y
player_height = 50
player_width = 7  # Set the body width to 7
walk_angle = 0  # Controls the swing of arms and legs
is_walking_left = False  # Initially walking to the right
is_walking_right = False
player_velocity_y = 0  # Player vertical velocity (for gravity)
on_ground = False  # Whether the player is standing on a platform
ground_level = SCREEN_HEIGHT - 80

# Platform data (x, y, width, height)
platforms = [
    pygame.Rect(100, SCREEN_HEIGHT - 50, 50, 50),  # First platform
    pygame.Rect(250, SCREEN_HEIGHT - 100, 50, 100),  # Second platform
    pygame.Rect(400, SCREEN_HEIGHT - 150, 50, 150),  # Third platform
    pygame.Rect(550, SCREEN_HEIGHT - 200, 50, 200),  # Fourth platform
]

# Main game loop
run = True
while run:
    screen.fill((255, 255, 255))  # Fill screen with white background

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    move_x = 0
    move_y = player_velocity_y
    is_walking_left = False
    is_walking_right = False

    # Reset position when R is pressed
    if keys[pygame.K_r]:
        player_x = START_X
        player_y = START_Y
        player_velocity_y = 0
        on_ground = False
        is_jumping = False
        jump_force = 0

    # Horizontal movement
    if keys[pygame.K_a]:  # Move left
        move_x = -PLAYER_SPEED
        is_walking_left = True
    elif keys[pygame.K_d]:  # Move right
        move_x = PLAYER_SPEED
        is_walking_right = True

    # Check horizontal collision
    if check_collision(player_x, player_y, player_width, player_height, move_x, 0, screen):
        player_x += move_x

    # Jumping
    if keys[pygame.K_SPACE] and on_ground:  # Jump
        jump_force = INITIAL_JUMP_FORCE
        is_jumping = True
        on_ground = False

    if is_jumping:
        player_velocity_y = jump_force
        jump_force = jump_force * 0.9
        if abs(jump_force) < 1:
            is_jumping = False

    # Gravity
    if not is_jumping and not on_ground:
        player_velocity_y += GRAVITY

    # Check vertical collision
    if check_collision(player_x, player_y, player_width, player_height, 0, move_y, screen):
        player_y += player_velocity_y
        on_ground = False
    else:  # If collision is detected, stop vertical movement
        if player_velocity_y > 0:  # Falling
            on_ground = True
            player_velocity_y = 0
        elif player_velocity_y < 0:  # Hitting ceiling
            player_velocity_y = 0

    # Ground collision
    if player_y >= ground_level:
        player_y = ground_level
        player_velocity_y = 0
        on_ground = True

    # Draw the player
    draw_player(screen, player_x, player_y, player_height, walk_angle, is_walking_left, player_width, time, is_walking_right, on_ground)

    time += 1   # Increment time for walking cycle

    # Update the screen
    pygame.display.flip()

    # Frame rate (FPS)
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()