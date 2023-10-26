import pygame

class Tree:

    def __init__(self, display, x, y):
        self.display = display
        self.x = x
        self.y = y
        self.state = "default"
        self.images = {
                "default": pygame.image.load("images/Tree.png"),
                "on-fire": pygame.image.load("images/TreeOnFire.png")
        }

    def Draw(self):
        image = self.images[self.state]
        self.display.blit(image, (self.x, self.y))
    
    def SetFire(self):
        self.state = "on-fire"
    
    def PutOutFire(self):
        self.state = "default"