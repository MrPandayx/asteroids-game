# Web-compatible version of Asteroids Game
import pygame
import asyncio
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from shake import Shake
from shakefield import ShakeField
from save_system import save_system
# Pre-generate star positions once to avoid reseeding random each frame
import random
import math

# Menu states
MENU_STATE = "MENU"
GAME_STATE = "GAME"
GAME_OVER_STATE = "GAME_OVER"
SHOP_STATE = "SHOP"

# Generate static star positions
def generate_stars():
    random.seed(42)  # Seed only once for star generation
    stars = []
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        brightness = random.randint(150, 255)
        size = random.choice([1, 1, 2])
        stars.append((x, y, brightness, size))
    
    # Add larger bright stars
    random.seed(123)
    bright_stars = []
    for _ in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        bright_stars.append((x, y))
    
    # Reset random to unseeded state for game logic
    random.seed()
    return stars, bright_stars

# Generate stars once at module level
STARS, BRIGHT_STARS = generate_stars()

def draw_space_background(screen):
    # Fill with a base dark space color
    screen.fill((15, 10, 35))  # Dark purple-blue space color
    
    # Draw pre-generated stars (no random calls) 
    for x, y, brightness, size in STARS:
        color = (brightness, brightness, brightness)
        if size == 1:
            screen.set_at((x, y), color)
        else:
            pygame.draw.circle(screen, color, (x, y), 1)
    
    # Draw bright stars
    for x, y in BRIGHT_STARS:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)

def draw_hearts(screen, lives):
    heart_spacing = 40
    start_x = 20
    start_y = 20
    pixel_size = 2  # Size of each "pixel" in the heart
    
    # Define the pixel pattern for a heart (13x11 grid)
    heart_pattern = [
        [0,0,1,1,0,0,0,1,1,0,0],
        [0,1,1,1,1,0,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,1,1,1,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0],
    ]
    
    for i in range(lives):
        heart_x = start_x + i * heart_spacing
        heart_y = start_y
        
        # Draw each pixel of the heart
        for row in range(len(heart_pattern)):
            for col in range(len(heart_pattern[row])):
                if heart_pattern[row][col] == 1:
                    pixel_x = heart_x + col * pixel_size
                    pixel_y = heart_y + row * pixel_size
                    pygame.draw.rect(screen, "red", (pixel_x, pixel_y, pixel_size, pixel_size))

