import enchant

class WordChecker:
    def __init__(self, language="en_US"):
        self.dictionary = enchant.Dict(language)
    
    def check_word(self, word):
        """
        Check if a word is valid
        Returns: tuple (is_valid: bool, message: str, color: tuple)
        """
        word = word.strip()
        
        if not word:
            return False, "Please type a word first!", (255, 255, 255)
        
        if self.dictionary.check(word):
            return True, f"'{word}' is a valid word!", (0, 255, 0)
        else:
            return False, f"'{word}' is NOT a valid word!", (255, 0, 0)
    
    def is_valid(self, word):
        """
        Simple check if word is valid (returns only boolean)
        """
        word = word.strip()
        if not word:
            return False
        return self.dictionary.check(word)