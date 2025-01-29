import pygame
import math
from specialmoves import RollPhase

RED = (255, 0, 0)

class PlayerPart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.scale = 1.0

class RollAnimator:
    def __init__(self, player_x, player_y, player_width, player_height, direction):
        self.x = player_x
        self.y = player_y
        self.width = player_width
        self.height = player_height
        self.direction = direction
        
        # Initialize body parts
        self.head = PlayerPart(player_x, player_y - player_height // 2)
        self.body = PlayerPart(player_x, player_y)
        self.arms = [PlayerPart(player_x, player_y) for _ in range(2)]
        self.legs = [PlayerPart(player_x, player_y) for _ in range(2)]
        
        # Animation parameters
        self.head_radius = 20
        self.limb_thickness = 5
    
    def _lerp(self, start, end, t):
        """Linear interpolation between start and end values"""
        return start + (end - start) * t
    
    def _update_leap(self, progress):
        """Update positions for leap phase"""
        # Head moves forward and slightly up
        self.head.x = self.x + (15 * self.direction)
        self.head.y = self.y - self.height // 2
        
        # Arms extend forward
        for i, arm in enumerate(self.arms):
            arm.x = self.x
            arm.y = self.y - self.height // 4
            arm.angle = 30 * self.direction
            
        # Legs extend backward
        spread = 20
        for i, leg in enumerate(self.legs):
            leg.x = self.x
            leg.y = self.y
            leg.angle = -30 + (i * spread)
            
        self.body.scale = 1.0
    
    def _update_hands(self, progress):
        """Update positions for hands touching ground phase"""
        # Head follows body lean
        self.head.x = self.x + (20 * self.direction)
        self.head.y = self.y - self.height // 3
        
        # Arms reach for ground
        arm_spread = 10
        for i, arm in enumerate(self.arms):
            arm.x = self.x
            arm.y = self.y - self.height // 4
            arm.angle = (45 + i * arm_spread) * self.direction
            
        # Legs start tucking
        leg_spread = 15
        for i, leg in enumerate(self.legs):
            leg.x = self.x
            leg.y = self.y
            leg.angle = (-15 + i * leg_spread) * self.direction
            
        self.body.scale = 0.8
    
    def _update_tuck(self, progress):
        """Update positions for tucking phase"""
        self.head.x = self.x + (10 * self.direction)
        self.head.y = self.y - self.height // 4
        
        # Arms and legs tuck in tight
        for arm in self.arms:
            arm.x = self.x
            arm.y = self.y
            arm.angle = 15 * self.direction
            
        for leg in self.legs:
            leg.x = self.x
            leg.y = self.y
            leg.angle = 10 * self.direction
            
        self.body.scale = 0.6
    
    def _update_rolling(self, progress):
        """Update positions for rolling phase"""
        roll_angle = progress * 360
        radius = self.height // 4  # Use 1/4 of height as rolling radius
        
        # Calculate center of rotation
        center_x = self.x
        center_y = self.y
        
        # Update head position with offset
        angle_rad = math.radians(roll_angle)
        self.head.x = center_x + radius * math.cos(angle_rad) * self.direction
        self.head.y = center_y + radius * math.sin(angle_rad)
        self.head.angle = roll_angle
        
        # Update arms with slight phase offset
        for i, arm in enumerate(self.arms):
            arm_angle = angle_rad + math.radians(45 * (1 if i == 0 else -1))
            arm.x = center_x + (radius * 0.8) * math.cos(arm_angle) * self.direction
            arm.y = center_y + (radius * 0.8) * math.sin(arm_angle)
            arm.angle = roll_angle + (45 * (1 if i == 0 else -1))
        
        # Update legs with different phase offset
        for i, leg in enumerate(self.legs):
            leg_angle = angle_rad + math.radians(90 * (1 if i == 0 else -1))
            leg.x = center_x + (radius * 0.9) * math.cos(leg_angle) * self.direction
            leg.y = center_y + (radius * 0.9) * math.sin(leg_angle)
            leg.angle = roll_angle + (90 * (1 if i == 0 else -1))
        
        # Scale body during roll
        self.body.scale = 0.6
    
    def _update_finish(self, progress):
        """Update positions for finish phase"""
        # Gradually return to normal stance
        self.head.x = self.x
        self.head.y = self._lerp(self.y, self.y - self.height // 2, progress)
        
        # Arms and legs spread back out
        arm_spread = 30 * progress
        leg_spread = 20 * progress
        
        for i, arm in enumerate(self.arms):
            arm.x = self.x
            arm.y = self._lerp(self.y, self.y - self.height // 4, progress)
            arm.angle = arm_spread * (-1 if i == 0 else 1)
            
        for i, leg in enumerate(self.legs):
            leg.x = self.x
            leg.y = self.y
            leg.angle = leg_spread * (-1 if i == 0 else 1)
            
        self.body.scale = self._lerp(0.5, 1.0, progress)
    
    def update(self, phase, phase_progress):
        """Update all body parts based on current phase"""
        update_funcs = {
            RollPhase.LEAP: self._update_leap,
            RollPhase.HANDS: self._update_hands,
            RollPhase.TUCK: self._update_tuck,
            RollPhase.ROLLING: self._update_rolling,
            RollPhase.FINISH: self._update_finish
        }
        
        if phase in update_funcs:
            update_funcs[phase](phase_progress)
    
    def draw(self, screen):
        """Draw the player in current pose"""
        # Draw in correct order: legs -> body -> arms -> head
        
        # Draw legs first
        for leg in self.legs:
            end_x = leg.x + math.cos(math.radians(leg.angle)) * (self.height // 3)
            end_y = leg.y + math.sin(math.radians(leg.angle)) * (self.height // 3)
            pygame.draw.line(screen, RED, (leg.x, leg.y), 
                           (end_x, end_y), self.limb_thickness)
        
        # Special handling for rolling phase
        if hasattr(self, 'current_phase') and self.current_phase == RollPhase.ROLLING:
            # Draw a circular body during roll
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), int(self.width * 0.4))
            
            # Draw rotation indicator
            roll_angle = self.body.angle
            radius = self.width * 0.4
            for angle_offset in [0, 90, 180, 270]:
                angle = math.radians(roll_angle + angle_offset)
                start_x = self.x + math.cos(angle) * radius * 0.5
                start_y = self.y + math.sin(angle) * radius * 0.5
                end_x = self.x + math.cos(angle) * radius
                end_y = self.y + math.sin(angle) * radius
                pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), 3)
        else:
            # Draw rectangular body
            body_width = self.width * self.body.scale
            body_height = self.height * self.body.scale
            body_rect = pygame.Rect(self.x - body_width // 2,
                                  self.y - body_height // 2,
                                  body_width, body_height)
            pygame.draw.rect(screen, RED, body_rect)
        
        # Draw arms
        for arm in self.arms:
            end_x = arm.x + math.cos(math.radians(arm.angle)) * (self.height // 3)
            end_y = arm.y + math.sin(math.radians(arm.angle)) * (self.height // 3)
            pygame.draw.line(screen, RED, (arm.x, arm.y), 
                           (end_x, end_y), self.limb_thickness)
        
        # Draw head last
        pygame.draw.circle(screen, RED, (int(self.head.x), int(self.head.y)), 
                         self.head_radius)

def draw_player(screen, player_x, player_y, player_height, walk_angle, is_walking_left, player_width, time, is_walking_right, on_ground, roll_state=None):
    if roll_state and roll_state.is_rolling:
        # Calculate phase progress (0 to 1)
        phase_progress = 1 - (roll_state.phase_timer / roll_state.phase_durations[roll_state.current_phase])
        
        # Create and update animator
        animator = RollAnimator(player_x, player_y, player_width, player_height, roll_state.roll_direction)
        animator.update(roll_state.current_phase, phase_progress)
        animator.draw(screen)
        return
        
    # Normal player drawing code
    pygame.draw.circle(screen, RED, (player_x, player_y - player_height // 2 - 20), 20)
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