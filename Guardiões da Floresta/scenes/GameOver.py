import pygame
from pygame.locals import QUIT
from database.JSONFileHandler import JSONFileHandler

WIDTH = 1280
HEIGHT = 720

GREEN = (0,76,8)
WHITE = (255,255,255)
BROWN = (165,68,66)

def Start(volume):
    game_over_state = "game-over"
    game_over_base = pygame.image.load("images/UI/GameOverBase.png")
    json_file_handler = JSONFileHandler("database/data.json")
    button_texts = ["Jogar Novamente", "Voltar ao Menu"]
    selected_button = 0
    change_button_audio = pygame.mixer.Sound("audios/SFX/UI/ChangeButton.mp3")
    change_button_audio.set_volume(volume)
    click_button_audio = pygame.mixer.Sound("audios/SFX/UI/ClickButton.mp3")
    click_button_audio.set_volume(volume)

    if volume > 0:
        pygame.mixer.music.load("audios/music/GameOver.mp3")
        pygame.mixer.music.play(-1)

    return game_over_state, game_over_base, json_file_handler, button_texts, selected_button, change_button_audio, click_button_audio

def HandleEvents(game_over_state, button_texts, selected_button, change_button_audio, click_button_audio):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            key_pressed = event.key
            
            if key_pressed == pygame.K_a or key_pressed == pygame.K_LEFT:
                change_button_audio.play()
                selected_button = (selected_button - 1) % len(button_texts)
            elif key_pressed == pygame.K_d or key_pressed == pygame.K_RIGHT:
                change_button_audio.play()
                selected_button = (selected_button + 1) % len(button_texts)
            
            elif key_pressed == pygame.K_SPACE or key_pressed == pygame.K_RETURN:
                click_button_audio.play()
                if selected_button == 0:
                    game_over_state = "play-again"
                elif selected_button == 1:
                    game_over_state = "menu"

    return game_over_state, selected_button

def DrawBase(display, game_over_base):
    x = WIDTH//2 - game_over_base.get_size()[0]//2
    y = HEIGHT//2 - game_over_base.get_size()[1]//2 - 80
    display.blit(game_over_base, (x, y))

def ShowLabels(display, font):
    y = (HEIGHT//2) - 68

    game = font.render("Game", True, WHITE)
    over = font.render("Over", True, WHITE)
    total = font.render("Total", True, WHITE)
    pascal = font.render("Pascal", True, WHITE)
    ruby = font.render("Ruby", True, WHITE)
    
    display.blit(game, (((WIDTH//2) - game.get_width()//2), y-135))
    display.blit(over, (((WIDTH//2) - over.get_width()//2), y-95))
    display.blit(total, (((WIDTH//2 - 273) - total.get_width()//2), y))
    display.blit(pascal, (((WIDTH//2 + 27) - pascal.get_width()//2), y))
    display.blit(ruby, (((WIDTH//2 + 277) - ruby.get_width()//2), y))

def ShowData(display, font, json_file_handler):
    y = (HEIGHT//2) + 5
    last_score = json_file_handler.get("last_score")
    
    score = last_score["score"]
    score_pascal = last_score["score_pascal"]
    score_ruby = last_score["score_ruby"]

    total_score = font.render(f"{score}", True, WHITE)
    pascal_score = font.render(f"{score_pascal}", True, WHITE)
    ruby_score = font.render(f"{score_ruby}", True, WHITE)
    
    display.blit(total_score, (((WIDTH//2 - 273) - total_score.get_width()//2), y))
    display.blit(pascal_score, (((WIDTH//2 + 27) - pascal_score.get_width()//2), y))
    display.blit(ruby_score, (((WIDTH//2 + 277) - ruby_score.get_width()//2), y))

def ShowScore(display, game_over_base, font, json_file_handler):
    DrawBase(display, game_over_base)
    ShowLabels(display, font)
    ShowData(display, font, json_file_handler)

def DrawButtons(display, font, button_texts, selected_button):
    button_width = 320
    button_spacing = 100

    start_x = (WIDTH - (button_width * len(button_texts) + button_spacing * (len(button_texts) - 1))) // 2
    start_y = (HEIGHT//5)*4
    
    for i, text in enumerate(button_texts):
        button_color = BROWN if i == selected_button else WHITE
        button_rect = pygame.Rect(start_x + i * (button_width + button_spacing), start_y, button_width, 50)
        pygame.draw.rect(display, button_color, button_rect)
        text_surface = font.render(text, True, WHITE if i == selected_button else GREEN)
        text_rect = text_surface.get_rect(center=button_rect.center)
        display.blit(text_surface, text_rect)

def UpdateRankingIfHigher(json_file_handler):
    last_score = json_file_handler.get('last_score')
    ranking = json_file_handler.get('ranking')
    updated = False

    for i in range(len(ranking)):
        if last_score['score'] >= ranking[i]['high_score']:
            ranking.insert(i, {
                'high_score': last_score['score'],
                'high_score_pascal': last_score['score_pascal'],
                'high_score_ruby': last_score['score_ruby']
            })
            updated = True
        
            if len(ranking) > 5:
                ranking.pop()
            break

    if updated:
        json_file_handler.set('ranking', ranking)

def GameOver(display, clock, font, volume):
    game_over_state, game_over_base, json_file_handler, button_texts, selected_button, change_button_audio, click_button_audio = Start(volume)
    UpdateRankingIfHigher(json_file_handler)

    while True:
        game_over_state, selected_button = HandleEvents(game_over_state, button_texts, selected_button, change_button_audio, click_button_audio)
        
        display.fill(GREEN)

        if game_over_state == "game-over": 
            ShowScore(display, game_over_base, font, json_file_handler)
            DrawButtons(display, font, button_texts, selected_button)
        elif game_over_state == "play-again":
            return "gameplay", False    
        elif game_over_state == "menu":
            return "main-menu", False

        clock.tick(60)
        pygame.display.update()
