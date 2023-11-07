import pygame
from gameobjects.Cooldown import Cooldown
from gameobjects.Monkey import Monkey

class Tree:

    def __init__(self, display, pos, size, volume):
        self.display = display
        self.name = "tree"
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.length = size[1]
        self.state = "default"
        self.char_cooldown = Cooldown(10)

        self.fire_audio = pygame.mixer.Sound("audios/SFX/gameobjects/Fire.mp3")
        self.fire_audio.set_volume(volume)
        self.monkey_audio = pygame.mixer.Sound("audios/SFX/gameobjects/Monkey.mp3")
        self.monkey_audio.set_volume(volume)

        self.images = {
                "default": pygame.image.load("images/gameobjects/Tree.png"),
                "on-fire": pygame.image.load("images/gameobjects/Tree.png"),
                "with-monkey": pygame.image.load("images/gameobjects/Tree.png"),
                "on-fire-with-monkey": pygame.image.load("images/gameobjects/Tree.png"),
                "charred": pygame.image.load("images/gameobjects/CharredTree.png")
        }
        self.fire_image = pygame.image.load("images/gameobjects/Fire.png")
        self.monkey = Monkey(display, self)

    def Draw(self):
        image = self.images[self.state]
        self.display.blit(image, (self.x, self.y))
        if self.state == "on-fire":
            self.display.blit(self.fire_image, (self.x-10, self.y-30))
        elif self.state == "with-monkey":
            self.monkey.Draw(60,140)
        elif self.state == "on-fire-with-monkey":
            self.display.blit(self.fire_image, (self.x-10, self.y-30))
            self.monkey.Draw(60,140)

    def SetFire(self):
        self.char_cooldown.Reset()
        self.fire_audio.play()
        if self.state == "default":
            self.state = "on-fire"
        elif self.state == "with-monkey":
            self.state = "on-fire-with-monkey"
    
    def PutOutFire(self):
        if self.state == "on-fire":
            self.state = "default"
        elif self.state == "on-fire-with-monkey":
            self.state = "with-monkey"
    
    def Char(self):
        self.state = "charred"

    def SpawnMonkey(self):
        self.monkey_audio.play()
        self.state = "with-monkey"

    def RemoveMonkey(self):
        self.state = "default"
