import os
import sys
import pygame
import json
# Ensure the project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.checkword import WordChecker
from ui.game_ui import GameScreen
from ui.main_page import MainPage

def main():
    """Main game loop - acts as a layout/container"""
    # Load config
    with open("config.json", "r") as f:
        default_data = json.load(f)

    screen_width = int(default_data["client"]["screen_width"])
    screen_height = int(default_data["client"]["screen_height"])

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TextOrDeath")

    # Initialize word checker
    word_checker = WordChecker("en_US")

    font1 = 'assets/fonts/Bungee-Regular.ttf'
    font2 = 'assets/fonts/IndieFlower-Regular.ttf'
    font3 = 'assets/fonts/Parkinsans-Regular.ttf'

    # Initialize game screen component (pass config)
    game_screen = GameScreen(screen, word_checker, default_data, font3)
    main_page = MainPage(screen, font3, screen_width, screen_height)

    # Main game loop
    game_run = True
    mainPage = True
    clock = pygame.time.Clock()

    while game_run:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                break

            if mainPage:
                # Any key press transitions to game screen
                if event.type == pygame.KEYDOWN:
                    mainPage = False
            else:
                # Let game screen handle events
                game_run = game_screen.handle_event(event)
                if not game_run:
                    break

        # Render
        if mainPage:
            main_page.render()
        else:
            game_screen.update()
            game_screen.render()

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
