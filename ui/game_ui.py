import pygame

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

        # Set up key repeat
        pygame.key.set_repeat(500, 50)

    def _load_background(self):
        """Load and scale background image or create gradient"""
        try:
            background = pygame.image.load("assets/Background/Pale/Background.png")
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            return background
        except Exception as e:
            print(f"Could not load background: {e}")
            # Create a solid color surface if image not found
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((40, 40, 60))  # Dark blue-grey color
            return background

    def handle_event(self, event):
        """
        Handle pygame events

        Args:
            event: pygame event object

        Returns:
            bool: True to continue game, False to quit
        """
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
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

            # Add regular characters
            elif len(self.pressed_key) == 1:
                self.message.append(self.pressed_key)
                self.check_result = ""

        return True

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
