import pygame
from pygame.locals import QUIT
from sys import exit
from gameobjects.FireFighter import FireFighter


WIDTH = 1920
HEIGHT = 1080

GREEN = (0,76,8)

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Guardiões da Floresta')

clock = pygame.time.Clock()

pascal = FireFighter(display, 700, 700)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()
    
    display.fill(GREEN)
    pascal.Draw()

    clock.tick(60)
    pygame.display.update()



