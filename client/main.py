import os
import sys
import pygame

# Ensure the project root is on sys.path so imports like `utils` resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.checkword import WordChecker

screenWidth = 1024
screenHeight = 768
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.init()

# Initialize word checker
word_checker = WordChecker("en_US")

# Set up font
font = pygame.font.Font(None, 50)
pressedKey = ""
gameRun = True
message = []
# For handling key repeat
pygame.key.set_repeat(500, 50)
isword = False
checkResult = ""
resultColor = (255, 255, 255)

while gameRun:
    keyInput = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRun = False
        elif event.type == pygame.KEYDOWN:
            pressedKey = pygame.key.name(event.key)
            # Handle backspace
            if event.key == pygame.K_BACKSPACE and message:
                message.pop()
                checkResult = ""
            # Handle Enter key
            elif event.key == pygame.K_RETURN:
                currentText = "".join(message)
                is_valid, result_message, color = word_checker.check_word(currentText)
                checkResult = result_message
                resultColor = color
            # Handle space
            elif event.key == pygame.K_SPACE:
                message.append(" ")
                checkResult = ""
            # Add regular characters
            elif len(pressedKey) == 1:
                message.append(pressedKey)
                checkResult = ""
    # Clear screen
    screen.fill((0, 0, 0))  # Black background
    # Render text
    if pressedKey:
        text = font.render(f"Key pressed: {pressedKey}", True, (255, 255, 255))
        screen.blit(text, (screenWidth//2 - text.get_width()//2, screenHeight//2))
    # Render message
    messageRen = font.render("".join(message), True, (255, 255, 255))
    screen.blit(messageRen, (screenWidth//2 - messageRen.get_width()//2, screenHeight//2 + 60))
    
    # Render Enter check result
    if checkResult:
        resultRen = font.render(checkResult, True, resultColor)
        screen.blit(resultRen, (screenWidth//2 - resultRen.get_width()//2, screenHeight//2 + 100))
    # Update display
    pygame.display.flip()
    
pygame.quit()