import pygame

class WaterPump:
    
    def __init__(self, display, pos, size):
        self.display = display
        self.name = "water-pump"
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.length = size[1]
        self.image = pygame.image.load("images/gameobjects/WaterPump.png")

    def Draw(self):
        self.display.blit(self.image, (self.x, self.y))