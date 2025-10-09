"""
Player class for Text or Death game
"""
import time
from enum import Enum

class PlayerState(Enum):
    WAITING = "waiting"
    TYPING = "typing"
    ELIMINATED = "eliminated"
    WINNER = "winner"

class Player:
    def __init__(self, player_id, name, connection=None):
        self.id = player_id
        self.name = name
        self.connection = connection
        self.state = PlayerState.WAITING
        self.score = 0
        self.lives = 3
        self.current_word = ""
        self.typed_text = ""
        self.typing_start_time = None
        self.typing_speed = 0  # WPM
        self.accuracy = 100.0
        self.total_characters_typed = 0
        self.total_errors = 0
        self.rounds_survived = 0
        self.is_bot = False  # Flag for AI bots
        
    def start_typing(self, word):
        """Start typing a new word"""
        self.current_word = word
        self.typed_text = ""
        self.typing_start_time = time.time()
        self.state = PlayerState.TYPING
    
    def update_typed_text(self, text):
        """Update the player's typed text"""
        self.typed_text = text
        self.calculate_accuracy()
    
    def finish_typing(self):
        """Finish typing and calculate stats"""
        if self.typing_start_time:
            typing_time = time.time() - self.typing_start_time
            words_typed = len(self.current_word.split())
            self.typing_speed = (words_typed / typing_time) * 60 if typing_time > 0 else 0
        
        self.state = PlayerState.WAITING
        return self.is_word_correct()
    
    def is_word_correct(self):
        """Check if the typed word is correct"""
        return self.typed_text.strip().lower() == self.current_word.lower()
    
    def calculate_accuracy(self):
        """Calculate typing accuracy"""
        if not self.current_word or not self.typed_text:
            self.accuracy = 100.0
            return
        
        correct_chars = 0
        total_chars = max(len(self.current_word), len(self.typed_text))
        
        for i in range(min(len(self.current_word), len(self.typed_text))):
            if self.current_word[i].lower() == self.typed_text[i].lower():
                correct_chars += 1
        
        self.accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 100.0
    
    def lose_life(self):
        """Player loses a life"""
        self.lives -= 1
        if self.lives <= 0:
            self.state = PlayerState.ELIMINATED
        return self.lives > 0
    
    def add_score(self, points):
        """Add points to player's score"""
        self.score += points
    
    def get_stats(self):
        """Get player statistics"""
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "lives": self.lives,
            "state": self.state.value,
            "typing_speed": round(self.typing_speed, 1),
            "accuracy": round(self.accuracy, 1),
            "rounds_survived": self.rounds_survived
        }
    
    def reset_for_new_game(self):
        """Reset player for a new game"""
        self.state = PlayerState.WAITING
        self.score = 0
        self.lives = 3
        self.current_word = ""
        self.typed_text = ""
        self.typing_start_time = None
        self.typing_speed = 0
        self.accuracy = 100.0
        self.rounds_survived = 0