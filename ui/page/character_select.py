import pygame
import os


class CharacterSelectScreen:
    def __init__(self, screen, font_path, screen_width, screen_height):
        """Initialize character selection screen"""
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.title_font = pygame.font.Font(font_path, 60)
        self.font = pygame.font.Font(font_path, 30)
        
        # Load background
        self.background = self._load_background()
        
        # Character options
        self.characters = self._load_characters()
        self.selected_index = 0
        
        # Layout
        self.card_width = 200
        self.card_height = 250
        self.card_spacing = 50
        self.start_x = self._calculate_start_x()
        
        # Colors
        self.card_color = (50, 50, 80)
        self.selected_color = (100, 150, 255)
        self.text_color = (255, 255, 255)
    
    def _load_background(self):
        """Load background image"""
        try:
            background = pygame.image.load('assets/Background/Bright/Background.png')
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            return background
        except Exception as e:
            print(f"Could not load background: {e}")
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((0,0,0))
            return background
    
    def _load_characters(self):
        """Load available characters"""
        characters = []
        
        # Define character options with their image paths
        character_data = [
            {"name": "Seiya", "path": "assets/character/Seiya.png"},
            {"name": "Mucsle man", "path": "assets/character/Muscle.png"},
            {"name": "Samurai", "path": "assets/Samurai/Idle.png"},
            {"name": "Shinobi", "path": "assets/Shinobi/Idle.png"},
        ]
        
        for char in character_data:
            try:
                image = pygame.image.load(char["path"])
                # Scale to fit card
                image = pygame.transform.scale(image, (150, 150))
                characters.append({
                    "name": char["name"],
                    "image": image,
                    "path": char["path"]
                })
            except Exception as e:
                print(f"Could not load character {char['name']}: {e}")
                # Create placeholder
                placeholder = pygame.Surface((150, 150))
                placeholder.fill((100, 100, 100))
                characters.append({
                    "name": char["name"],
                    "image": placeholder,
                    "path": char["path"]
                })
        
        return characters
    
    def _calculate_start_x(self):
        """Calculate starting X position to center cards"""
        total_width = len(self.characters) * self.card_width + (len(self.characters) - 1) * self.card_spacing
        return (self.screen_width - total_width) // 2
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.QUIT:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Return selected character path
                return self.characters[self.selected_index]["path"]
            elif event.key == pygame.K_ESCAPE:
                return "back"
        
        # Mouse click selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i in range(len(self.characters)):
                card_x = self.start_x + i * (self.card_width + self.card_spacing)
                card_y = self.screen_height // 2 - self.card_height // 2
                card_rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)
                
                if card_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_index = i
                    return self.characters[self.selected_index]["path"]
        
        return False
    
    def render(self):
        """Render character selection screen"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        title_text = self.title_font.render("SELECT YOUR CHARACTER", True, self.text_color)
        title_x = self.screen_width // 2 - title_text.get_width() // 2
        title_y = 80
        self.screen.blit(title_text, (title_x, title_y))
        
        # Draw character cards
        for i, character in enumerate(self.characters):
            card_x = self.start_x + i * (self.card_width + self.card_spacing)
            card_y = self.screen_height // 2 - self.card_height // 2
            
            # Determine card color
            is_selected = (i == self.selected_index)
            color = self.selected_color if is_selected else self.card_color
            
            # Draw card background
            card_rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)
            pygame.draw.rect(self.screen, color, card_rect, border_radius=15)
            
            # Draw border for selected card
            if is_selected:
                pygame.draw.rect(self.screen, (255, 255, 255), card_rect, 4, border_radius=15)
            
            # Draw character image
            image_x = card_x + (self.card_width - character["image"].get_width()) // 2
            image_y = card_y + 20
            self.screen.blit(character["image"], (image_x, image_y))
            
            # Draw character name
            name_text = self.font.render(character["name"], True, self.text_color)
            name_x = card_x + (self.card_width - name_text.get_width()) // 2
            name_y = card_y + self.card_height - 50
            self.screen.blit(name_text, (name_x, name_y))
        
        # Draw instructions
        instruction_text = self.font.render("Use ARROW KEYS or CLICK to select, ENTER to confirm", True, self.text_color)
        instruction_x = self.screen_width // 2 - instruction_text.get_width() // 2
        instruction_y = self.screen_height - 100
        self.screen.blit(instruction_text, (instruction_x, instruction_y))
