import pygame
import math
import time
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, PLAYER_LIVES, SHAKE_EFFECT_DURATION, PLAYER_SKINS
from shot import Shot
from save_system import save_system

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = PLAYER_LIVES
        self.shake_effect_timer = 0  # Timer for shake power-up effect
        self.skin_id = save_system.get_current_skin()
        self.rainbow_time = 0  # For rainbow skin effect
    
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        # Get skin color
        color = self.get_skin_color()
        pygame.draw.polygon(screen, color, self.triangle(), 2)
    
    def get_skin_color(self):
        """Get the current skin color, with special effects for certain skins"""
        if self.skin_id == "rainbow":
            # Rainbow effect - cycle through colors
            self.rainbow_time += 0.1
            r = int(127 + 127 * math.sin(self.rainbow_time))
            g = int(127 + 127 * math.sin(self.rainbow_time + 2.09))  # 120 degrees offset
            b = int(127 + 127 * math.sin(self.rainbow_time + 4.18))  # 240 degrees offset
            return (r, g, b)
        else:
            return PLAYER_SKINS[self.skin_id]["color"]
    
    def update_skin(self):
        """Update skin from save system (call when skin changes)"""
        self.skin_id = save_system.get_current_skin()
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        # Create a new shot at the player's position
        shot = Shot(self.position.x, self.position.y)
        # Set the shot's velocity in the direction the player is facing
        velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = velocity * PLAYER_SHOOT_SPEED
        # Set the cooldown timer
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
    
    def take_damage(self):
        self.lives -= 1
        return self.lives <= 0  # Return True if player is dead
    
    def activate_shake_effect(self):
        self.shake_effect_timer = SHAKE_EFFECT_DURATION
    
    def has_shake_effect(self):
        return self.shake_effect_timer > 0
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            # If shake effect is active, ignore cooldown, otherwise check timer
            if self.has_shake_effect() or self.shoot_timer <= 0:
                self.shoot()
        
        # Decrease the shoot timer
        self.shoot_timer -= dt
        
        # Decrease the shake effect timer
        self.shake_effect_timer -= dt
