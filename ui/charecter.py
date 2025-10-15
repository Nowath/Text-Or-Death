import pygame
import os

class Charecter:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        
        # Load the sprite sheet
        sprite_path = os.path.join('assets', 'Fighter', 'Idle.png')
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        
        # Animation settings
        self.frame_width = 48  # Adjust based on your sprite dimensions
        self.frame_height = 48  # Adjust based on your sprite dimensions
        self.total_frames = 6  # 6 frames in your idle animation
        self.current_frame = 0
        self.animation_speed = 0.15  # Adjust for faster/slower animation
        self.animation_counter = 0
        
        # Extract frames from sprite sheet
        self.idle_frames = []
        self.load_frames()
        
    def load_frames(self):
        """Extract individual frames from the sprite sheet"""
        for i in range(self.total_frames):
            # Create a surface for each frame
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            # Blit the portion of sprite sheet onto the frame
            frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            self.idle_frames.append(frame)
    
    def update(self):
        """Update animation frame"""
        self.animation_counter += self.animation_speed
        
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % self.total_frames
    
    def draw(self, surface):
        """Draw the current animation frame"""
        current_image = self.idle_frames[self.current_frame]
        surface.blit(current_image, (self.x, self.y))
    
    def set_position(self, x, y):
        """Update character position"""
        self.x = x
        self.y = y