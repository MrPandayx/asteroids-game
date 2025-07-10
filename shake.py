import pygame
from circleshape import CircleShape
from constants import SHAKE_RADIUS

class Shake(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHAKE_RADIUS)
    
    def draw(self, screen):
        # Draw detailed McDonald's birthday shake based on the image
        center_x, center_y = int(self.position.x), int(self.position.y)
        
        # Draw the cup body (gradient purple to white)
        # Bottom part (white/cream base)
        bottom_height = self.radius // 2
        pygame.draw.circle(screen, (240, 240, 240), (center_x, center_y + bottom_height//2), self.radius - 2, 0)
        
        # Middle part (purple gradient)
        for i in range(bottom_height):
            y_offset = center_y - bottom_height + i
            purple_intensity = 150 + (100 * i // bottom_height)
            color = (purple_intensity, 100 + (50 * i // bottom_height), 200)
            pygame.draw.circle(screen, color, (center_x, y_offset), self.radius - 2 - i//3, 0)
        
        # Cup rim/lid (clear dome effect)
        pygame.draw.circle(screen, (200, 200, 255, 100), (center_x, center_y - self.radius//2), self.radius//3, 2)
        
        # Whipped cream on top
        cream_y = center_y - self.radius + 5
        pygame.draw.circle(screen, (255, 255, 255), (center_x, cream_y), self.radius//4, 0)
        pygame.draw.circle(screen, (250, 250, 250), (center_x - 3, cream_y), self.radius//6, 0)
        pygame.draw.circle(screen, (250, 250, 250), (center_x + 3, cream_y), self.radius//6, 0)
        
        # Colorful sprinkles scattered around
        sprinkle_colors = [
            (255, 100, 100),   # Red
            (100, 255, 100),   # Green  
            (100, 100, 255),   # Blue
            (255, 255, 100),   # Yellow
            (255, 150, 255),   # Pink
            (150, 255, 150),   # Light green
            (255, 165, 0),     # Orange
            (128, 0, 128),     # Purple
        ]
        
        for i, color in enumerate(sprinkle_colors):
            # Spread sprinkles around the cup
            angle = (i * 45) % 360  # Distribute around circle
            offset_x = int(10 * pygame.math.Vector2(1, 0).rotate(angle).x)
            offset_y = int(10 * pygame.math.Vector2(1, 0).rotate(angle).y) - 5
            
            sprinkle_x = center_x + offset_x
            sprinkle_y = center_y + offset_y
            
            # Draw sprinkle as small rectangle
            pygame.draw.rect(screen, color, (sprinkle_x-2, sprinkle_y-1, 4, 8))
        
        # "GRIMACE'S BIRTHDAY" text effect (simplified)
        text_y = center_y + 2
        pygame.draw.rect(screen, (255, 255, 255), (center_x-15, text_y-3, 30, 6), 0)
        pygame.draw.rect(screen, (100, 50, 150), (center_x-15, text_y-3, 30, 6), 1)
        
        # McDonald's "M" logo at bottom
        logo_y = center_y + self.radius - 8
        # Draw golden arches
        pygame.draw.rect(screen, (255, 215, 0), (center_x-8, logo_y, 4, 6), 0)  # Left arch
        pygame.draw.rect(screen, (255, 215, 0), (center_x+4, logo_y, 4, 6), 0)   # Right arch
        pygame.draw.rect(screen, (255, 0, 0), (center_x-10, logo_y+6, 20, 4), 0) # Red background
        
        # Cup outline
        pygame.draw.circle(screen, (100, 100, 100), (center_x, center_y), self.radius, 3)
    
    def update(self, dt):
        # Power-ups don't move, they stay in place
        pass