def draw_timer(screen, game_time, current_level, asteroids_killed):
    # Convert game_time (in seconds) to minutes:seconds:milliseconds format
    minutes = int(game_time // 60)
    seconds = int(game_time % 60)
    milliseconds = int((game_time % 1) * 100)
    
    # Format the time string
    time_str = f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
    
    # Calculate asteroids needed for next level
    if current_level < MAX_LEVEL:
        asteroids_needed_for_next = get_asteroids_needed_for_level(current_level + 1)
        asteroids_remaining = asteroids_needed_for_next - asteroids_killed
        progress_str = f"Next: {asteroids_remaining} kills"
    else:
        progress_str = "MAX LEVEL!"
    
    # Create fonts
    time_font = pygame.font.Font(None, 36)
    progress_font = pygame.font.Font(None, 28)
    
    # Render text surfaces
    time_surface = time_font.render(time_str, True, (255, 255, 255))
    progress_surface = progress_font.render(progress_str, True, (200, 200, 255))
    
    # Position in top-right corner
    time_rect = time_surface.get_rect()
    time_rect.topright = (SCREEN_WIDTH - 20, 20)
    
    progress_rect = progress_surface.get_rect()
    progress_rect.topright = (SCREEN_WIDTH - 20, 55)
    
    screen.blit(time_surface, time_rect)
    screen.blit(progress_surface, progress_rect)

def draw_level(screen, level):
    # Create font for the level display
    font = pygame.font.Font(None, 48)
    level_text = f"Level {level}"
    text_surface = font.render(level_text, True, (255, 255, 255))
    
    # Position in top-center of screen
    text_rect = text_surface.get_rect()
    text_rect.centerx = SCREEN_WIDTH // 2
    text_rect.top = 20
    
    screen.blit(text_surface, text_rect)

# Button class for menu interface
class Button:
    def __init__(self, x, y, width, height, text, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        
    def draw(self, screen):
        # Button colors
        if self.is_hovered:
            button_color = (100, 100, 200)  # Light blue when hovered
            text_color = (255, 255, 255)
        else:
            button_color = (50, 50, 150)   # Dark blue normally
            text_color = (200, 200, 200)
        
        # Draw button background
        pygame.draw.rect(screen, button_color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)  # White border
        
        # Draw button text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # Left click
                return True
        return False

def draw_menu(screen, buttons):
    # Draw space background
    draw_space_background(screen)
    
    # Draw coin display
    draw_coins(screen, save_system.get_coins())
    
    # Draw game title
    title_font = pygame.font.Font(None, 72)
    title_text = "Asteroids Game!"
    title_surface = title_font.render(title_text, True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
    screen.blit(title_surface, title_rect)
    
    # Draw subtitle
    subtitle_font = pygame.font.Font(None, 24)
    subtitle_text = "Survive 1000 levels of asteroid mayhem!"
    subtitle_surface = subtitle_font.render(subtitle_text, True, (200, 200, 255))
    subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(subtitle_surface, subtitle_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    # Draw GitHub link at bottom center (clickable)
    link_font = pygame.font.Font(None, 20)
    link_text = "https://github.com/MrPandayx/"
    link_surface = link_font.render(link_text, True, (150, 150, 255))
    link_rect = link_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
    screen.blit(link_surface, link_rect)
    
    # Return the link rect for click detection
    return link_rect

def draw_game_over_screen(screen, level, time, buttons, coins_earned=0):
    # Draw space background
    draw_space_background(screen)
    
    # Draw coin display
    draw_coins(screen, save_system.get_coins())
    
    # Draw game over title
    title_font = pygame.font.Font(None, 72)
    title_text = "GAME OVER"
    title_surface = title_font.render(title_text, True, (255, 100, 100))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
    screen.blit(title_surface, title_rect)
    
    # Draw stats
    stats_font = pygame.font.Font(None, 36)
    
    # Format time
    minutes = int(time // 60)
    seconds = int(time % 60)
    milliseconds = int((time % 1) * 100)
    time_str = f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
    
    level_text = f"Level Reached: {level}"
    time_text = f"Survival Time: {time_str}"
    coins_text = f"Coins Earned: {coins_earned}"
    
    level_surface = stats_font.render(level_text, True, (255, 255, 255))
    time_surface = stats_font.render(time_text, True, (255, 255, 255))
    coins_surface = stats_font.render(coins_text, True, (255, 215, 0))
    
    level_rect = level_surface.get_rect(center=(SCREEN_WIDTH // 2, 220))
    time_rect = time_surface.get_rect(center=(SCREEN_WIDTH // 2, 260))
    coins_rect = coins_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
    
    screen.blit(level_surface, level_rect)
    screen.blit(time_surface, time_rect)
    screen.blit(coins_surface, coins_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)

def draw_coins(screen, coins):
    """Draw coin display in bottom right corner"""
    font = pygame.font.Font(None, 36)
    
    # Draw coin icon (simple circle)
    coin_radius = 15
    coin_x = SCREEN_WIDTH - 120
    coin_y = SCREEN_HEIGHT - 40
    
    # Draw coin with gradient effect
    pygame.draw.circle(screen, (255, 215, 0), (coin_x, coin_y), coin_radius)  # Gold
    pygame.draw.circle(screen, (255, 255, 255), (coin_x - 3, coin_y - 3), coin_radius // 3)  # Highlight
    pygame.draw.circle(screen, (184, 134, 11), (coin_x, coin_y), coin_radius, 2)  # Dark gold border
    
    # Draw coin count
    coin_text = f"{coins}"
    coin_surface = font.render(coin_text, True, (255, 255, 255))
    screen.blit(coin_surface, (coin_x + 25, coin_y - 15))

def draw_shop(screen, buttons, shop_items, scroll_offset=0):
    """Draw the shop interface"""
    # Draw space background
    draw_space_background(screen)
    
    # Draw shop title
    title_font = pygame.font.Font(None, 72)
    title_text = "SHIP SKINS SHOP"
    title_surface = title_font.render(title_text, True, (255, 215, 0))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_surface, title_rect)
    
    # Draw coin display
    draw_coins(screen, save_system.get_coins())
    
    # Draw shop items
    items_per_row = 3
    item_width = 200
    item_height = 120
    start_x = (SCREEN_WIDTH - (items_per_row * item_width + (items_per_row - 1) * 20)) // 2
    start_y = 150 + scroll_offset
    
    owned_skins = save_system.get_owned_skins()
    current_skin = save_system.get_current_skin()
    
    for i, (skin_id, skin_data) in enumerate(PLAYER_SKINS.items()):
        row = i // items_per_row
        col = i % items_per_row
        
        x = start_x + col * (item_width + 20)
        y = start_y + row * (item_height + 30)
        
        # Skip if off screen
        if y < -item_height or y > SCREEN_HEIGHT:
            continue
        
        # Draw item background
        is_owned = skin_id in owned_skins
        is_current = skin_id == current_skin
        
        if is_current:
            bg_color = (50, 150, 50)  # Green for current
            border_color = (100, 255, 100)
        elif is_owned:
            bg_color = (50, 50, 150)  # Blue for owned
            border_color = (100, 100, 255)
        else:
            bg_color = (50, 50, 50)   # Gray for not owned
            border_color = (150, 150, 150)
        
        item_rect = pygame.Rect(x, y, item_width, item_height)
        pygame.draw.rect(screen, bg_color, item_rect)
        pygame.draw.rect(screen, border_color, item_rect, 3)
        
        # Draw preview triangle
        preview_center = (x + item_width // 2, y + 35)
        preview_radius = 15
        
        # Create triangle points
        triangle_points = []
        for angle in [0, 120, 240]:  # Triangle vertices
            angle_rad = math.radians(angle)
            point_x = preview_center[0] + preview_radius * math.cos(angle_rad)
            point_y = preview_center[1] + preview_radius * math.sin(angle_rad)
            triangle_points.append((point_x, point_y))
        
        # Get color for preview
        if skin_id == "rainbow":
            # Simple rainbow effect for preview
            time_offset = i * 0.5
            r = int(127 + 127 * math.sin(time_offset))
            g = int(127 + 127 * math.sin(time_offset + 2.09))
            b = int(127 + 127 * math.sin(time_offset + 4.18))
            preview_color = (r, g, b)
        else:
            preview_color = skin_data["color"]
        
        pygame.draw.polygon(screen, preview_color, triangle_points, 2)
        
        # Draw skin name
        name_font = pygame.font.Font(None, 24)
        name_surface = name_font.render(skin_data["name"], True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(x + item_width // 2, y + 70))
        screen.blit(name_surface, name_rect)
        
        # Draw price/status
        status_font = pygame.font.Font(None, 20)
        if is_current:
            status_text = "EQUIPPED"
            status_color = (100, 255, 100)
        elif is_owned:
            status_text = "OWNED"
            status_color = (100, 150, 255)
        else:
            status_text = f"{skin_data['price']} coins"
            status_color = (255, 215, 0)
        
        status_surface = status_font.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(x + item_width // 2, y + 95))
        screen.blit(status_surface, status_rect)
        
        # Store item rect for clicking
        shop_items.append({
            "rect": item_rect,
            "skin_id": skin_id,
            "skin_data": skin_data,
            "is_owned": is_owned,
            "is_current": is_current
        })
    
    # Draw navigation buttons
    for button in buttons:
        button.draw(screen)

class ShopItem:
    def __init__(self, x, y, width, height, skin_id, skin_data):
        self.rect = pygame.Rect(x, y, width, height)
        self.skin_id = skin_id
        self.skin_data = skin_data
        self.is_owned = skin_id in save_system.get_owned_skins()
        self.is_current = skin_id == save_system.get_current_skin()
    
    def handle_click(self):
        """Handle clicking on this shop item"""
        if self.is_current:
            return False  # Already equipped
        elif self.is_owned:
            # Equip this skin
            save_system.set_current_skin(self.skin_id)
            return True
        else:
            # Try to buy this skin
            if save_system.buy_skin(self.skin_id):
                save_system.set_current_skin(self.skin_id)
                return True
            return False  # Not enough coins

async def main():
    print("Initializing pygame...")
    pygame.init()
    print("Pygame initialized successfully!")
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids - 1000 Levels")
        print("Display initialized successfully!")
    except Exception as e:
        print(f"Error initializing display: {e}")
        return
        
    clock = pygame.time.Clock()
    
    # Game state
    current_state = MENU_STATE
    print(f"Initial game state: {current_state}")
    
    # Create menu buttons
    button_width = 200
    button_height = 60
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    print(f"Creating buttons at x={button_x}")
    
    try:
        play_button = Button(button_x, 280, button_width, button_height, "PLAY")
        shop_button = Button(button_x, 360, button_width, button_height, "SHOP") 
        quit_button = Button(button_x, 440, button_width, button_height, "QUIT")
        menu_buttons = [play_button, shop_button, quit_button]
        print(f"Created {len(menu_buttons)} menu buttons successfully!")
    except Exception as e:
        print(f"Error creating buttons: {e}")
        return
    
    # Create shop buttons
    back_button = Button(50, SCREEN_HEIGHT - 80, 120, 50, "BACK")
    shop_buttons = [back_button]
    
    # Create game over buttons
    play_again_button = Button(button_x, 350, button_width, button_height, "PLAY AGAIN")
    main_menu_button = Button(button_x, 430, button_width, button_height, "MAIN MENU")
    game_over_buttons = [play_again_button, main_menu_button]
    
    # Game variables (will be reset when starting new game)
    dt = 0
    game_time = 0
    current_level = 1
    asteroids_killed = 0
    final_level = 1
    final_time = 0
    coins_earned_this_game = 0
    starting_level = 1
    github_link_rect = None  # Store the GitHub link rect for click detection
    
    # Game objects (will be created when starting new game)
    updatable = None
    drawable = None
    asteroids = None
    shots = None
    shakes = None
    player = None
    asteroid_field = None
    shake_field = None
    
    print("Starting main game loop...")
    frame_count = 0
    while True:
        frame_count += 1
        if frame_count % 60 == 0:  # Log every second
            print(f"Game running... Frame {frame_count}, State: {current_state}")
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Handle menu events
            if current_state == MENU_STATE:
                # Handle GitHub link clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if github_link_rect and github_link_rect.collidepoint(event.pos):
                        print("Opening GitHub link...")
                        # GitHub link disabled for web version
                        pass
                
                for button in menu_buttons:
                    if button.handle_event(event):
                        if button == play_button:
                            # Start new game
                            current_state = GAME_STATE
                            
                            # Reset game variables
                            dt = 0
                            game_time = 0
                            current_level = 1
                            asteroids_killed = 0
                            coins_earned_this_game = 0
                            starting_level = current_level
                            
                            # Create groups
                            updatable = pygame.sprite.Group()
                            drawable = pygame.sprite.Group()
                            asteroids = pygame.sprite.Group()
                            shots = pygame.sprite.Group()
                            shakes = pygame.sprite.Group()
                            
                            # Set containers for all classes
                            Player.containers = (updatable, drawable)
                            Asteroid.containers = (asteroids, updatable, drawable)
                            AsteroidField.containers = (updatable,)
                            Shot.containers = (shots, updatable, drawable)
                            Shake.containers = (shakes, updatable, drawable)
                            ShakeField.containers = (updatable,)
                            
                            # Create game objects
                            x = SCREEN_WIDTH / 2
                            y = SCREEN_HEIGHT / 2
                            player = Player(x, y)
                            # Update player skin from save system
                            player.update_skin()
                            asteroid_field = AsteroidField()
                            shake_field = ShakeField()
                            
                        elif button == shop_button:
                            current_state = SHOP_STATE
                            
                        elif button == quit_button:
                            return
            
            # Handle shop events
            elif current_state == SHOP_STATE:
                shop_items = []  # Reset shop items list
                
                for button in shop_buttons:
                    if button.handle_event(event):
                        if button == back_button:
                            current_state = MENU_STATE
                
                # Handle shop item clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    
                    # Check shop items (we need to recreate the layout)
                    items_per_row = 3
                    item_width = 200
                    item_height = 120
                    start_x = (SCREEN_WIDTH - (items_per_row * item_width + (items_per_row - 1) * 20)) // 2
                    start_y = 150
                    
                    for i, (skin_id, skin_data) in enumerate(PLAYER_SKINS.items()):
                        row = i // items_per_row
                        col = i % items_per_row
                        
                        x = start_x + col * (item_width + 20)
                        y = start_y + row * (item_height + 30)
                        
                        item_rect = pygame.Rect(x, y, item_width, item_height)
                        
                        if item_rect.collidepoint(mouse_pos):
                            owned_skins = save_system.get_owned_skins()
                            current_skin = save_system.get_current_skin()
                            
                            if skin_id == current_skin:
                                continue  # Already equipped
                            elif skin_id in owned_skins:
                                # Equip this skin
                                save_system.set_current_skin(skin_id)
                                print(f"Equipped {skin_data['name']}")
                            else:
                                # Try to buy this skin
                                if save_system.buy_skin(skin_id):
                                    save_system.set_current_skin(skin_id)
                                    print(f"Bought and equipped {skin_data['name']} for {skin_data['price']} coins!")
                                else:
                                    print(f"Not enough coins! Need {skin_data['price']} coins for {skin_data['name']}")
                            break
            
            # Handle game over events
            elif current_state == GAME_OVER_STATE:
                for button in game_over_buttons:
                    if button.handle_event(event):
                        if button == play_again_button:
                            # Start new game
                            current_state = GAME_STATE
                            
                            # Reset game variables
                            dt = 0
                            game_time = 0
                            current_level = 1
                            asteroids_killed = 0
                            coins_earned_this_game = 0
                            starting_level = current_level
                            
                            # Create groups
                            updatable = pygame.sprite.Group()
                            drawable = pygame.sprite.Group()
                            asteroids = pygame.sprite.Group()
                            shots = pygame.sprite.Group()
                            shakes = pygame.sprite.Group()
                            
                            # Set containers for all classes
                            Player.containers = (updatable, drawable)
                            Asteroid.containers = (asteroids, updatable, drawable)
                            AsteroidField.containers = (updatable,)
                            Shot.containers = (shots, updatable, drawable)
                            Shake.containers = (shakes, updatable, drawable)
                            ShakeField.containers = (updatable,)
                            
                            # Create game objects
                            x = SCREEN_WIDTH / 2
                            y = SCREEN_HEIGHT / 2
                            player = Player(x, y)
                            # Update player skin from save system
                            player.update_skin()
                            asteroid_field = AsteroidField()
                            shake_field = ShakeField()
                            
                        elif button == main_menu_button:
                            current_state = MENU_STATE
        
        # Game logic
        if current_state == GAME_STATE:
            # Update all updatable objects
            updatable.update(dt)
            
            # Update game time
            game_time += dt
            
            # Update level based on asteroid kills
            asteroids_needed_for_next = get_asteroids_needed_for_level(current_level + 1)
            if asteroids_killed >= asteroids_needed_for_next and current_level < MAX_LEVEL:
                current_level += 1
                
                # Award coin for reaching new level
                save_system.add_coins(COINS_PER_LEVEL)
                coins_earned_this_game += COINS_PER_LEVEL
                
                asteroid_field.set_level(current_level)
                print(f"Level up! Now at level {current_level} (killed {asteroids_killed} asteroids) - Earned {COINS_PER_LEVEL} coin!")
            
            # Check for collisions between player and asteroids
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    if player.take_damage():
                        # Game over - save final stats
                        final_level = current_level
                        final_time = game_time
                        current_state = GAME_OVER_STATE
                        
                        # Award coins for levels completed (if any)
                        levels_completed = current_level - starting_level
                        if levels_completed > 0:
                            bonus_coins = levels_completed * COINS_PER_LEVEL
                            save_system.add_coins(bonus_coins)
                            coins_earned_this_game += bonus_coins
                        
                        # Format the final time for display
                        minutes = int(game_time // 60)
                        seconds = int(game_time % 60)
                        milliseconds = int((game_time % 1) * 100)
                        time_str = f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
                        print(f"Game over! You reached level {current_level} and survived for {time_str}")
                        print(f"Total coins earned this game: {coins_earned_this_game}")
                    else:
                        print(f"Hit! {player.lives} hearts remaining")
                    asteroid.kill()  # Remove the asteroid that hit the player
            
            # Check for collisions between player and shakes
            for shake in shakes:
                if player.collides_with(shake):
                    player.activate_shake_effect()
                    shake.kill()
                    print("Shake power-up collected! No shooting delay for 5 seconds!")
            
            # Check for collisions between shots and asteroids
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.kill()
                        asteroids_killed += 1  # Count the kill
        
        # Rendering
        if current_state == MENU_STATE:
            github_link_rect = draw_menu(screen, menu_buttons)
        elif current_state == SHOP_STATE:
            shop_items = []
            draw_shop(screen, shop_buttons, shop_items)
        elif current_state == GAME_STATE:
            draw_space_background(screen)  # Draw the space background
            
            # Draw all drawable objects
            for sprite in drawable:
                sprite.draw(screen)
            
            draw_hearts(screen, player.lives)  # Draw the player's lives as hearts
            draw_coins(screen, save_system.get_coins())  # Draw coin display
            draw_timer(screen, game_time, current_level, asteroids_killed)  # Draw the timer and progress
            draw_level(screen, current_level)  # Draw the current level
        elif current_state == GAME_OVER_STATE:
            draw_game_over_screen(screen, final_level, final_time, game_over_buttons, coins_earned_this_game)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
