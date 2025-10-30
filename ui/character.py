import pygame
import os
from utils.spritesheet import SpriteSheet  # Adjust the import path as needed

# idle run `

class Character:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

        # Load the sprite sheet
        sprite_path = os.path.join('assets', 'Fighter', 'Idle.png')
        sprite_sheet_image = pygame.image.load(sprite_path).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        # Animation settings
        self.frame_width = 48  # Adjust based on your sprite dimensions
        self.frame_height = 48  # Adjust based on your sprite dimensions
        self.scale = 3  # Scale up the sprite (adjust as needed)
        self.total_frames = 6  # 6 frames in your idle animation
        self.current_frame = 0
        self.animation_speed = 0.15  # Adjust for faster/slower animation
        self.animation_counter = 0

        # Extract frames from sprite sheet
        self.idle_frames = []
        self.load_frames(sprite_sheet)

    def load_frames(self, sprite_sheet):
        """Extract individual frames from the sprite sheet"""
        for i in range(self.total_frames):
            # Use your SpriteSheet.get_image method
            # The colour parameter is for transparency (usually black (0,0,0) or white (255,255,255))
            frame = sprite_sheet.get_image(
                i,  # frame number
                self.frame_width,  # width
                self.frame_height,  # height
                self.scale,  # scale
                (0, 0, 0)  # color key for transparency (try (0,0,0) or (255,255,255))
            )
            self.idle_frames.append(frame)
        print(f"Loaded {len(self.idle_frames)} frames")  # DEBUG

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

        # DEBUG: Draw a red rectangle to show where character should be
        rect_width = self.frame_width * self.scale
        rect_height = self.frame_height * self.scale
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, rect_width, rect_height), 2)

    def set_position(self, x, y):
        """Update character position"""
        self.x = x
        self.y = y
