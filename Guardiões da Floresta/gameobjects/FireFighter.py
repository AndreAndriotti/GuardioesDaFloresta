import pygame
from gameobjects.Cooldown import Cooldown
from gameobjects.Monkey import Monkey

class FireFighter:

    def __init__(self, display, name, pos, size, volume):
        self.display = display
        self.name = name
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.length = size[1]
        self.speed = 4
        self.score = 0
        self.water_tank_capacity = 6
        self.water_charges = self.water_tank_capacity
        self.state = "default"
        self.direction = "front"
        self.nearby_objects = []
        self.nearby_civilians = []
        self.is_interacting = False
        
        self.put_out_fire_cooldown = Cooldown(1.5)
        self.rescue_monkey_cooldown = Cooldown(1)
        self.rescue_civilian_cooldown = Cooldown(0.5)
        self.refil_water_tank_cooldown = Cooldown(1)
        
        self.put_out_fire_audio = pygame.mixer.Sound("audios/SFX/firefighter/PutOutFire.mp3")
        self.put_out_fire_audio.set_volume(volume)
        self.rescue_monkey_audio = pygame.mixer.Sound("audios/SFX/firefighter/RescueMonkey.mp3")
        self.rescue_monkey_audio.set_volume(volume)
        self.rescue_civilian_audio = pygame.mixer.Sound("audios/SFX/firefighter/RescueCivilian.mp3")
        self.rescue_civilian_audio.set_volume(volume)
        self.refil_water_tank_audio = pygame.mixer.Sound("audios/SFX/firefighter/PutOutFire.mp3")
        self.refil_water_tank_audio.set_volume(volume)
        self.got_point_audio = pygame.mixer.Sound("audios/SFX/UI/GotPoint.mp3")
        self.got_point_audio.set_volume(volume)
        
        self.monkey = Monkey(display, self)
        self.no_water_icon = pygame.image.load("images/UI/NoWaterIcon.png")

        if self.name == "Pascal":
            self.default_images = {
                "front": pygame.image.load("images/Pascal/Default/PascalFront.png"),
                "back": pygame.image.load("images/Pascal/Default/PascalBack.png"),
                "left": pygame.image.load("images/Pascal/Default/PascalLeft.png"),
                "right": pygame.image.load("images/Pascal/Default/PascalRight.png")
            }
            self.put_out_fire_images = {
                "front": pygame.image.load("images/Pascal/PutOutFire/PascalFront_PutOutFire.png"),
                "back": pygame.image.load("images/Pascal/PutOutFire/PascalBack_PutOutFire.png"),
                "left": pygame.image.load("images/Pascal/PutOutFire/PascalLeft_PutOutFire.png"),
                "right": pygame.image.load("images/Pascal/PutOutFire/PascalRight_PutOutFire.png")
            }
            self.walk_keys = (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

        elif self.name == "Ruby":
            self.default_images = {
                "front": pygame.image.load("images/Ruby/Default/RubyFront.png"),
                "back": pygame.image.load("images/Ruby/Default/RubyBack.png"),
                "left": pygame.image.load("images/Ruby/Default/RubyLeft.png"),
                "right": pygame.image.load("images/Ruby/Default/RubyRight.png")
            }
            self.put_out_fire_images = {
                "front": pygame.image.load("images/Ruby/PutOutFire/RubyFront_PutOutFire.png"),
                "back": pygame.image.load("images/Ruby/PutOutFire/RubyBack_PutOutFire.png"),
                "left": pygame.image.load("images/Ruby/PutOutFire/RubyLeft_PutOutFire.png"),
                "right": pygame.image.load("images/Ruby/PutOutFire/RubyRight_PutOutFire.png")
            }
            self.walk_keys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)


    def FixSpritePosition(self):
        x = 0
        y = 0
        if self.state == "put-out-fire":
            if self.direction == "back":
                if self.is_interacting:
                    y = -13
                else:
                    y = 13
            elif self.direction == "front":
                if self.is_interacting:
                    x = -8
                else:
                    x = 8
            elif self.direction == "left":
                if self.is_interacting:
                    x = -36
                else:
                    x = 36

        self.x += x
        self.y += y

    def Draw(self):
        if self.is_interacting:
            if self.state == "put-out-fire":
                image = self.put_out_fire_images[self.direction]
            elif self.state == "rescue-monkey" or self.state == "rescue-civilian" or self.state == "refil-water-tank":
                image = self.default_images[self.direction]
        else:
            if self.state == "with-monkey":
                self.monkey.Draw(-17,20)
            image = self.default_images[self.direction]
        
        if self.water_charges <= 0:
            self.display.blit(self.no_water_icon, (self.x + 5, self.y - 35))

        self.display.blit(image, (self.x, self.y))


    def Walk(self, key, width, height):
        if not self.is_interacting:
            if key == self.walk_keys[0]:
                self.direction = "back"
                if self.y > self.speed:
                    self.y -= self.speed
            elif key == self.walk_keys[1]:
                self.direction = "front"
                if self.y < height - self.length - self.speed:
                    self.y += self.speed
            elif key == self.walk_keys[2]:
                self.direction = "left"
                if self.x > self.speed:
                    self.x -= self.speed
            elif key == self.walk_keys[3]:
                self.direction = "right"
                if self.x < width - self.width - self.speed:
                    self.x += self.speed

    def UpdateScore(self, points):
        self.got_point_audio.play()
        self.score += points
    
    def StopInteractionAudios(self):
        self.put_out_fire_audio.stop()
        self.rescue_monkey_audio.stop()
        self.rescue_civilian_audio.stop()
        self.refil_water_tank_audio.stop()

    def StartPutOutFire(self):
        self.is_interacting = True
        self.state = "put-out-fire"
        self.FixSpritePosition()
        self.put_out_fire_audio.play()
        self.put_out_fire_cooldown.Reset()

    def PutOutFire(self, tree):
        self.is_interacting = False
        self.FixSpritePosition()
        self.state = "default"
        self.water_charges -= 1
        tree.PutOutFire()
        self.UpdateScore(10)
    
    def StartRescueMonkey(self):
        self.is_interacting = True
        self.state = "rescue-monkey"
        self.rescue_monkey_audio.play()
        self.rescue_monkey_cooldown.Reset()
    
    def RescueMonkey(self, tree):
        self.is_interacting = False
        self.state = "with-monkey"
        tree.RemoveMonkey()
    
    def DeliverMonkey(self):
        self.state = "default"
        self.UpdateScore(20)

    def StartRescueCivilian(self):
        self.is_interacting = True
        self.state = "rescue-civilian"
        self.rescue_civilian_audio.play()
        self.rescue_civilian_cooldown.Reset()

    def RescueCivilian(self, civilian):
        self.is_interacting = False
        self.state = "default"
        civilian.state = "rescued"
        self.UpdateScore(30)

    def StartRefilWaterTank(self):
        self.is_interacting = True
        self.state = "refil-water-tank"
        self.refil_water_tank_audio.play()
        self.refil_water_tank_cooldown.Reset()
    
    def RefilWaterTank(self):
        self.is_interacting = False
        self.state = "default"
        self.water_charges = self.water_tank_capacity

