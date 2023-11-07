import pygame

class Civilian:

    def __init__(self, display, pos, size, direction):
        self.display = display
        self.name = "civilian"
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.length = size[1]
        self.speed = 1
        self.state = "walk"
        self.direction = direction
        self.images = {
            "left": pygame.image.load("images/gameobjects/CivilianLeft.png"),
            "right": pygame.image.load("images/gameobjects/CivilianRight.png")
        }
    
    def Draw(self, civilians):
        image = self.images[self.direction]
        self.display.blit(image, (self.x, self.y))
        if self.state == "walk":
            self.Move()
        if self.state == "rescued":
            self.MoveToShelter(624, 410, civilians)
    
    def Move(self):
        if self.direction == "right":
            self.x += self.speed
        else:
            self.x -= self.speed
    
    def MoveToShelter(self, shelter_x, shelter_y, civilians):
        if self.x == shelter_x and self.y == shelter_y:
            civilians.remove(self)
        
        if self.x < shelter_x:
            self.direction = "right"
            self.x += self.speed
        elif self.x > shelter_x:
            self.direction = "left"
            self.x -= self.speed
        
        if self.y < shelter_y:
            self.y += self.speed
        elif self.y > shelter_y:
            self.y -= self.speed
