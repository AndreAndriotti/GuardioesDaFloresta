import pygame
from pygame.locals import QUIT

WIDTH = 1280
HEIGHT = 720

GREEN = (0,76,8)
WHITE = (255,255,255)
BROWN = (165,68,66)

def Start():
    logo = pygame.image.load("images/Logo.png")
    button_texts = ["Jogar", "Instruções", "Ranking", "Áudio"]
    selected_button = 0

    return logo, button_texts, selected_button

def HandleEvents(menu_state, button_texts, selected_button):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            key_pressed = event.key

            
            
            if menu_state == "intro-menu":
                if key_pressed == pygame.K_SPACE or key_pressed == pygame.K_RETURN:
                    menu_state = "main-menu"

            elif menu_state == "main-menu":
                if key_pressed == pygame.K_ESCAPE:
                    menu_state = "intro-menu"

                elif key_pressed == pygame.K_a or key_pressed == pygame.K_LEFT:
                    selected_button = (selected_button - 1) % len(button_texts)
                elif key_pressed == pygame.K_d or key_pressed == pygame.K_RIGHT:
                    selected_button = (selected_button + 1) % len(button_texts)
                
                elif key_pressed == pygame.K_SPACE or key_pressed == pygame.K_RETURN:
                    if selected_button == 0:
                        menu_state = "play"
                    elif selected_button == 1:
                        print("Você pressionou o botão 'Instruções'")
                    elif selected_button == 2:
                        menu_state = "ranking"
                    elif selected_button == 3:
                        print("Você pressionou o botão 'Áudio'")

    return menu_state, selected_button

def DrawLogo(display, logo):
    display.blit(logo, (WIDTH//2 - logo.get_size()[0]//2, HEIGHT//2 - logo.get_size()[1]//2 - 50))

def ShowIntroText(display, font):
    intro_text = font.render(f"Pressione SPACE/ENTER para começar!", True, WHITE)
    display.blit(intro_text, ((WIDTH//2 - intro_text.get_width()//2), (HEIGHT//5)*4))

def DrawButtons(display, font, button_texts, selected_button):
    button_width = 200
    button_spacing = 50

    start_x = (WIDTH - (button_width * len(button_texts) + button_spacing * (len(button_texts) - 1))) // 2
    start_y = (HEIGHT//5)*4
    
    for i, text in enumerate(button_texts):
        button_color = BROWN if i == selected_button else WHITE
        button_rect = pygame.Rect(start_x + i * (button_width + button_spacing), start_y, button_width, 50)
        pygame.draw.rect(display, button_color, button_rect)
        text_surface = font.render(text, True, WHITE if i == selected_button else GREEN)
        text_rect = text_surface.get_rect(center=button_rect.center)
        display.blit(text_surface, text_rect)


def Menu(display, clock, font, menu_state):
    
    logo, button_texts, selected_button = Start()

    while True:
        #print(menu_state)
        menu_state, selected_button = HandleEvents(menu_state, button_texts, selected_button)
        
        display.fill(GREEN)
        DrawLogo(display, logo)

        if menu_state == "intro-menu":
            ShowIntroText(display, font)
        elif menu_state == "main-menu":    
            DrawButtons(display, font, button_texts, selected_button)
        elif menu_state == "play":
            return "gameplay"
        elif menu_state == "ranking":
            return "ranking"

        clock.tick(60)
        pygame.display.update()
