# Web-compatible version of Asteroids Game
import pygame
import asyncio
import math
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from shake import Shake
from shakefield import ShakeField
from save_system import save_system

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
    
    # Create a subtle gradient effect
    for y in range(0, SCREEN_HEIGHT, 10):
        alpha = int(30 * (1 - y / SCREEN_HEIGHT))
        if alpha > 0:
            gradient_color = (15 + alpha, 10 + alpha, 35 + alpha)
            pygame.draw.rect(screen, gradient_color, (0, y, SCREEN_WIDTH, 10))
    
    # Draw stars
    for x, y, brightness, size in STARS:
        star_color = (brightness, brightness, brightness)
        if size == 1:
            pygame.draw.circle(screen, star_color, (x, y), 1)
        else:
            pygame.draw.circle(screen, star_color, (x, y), 2)
    
    # Draw larger bright stars with twinkling effect
    for x, y in BRIGHT_STARS:
        # Simple twinkling by varying the brightness
        twinkle = 50 + 50 * math.sin(pygame.time.get_ticks() * 0.01 + x * 0.1)
        star_color = (200 + twinkle, 200 + twinkle, 255)
        pygame.draw.circle(screen, star_color, (x, y), 2)
        # Add a subtle glow
        pygame.draw.circle(screen, (100, 100, 150), (x, y), 4, 1)

def draw_hearts(screen, lives):
    heart_size = 20
    heart_spacing = 30
    start_x = 20
    start_y = 20
    
    for i in range(lives):
        heart_x = start_x + i * heart_spacing
        heart_y = start_y
        
        # Draw a pixelated heart shape
        # Heart is made of squares to look retro/pixelated
        heart_color = (255, 100, 100)  # Red color
        
        # Define heart pattern (each 1 represents a filled pixel)
        heart_pattern = [
            [0,1,1,0,1,1,0],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [0,1,1,1,1,1,0],
            [0,0,1,1,1,0,0],
            [0,0,0,1,0,0,0]
        ]
        
        # Draw the heart pixel by pixel
        pixel_size = 3
        for row_idx, row in enumerate(heart_pattern):
            for col_idx, pixel in enumerate(row):
                if pixel == 1:
                    pixel_x = heart_x + col_idx * pixel_size
                    pixel_y = heart_y + row_idx * pixel_size
                    pygame.draw.rect(screen, heart_color, 
                                   (pixel_x, pixel_y, pixel_size, pixel_size))

def draw_timer(screen, time, level, asteroids_killed):
    font = pygame.font.Font(None, 36)
    
    # Format time as MM:SS:MS
    minutes = int(time // 60)
    seconds = int(time % 60)
    milliseconds = int((time % 1) * 100)
    time_str = f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
    
    time_text = f"Time: {time_str}"
    time_surface = font.render(time_text, True, (255, 255, 255))
    screen.blit(time_surface, (20, 80))
    
    # Show progress to next level
    asteroids_needed = get_asteroids_needed_for_level(level + 1)
    progress_text = f"Next Level: {asteroids_killed}/{asteroids_needed} kills"
    progress_surface = font.render(progress_text, True, (255, 255, 255))
    screen.blit(progress_surface, (20, 120))

def draw_level(screen, level):
    font = pygame.font.Font(None, 48)
    level_text = f"Level: {level}"
    level_surface = font.render(level_text, True, (255, 255, 255))
    screen.blit(level_surface, (SCREEN_WIDTH - 200, 20))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
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

async def main():
    pygame.init()
    print("Starting Asteroids Game for Web!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids Game - 1000 Levels")
    clock = pygame.time.Clock()
    
    # Game state
    current_state = MENU_STATE
    
    # Create menu buttons
    button_width = 200
    button_height = 60
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    
    play_button = Button(button_x, 280, button_width, button_height, "PLAY")
    shop_button = Button(button_x, 360, button_width, button_height, "SHOP") 
    quit_button = Button(button_x, 440, button_width, button_height, "QUIT")
    menu_buttons = [play_button, shop_button, quit_button]
    
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
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            # Handle menu events
            if current_state == MENU_STATE:
                # Handle GitHub link clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if github_link_rect and github_link_rect.collidepoint(event.pos):
                        print("GitHub link clicked - would open in web version")
                        # In web version, this would open the link
                
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
                            running = False
            
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
        await asyncio.sleep(0)  # Allow other tasks to run

if __name__ == "__main__":
    asyncio.run(main())
