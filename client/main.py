import os
import sys
import pygame
# Ensure the project root is on sys.path so imports like `utils` resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.checkword import WordChecker

screenWidth = 1024
screenHeight = 768
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.init()

# Initialize word checker
word_checker = WordChecker("en_US")

# Set up font
font = pygame.font.Font(None, 50)

# Load and scale background image
try:
    # Try to load background image - replace with your image path
    background = pygame.image.load("assets/Background/Pale/Background.png")
    background = pygame.transform.scale(background, (screenWidth, screenHeight))
    has_background = True
except:
    # If image not found, create a gradient background
    has_background = False
    background = pygame.Surface((screenWidth, screenHeight))
    for y in range(screenHeight):
        color_value = int(20 + (y / screenHeight) * 40)
        pygame.draw.line(background, (color_value, color_value, color_value * 1.2), (0, y), (screenWidth, y))

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
    
    # Draw background
    screen.blit(background, (0, 0))
    
    # Create semi-transparent overlay for better text readability
    # overlay = pygame.Surface((screenWidth, 300))
    # overlay.set_alpha(128)
    # overlay.fill((0, 0, 0))
    # screen.blit(overlay, (0, screenHeight//2 - 50))
    
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