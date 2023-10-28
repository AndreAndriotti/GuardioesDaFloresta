import pygame
from gameobjects.Cooldown import Cooldown

class Tree:

    def __init__(self, display, pos, size):
        self.display = display
        self.name = "tree"
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.length = size[1]
        self.char_cooldown = Cooldown(10)
        self.state = "default"
        self.images = {
                "default": pygame.image.load("images/Tree.png"),
                "on-fire": pygame.image.load("images/Tree.png"),
                "charred": pygame.image.load("images/CharredTree.png")
        }
        self.fire_image = pygame.image.load("images/Fire.png")

    def Draw(self):
        image = self.images[self.state]
        self.display.blit(image, (self.x, self.y))
        if (self.state == "on-fire"):
            self.display.blit(self.fire_image, (self.x-10, self.y-30))

    def SetFire(self):
        self.char_cooldown.Reset()
        self.state = "on-fire"
    
    def PutOutFire(self):
        self.state = "default"
    
    def Char(self):
        self.state = "charred"
