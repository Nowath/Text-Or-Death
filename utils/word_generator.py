"""
Word generation and challenge utilities
"""
import random
import json
import os

class WordGenerator:
    def __init__(self):
        self.word_lists = {
            "easy": [
                "cat", "dog", "run", "jump", "happy", "blue", "red", "big", "small", "fast",
                "slow", "hot", "cold", "good", "bad", "yes", "no", "go", "stop", "help"
            ],
            "medium": [
                "computer", "keyboard", "challenge", "victory", "defeat", "strategy", "battle",
                "warrior", "magic", "dragon", "castle", "forest", "mountain", "river", "ocean",
                "adventure", "treasure", "mystery", "legend", "ancient"
            ],
            "hard": [
                "extraordinary", "magnificent", "tremendous", "spectacular", "phenomenal",
                "incomprehensible", "revolutionary", "sophisticated", "unprecedented",
                "unbelievable", "extraordinary", "philosophical", "psychological",
                "technological", "archaeological", "meteorological", "astronomical",
                "mathematical", "geographical", "biographical"
            ]
        }
        self.load_custom_words()
    
    def load_custom_words(self):
        """Load custom word lists from files if they exist"""
        for difficulty in self.word_lists.keys():
            filename = f"words_{difficulty}.json"
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        custom_words = json.load(f)
                        self.word_lists[difficulty].extend(custom_words)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def get_random_word(self, difficulty="medium"):
        """Get a random word from the specified difficulty level"""
        if difficulty not in self.word_lists:
            difficulty = "medium"
        return random.choice(self.word_lists[difficulty])
    
    def get_word_batch(self, count=5, difficulty="medium"):
        """Get a batch of random words"""
        words = []
        word_list = self.word_lists.get(difficulty, self.word_lists["medium"])
        
        for _ in range(count):
            word = random.choice(word_list)
            words.append(word)
        
        return words
    
    def calculate_difficulty_score(self, word):
        """Calculate difficulty score based on word characteristics"""
        score = len(word)
        
        # Add points for uncommon letters
        uncommon_letters = "qxzjkv"
        for letter in word.lower():
            if letter in uncommon_letters:
                score += 2
        
        # Add points for repeated letters
        unique_letters = len(set(word.lower()))
        if unique_letters < len(word):
            score += (len(word) - unique_letters)
        
        return score
    
    def create_typing_challenge(self, difficulty="medium", word_count=1):
        """Create a typing challenge with words and metadata"""
        words = self.get_word_batch(word_count, difficulty)
        
        challenge = {
            "words": words,
            "difficulty": difficulty,
            "total_characters": sum(len(word) for word in words),
            "estimated_time": sum(len(word) for word in words) * 0.2,  # rough estimate
            "difficulty_scores": [self.calculate_difficulty_score(word) for word in words]
        }
        
        return challenge