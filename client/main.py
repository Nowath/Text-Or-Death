import os
import sys
import pygame
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.checkword import WordChecker
from ui.page.game_ui import GameScreen
from ui.page.main_page import MainPage
from ui.page.splash_screen import SplashScreen
from ui.page.character_select import CharacterSelectScreen

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

    # Show splash screen
    splash = SplashScreen(screen, logo_path='assets/logo/logopygame.png', duration=2000)
    if not splash.show():  # ถ้า user กด quit ระหว่าง splash
        pygame.quit()
        return

    # Initialize word checker
    word_checker = WordChecker("en_US")
    font3 = 'assets/fonts/Parkinsans-Regular.ttf'

    # Initialize pages
    main_page = MainPage(screen, font3, screen_width, screen_height)
    character_select = CharacterSelectScreen(screen, font3, screen_width, screen_height)
    game_screen = None
    selected_character = None

    # Main game loop
    game_run = True
    current_screen = "main"  # "main", "character_select", "game"
    clock = pygame.time.Clock()

    while game_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                break
            
            if current_screen == "main":
                if event.type == pygame.KEYDOWN:
                    # Go to character select
                    current_screen = "character_select"
            
            elif current_screen == "character_select":
                result = character_select.handle_event(event)
                if result and result != False:
                    if result == "back":
                        current_screen = "main"
                    else:
                        # Character selected, start game
                        selected_character = result
                        game_screen = GameScreen(screen, word_checker, default_data, font3, selected_character)
                        current_screen = "game"
            
            elif current_screen == "game":
                result = game_screen.handle_event(event)
                if result == "menu":
                    # Return to main page
                    current_screen = "main"
                    game_screen = None
                elif not result:
                    # Quit game
                    game_run = False
                    break

        # Render
        if current_screen == "main":
            main_page.render()
        elif current_screen == "character_select":
            character_select.render()
        elif current_screen == "game":
            game_screen.update()
            game_screen.render()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

#juhfguikjugh
