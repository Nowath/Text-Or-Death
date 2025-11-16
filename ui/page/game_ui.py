import pygame
from ui.character import Character
from ui.button import Button
import json
import random

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

        # Set up fonts
        self.font = pygame.font.Font(font, 50)
        self.small_font = pygame.font.Font(font, 30)
        self.block_font = pygame.font.Font(font, 24)

        # Load background
        self.background = self._load_background()

        # Game state - define block_size FIRST before loading images
        self.current_input = ""
        self.blocks = []  # List of letter blocks: [(letter, x, y, animation_progress), ...]
        self.block_width = 140  # Width of block
        self.block_height = 60  # Height of block
        self.block_spacing = -26
        self.block_base_y = self.screen_height - 60
        self.animation_speed = 0.15  # Animation speed (0-1 per frame)

        # Load block images (after block_size is defined)
        self.block_top_image = self._load_block_image('assets/Block/top.png')
        self.block_bottom_image = self._load_block_image('assets/Block/bottom.png')

        # Load questions database
        with open('database.json', "r", encoding='utf-8') as f:
            self.questions_data = json.load(f)

        # Timer (30 seconds per question)
        self.time_limit = 30
        self.time_remaining = self.time_limit
        self.timer_start = pygame.time.get_ticks()
        
        # Question system
        self.current_question = None
        self.current_answers = []
        self.question_index = 0
        self.load_next_question()

        # Game status
        self.game_over = False
        self.game_won = False
        self.game_message = ""
        self.feedback_message = ""
        self.feedback_timer = 0
        self.feedback_color = (255, 255, 255)

        # Create player character - will be positioned on top of blocks
        self.player1 = Character(0, 0)  # Position will be updated dynamically

        # Create button in top right corner
        button_width = 120
        button_height = 50
        button_x = self.screen_width - button_width - 20
        button_y = 20
        self.menu_button = Button(
            button_x, button_y, button_width, button_height,
            "Quit",
            font_size=30,
            color=(70, 130, 180),
            hover_color=(100, 160, 210)
        )

        # Set up key repeat
        pygame.key.set_repeat(500, 50)

    def load_next_question(self):
        """Load the next question from database"""
        if self.question_index < len(self.questions_data):
            question_data = self.questions_data[self.question_index]
            self.current_question = question_data["question"]
            self.current_answers = [ans.lower() for ans in question_data["answer"]]
            self.question_index += 1
            self.time_remaining = self.time_limit
            self.timer_start = pygame.time.get_ticks()
        else:
            # All questions answered - WIN!
            self.game_won = True
            self.game_over = True
            self.game_message = "YOU WIN! All questions completed!"

    def check_answer(self, answer):
        """Check if the answer is correct"""
        answer = answer.lower().strip()
        if answer in self.current_answers:
            # Correct answer - create blocks
            self.create_blocks(answer)
            self.current_input = ""
            self.feedback_message = f"Correct! '{answer}'"
            self.feedback_color = (0, 255, 0)
            self.feedback_timer = pygame.time.get_ticks()
            self.load_next_question()
            return True
        else:
            # Wrong answer
            self.feedback_message = "Wrong answer! Try again"
            self.feedback_color = (255, 100, 100)
            self.feedback_timer = pygame.time.get_ticks()
            self.current_input = ""
            return False

    def create_blocks(self, word):
        """Create letter blocks from the word - stacking vertically in center"""
        # Reverse the word so first letter is at bottom
        reversed_word = word[::-1]
        for letter in reversed_word:
            # Stack blocks vertically in the center
            x = self.screen_width // 2 - self.block_width // 2
            y = self.block_base_y - len(self.blocks) * (self.block_height + self.block_spacing)
            # Add animation progress (0 = just added, 1 = fully animated)
            self.blocks.append((letter, x, y, 0.0))
        
        # Remove bottom blocks if character would go above screen
        self.remove_bottom_blocks_if_needed()
    
    def remove_bottom_blocks_if_needed(self):
        """Remove blocks from bottom if tower gets too high"""
        min_char_y = 150  # Minimum Y position for character (below question area)
        
        while self.blocks:
            char_x, char_y = self.get_character_position()
            if char_y < min_char_y:
                # Remove the bottom block
                self.blocks.pop(0)
                # Recalculate all block positions
                temp_blocks = self.blocks.copy()
                self.blocks = []
                for letter, _, _, anim_progress in temp_blocks:
                    x = self.screen_width // 2 - self.block_width // 2
                    y = self.block_base_y - len(self.blocks) * (self.block_height + self.block_spacing)
                    self.blocks.append((letter, x, y, anim_progress))
            else:
                break
    
    def get_character_position(self):
        """Calculate character position on top of the block tower"""
        if self.blocks:
            # Position character on top of the highest block
            top_block_y = self.block_base_y - len(self.blocks) * (self.block_height + self.block_spacing)
            char_x = self.screen_width // 2 - 25  # Center character (assuming width=50)
            char_y = top_block_y + 6  # Closer to the top block
            return char_x, char_y
        else:
            # Default position at bottom center
            return self.screen_width // 2 - 25, self.screen_height - 100

    def update_timer(self):
        """Update the countdown timer"""
        if not self.game_over:
            elapsed = (pygame.time.get_ticks() - self.timer_start) / 1000
            self.time_remaining = max(0, self.time_limit - elapsed)
            
            if self.time_remaining <= 0:
                # Time's up - GAME OVER
                self.game_over = True
                self.game_message = "TIME'S UP! You died!"

    def _load_background(self):
        """Load and scale background image or create gradient"""
        try:
            background = pygame.image.load("assets/Background/Sea/background_sea.jpg")
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            return background
        except Exception as e:
            print(f"Could not load background: {e}")
            # Create a solid color surface if image not found
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((40, 40, 60))  # Dark blue-grey color
            return background

    def _load_block_image(self, path):
        """Load and scale block image"""
        try:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (self.block_width, self.block_height))
            return image
        except Exception as e:
            print(f"Could not load block image {path}: {e}")
            # Return None if image not found, will use fallback rendering
            return None
            # Create a solid color surface if image not found
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((40, 40, 60))  # Dark blue-grey color
            return background

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        # Check if button was clicked
        if self.menu_button.is_clicked(event):
            print("Menu button clicked!")
            return "menu"  # Return to main page

        # Don't handle input if game is over
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Restart game - reset all variables
                self.current_input = ""
                self.blocks = []
                self.question_index = 0
                self.game_over = False
                self.game_won = False
                self.game_message = ""
                self.load_next_question()
            return True

        if event.type == pygame.KEYDOWN:
            # Handle backspace
            if event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]

            # Handle Enter key - submit answer
            elif event.key == pygame.K_RETURN:
                if self.current_input:
                    self.check_answer(self.current_input)

            # Handle space
            elif event.key == pygame.K_SPACE:
                self.current_input += " "

            # Handle letter keys
            else:
                key_name = pygame.key.name(event.key)
                if len(key_name) == 1:
                    self.current_input += key_name

        return True

    def update(self):
        """Update game state (call this in main game loop)"""
        # Update button animation
        mouse_pos = pygame.mouse.get_pos()
        self.menu_button.update(mouse_pos)

        # Update timer ้ัพ่ะีา่ั้
        self.update_timer()

        # Update block animations
        updated_blocks = []
        for letter, x, y, anim_progress in self.blocks:
            if anim_progress < 1.0:
                anim_progress = min(1.0, anim_progress + self.animation_speed)
            updated_blocks.append((letter, x, y, anim_progress))
        self.blocks = updated_blocks

        # Update character position to be on top of blocks
        char_x, char_y = self.get_character_position()
        self.player1.x = char_x
        self.player1.y = char_y

        # Clear feedback message after 2 seconds
        if self.feedback_message and pygame.time.get_ticks() - self.feedback_timer > 2000:
            self.feedback_message = ""

    def render(self):
        """Render all UI elements"""
        # Draw background (bottom layer)
        self.screen.blit(self.background, (0, 0))

        if self.game_over:
            # Show game over screen
            if self.game_won:
                message_color = (0, 255, 0)  # Green for win
            else:
                message_color = (255, 0, 0)  # Red for lose
            
            game_over_text = self.font.render(self.game_message, True, message_color)
            text_x = self.screen_width // 2 - game_over_text.get_width() // 2
            text_y = self.screen_height // 2 - 50
            self.screen.blit(game_over_text, (text_x, text_y))

            restart_text = self.small_font.render("Press ENTER to restart", True, (255, 255, 255))
            restart_x = self.screen_width // 2 - restart_text.get_width() // 2
            restart_y = self.screen_height // 2 + 50
            self.screen.blit(restart_text, (restart_x, restart_y))
        else:
            # Render question at top
            if self.current_question:
                question_text = self.small_font.render(self.current_question.upper(), True, (255, 255, 255))
                question_x = self.screen_width // 2 - question_text.get_width() // 2
                question_y = 50
                
                # Draw background for question
                padding = 20
                question_bg = pygame.Rect(question_x - padding, question_y - padding,
                                         question_text.get_width() + padding * 2,
                                         question_text.get_height() + padding * 2)
                pygame.draw.rect(self.screen, (0, 0, 0, 128), question_bg, border_radius=10)
                
                self.screen.blit(question_text, (question_x, question_y))

            # Render timer
            timer_color = (255, 255, 255) if self.time_remaining > 10 else (255, 0, 0)
            timer_text = self.small_font.render(f"Time: {int(self.time_remaining)}s", True, timer_color)
            self.screen.blit(timer_text, (20, 20))

            # Render question progress
            progress_text = self.small_font.render(f"Question: {self.question_index}/{len(self.questions_data)}", 
                                                   True, (255, 255, 255))
            self.screen.blit(progress_text, (20, 60))

            # Render current input on the right side (BEFORE blocks so blocks can cover it)
            input_display = self.current_input + "_"  # Add cursor
            input_text = self.font.render(input_display, True, (255, 255, 255))
            
            # Position on right side
            padding = 15
            input_width = max(input_text.get_width(), 300) + padding * 2
            input_x = self.screen_width - input_width - 20
            input_y = 150
            
            # Draw input background
            input_bg = pygame.Rect(input_x, input_y,
                                  input_width,
                                  input_text.get_height() + padding * 2)
            pygame.draw.rect(self.screen, (50, 50, 50, 200), input_bg, border_radius=10)
            
            # Center text in the box
            text_x = input_x + (input_width - input_text.get_width()) // 2
            text_y = input_y + padding
            self.screen.blit(input_text, (text_x, text_y))

            # Render feedback message on the right side (BEFORE blocks)
            if self.feedback_message:
                feedback_text = self.small_font.render(self.feedback_message, True, self.feedback_color)
                feedback_x = self.screen_width - feedback_text.get_width() - 30
                feedback_y = input_y + input_text.get_height() + padding * 2 + 20
                self.screen.blit(feedback_text, (feedback_x, feedback_y))

            # Render letter blocks (ON TOP so they cover content below)
            for i, (letter, x, y, anim_progress) in enumerate(self.blocks):
                # Determine if this is the top block (last in list = highest position)
                is_top_block = (i == len(self.blocks) - 1)
                
                # Apply animation: slide up + fade in
                # Easing function for smooth animation
                eased_progress = 1 - (1 - anim_progress) ** 3  # Cubic ease-out
                
                # Calculate animated position (slide up from below)
                slide_distance = 30
                animated_y = y + (1 - eased_progress) * slide_distance
                
                # Calculate alpha for fade in
                alpha = int(255 * eased_progress)
                
                # Choose the appropriate block image
                if is_top_block and self.block_top_image:
                    block_img = self.block_top_image.copy()
                    scaled_image = pygame.transform.scale(block_img, (120, 60))
                    scaled_image.set_alpha(alpha)
                    self.screen.blit(scaled_image, (x+10, animated_y))
                elif not is_top_block and self.block_bottom_image:
                    block_img = self.block_bottom_image.copy()
                    block_img.set_alpha(alpha)
                    self.screen.blit(block_img, (x, animated_y))
                else:
                    # Fallback: draw colored rectangle if images not loaded
                    block_rect = pygame.Rect(x, animated_y, self.block_width, self.block_height)
                    color_with_alpha = (*((100, 100, 200)), alpha)
                    pygame.draw.rect(self.screen, (100, 100, 200), block_rect, border_radius=5)
                    pygame.draw.rect(self.screen, (255, 255, 255), block_rect, 2, border_radius=5)
                
                # Draw letter on top of the block with fade
                letter_surface = self.block_font.render(letter.upper(), True, (255, 255, 255))
                letter_surface.set_alpha(alpha)
                letter_x = x + (self.block_width - letter_surface.get_width()) // 2
                letter_y = animated_y + (self.block_height - letter_surface.get_height()) // 2+14
                self.screen.blit(letter_surface, (letter_x, letter_y))

            # Render character on top of blocks (TOP LAYER)
            self.player1.render(self.screen)

        # Render button (top layer - last so it's on top)
        self.menu_button.draw(self.screen)
