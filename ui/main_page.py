import pygame

class MainPage:
    def __init__(self, screen, font , screenWidth, screenHeight):
        self.screen = screen
        self.font = pygame.font.Font(font,50)
        self.font1 = pygame.font.Font(font,20)
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.background = self._load_background()

    def _load_background(self):
            """Load and scale background image or create gradient"""
            try:
                background = pygame.image.load('assets/Background/Sea/background.png')
                background = pygame.transform.scale(background, (self.screenWidth, self.screenHeight))
                return background
            except Exception as e:
                print(f"Could not load background: {e}")
                # Return a solid color surface instead of None
                background = pygame.Surface((self.screenWidth, self.screenHeight))
                background.fill((20, 100, 150))  # Sea blue color
                return background
    def render(self):
        self.screen.blit(self.background, (0, 0))

        title = self.font.render('Text Or Death', True, (0, 0, 0))
        text1 = self.font1.render('press any key', True, (90, 90, 90))

        title_rect = title.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
        text1_rect = text1.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2 + 60))

        self.screen.blit(title, title_rect)
        self.screen.blit(text1, text1_rect)
