import pygame
import sys
import random
import math

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Frogs")

green_background = pygame.Color(50, 150, 50)
black_background = pygame.Color(0, 0, 0)
current_background = green_background

clock = pygame.time.Clock()

frog_image_original = pygame.image.load('assets/image/frog.png')
frog_size = 150
frog_image = pygame.transform.scale(frog_image_original, (frog_size, frog_size))

class Frog:
    def __init__(self, x, y, vx, vy):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(vx, vy)
        self.rect = pygame.Rect(x, y, frog_size, frog_size)
        
    def update(self):
        self.pos += self.velocity

        if self.pos.x <= 0 or self.pos.x >= screen_width - frog_size:
            self.velocity.x = -self.velocity.x
            self.pos.x = max(0, min(screen_width - frog_size, self.pos.x))
            
        if self.pos.y <= 0 or self.pos.y >= screen_height - frog_size:
            self.velocity.y = -self.velocity.y
            self.pos.y = max(0, min(screen_height - frog_size, self.pos.y))
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def draw(self, screen):
        screen.blit(frog_image, self.pos)

frog1 = Frog(100, 100, 3, 2)
frog2 = Frog(600, 400, -2, -3)

running = True
while running:
    dt = clock.tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    frog1.update()
    frog2.update()

    if frog1.rect.colliderect(frog2.rect):
        current_background = black_background
        
        center1 = pygame.Vector2(frog1.rect.center)
        center2 = pygame.Vector2(frog2.rect.center)
        
        dx = center2.x - center1.x
        dy = center2.y - center1.y

        if abs(dx) > abs(dy):
            frog1.velocity.x = -frog1.velocity.x
            frog2.velocity.x = -frog2.velocity.x 
        else:
            frog1.velocity.y = -frog1.velocity.y
            frog2.velocity.y = -frog2.velocity.y
        if dx != 0 or dy != 0:
            if abs(dx) > abs(dy):
                if dx > 0:
                    frog1.pos.x = frog2.pos.x - frog_size - 1
                else:
                    frog1.pos.x = frog2.pos.x + frog_size + 1
            else:
                if dy > 0:
                    frog1.pos.y = frog2.pos.y - frog_size - 1
                else:
                    frog1.pos.y = frog2.pos.y + frog_size + 1
            frog1.rect.x = frog1.pos.x
            frog1.rect.y = frog1.pos.y
            frog2.rect.x = frog2.pos.x
            frog2.rect.y = frog2.pos.y
    else:
        current_background = green_background
    
    # Draw everything
    screen.fill(current_background)
    frog1.draw(screen)
    frog2.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()