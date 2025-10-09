"""
Configuration management for Text or Death game
"""
import json
import os

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            "client": {
                "screen_width": 1024,
                "screen_height": 768,
                "fps": 60,
                "server_host": "localhost",
                "server_port": 8888
            },
            "server": {
                "host": "localhost",
                "port": 8888,
                "max_players": 4,
                "round_time": 30
            },
            "game": {
                "typing_time_limit": 10,
                "words_per_round": 5,
                "difficulty_levels": ["easy", "medium", "hard"]
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                config = self.default_config.copy()
                config.update(loaded_config)
                return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config
        else:
            self.save_config()
            return self.default_config
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get(self, section, key=None):
        if key:
            return self.config.get(section, {}).get(key)
        return self.config.get(section, {})