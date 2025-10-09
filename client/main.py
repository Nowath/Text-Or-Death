"""
Text or Death - Client Main Entry Point
"""
import pygame
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_client import GameClient
from utils.config import Config

def main():
    pygame.init()
    
    config = Config()
    client = GameClient(config)
    
    try:
        client.run()
    except KeyboardInterrupt:
        print("Game interrupted by user")
    finally:
        client.cleanup()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()