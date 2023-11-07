import pygame
from pygame.locals import QUIT

WIDTH = 1280
HEIGHT = 720

GREEN = (0,76,8)

def Start(volume):
    instructions_state = "instructions"
    instructions_image = pygame.image.load("images/UI/Instructions.png")
    back_button = pygame.image.load("images/UI/BackButton.png")
    return_button_audio = pygame.mixer.Sound("audios/SFX/UI/ReturnButton.wav")
    return_button_audio.set_volume(volume)

    return instructions_state, instructions_image, back_button, return_button_audio

def HandleEvents(instructions_state, return_button_audio):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            key_pressed = event.key

            if key_pressed == pygame.K_ESCAPE:
                return_button_audio.play()
                instructions_state = "menu"

    return instructions_state

def ShowInstructions(display, instructions_image, back_button):
    display.blit(back_button, (20,20))
    display.blit(instructions_image, (15,25))

def Instructions(display, clock, volume):
    instructions_state, instructions_image, back_button, return_button_audio = Start(volume)

    while True:
        instructions_state = HandleEvents(instructions_state, return_button_audio)

        display.fill(GREEN)

        if instructions_state == "instructions":
            ShowInstructions(display, instructions_image, back_button)
        elif instructions_state == "menu":
            return "main-menu"
        
        clock.tick(60)
        pygame.display.update()
