import pygame
from pygame.locals import QUIT
from database.JSONFileHandler import JSONFileHandler

WIDTH = 1280
HEIGHT = 720

GREEN = (0,76,8)
WHITE = (255,255,255)

def Start():
    ranking_state = "ranking"
    ranking_base = pygame.image.load("images/UI/RankingBase.png")
    json_file_handler = JSONFileHandler("database/data.json")

    return ranking_state, ranking_base, json_file_handler

def HandleEvents(ranking_state):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            key_pressed = event.key

            if key_pressed == pygame.K_ESCAPE:
                ranking_state = "menu"

    return ranking_state

def DrawBase(display, ranking_base):
    x = WIDTH//2 - ranking_base.get_size()[0]//2
    y = HEIGHT//2 - ranking_base.get_size()[1]//2 + 12
    display.blit(ranking_base, (x, y))

def ShowLabels(display, font):
    y = (HEIGHT//2)-100

    title = font.render("Ranking", True, WHITE)
    rank = font.render("Rank", True, WHITE)
    total = font.render("Total", True, WHITE)
    pascal = font.render("Pascal", True, WHITE)
    ruby = font.render("Ruby", True, WHITE)
    
    display.blit(title, (((WIDTH//2) - title.get_width()//2), y-90))
    display.blit(rank, (((WIDTH//2 - 400) - rank.get_width()//2), y))
    display.blit(total, (((WIDTH//2 - 150) - total.get_width()//2), y))
    display.blit(pascal, (((WIDTH//2 + 150) - pascal.get_width()//2), y))
    display.blit(ruby, (((WIDTH//2 + 400) - ruby.get_width()//2), y))

def ShowData(display, font, json_file_handler):
    y = (HEIGHT//2)-25
    ranking = json_file_handler.get("ranking")
    
    for i in range(5):
        high_score = ranking[i]["high_score"]
        high_score_pascal = ranking[i]["high_score_pascal"]
        high_score_ruby = ranking[i]["high_score_ruby"]

        rank = font.render(f"{i+1}º", True, WHITE)
        total_score = font.render(f"{high_score}", True, WHITE)
        pascal_score = font.render(f"{high_score_pascal}", True, WHITE)
        ruby_score = font.render(f"{high_score_ruby}", True, WHITE)
        
        display.blit(rank, (((WIDTH//2 - 400) - rank.get_width()//2), y))
        display.blit(total_score, (((WIDTH//2 - 150) - total_score.get_width()//2), y))
        display.blit(pascal_score, (((WIDTH//2 + 150) - pascal_score.get_width()//2), y))
        display.blit(ruby_score, (((WIDTH//2 + 400) - ruby_score.get_width()//2), y))

        y += 55

def ShowRanking(display, ranking_base, font, json_file_handler):
    DrawBase(display, ranking_base)
    ShowLabels(display, font)
    ShowData(display, font, json_file_handler)

def Ranking(display, clock, font):
    ranking_state, ranking_base, json_file_handler = Start()

    while True:
        ranking_state = HandleEvents(ranking_state)
        
        display.fill(GREEN)

        if ranking_state == "ranking":
            ShowRanking(display, ranking_base, font, json_file_handler)
        elif ranking_state == "menu":
            return "main-menu"

        clock.tick(60)
        pygame.display.update()
