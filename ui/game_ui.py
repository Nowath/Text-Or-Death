"""
Game UI for Text or Death
"""
import pygame
import pygame.font

class GameUI:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Initialize fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Colors
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "gray": (128, 128, 128),
            "dark_gray": (64, 64, 64),
            "light_gray": (192, 192, 192)
        }
    
    def draw_text(self, text, font, color, x, y, center=False):
        """Draw text on screen"""
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            self.screen.blit(text_surface, text_rect)
        else:
            self.screen.blit(text_surface, (x, y))
        return text_surface.get_rect()
    
    def show_connection_screen(self):
        """Show connection screen and get player name"""
        player_name = ""
        input_active = True
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        char = event.unicode
                        if char.isprintable() and len(player_name) < 20:
                            player_name += char
            
            self.screen.fill(self.colors["black"])
            
            # Title
            self.draw_text("TEXT OR DEATH", self.font_large, self.colors["red"], 
                          self.width // 2, 200, center=True)
            
            # Instructions
            self.draw_text("Enter your name:", self.font_medium, self.colors["white"],
                          self.width // 2, 300, center=True)
            
            # Input box
            input_rect = pygame.Rect(self.width // 2 - 150, 350, 300, 40)
            pygame.draw.rect(self.screen, self.colors["white"], input_rect)
            pygame.draw.rect(self.screen, self.colors["black"], input_rect, 2)
            
            # Player name text
            self.draw_text(player_name, self.font_medium, self.colors["black"],
                          input_rect.x + 5, input_rect.y + 8)
            
            # Instructions
            self.draw_text("Press ENTER to connect", self.font_small, self.colors["gray"],
                          self.width // 2, 450, center=True)
            
            pygame.display.flip()
        
        return player_name.strip()
    
    def draw_waiting_screen(self, message):
        """Draw waiting screen"""
        self.draw_text(message, self.font_medium, self.colors["white"],
                      self.width // 2, self.height // 2, center=True)
    
    def draw_lobby_screen(self, players):
        """Draw lobby screen with connected players"""
        self.draw_text("WAITING FOR PLAYERS", self.font_large, self.colors["yellow"],
                      self.width // 2, 100, center=True)
        
        self.draw_text(f"Players: {len(players)}/4", self.font_medium, self.colors["white"],
                      self.width // 2, 150, center=True)
        
        # List players
        y_offset = 200
        for i, player_data in enumerate(players.values()):
            color = self.colors["green"] if player_data["lives"] > 0 else self.colors["red"]
            self.draw_text(f"{player_data['name']} - Lives: {player_data['lives']}", 
                          self.font_small, color, 50, y_offset + i * 30)
        
        if len(players) >= 2:
            self.draw_text("Game starting soon...", self.font_medium, self.colors["green"],
                          self.width // 2, self.height - 100, center=True)
    
    def draw_game_screen(self, current_word, typed_text, players, round_num, time_remaining):
        """Draw main game screen"""
        # Round info
        self.draw_text(f"Round {round_num}", self.font_medium, self.colors["white"], 20, 20)
        self.draw_text(f"Time: {time_remaining}", self.font_medium, self.colors["yellow"], 
                      self.width - 150, 20)
        
        # Current word
        if current_word:
            self.draw_text("Type this word:", self.font_medium, self.colors["white"],
                          self.width // 2, 200, center=True)
            
            self.draw_text(current_word, self.font_large, self.colors["yellow"],
                          self.width // 2, 250, center=True)
            
            # Typed text with correctness indication
            self.draw_typed_text(current_word, typed_text, self.width // 2, 320)
        
        # Player list
        self.draw_player_list(players, 50, 400)
    
    def draw_typed_text(self, target_word, typed_text, x, y):
        """Draw typed text with color coding for correctness"""
        char_width = 20
        start_x = x - (len(target_word) * char_width) // 2
        
        for i, char in enumerate(target_word):
            color = self.colors["gray"]
            
            if i < len(typed_text):
                if typed_text[i].lower() == char.lower():
                    color = self.colors["green"]
                else:
                    color = self.colors["red"]
            
            self.draw_text(char, self.font_large, color, start_x + i * char_width, y)
        
        # Show cursor
        if len(typed_text) < len(target_word):
            cursor_x = start_x + len(typed_text) * char_width
            pygame.draw.line(self.screen, self.colors["white"], 
                           (cursor_x, y), (cursor_x, y + 30), 2)
    
    def draw_player_list(self, players, x, y):
        """Draw list of players with their stats"""
        self.draw_text("Players:", self.font_medium, self.colors["white"], x, y)
        
        y_offset = y + 40
        for i, player_data in enumerate(players.values()):
            name = player_data["name"]
            lives = player_data["lives"]
            score = player_data["score"]
            state = player_data["state"]
            
            # Color based on state
            if state == "eliminated":
                color = self.colors["red"]
            elif state == "winner":
                color = self.colors["yellow"]
            else:
                color = self.colors["white"]
            
            player_text = f"{name} - Lives: {lives} - Score: {score}"
            self.draw_text(player_text, self.font_small, color, x, y_offset + i * 25)
    
    def show_error(self, message):
        """Show error message"""
        self.screen.fill(self.colors["black"])
        self.draw_text("ERROR", self.font_large, self.colors["red"],
                      self.width // 2, self.height // 2 - 50, center=True)
        self.draw_text(message, self.font_medium, self.colors["white"],
                      self.width // 2, self.height // 2, center=True)
        pygame.display.flip()
        pygame.time.wait(3000)
    
    def show_game_over(self, winner, final_scores):
        """Show game over screen"""
        self.screen.fill(self.colors["black"])
        
        if winner:
            self.draw_text("GAME OVER", self.font_large, self.colors["red"],
                          self.width // 2, 100, center=True)
            self.draw_text(f"Winner: {winner['name']}", self.font_large, self.colors["yellow"],
                          self.width // 2, 150, center=True)
        else:
            self.draw_text("GAME ENDED", self.font_large, self.colors["red"],
                          self.width // 2, 125, center=True)
        
        # Final scores
        self.draw_text("Final Scores:", self.font_medium, self.colors["white"],
                      self.width // 2, 250, center=True)
        
        sorted_scores = sorted(final_scores, key=lambda x: x["score"], reverse=True)
        for i, player_data in enumerate(sorted_scores):
            color = self.colors["yellow"] if i == 0 else self.colors["white"]
            score_text = f"{i+1}. {player_data['name']} - {player_data['score']} points"
            self.draw_text(score_text, self.font_small, color,
                          self.width // 2, 300 + i * 30, center=True)
        
        pygame.display.flip()
        pygame.time.wait(5000)