import pygame


class BlockManager:
    def __init__(self, screen_width, screen_height, block_width=140, block_height=60):
        """Initialize block manager"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_width = block_width
        self.block_height = block_height
        self.block_spacing = -26
        self.block_base_y = screen_height - 60
        self.animation_speed = 0.15
        
        # List of blocks: [(letter, x, y, animation_progress), ...]
        self.blocks = []
        
        # Load block images
        self.block_top_image = self._load_block_image('assets/Block/top.png',True)
        self.block_bottom_image = self._load_block_image('assets/Block/bottom.png', False)
        
        # Font for letters
        self.block_font = None  # Will be set from outside
    
    def _load_block_image(self, path, isTop):
        """Load and scale block image"""
        try:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (self.block_width if not isTop else self.block_width-20, self.block_height))
            return image
        except Exception as e:
            print(f"Could not load block image {path}: {e}")
            return None
    
    
    def set_font(self, font):
        """Set the font for rendering letters"""
        self.block_font = font
    
    def add_blocks(self, word):
        """Add blocks for a word (reversed so first letter is at bottom)"""
        reversed_word = word[::-1]
        for letter in reversed_word:
            x = self.screen_width // 2 - self.block_width // 2
            y = self.block_base_y - len(self.blocks) * (self.block_height + self.block_spacing)
            self.blocks.append((letter, x, y, 0.0))  # 0.0 = animation just started
        
        self._remove_bottom_blocks_if_needed()
    
    def _remove_bottom_blocks_if_needed(self):
        """Remove blocks from bottom if tower gets too high"""
        min_y = 180  # Minimum Y position for top block
        
        while self.blocks:
            top_block_y = self._get_top_block_y()
            if top_block_y < min_y:
                self.blocks.pop(0)
                self._recalculate_positions()
            else:
                break
    
    def _recalculate_positions(self):
        """Recalculate all block positions after removing bottom blocks"""
        temp_blocks = self.blocks.copy()
        self.blocks = []
        for letter, _, _, anim_progress in temp_blocks:
            x = self.screen_width // 2 - self.block_width // 2
            y = self.block_base_y - len(self.blocks) * (self.block_height + self.block_spacing)
            self.blocks.append((letter, x, y, anim_progress))
    
    def _get_top_block_y(self):
        """Get Y position of the top block"""
        if self.blocks:
            return self.block_base_y - len(self.blocks) * (self.block_height + self.block_spacing)
        return self.block_base_y
    
    def get_character_position(self, char_width=50, char_height=50):
        """Calculate character position on top of blocks"""
        if self.blocks:
            top_block_y = self._get_top_block_y()
            char_x = self.screen_width // 2 - char_width // 2
            char_y = top_block_y - 10  # 10 pixels above top block
            return char_x, char_y
        else:
            return self.screen_width // 2 - char_width // 2, self.screen_height - 100
    
    def update(self):
        """Update block animations"""
        updated_blocks = []
        for letter, x, y, anim_progress in self.blocks:
            if anim_progress < 1.0:
                anim_progress = min(1.0, anim_progress + self.animation_speed)
            updated_blocks.append((letter, x, y, anim_progress))
        self.blocks = updated_blocks
    
    def render(self, screen):
        """Render all blocks"""
        if not self.block_font:
            return
        
        for i, (letter, x, y, anim_progress) in enumerate(self.blocks):
            is_top_block = (i == len(self.blocks) - 1)
            
            # Apply animation: slide up + fade in
            eased_progress = 1 - (1 - anim_progress) ** 3  # Cubic ease-out
            slide_distance = 30
            animated_y = y + (1 - eased_progress) * slide_distance
            alpha = int(255 * eased_progress)
            
            # Render block image
            if is_top_block and self.block_top_image:
                block_img = self.block_top_image.copy()
                block_img.set_alpha(alpha)
                screen.blit(block_img, (x+10, animated_y))
            elif not is_top_block and self.block_bottom_image:
                block_img = self.block_bottom_image.copy()
                block_img.set_alpha(alpha)
                screen.blit(block_img, (x, animated_y))
            else:
                # Fallback: colored rectangle
                block_rect = pygame.Rect(x, animated_y, self.block_width, self.block_height)
                pygame.draw.rect(screen, (100, 100, 200), block_rect, border_radius=5)
                pygame.draw.rect(screen, (255, 255, 255), block_rect, 2, border_radius=5)
            
            # Render letter
            letter_surface = self.block_font.render(letter.upper(), True, (255, 255, 255))
            letter_surface.set_alpha(alpha)
            letter_x = x + (self.block_width - letter_surface.get_width()) // 2
            letter_y = animated_y + (self.block_height - letter_surface.get_height()) // 2+12
            screen.blit(letter_surface, (letter_x, letter_y))
    
    def clear(self):
        """Clear all blocks"""
        self.blocks = []
    
    def get_block_count(self):
        """Get number of blocks"""
        return len(self.blocks)
