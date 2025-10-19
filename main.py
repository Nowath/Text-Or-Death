import pygame
import os

from pygame.constants import QUIT

pygame.init()

width = 800
height = 800
font = pygame.font.Font('font/wwfont.ttf', 30)
text_surface = font.render('Hello World', True, (0,0,0))

screen = pygame.display.set_mode((width,height))

running = True
while running:
    typing = pygame.event.get_keyboard_grab()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_a):
                running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            if(event.button == 3):
                running = False

    screen.fill((255,255,255))
    screen.blit(text_surface,(0,0))

    pygame.display.flip()
pygame.quit()
