SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3

SHOT_RADIUS = 5

# Player lives/hearts
PLAYER_LIVES = 3

# Power-up constants
SHAKE_RADIUS = 30  # 2x bigger (was 15)
SHAKE_SPAWN_RATE = 15.0  # seconds
SHAKE_EFFECT_DURATION = 5.0  # seconds

# Coin and shop system
COINS_PER_LEVEL = 1  # Coins earned per level completed
STARTING_COINS = 0   # Starting amount of coins

# Player skin colors and prices
PLAYER_SKINS = {
    "white": {"color": (255, 255, 255), "price": 0, "name": "Default White"},
    "red": {"color": (255, 100, 100), "price": 5, "name": "Racing Red"},
    "blue": {"color": (100, 150, 255), "price": 8, "name": "Ocean Blue"},
    "green": {"color": (100, 255, 100), "price": 10, "name": "Neon Green"},
    "purple": {"color": (200, 100, 255), "price": 12, "name": "Royal Purple"},
    "gold": {"color": (255, 215, 0), "price": 15, "name": "Golden Elite"},
    "cyan": {"color": (0, 255, 255), "price": 18, "name": "Cyber Cyan"},
    "orange": {"color": (255, 165, 0), "price": 20, "name": "Fire Orange"},
    "pink": {"color": (255, 192, 203), "price": 25, "name": "Hot Pink"},
    "rainbow": {"color": (255, 255, 255), "price": 50, "name": "Rainbow Special"}  # Special effect
}

# Level system constants
MAX_LEVEL = 1000
LEVEL_UP_TIME = 10.0  # seconds per level (backup system)
BASE_ASTEROID_SPAWN_RATE = 1.5  # slowest spawn rate (level 1)
MIN_ASTEROID_SPAWN_RATE = 0.05  # fastest spawn rate (level 1000) - even faster for extreme levels
BASE_ASTEROID_SPEED_MIN = 20     # slowest speed range (level 1)
BASE_ASTEROID_SPEED_MAX = 40
MAX_ASTEROID_SPEED_MIN = 100     # fastest speed range (level 100)
MAX_ASTEROID_SPEED_MAX = 200

# Kill-based level up system
def get_asteroids_needed_for_level(level):
    """Calculate how many asteroids need to be destroyed to reach the given level"""
    return level * 2  # Level 2 needs 2 kills, Level 3 needs 4 total, etc.
