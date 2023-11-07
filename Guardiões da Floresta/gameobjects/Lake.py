import pygame

class Lake:

    def __init__(self, display, pos):
        self.display = display
        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.image.load("images/gameobjects/Lake.png")

    def Draw(self):
        self.display.blit(self.image, (self.x, self.y))