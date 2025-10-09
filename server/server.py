"""
Text or Death - Game Server
"""
import socket
import threading
import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import Config
from game.game_server import GameServer

def main():
    config = Config()
    server = GameServer(config)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server.stop()

if __name__ == "__main__":
    main()