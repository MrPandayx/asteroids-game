import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        # Left edge - spawn on left, move right
        [
            pygame.Vector2(1, 0),  # Move right (positive x)
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        # Right edge - spawn on right, move left
        [
            pygame.Vector2(-1, 0),  # Move left (negative x)
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        # Top edge - spawn on top, move down
        [
            pygame.Vector2(0, 1),  # Move down (positive y)
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        # Bottom edge - spawn on bottom, move up
        [
            pygame.Vector2(0, -1),  # Move up (negative y)
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.current_level = 1

    def set_level(self, level):
        self.current_level = min(level, MAX_LEVEL)

    def get_spawn_rate(self):
        # Calculate spawn rate based on level (linear interpolation)
        progress = (self.current_level - 1) / (MAX_LEVEL - 1)
        return BASE_ASTEROID_SPAWN_RATE - (BASE_ASTEROID_SPAWN_RATE - MIN_ASTEROID_SPAWN_RATE) * progress

    def get_speed_range(self):
        # Calculate speed range based on level
        progress = (self.current_level - 1) / (MAX_LEVEL - 1)
        min_speed = BASE_ASTEROID_SPEED_MIN + (MAX_ASTEROID_SPEED_MIN - BASE_ASTEROID_SPEED_MIN) * progress
        max_speed = BASE_ASTEROID_SPEED_MAX + (MAX_ASTEROID_SPEED_MAX - BASE_ASTEROID_SPEED_MAX) * progress
        return int(min_speed), int(max_speed)

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        current_spawn_rate = self.get_spawn_rate()
        if self.spawn_timer > current_spawn_rate:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            
            # Get speed range based on current level
            min_speed, max_speed = self.get_speed_range()
            speed = random.randint(min_speed, max_speed)
            
            # Get base velocity direction toward screen
            velocity = edge[0] * speed
            
            # Add some random rotation (-30 to +30 degrees)
            rotation_angle = random.randint(-30, 30)
            velocity = velocity.rotate(rotation_angle)
            
            # Get spawn position
            position = edge[1](random.uniform(0, 1))
            
            # Choose asteroid size
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
