import pygame

class FireFighter:

    def __init__(self, display, x, y):
        self.display = display
        self.x = x
        self.y = y

        fire_fighter = pygame.image.load("Images/PascalFront.png")
        

    @classmethod

    def Draw():
        display.blit(fire_fighter, (x,y))

