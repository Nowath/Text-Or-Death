import pygame


class Lava:
    def __init__(self, screen_width, screen_height):
        """Initialize lava system"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Lava properties
        self.lava_y = screen_height  # Start below screen
        self.lava_height = 100
        self.lava_speed = 0  # Will be set to constant speed after start_question
        self.start_question = 3  # Lava starts rising after this many questions
        self.constant_speed = 0.5  # Constant speed (not increasing)
        
        # Colors
        self.lava_color = (255, 50, 0)  # Bright red-orange
        self.lava_top_color = (200, 0, 0)  # Dark red
    
    def start_rising(self):
        """Start lava rising at constant speed"""
        if self.lava_speed == 0:
            self.lava_speed = self.constant_speed
    
    def lower_lava(self, amount):
        """Lower the lava by a certain amount"""
        self.lava_y = min(self.screen_height, self.lava_y + amount)
    
    def update(self):
        """Update lava position"""
        if self.lava_speed > 0:
            self.lava_y -= self.lava_speed
    
    def check_collision(self, character):
        """Check if lava touches the character"""
        char_bottom = character.y + character.height
        return char_bottom >= self.lava_y
    
    def render(self, screen):
        """Render the lava"""
        if self.lava_y < self.screen_height:
            # Draw main lava body
            lava_rect = pygame.Rect(0, self.lava_y, self.screen_width, 
                                   self.screen_height - self.lava_y)
            pygame.draw.rect(screen, self.lava_color, lava_rect)
            
            # Add darker red on top for effect
            top_lava = pygame.Rect(0, self.lava_y, self.screen_width, 20)
            pygame.draw.rect(screen, self.lava_top_color, top_lava)
    
    def reset(self):
        """Reset lava to initial state"""
        self.lava_y = self.screen_height
        self.lava_speed = 0
