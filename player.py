import pygame
import math

RED = (255, 0, 0)

def draw_player(screen, player_x, player_y, player_height, walk_angle, is_walking_left, player_width, time, is_walking_right, on_ground):
    # Head - Red circle
    head_radius = 20
    pygame.draw.circle(screen, RED, (player_x, player_y - player_height // 2 - head_radius), head_radius)

    # Body - Red rectangle (control width directly here)
    pygame.draw.rect(screen, RED, (player_x - player_width // 2, player_y - player_height // 2, player_width, player_height))

    # Arms and legs (same as before)
    arm_length = 30
    arm_offset = 5  # Reduced from 10 to bring arms closer to body
    upper_leg_length = 30
    lower_leg_length = 30
    leg_offset = 10

    # Calculate the base position for arms and legs
    base_y = player_y - player_height // 2

    # Create a walking cycle using sine waves
    arm_swing = math.sin(time * 2 * math.pi / 60) if (is_walking_left or is_walking_right) else 0  # Only swing when walking
    leg_swing = math.sin(time * 2 * math.pi / 60) if (is_walking_left or is_walking_right) else 0  # Only swing when walking

    # Arm calculations
    upper_arm_length = 30
    lower_arm_length = 30
    left_rest_angle = 120  # 120 degrees from vertical
    right_rest_angle = 60  # 120 degrees from vertical
    swing_range = 30  # Amount of swing during running

    # Left arm
    if is_walking_left or is_walking_right:
        if is_walking_left:
            
            left_upper_arm_angle = math.radians(-270 + (swing_range * arm_swing))
            left_lower_arm_angle = left_upper_arm_angle + math.radians(120)
        else:  # walking right
            
            left_upper_arm_angle = math.radians(120 + (-swing_range * arm_swing))
            left_lower_arm_angle = left_upper_arm_angle - math.radians(120)
    else:
        left_upper_arm_angle = math.radians(left_rest_angle)
        left_lower_arm_angle = left_upper_arm_angle  # Aligned with upper arm

    left_upper_arm_x = player_x - arm_offset + math.cos(left_upper_arm_angle) * upper_arm_length
    left_upper_arm_y = base_y + math.sin(left_upper_arm_angle) * upper_arm_length

    left_lower_arm_x = left_upper_arm_x + math.cos(left_lower_arm_angle) * lower_arm_length
    left_lower_arm_y = left_upper_arm_y + math.sin(left_lower_arm_angle) * lower_arm_length

    # Right arm
    if is_walking_left or is_walking_right:
        if is_walking_left:
            # Arms on left side when running left (rotated 90° CCW)
            right_upper_arm_angle = math.radians(-270 + (-swing_range * arm_swing))  # -120° + 90° = -30°
            right_lower_arm_angle = right_upper_arm_angle + math.radians(120)
        else:  # walking right
            # Arms on right side when running right
            right_upper_arm_angle = math.radians(120 + (swing_range * arm_swing))
            right_lower_arm_angle = right_upper_arm_angle - math.radians(120)
    else:
        # Resting position: 120 degrees from vertical
        right_upper_arm_angle = math.radians(right_rest_angle)
        right_lower_arm_angle = right_upper_arm_angle  # Aligned with upper arm

    # Calculate right arm positions
    right_upper_arm_x = player_x + arm_offset + math.cos(right_upper_arm_angle) * upper_arm_length
    right_upper_arm_y = base_y + math.sin(right_upper_arm_angle) * upper_arm_length

    right_lower_arm_x = right_upper_arm_x + math.cos(right_lower_arm_angle) * lower_arm_length
    right_lower_arm_y = right_upper_arm_y + math.sin(right_lower_arm_angle) * lower_arm_length

    # Draw the arms
    # Left arm
    pygame.draw.line(screen, RED, (player_x - arm_offset, base_y), (left_upper_arm_x, left_upper_arm_y), 5)  # Upper arm
    pygame.draw.line(screen, RED, (left_upper_arm_x, left_upper_arm_y), (left_lower_arm_x, left_lower_arm_y), 5)  # Lower arm

    # Right arm
    pygame.draw.line(screen, RED, (player_x + arm_offset, base_y), (right_upper_arm_x, right_upper_arm_y), 5)  # Upper arm
    pygame.draw.line(screen, RED, (right_upper_arm_x, right_upper_arm_y), (right_lower_arm_x, right_lower_arm_y), 5)  # Lower arm

    # Calculate leg positions
    leg_base_x = player_x  # Center the legs under the character
    leg_base_y = player_y + player_height // 2  # Start from bottom of body

    # Walking logic for legs
    if is_walking_left or is_walking_right:
        # Create two offset sine waves for the legs (one is half a cycle ahead)
        leg1_phase = math.sin(time * 2 * math.pi / 60)  # First leg
        leg2_phase = math.sin((time * 2 * math.pi / 60) + math.pi)  # Second leg (opposite phase)
        
        if is_walking_left:
            # Left leg
            # Base angle is 90° (vertical up), swing ±30°
            upper_leg1_angle = math.radians(90 + (-30 * leg1_phase))  # Negative for left walking
            # Lower leg straightens as it moves through stride
            knee_bend1 = abs(leg1_phase) * math.pi / 6  # Max 30° bend, straightens in middle
            lower_leg1_angle = upper_leg1_angle - knee_bend1  # Subtract for counterclockwise bend
            
            # Right leg (opposite phase)
            upper_leg2_angle = math.radians(90 + (-30 * leg2_phase))
            knee_bend2 = abs(leg2_phase) * math.pi / 6
            lower_leg2_angle = upper_leg2_angle - knee_bend2
        else:  # walking right
            # Right leg
            upper_leg1_angle = math.radians(90 + (30 * leg1_phase))  # Positive for right walking
            knee_bend1 = abs(leg1_phase) * math.pi / 6
            lower_leg1_angle = upper_leg1_angle + knee_bend1  # Add for clockwise bend
            
            # Left leg (opposite phase)
            upper_leg2_angle = math.radians(90 + (30 * leg2_phase))
            knee_bend2 = abs(leg2_phase) * math.pi / 6
            lower_leg2_angle = upper_leg2_angle + knee_bend2
    else:  # Standing still
        # Set legs to vertical up position
        upper_leg1_angle = math.radians(90)  # Vertical up
        lower_leg1_angle = upper_leg1_angle
        upper_leg2_angle = math.radians(90)
        lower_leg2_angle = upper_leg2_angle

    # Calculate the positions of the upper and lower legs with slight horizontal offset
    upper_leg1_x = leg_base_x - 5 + math.cos(upper_leg1_angle) * upper_leg_length
    upper_leg1_y = leg_base_y + math.sin(upper_leg1_angle) * upper_leg_length

    lower_leg1_x = upper_leg1_x + math.cos(lower_leg1_angle) * lower_leg_length
    lower_leg1_y = upper_leg1_y + math.sin(lower_leg1_angle) * lower_leg_length

    upper_leg2_x = leg_base_x + 5 + math.cos(upper_leg2_angle) * upper_leg_length
    upper_leg2_y = leg_base_y + math.sin(upper_leg2_angle) * upper_leg_length

    lower_leg2_x = upper_leg2_x + math.cos(lower_leg2_angle) * lower_leg_length
    lower_leg2_y = upper_leg2_y + math.sin(lower_leg2_angle) * lower_leg_length

    # Draw the upper and lower legs
    pygame.draw.line(screen, RED, (leg_base_x, leg_base_y), (upper_leg1_x, upper_leg1_y), 5)  # Left upper leg
    pygame.draw.line(screen, RED, (upper_leg1_x, upper_leg1_y), (lower_leg1_x, lower_leg1_y), 5)  # Left lower leg

    pygame.draw.line(screen, RED, (leg_base_x, leg_base_y), (upper_leg2_x, upper_leg2_y), 5)  # Right upper leg
    pygame.draw.line(screen, RED, (upper_leg2_x, upper_leg2_y), (lower_leg2_x, lower_leg2_y), 5)  # Right lower leg