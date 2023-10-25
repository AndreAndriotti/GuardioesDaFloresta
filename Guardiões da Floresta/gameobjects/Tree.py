import pygame

class Tree:

    def __init__(self, display, x, y):
        self.display = display
        self.x = x
        self.y = y
        self.images = {
                "default": pygame.image.load("Images/Tree.png"),
                "on-fire": pygame.image.load("Images/TreeOnFire.png")
    }


    def Draw(self):
        image = self.images["default"]
        self.display.blit(image, (self.x, self.y))
