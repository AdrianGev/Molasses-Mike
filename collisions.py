import pygame

def check_collision(player_x, player_y, player_width, player_height, move_x, move_y, screen):
    """
    Check for collisions between the player and the environment.

    Args:
        player_x (float): Player's current x position.
        player_y (float): Player's current y position.
        player_width (int): Player's width.
        player_height (int): Player's height.
        move_x (float): Horizontal movement to check.
        move_y (float): Vertical movement to check.
        screen (pygame.Surface): The game screen to check colors.

    Returns:
        bool: True if movement is allowed, False if it would cause a collision.
    """
    # Check edges of the player after movement
    new_left = player_x + move_x
    new_right = player_x + player_width + move_x
    new_top = player_y + move_y
    new_bottom = player_y + player_height + move_y

    # Check horizontal movement collision
    for x in range(int(new_left), int(new_right) + 1, player_width // 2):  # Horizontal edge points
        for y in range(int(new_top), int(new_bottom) + 1, player_height // 2):  # Vertical edge points
            # Check if coordinates are within screen bounds
            if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
                color = screen.get_at((x, y))
                if color == (0, 0, 0):  # Black indicates a collision
                    # If moving down and collides with a platform (the player is falling)
                    if move_y > 0 and y <= player_y + player_height:  # Standing on top of a platform
                        player_y = y - player_height - 50  # Adjust position to just above the platform
                        return False
                    # If moving up and collides (hitting the ceiling)
                    elif move_y < 0 and y >= player_y:  # Hitting the ceiling
                        return False
                    else:
                        return False  # For left and right movement or invalid cases

    return True