import pygame
import random
from shake import Shake
from constants import *

class ShakeField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, position):
        shake = Shake(position.x, position.y)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > SHAKE_SPAWN_RATE:
            self.spawn_timer = 0

            # Spawn a shake at a random position on screen (avoiding edges)
            x = random.randint(SHAKE_RADIUS * 2, SCREEN_WIDTH - SHAKE_RADIUS * 2)
            y = random.randint(SHAKE_RADIUS * 2, SCREEN_HEIGHT - SHAKE_RADIUS * 2)
            position = pygame.Vector2(x, y)
            self.spawn(position)
