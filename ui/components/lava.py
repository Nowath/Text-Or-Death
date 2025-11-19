# import pygame


# class Lava:
#     def __init__(self, screen_width, screen_height):
#         """Initialize lava system"""
#         self.screen_width = screen_width
#         self.screen_height = screen_height
        
#         # Lava properties
#         self.lava_y = screen_height  # Start below screen
#         self.lava_height = 100
#         self.lava_speed = 0  # Will be set to constant speed after start_question
#         self.start_question = 3  # Lava starts rising after this many questions
#         self.constant_speed = 0.5  # Constant speed (not increasing)
        
#         # Colors
#         self.lava_color = (255, 50, 0)  # Bright red-orange
#         self.lava_top_color = (200, 0, 0)  # Dark red
    
#     def start_rising(self):
#         """Start lava rising at constant speed"""
#         if self.lava_speed == 0:
#             self.lava_speed = self.constant_speed
    
#     def lower_lava(self, amount):
#         """Lower the lava by a certain amount"""
#         self.lava_y = min(self.screen_height, self.lava_y + amount)
    
#     def update(self):
#         """Update lava position"""
#         if self.lava_speed > 0:
#             self.lava_y -= self.lava_speed
    
#     def check_collision(self, character):
#         """Check if lava touches the character"""
#         char_bottom = character.y + character.height
#         return char_bottom >= self.lava_y
    
#     def render(self, screen):
#         """Render the lava"""
#         if self.lava_y < self.screen_height:
#             # Draw main lava body
#             lava_rect = pygame.Rect(0, self.lava_y, self.screen_width, 
#                                    self.screen_height - self.lava_y)
#             pygame.draw.rect(screen, self.lava_color, lava_rect)
            
#             # Add darker red on top for effect
#             top_lava = pygame.Rect(0, self.lava_y, self.screen_width, 20)
#             pygame.draw.rect(screen, self.lava_top_color, top_lava)
    
#     def reset(self):
#         """Reset lava to initial state"""
#         self.lava_y = self.screen_height
#         self.lava_speed = 0


import pygame
from PIL import Image

class Lava:
    def __init__(self, screen_width, screen_height):
        """Initialize lava system"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Lava properties
        self.lava_y = screen_height  # Start below screen
        self.lava_height = 500
        self.lava_speed = 0  # Will be set to constant speed after start_question
        self.start_question = 3  # Lava starts rising after this many questions
        self.constant_speed = 0.5  # Constant speed (not increasing)

        # Load lava GIF frames
        self.frames = []
        self.current_frame = 0
        self.frame_delay = 40  # milliseconds between frames
        self.last_frame_time = pygame.time.get_ticks()

        try:
            # Load GIF using PIL
            gif = Image.open('assets/new_lava.gif')
            # gif = pygame.transform.scale(gif, (640,480))

            # Extract all frames from GIF
            for frame_num in range(gif.n_frames):
                gif.seek(frame_num)
                # Convert PIL image to pygame surface
                frame = gif.convert('RGBA')
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()

                # Create pygame surface
                pygame_surface = pygame.image.fromstring(data, size, mode)
                # Scale the frame to 1280x500
                scaled_surface = pygame.transform.scale(
                    pygame_surface,
                    (1280, 500)
                )
                self.frames.append(scaled_surface)

            print(f"Loaded {len(self.frames)} frames from GIF")

        except Exception as e:
            # Fallback to colored rectangle if image not found
            self.frames = []
            print(f"Warning: assets/output2.gif not found ({e}), using default lava rendering")

        # Colors (fallback)
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
        """Update lava position and animation"""
        if self.lava_speed > 0:
            self.lava_y -= self.lava_speed

        # Update animation frame
        if len(self.frames) > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time > self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.last_frame_time = current_time
    
    def check_collision(self, character):
        """Check if lava touches the character"""
        char_bottom = character.y + character.height
        return char_bottom >= self.lava_y
    
    def render(self, screen):
        """Render the lava"""
        if self.lava_y < self.screen_height:
            if len(self.frames) > 0:
                # Draw red background first
                red_background = pygame.Rect(0, self.lava_y+50, self.screen_width,
                                            self.screen_height - self.lava_y)
                pygame.draw.rect(screen, (169, 59, 59), red_background)

                # Draw GIF frame once at the lava position
                screen.blit(self.frames[self.current_frame], (0, self.lava_y))
            else:
                # Fallback: Draw main lava body
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
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()