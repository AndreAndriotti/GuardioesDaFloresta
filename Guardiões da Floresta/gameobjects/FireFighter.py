import pygame

class FireFighter:

    def __init__(self, display, name, x, y):
        self.display = display
        self.name = name
        self.x = x
        self.y = y
        self.speed = 3
        self.direction = "front"
        
        if self.name == "Pascal":
            self.images = {
                "front": pygame.image.load("images/PascalFront.png"),
                "back": pygame.image.load("images/PascalBack.png"),
                "left": pygame.image.load("images/PascalLeft.png"),
                "right": pygame.image.load("images/PascalRight.png")
            }
            self.walk_keys = (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

        elif self.name == "Ruby":
            self.images = {
                "front": pygame.image.load("images/RubyFront.png"),
                "back": pygame.image.load("images/RubyBack.png"),
                "left": pygame.image.load("images/RubyLeft.png"),
                "right": pygame.image.load("images/RubyRight.png")
            }
            self.walk_keys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)


    def Draw(self):
        image = self.images[self.direction]
        self.display.blit(image, (self.x, self.y))

    def Walk(self, key):
        if key == self.walk_keys[0]:
            self.direction = "back"
            self.y -= self.speed
        elif key == self.walk_keys[1]:
            self.direction = "front"
            self.y += self.speed
        elif key == self.walk_keys[2]:
            self.direction = "left"
            self.x -= self.speed
        elif key == self.walk_keys[3]:
            self.direction = "right"
            self.x += self.speed

