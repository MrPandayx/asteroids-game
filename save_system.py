import json
import os
from constants import STARTING_COINS

SAVE_FILE = "game_save.json"

class SaveSystem:
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """Load save data from file, create default if not exists"""
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Default save data
        return {
            "coins": STARTING_COINS,
            "owned_skins": ["white"],  # Default skin is always owned
            "current_skin": "white"
        }
    
    def save_data(self):
        """Save current data to file"""
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError:
            print("Failed to save game data")
    
    def get_coins(self):
        return self.data.get("coins", STARTING_COINS)
    
    def add_coins(self, amount):
        self.data["coins"] = self.data.get("coins", STARTING_COINS) + amount
        self.save_data()
    
    def spend_coins(self, amount):
        """Returns True if successful, False if not enough coins"""
        current_coins = self.data.get("coins", STARTING_COINS)
        if current_coins >= amount:
            self.data["coins"] = current_coins - amount
            self.save_data()
            return True
        return False
    
    def get_owned_skins(self):
        return self.data.get("owned_skins", ["white"])
    
    def buy_skin(self, skin_id):
        """Returns True if successful, False if already owned or not enough coins"""
        owned_skins = self.get_owned_skins()
        if skin_id in owned_skins:
            return False  # Already owned
        
        from constants import PLAYER_SKINS
        if skin_id not in PLAYER_SKINS:
            return False  # Invalid skin
        
        price = PLAYER_SKINS[skin_id]["price"]
        if self.spend_coins(price):
            self.data["owned_skins"].append(skin_id)
            self.save_data()
            return True
        return False
    
    def get_current_skin(self):
        return self.data.get("current_skin", "white")
    
    def set_current_skin(self, skin_id):
        """Returns True if successful, False if not owned"""
        if skin_id in self.get_owned_skins():
            self.data["current_skin"] = skin_id
            self.save_data()
            return True
        return False

# Global save system instance
save_system = SaveSystem()
