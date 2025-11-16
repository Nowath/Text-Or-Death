import pygame
from io import BytesIO

class Character:
    def __init__(self, x, y, width=50, height=50, speed=5, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.velocity_x = 0

        # Load character sprite
        if image_path is None:
            image_path = 'assets/Items/000_0017_star3.png'
        
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
            self.use_image = True
        except Exception as e:
            print(f"Could not load character image {image_path}: {e}")
            self.use_image = False
            self.color = (255, 100, 100)  # Red color

    def handle_event(self, event):
        """Handle key press and release events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.velocity_x = -self.speed
            elif event.key == pygame.K_d:
                self.velocity_x = self.speed

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a and self.velocity_x < 0:
                self.velocity_x = 0
            elif event.key == pygame.K_d and self.velocity_x > 0:
                self.velocity_x = 0

    def update(self, screen_width):
        """Update character position"""
        self.x += self.velocity_x

        # Keep character within screen bounds
        if self.x < 0:
            self.x = 0
        elif self.x > screen_width - self.width:
            self.x = screen_width - self.width

    def render(self, screen):
        """Draw the character"""
        if self.use_image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color,
                           (self.x, self.y, self.width, self.height))
