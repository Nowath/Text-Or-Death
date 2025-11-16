import pygame
from ui.character import Character
from ui.button import Button
from ui.components import Lava, BlockManager
import json


class GameScreen:
    def __init__(self, screen, word_checker, config, font):
        """Initialize the game screen component"""
        self.screen = screen
        self.word_checker = word_checker

        # Get screen dimensions from config
        self.screen_width = int(config["client"]["screen_width"])
        self.screen_height = int(config["client"]["screen_height"])

        # Set up fonts
        self.font = pygame.font.Font(font, 50)
        self.small_font = pygame.font.Font(font, 30)
        self.block_font = pygame.font.Font(font, 25)

        # Load background
        self.background = self._load_background()

        # Initialize components
        self.block_manager = BlockManager(self.screen_width, self.screen_height)
        self.block_manager.set_font(self.block_font)
        
        self.lava = Lava(self.screen_width, self.screen_height)

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

        # Game state
        self.current_input = ""
        self.game_over = False
        self.game_won = False
        self.game_message = ""
        self.feedback_message = ""
        self.feedback_timer = 0
        self.feedback_color = (255, 255, 255)

        # Create player character
        self.player1 = Character(0, 0)

        # Create menu button
        button_width = 120
        button_height = 50
        button_x = self.screen_width - button_width - 20
        button_y = 20
        self.menu_button = Button(
            button_x, button_y, button_width, button_height,
            "Menu",
            font_size=30,
            color=(70, 130, 180),
            hover_color=(100, 160, 210)
        )

        # Set up key repeat
        pygame.key.set_repeat(500, 50)

    def _load_background(self):
        """Load and scale background image"""
        try:
            background = pygame.image.load("assets/Background/Sea/background_sea.jpg")
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            return background
        except Exception as e:
            print(f"Could not load background: {e}")
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((40, 40, 60))
            return background

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
            # Calculate lava decrease based on answer length
            num_blocks = len(answer)
            lava_decrease = num_blocks * (self.block_manager.block_height + self.block_manager.block_spacing)
            self.lava.lower_lava(lava_decrease)
            
            # Add blocks
            self.block_manager.add_blocks(answer)
            
            # Update feedback
            self.current_input = ""
            self.feedback_message = f"Correct! '{answer}'"
            self.feedback_color = (0, 255, 0)
            self.feedback_timer = pygame.time.get_ticks()
            
            # Increase lava speed after certain questions
            if self.question_index >= self.lava.start_question:
                self.lava.increase_speed()
            
            self.load_next_question()
            return True
        else:
            # Wrong answer
            self.feedback_message = "Wrong answer! Try again"
            self.feedback_color = (255, 100, 100)
            self.feedback_timer = pygame.time.get_ticks()
            self.current_input = ""
            return False

    def update_timer(self):
        """Update the countdown timer"""
        if not self.game_over:
            elapsed = (pygame.time.get_ticks() - self.timer_start) / 1000
            self.time_remaining = max(0, self.time_limit - elapsed)
            
            if self.time_remaining <= 0:
                self.game_over = True
                self.game_message = "TIME'S UP! You died!"

    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.QUIT:
            return False

        # Check if menu button was clicked
        if self.menu_button.is_clicked(event):
            return "menu"

        # Handle game over state
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.restart_game()
            return True

        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            elif event.key == pygame.K_RETURN:
                if self.current_input:
                    self.check_answer(self.current_input)
            elif event.key == pygame.K_SPACE:
                self.current_input += " "
            else:
                key_name = pygame.key.name(event.key)
                if len(key_name) == 1:
                    self.current_input += key_name

        return True

    def restart_game(self):
        """Restart the game"""
        self.current_input = ""
        self.block_manager.clear()
        self.question_index = 0
        self.game_over = False
        self.game_won = False
        self.game_message = ""
        self.lava.reset()
        self.load_next_question()

    def update(self):
        """Update game state"""
        # Update button
        mouse_pos = pygame.mouse.get_pos()
        self.menu_button.update(mouse_pos)

        # Update timer
        self.update_timer()

        # Update lava
        self.lava.update()
        
        # Check lava collision
        if not self.game_over and self.lava.check_collision(self.player1):
            self.game_over = True
            self.game_message = "LAVA GOT YOU! You died!"

        # Update blocks
        self.block_manager.update()

        # Update character position
        char_x, char_y = self.block_manager.get_character_position(
            self.player1.width, self.player1.height
        )
        self.player1.x = char_x
        self.player1.y = char_y

        # Clear feedback after 2 seconds
        if self.feedback_message and pygame.time.get_ticks() - self.feedback_timer > 2000:
            self.feedback_message = ""

    def render(self):
        """Render all UI elements"""
        # Draw background
        self.screen.blit(self.background, (0, 0))

        if self.game_over:
            self._render_game_over()
        else:
            self._render_game()

        # Render menu button (always on top)
        self.menu_button.draw(self.screen)

    def _render_game_over(self):
        """Render game over screen"""
        message_color = (0, 255, 0) if self.game_won else (255, 0, 0)
        
        game_over_text = self.font.render(self.game_message, True, message_color)
        text_x = self.screen_width // 2 - game_over_text.get_width() // 2
        text_y = self.screen_height // 2 - 50
        self.screen.blit(game_over_text, (text_x, text_y))

        restart_text = self.small_font.render("Press ENTER to restart", True, (255, 255, 255))
        restart_x = self.screen_width // 2 - restart_text.get_width() // 2
        restart_y = self.screen_height // 2 + 50
        self.screen.blit(restart_text, (restart_x, restart_y))

    def _render_game(self):
        """Render active game"""
        # Render question
        if self.current_question:
            question_text = self.small_font.render(self.current_question.upper(), True, (255, 255, 255))
            question_x = self.screen_width // 2 - question_text.get_width() // 2
            question_y = 50
            
            padding = 20
            question_bg = pygame.Rect(
                question_x - padding, question_y - padding,
                question_text.get_width() + padding * 2,
                question_text.get_height() + padding * 2
            )
            pygame.draw.rect(self.screen, (0, 0, 0, 128), question_bg, border_radius=10)
            self.screen.blit(question_text, (question_x, question_y))

        # Render timer
        timer_color = (255, 255, 255) if self.time_remaining > 10 else (255, 0, 0)
        timer_text = self.small_font.render(f"Time: {int(self.time_remaining)}s", True, timer_color)
        self.screen.blit(timer_text, (20, 20))

        # Render progress
        progress_text = self.small_font.render(
            f"Question: {self.question_index}/{len(self.questions_data)}", 
            True, (255, 255, 255)
        )
        self.screen.blit(progress_text, (20, 60))

        # Render input box
        self._render_input_box()

        # Render feedback
        if self.feedback_message:
            feedback_text = self.small_font.render(self.feedback_message, True, self.feedback_color)
            feedback_x = self.screen_width - feedback_text.get_width() - 30
            feedback_y = 230
            self.screen.blit(feedback_text, (feedback_x, feedback_y))

        # Render blocks
        self.block_manager.render(self.screen)

        # Render character
        self.player1.render(self.screen)

        # Render lava
        self.lava.render(self.screen)

    def _render_input_box(self):
        """Render the input box on the right side"""
        input_display = self.current_input + "_"
        input_text = self.font.render(input_display, True, (255, 255, 255))
        
        padding = 15
        input_width = max(input_text.get_width(), 300) + padding * 2
        input_x = self.screen_width - input_width - 20
        input_y = 150
        
        input_bg = pygame.Rect(input_x, input_y, input_width, input_text.get_height() + padding * 2)
        pygame.draw.rect(self.screen, (50, 50, 50, 200), input_bg, border_radius=10)
        
        text_x = input_x + (input_width - input_text.get_width()) // 2
        text_y = input_y + padding
        self.screen.blit(input_text, (text_x, text_y))
