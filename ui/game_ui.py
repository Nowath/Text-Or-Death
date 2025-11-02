import pygame
from ui.character import Character
from ui.button import Button  # Import Button from separate file

class GameScreen:
    def __init__(self, screen, word_checker, config, font):
        """
        Initialize the game screen component

        Args:
            screen: pygame display surface
            word_checker: WordChecker instance
            config: configuration dictionary from config.json
        """
        self.screen = screen
        self.word_checker = word_checker

        # Get screen dimensions from config
        self.screen_width = int(config["client"]["screen_width"])
        self.screen_height = int(config["client"]["screen_height"])

        # Set up font
        self.font = pygame.font.Font(font, 50)

        # Load background
        self.background = self._load_background()

        # Game state
        self.message = []
        self.pressed_key = ""
        self.check_result = ""
        self.result_color = (255, 255, 255)

        # Create player character at bottom center of screen
        char_x = self.screen_width // 2 - 25  # Center (assuming width=50)
        char_y = self.screen_height - 100  # 100 pixels from bottom
        self.player1 = Character(char_x, char_y)

        # Create button in top right corner
        button_width = 120
        button_height = 50
        button_x = self.screen_width - button_width - 20  # 20px from right edge
        button_y = 20  # 20px from top
        self.menu_button = Button(
            button_x, button_y, button_width, button_height,
            "Menu",
            font_size=30,
            color=(70, 130, 180),
            hover_color=(100, 160, 210)
        )

        # Set up key repeat
        pygame.key.set_repeat(500, 50)

    def _load_background(self):
        """Load and scale background image or create gradient"""
        try:
            background = pygame.image.load("assets/Background/Sea/background_sea.jpg")
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            return background
        except Exception as e:
            print(f"Could not load background: {e}")
            # Create a solid color surface if image not found
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((40, 40, 60))  # Dark blue-grey color
            return background

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        # Check if button was clicked
        if self.menu_button.is_clicked(event):
            print("Menu button clicked!")
            # Add your button action here
            # For example: return "menu" to switch to menu screen

        # ส่ง event ให้ Character จัดการการเคลื่อนที่
        self.player1.handle_event(event)

        if event.type == pygame.KEYDOWN:
            self.pressed_key = pygame.key.name(event.key)

            # Handle backspace
            if event.key == pygame.K_BACKSPACE and self.message:
                self.message.pop()
                self.check_result = ""

            # Handle Enter key
            elif event.key == pygame.K_RETURN:
                current_text = "".join(self.message)
                is_valid, result_message, color = self.word_checker.check_word(current_text)
                self.check_result = "word" if is_valid else "not word"
                self.result_color = color

            # Handle space
            elif event.key == pygame.K_SPACE:
                self.message.append(" ")
                self.check_result = ""

            elif len(self.pressed_key) == 1 and (self.pressed_key not in ["a","d"]):
                self.message.append(self.pressed_key)
                self.check_result = ""

        return True

    def update(self):
        """Update game state (call this in main game loop)"""
        # Update button animation
        mouse_pos = pygame.mouse.get_pos()
        self.menu_button.update(mouse_pos)

        # Update player
        self.player1.update(self.screen_width)

    def render(self):
        """Render all UI elements"""
        # Draw background (bottom layer)
        self.screen.blit(self.background, (0, 0))

        # Render pressed key text
        if self.pressed_key:
            text = self.font.render(f"Key pressed: {self.pressed_key}", True, (255, 255, 255))
            text_x = self.screen_width // 2 - text.get_width() // 2
            text_y = self.screen_height // 2
            self.screen.blit(text, (text_x, text_y))

        # Render message
        message_text = "".join(self.message)
        message_render = self.font.render(message_text, True, (255, 255, 255))
        message_x = self.screen_width // 2 - message_render.get_width() // 2
        message_y = self.screen_height // 2 + 60
        self.screen.blit(message_render, (message_x, message_y))

        # Render check result
        if self.check_result:
            result_render = self.font.render(self.check_result, True, self.result_color)
            result_x = self.screen_width // 2 - result_render.get_width() // 2
            result_y = self.screen_height // 2 + 100
            self.screen.blit(result_render, (result_x, result_y))

        # Render character (top layer)
        self.player1.render(self.screen)

        # Render button (top layer - last so it's on top)
        self.menu_button.draw(self.screen)
