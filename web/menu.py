import pygame
import sys
from constants import *

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 48)
        self.font_coin = pygame.font.Font(None, 36)
        
        # Button properties
        self.button_width = 200
        self.button_height = 60
        self.button_margin = 20
        
        # Calculate button positions
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        self.play_button = pygame.Rect(center_x - self.button_width // 2, start_y, self.button_width, self.button_height)
        self.shop_button = pygame.Rect(center_x - self.button_width // 2, start_y + self.button_height + self.button_margin, self.button_width, self.button_height)
        self.quit_button = pygame.Rect(center_x - self.button_width // 2, start_y + 2 * (self.button_height + self.button_margin), self.button_width, self.button_height)
        
        # Colors
        self.button_color = (70, 70, 70)
        self.button_hover_color = (100, 100, 100)
        self.button_text_color = (255, 255, 255)
        self.title_color = (255, 255, 255)
        self.coin_color = (255, 215, 0)  # Gold color for coins
        
        self.hovered_button = None
    
    def handle_event(self, event, game_state):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            self.hovered_button = None
            
            if self.play_button.collidepoint(mouse_pos):
                self.hovered_button = "play"
            elif self.shop_button.collidepoint(mouse_pos):
                self.hovered_button = "shop"
            elif self.quit_button.collidepoint(mouse_pos):
                self.hovered_button = "quit"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                
                if self.play_button.collidepoint(mouse_pos):
                    return "play"
                elif self.shop_button.collidepoint(mouse_pos):
                    return "shop"
                elif self.quit_button.collidepoint(mouse_pos):
                    return "quit"
        
        return "menu"
    
    def draw(self, coins):
        # Fill background with space-like color
        self.screen.fill((10, 10, 30))
        
        # Draw stars background (simple version)
        for i in range(50):
            x = (i * 47) % SCREEN_WIDTH
            y = (i * 73) % SCREEN_HEIGHT
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)
        
        # Draw title
        title_text = self.font_title.render("Asteroid Game", True, self.title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Draw coin counter
        coin_text = self.font_coin.render(f"Coins: {coins}", True, self.coin_color)
        coin_rect = coin_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(coin_text, coin_rect)
        
        # Draw buttons
        self.draw_button(self.play_button, "Play", self.hovered_button == "play")
        self.draw_button(self.shop_button, "Shop", self.hovered_button == "shop")
        self.draw_button(self.quit_button, "Quit", self.hovered_button == "quit")
    
    def draw_button(self, rect, text, is_hovered):
        color = self.button_hover_color if is_hovered else self.button_color
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.button_text_color, rect, 2)
        
        text_surface = self.font_button.render(text, True, self.button_text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
