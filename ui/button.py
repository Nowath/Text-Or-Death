import pygame

class Button:
    def __init__(self, x, y, width, height, text, font_size=30,
                 color=(70, 130, 180), hover_color=(100, 160, 210),
                 text_color=(255, 255, 255), border_radius=10):
        """
        Initialize a button with hover animation.

        Args:
            x, y: Position of the button
            width, height: Size of the button
            text: Text to display on the button
            font_size: Size of the text
            color: Default button color (RGB)
            hover_color: Color when hovering (RGB)
            text_color: Color of the text (RGB)
            border_radius: Radius for rounded corners
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius

        # Animation properties
        self.current_color = list(color)
        self.target_color = list(color)
        self.animation_speed = 10  # Higher = faster transition

        # Scale animation
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.05

        # Font
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False

    def update(self, mouse_pos):
        """Update button state and animations."""
        # Check if mouse is hovering
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Set target colors and scale based on hover state
        if self.is_hovered:
            self.target_color = list(self.hover_color)
            self.target_scale = 1.05
        else:
            self.target_color = list(self.color)
            self.target_scale = 1.0

        # Smooth color transition
        for i in range(3):
            if self.current_color[i] < self.target_color[i]:
                self.current_color[i] = min(self.current_color[i] + self.animation_speed,
                                           self.target_color[i])
            elif self.current_color[i] > self.target_color[i]:
                self.current_color[i] = max(self.current_color[i] - self.animation_speed,
                                           self.target_color[i])

        # Smooth scale transition
        if self.scale < self.target_scale:
            self.scale = min(self.scale + self.scale_speed, self.target_scale)
        elif self.scale > self.target_scale:
            self.scale = max(self.scale - self.scale_speed, self.target_scale)

    def draw(self, surface):
        """Draw the button on the surface."""
        # Calculate scaled dimensions
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2

        # Create scaled rect
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)

        # Draw button
        pygame.draw.rect(surface, self.current_color, scaled_rect,
                        border_radius=self.border_radius)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """Check if button was clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False
