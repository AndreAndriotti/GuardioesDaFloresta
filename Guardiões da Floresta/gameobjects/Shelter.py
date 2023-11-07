import pygame

class Shelter:

    def __init__(self, display, pos, size):
        self.display = display
        self.name = "shelter"
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.length = size[1]
        self.image = pygame.image.load("images/gameobjects/Shelter.png")
    
    def Draw(self):
        self.display.blit(self.image, (self.x, self.y))