import math
import pygame

class RollPhase:
    LEAP = 0      # Initial leap with extended arms
    HANDS = 1     # Hands touch ground
    TUCK = 2      # Head tucked, starting roll
    ROLLING = 3   # Rolling over shoulder
    FINISH = 4    # Getting back to feet

class RollState:
    def __init__(self):
        self.is_rolling = False
        self.roll_distance = 100  # Total distance to roll
        self.roll_progress = 0  # Current progress of the roll (0 to 100)
        self.roll_speed = 8  # pixels per frame
        self.roll_cooldown = 30  # frames
        self.cooldown_timer = 0
        self.roll_direction = 1  # 1 for right, -1 for left
        self.current_phase = RollPhase.LEAP
        self.phase_durations = {
            RollPhase.LEAP: 3,     # 3 frames for initial leap
            RollPhase.HANDS: 3,    # 3 frames for hands touching
            RollPhase.TUCK: 2,     # 2 frames for tucking
            RollPhase.ROLLING: 6,  # 6 frames for roll
            RollPhase.FINISH: 3    # 3 frames for standing up
        }
        self.phase_timer = 0
        self.total_frames = sum(self.phase_durations.values())

    def start_roll(self, facing_left):
        if self.cooldown_timer == 0 and not self.is_rolling:
            self.is_rolling = True
            self.roll_progress = 0
            self.roll_direction = -1 if facing_left else 1
            self.current_phase = RollPhase.LEAP
            self.phase_timer = self.phase_durations[RollPhase.LEAP]
            return self.roll_speed * self.roll_direction
        return 0

    def update(self):
        roll_velocity = 0
        if self.is_rolling:
            # Update roll progress
            self.roll_progress += self.roll_speed
            self.phase_timer -= 1

            # Update phases
            if self.phase_timer <= 0:
                if self.current_phase == RollPhase.LEAP:
                    self.current_phase = RollPhase.HANDS
                    self.phase_timer = self.phase_durations[RollPhase.HANDS]
                elif self.current_phase == RollPhase.HANDS:
                    self.current_phase = RollPhase.TUCK
                    self.phase_timer = self.phase_durations[RollPhase.TUCK]
                elif self.current_phase == RollPhase.TUCK:
                    self.current_phase = RollPhase.ROLLING
                    self.phase_timer = self.phase_durations[RollPhase.ROLLING]
                elif self.current_phase == RollPhase.ROLLING:
                    self.current_phase = RollPhase.FINISH
                    self.phase_timer = self.phase_durations[RollPhase.FINISH]
                elif self.current_phase == RollPhase.FINISH:
                    self.is_rolling = False
                    self.roll_progress = 0
                    self.cooldown_timer = self.roll_cooldown
                    return 0

            roll_velocity = self.roll_speed * self.roll_direction

        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

        return roll_velocity

def handle_roll(keys, roll_state, is_walking_left, is_walking_right):
    if keys[pygame.K_SPACE]:
        # Determine roll direction based on movement or facing direction
        facing_left = is_walking_left or (not is_walking_right and not is_walking_left)
        return roll_state.start_roll(facing_left)
    
    return roll_state.update()