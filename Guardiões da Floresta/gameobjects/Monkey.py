import pygame

class Monkey:

    def __init__(self, display, object):
        self.display = display
        self.object = object
        self.image = pygame.image.load("images/gameobjects/Monkey.png")
    
    def Draw(self, x, y):
        self.display.blit(self.image, (self.object.x + x, self.object.y + y))
