import pygame
import json
import os
from constants import *

class Shop:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 64)
        self.font_button = pygame.font.Font(None, 36)
        self.font_price = pygame.font.Font(None, 32)
        self.font_coin = pygame.font.Font(None, 36)
        
        # Shop items (player triangle colors)
        self.skins = [
            {"name": "Default White", "color": (255, 255, 255), "price": 0, "owned": True},
            {"name": "Fire Red", "color": (255, 50, 50), "price": 10, "owned": False},
            {"name": "Ocean Blue", "color": (50, 150, 255), "price": 15, "owned": False},
            {"name": "Forest Green", "color": (50, 255, 100), "price": 20, "owned": False},
            {"name": "Royal Purple", "color": (150, 50, 255), "price": 25, "owned": False},
            {"name": "Sunset Orange", "color": (255, 150, 50), "price": 30, "owned": False},
            {"name": "Hot Pink", "color": (255, 50, 150), "price": 35, "owned": False},
            {"name": "Electric Yellow", "color": (255, 255, 50), "price": 40, "owned": False},
            {"name": "Cosmic Cyan", "color": (50, 255, 255), "price": 50, "owned": False},
            {"name": "Galaxy Gold", "color": (255, 215, 0), "price": 100, "owned": False}
        ]
        
        # Current selected skin
        self.selected_skin = 0
        
        # Load saved data
        self.load_shop_data()
        
        # Button properties
        self.back_button = pygame.Rect(20, 20, 100, 40)
        self.item_width = 180
        self.item_height = 120
        self.items_per_row = 4
        self.item_margin = 20
        
        # Colors
        self.bg_color = (10, 10, 30)
        self.button_color = (70, 70, 70)
        self.button_hover_color = (100, 100, 100)
        self.selected_color = (0, 255, 0)
        self.owned_color = (100, 255, 100)
        self.locked_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.coin_color = (255, 215, 0)
        
        self.hovered_item = None
        self.hovered_back = False
    
    def load_shop_data(self):
        """Load shop data from session storage for web version"""
        # For web version, we'll use simple defaults since file I/O is limited
        pass
    
    def save_shop_data(self):
        """Save shop data for web version"""
        # For web version, we'll use simple session storage
        pass
    
    def handle_event(self, event, coins):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            self.hovered_item = None
            self.hovered_back = False
            
            if self.back_button.collidepoint(mouse_pos):
                self.hovered_back = True
            else:
                # Check if hovering over an item
                for i in range(len(self.skins)):
                    item_rect = self.get_item_rect(i)
                    if item_rect.collidepoint(mouse_pos):
                        self.hovered_item = i
                        break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                
                if self.back_button.collidepoint(mouse_pos):
                    return "menu", coins
                
                # Check if clicking on an item
                for i in range(len(self.skins)):
                    item_rect = self.get_item_rect(i)
                    if item_rect.collidepoint(mouse_pos):
                        skin = self.skins[i]
                        
                        if skin["owned"]:
                            # Select this skin
                            self.selected_skin = i
                            self.save_shop_data()
                        elif coins >= skin["price"]:
                            # Buy this skin
                            skin["owned"] = True
                            self.selected_skin = i
                            coins -= skin["price"]
                            self.save_shop_data()
                        
                        return "shop", coins
        
        return "shop", coins
    
    def get_item_rect(self, index):
        """Get the rectangle for a shop item"""
        row = index // self.items_per_row
        col = index % self.items_per_row
        
        start_x = (SCREEN_WIDTH - (self.items_per_row * self.item_width + (self.items_per_row - 1) * self.item_margin)) // 2
        start_y = 150
        
        x = start_x + col * (self.item_width + self.item_margin)
        y = start_y + row * (self.item_height + self.item_margin)
        
        return pygame.Rect(x, y, self.item_width, self.item_height)
    
    def get_selected_skin_color(self):
        """Get the color of the currently selected skin"""
        return self.skins[self.selected_skin]["color"]
    
    def draw(self, coins):
        # Fill background
        self.screen.fill(self.bg_color)
        
        # Draw stars background
        for i in range(50):
            x = (i * 47) % SCREEN_WIDTH
            y = (i * 73) % SCREEN_HEIGHT
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)
        
        # Draw title
        title_text = self.font_title.render("Shop", True, self.text_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw coin counter
        coin_text = self.font_coin.render(f"Coins: {coins}", True, self.coin_color)
        coin_rect = coin_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(coin_text, coin_rect)
        
        # Draw back button
        back_color = self.button_hover_color if self.hovered_back else self.button_color
        pygame.draw.rect(self.screen, back_color, self.back_button)
        pygame.draw.rect(self.screen, self.text_color, self.back_button, 2)
        back_text = self.font_button.render("Back", True, self.text_color)
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw shop items
        for i, skin in enumerate(self.skins):
            self.draw_shop_item(i, skin, coins)
    
    def draw_shop_item(self, index, skin, coins):
        item_rect = self.get_item_rect(index)
        
        # Determine border color
        border_color = self.text_color
        if index == self.selected_skin:
            border_color = self.selected_color
        elif skin["owned"]:
            border_color = self.owned_color
        elif coins < skin["price"]:
            border_color = self.locked_color
        
        # Draw item background
        item_color = (30, 30, 50) if self.hovered_item == index else (20, 20, 40)
        pygame.draw.rect(self.screen, item_color, item_rect)
        pygame.draw.rect(self.screen, border_color, item_rect, 3)
        
        # Draw player triangle preview
        triangle_center = (item_rect.centerx, item_rect.centery - 20)
        triangle_size = 20
        triangle_points = [
            (triangle_center[0], triangle_center[1] - triangle_size),
            (triangle_center[0] - triangle_size * 0.866, triangle_center[1] + triangle_size * 0.5),
            (triangle_center[0] + triangle_size * 0.866, triangle_center[1] + triangle_size * 0.5)
        ]
        pygame.draw.polygon(self.screen, skin["color"], triangle_points)
        pygame.draw.polygon(self.screen, self.text_color, triangle_points, 2)
        
        # Draw skin name
        name_text = self.font_button.render(skin["name"], True, self.text_color)
        name_rect = name_text.get_rect(center=(item_rect.centerx, item_rect.bottom - 40))
        self.screen.blit(name_text, name_rect)
        
        # Draw price or status
        if index == self.selected_skin:
            status_text = self.font_price.render("SELECTED", True, self.selected_color)
        elif skin["owned"]:
            status_text = self.font_price.render("OWNED", True, self.owned_color)
        elif coins >= skin["price"]:
            status_text = self.font_price.render(f"{skin['price']} coins", True, self.coin_color)
        else:
            status_text = self.font_price.render(f"{skin['price']} coins", True, self.locked_color)
        
        status_rect = status_text.get_rect(center=(item_rect.centerx, item_rect.bottom - 15))
        self.screen.blit(status_text, status_rect)
