import pygame

class Tree:

    def __init__(self, display, pos, size):
        self.display = display
        self.name = "tree"
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.length = size[1]
        self.state = "default"
        self.images = {
                "default": pygame.image.load("images/Tree.png"),
                "on-fire": pygame.image.load("images/Tree.png")
        }
        self.fire_image = pygame.image.load("images/Fire.png")

    def Draw(self):
        image = self.images[self.state]
        self.display.blit(image, (self.x, self.y))
        if (self.state == "on-fire"):
            self.display.blit(self.fire_image, (self.x-10, self.y-30))

    def SetFire(self):
        self.state = "on-fire"
    
    def PutOutFire(self):
        self.state = "default"
