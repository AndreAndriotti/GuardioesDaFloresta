import pygame
from pygame.locals import QUIT

WIDTH = 1280
HEIGHT = 720

GREEN = (0,76,8)
WHITE = (255,255,255)
BROWN = (165,68,66)

def Start(volume, is_music_playing):
    logo = pygame.image.load("images/UI/Logo.png")
    button_texts = ["Jogar", "Instruções", "Ranking", "Áudio"]
    selected_button = 0
    change_button_audio = pygame.mixer.Sound("audios/SFX/UI/ChangeButton.wav")
    change_button_audio.set_volume(volume)
    click_button_audio = pygame.mixer.Sound("audios/SFX/UI/ClickButton.wav")
    click_button_audio.set_volume(volume)
    start_game_audio = pygame.mixer.Sound("audios/SFX/UI/StartGame.wav")
    start_game_audio.set_volume(volume)

    if volume > 0 and not is_music_playing:
        pygame.mixer.music.load("audios/music/Menu.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume * 0.3)
        is_music_playing = True

    return logo, button_texts, selected_button, change_button_audio, click_button_audio, start_game_audio, is_music_playing

def HandleEvents(menu_state, button_texts, selected_button, volume, is_music_playing, change_button_audio, click_button_audio, start_game_audio):
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
                if key_pressed == pygame.K_a or key_pressed == pygame.K_LEFT:
                    change_button_audio.play()
                    selected_button = (selected_button - 1) % len(button_texts)
                elif key_pressed == pygame.K_d or key_pressed == pygame.K_RIGHT:
                    change_button_audio.play()
                    selected_button = (selected_button + 1) % len(button_texts)
                
                elif key_pressed == pygame.K_SPACE or key_pressed == pygame.K_RETURN:
                    if selected_button == 0:
                        start_game_audio.play()
                        menu_state = "play"
                    elif selected_button == 1:
                        click_button_audio.play()
                        menu_state = "instructions"
                        if volume == 0:
                            click_button_audio.play()
                            is_music_playing = False
                    elif selected_button == 2:
                        click_button_audio.play()
                        menu_state = "ranking"
                        if volume == 0:
                            is_music_playing = False
                    elif selected_button == 3:
                        click_button_audio.play()
                        volume, is_music_playing = UpdateAudio(volume, is_music_playing, change_button_audio, click_button_audio)

    return menu_state, selected_button, volume, is_music_playing

def UpdateAudio(volume, is_music_playing, change_button_audio, click_button_audio):
    if volume > 0:
        volume = 0
        pygame.mixer.music.pause()
    else:
        volume = 1
        if is_music_playing:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.load("audios/music/Menu.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume * 0.3)
            is_music_playing = True

    change_button_audio.set_volume(volume)
    click_button_audio.set_volume(volume)
    
    return volume, is_music_playing

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


def Menu(display, clock, font, volume, is_music_playing, menu_state):
    
    logo, button_texts, selected_button, change_button_audio, click_button_audio, start_game_audio, is_music_playing = Start(volume, is_music_playing)

    while True:
        menu_state, selected_button, volume, is_music_playing = HandleEvents(menu_state, button_texts, selected_button, volume, is_music_playing, change_button_audio, click_button_audio, start_game_audio)
        
        display.fill(GREEN)
        DrawLogo(display, logo)

        if menu_state == "intro-menu":
            ShowIntroText(display, font)
        elif menu_state == "main-menu":    
            DrawButtons(display, font, button_texts, selected_button)
        elif menu_state == "play":
            return "gameplay", volume, is_music_playing
        elif menu_state == "instructions":
            return "instructions", volume, is_music_playing
        elif menu_state == "ranking":
            return "ranking", volume, is_music_playing

        clock.tick(60)
        pygame.display.update()
