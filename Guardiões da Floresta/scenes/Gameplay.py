import pygame
from pygame.locals import QUIT
from random import randint
from math import sqrt
from gameobjects.Lake import Lake
from gameobjects.Shelter import Shelter
from gameobjects.WaterPump import WaterPump
from gameobjects.FireFighter import FireFighter
from gameobjects.Civilian import Civilian
from gameobjects.Tree import Tree
from gameobjects.Cooldown import Cooldown
from database.JSONFileHandler import JSONFileHandler

WIDTH = 1280
HEIGHT = 720

GREEN = (0,76,8)
WHITE = (255,255,255)
RED = (235,53,40)
LIGHT_GREEN = (140,196,63)
YELLOW = (255,207,15)

TREES_POSITION = [[40,20], [320,60], [640,10], [1040,30], [190,250], 
                  [830,140], [40,410], [320,470], [740,380], [1070,250]]

def Start(volume):
    gameplay_state = "gameplay"
    game_difficulty = ["fire"]
    keys_pressed = set()
    trees_qtt = 10
    trees_chared_qtt = 0
    trees_default_qtt = trees_qtt
    fire_cooldown = Cooldown(3)
    fire_cooldown.Reset()
    monkeys_qtt = 0
    monkey_cooldown = Cooldown(10)
    monkey_cooldown.Reset()
    civilians = []
    civilian_cooldown = Cooldown(5)
    civilian_cooldown.Reset()
    civilian_audio = pygame.mixer.Sound("audios/SFX/gameobjects/Civilian.wav")
    civilian_audio.set_volume(volume * 0.5)
    lost_point_audio = pygame.mixer.Sound("audios/SFX/UI/LostPoint.wav")
    lost_point_audio.set_volume(volume * 1.3)
    end_game_audio = pygame.mixer.Sound("audios/SFX/UI/EndGame.wav")
    end_game_audio.set_volume(volume)
    json_file_handler = JSONFileHandler("database/data.json")

    if volume > 0:
        pygame.mixer.music.load("audios/music/Gameplay.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume * 0.3)

    
    return gameplay_state, game_difficulty, keys_pressed, trees_qtt, trees_chared_qtt, trees_default_qtt, fire_cooldown, monkeys_qtt, monkey_cooldown, civilians, civilian_cooldown, civilian_audio, lost_point_audio, end_game_audio, json_file_handler

def CreateObjects(display, trees_qtt, volume):
    lake_size = (302,191)
    lake = Lake(display, ((WIDTH - lake_size[0] - 50), (HEIGHT - lake_size[1] - 20)))
    
    shelter_size = (325,227)
    shelter = Shelter(display, ((WIDTH // 2 - shelter_size[0]//2), (HEIGHT // 2 - shelter_size[1]//2)), shelter_size) 
    
    water_pump_size = (111,137)
    water_pump = WaterPump(display, ((WIDTH - 235), (HEIGHT - 260)), water_pump_size)
    
    firefighter_size = (38,66)
    pascal = FireFighter(display, "Pascal", ((WIDTH // 2 - 40), (HEIGHT // 2 + 90)), firefighter_size, volume)
    ruby = FireFighter(display, "Ruby", ((WIDTH // 2 + 5), (HEIGHT // 2 + 90)), firefighter_size, volume)

    tree_size = (187,243)
    forest = []
    for t in range(trees_qtt):
        new_tree = Tree(display, (TREES_POSITION[t][0], TREES_POSITION[t][1]), tree_size, volume)
        forest.append(new_tree)

    return lake, shelter, water_pump, pascal, ruby, forest

def FireFighterInteractions(firefighter, trees_default_qtt, monkeys_qtt):
    if len(firefighter.nearby_civilians) > 0:
        civilian = firefighter.nearby_civilians[0]
    else:
        civilian = None

    if len(firefighter.nearby_objects) > 0:
        object = firefighter.nearby_objects[0]
    else:
        object = None
        
    if firefighter.is_interacting:
        if firefighter.state == "rescue-civilian":
            if firefighter.rescue_civilian_cooldown.IsReady():
                if civilian != None:
                    if civilian.state == "walk":
                        firefighter.RescueCivilian(civilian)
                        firefighter.nearby_civilians.remove(civilian)

        elif firefighter.state == "put-out-fire":
            if firefighter.put_out_fire_cooldown.IsReady():
                if object != None:
                    if object.state == "on-fire" or object.state == "on-fire-with-monkey":
                        firefighter.PutOutFire(object)
                        trees_default_qtt += 1

        elif firefighter.state == "rescue-monkey":
            if firefighter.rescue_monkey_cooldown.IsReady():
                if object != None:
                    if object.state == "with-monkey":
                        firefighter.RescueMonkey(object)
                        monkeys_qtt -= 1
        
        elif firefighter.state == "refil-water-tank":
            if firefighter.refil_water_tank_cooldown.IsReady():
                firefighter.RefilWaterTank()

    else:
        if civilian == None:
            if object != None:
                if object.name == "tree":
                    if firefighter.state != "with-monkey":
                        if object.state == "on-fire" or object.state == "on-fire-with-monkey":
                            if firefighter.water_charges > 0:
                                firefighter.StartPutOutFire()

                        elif object.state == "with-monkey":
                            firefighter.StartRescueMonkey()

                elif object.name == "shelter":
                    if firefighter.state == "with-monkey":
                        firefighter.DeliverMonkey()
                
                elif object.name == "water-pump":
                    if firefighter.state != "with-monkey":
                        if firefighter.water_charges <= 0:
                            firefighter.StartRefilWaterTank()

        else:
            if firefighter.state != "with-monkey":
                    firefighter.StartRescueCivilian()
    
    return trees_default_qtt, monkeys_qtt

def HandleEvents(keys_pressed, pascal, ruby, trees_default_qtt, monkeys_qtt, gameplay_state):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            key_pressed = event.key
            keys_pressed.add(key_pressed)

            if key_pressed == pygame.K_ESCAPE:
                gameplay_state = "menu"

        if event.type == pygame.KEYUP:
            key_released = event.key
            keys_pressed.discard(key_released)

            if key_released == pygame.K_SPACE:
                pascal.is_interacting = False
                pascal.FixSpritePosition()
                pascal.StopInteractionAudios()
                if pascal.state != "with-monkey":
                    pascal.state = "default"

            if key_released == pygame.K_RETURN:
                ruby.is_interacting = False
                ruby.FixSpritePosition()
                ruby.StopInteractionAudios()
                if ruby.state != "with-monkey":
                    ruby.state = "default"
        
    if pygame.K_SPACE in keys_pressed:
            trees_default_qtt, monkeys_qtt = FireFighterInteractions(pascal, trees_default_qtt, monkeys_qtt)
    
    if pygame.K_RETURN in keys_pressed:
            trees_default_qtt, monkeys_qtt = FireFighterInteractions(ruby, trees_default_qtt, monkeys_qtt)
    
    return trees_default_qtt, monkeys_qtt, gameplay_state

def MoveFireFighters(keys_pressed, pascal, ruby):
    isPascalMoving = any(key in keys_pressed for key in pascal.walk_keys)
    isRubyMoving = any(key in keys_pressed for key in ruby.walk_keys)

    if isPascalMoving:
        for key in keys_pressed:
            pascal.Walk(key, WIDTH, HEIGHT)

    if isRubyMoving:
        for key in keys_pressed:
            ruby.Walk(key, WIDTH, HEIGHT)

def DrawObjects(lake, shelter, water_pump, ruby, pascal, civilians, forest):
    lake.Draw()
    shelter.Draw()
    water_pump.Draw()
    ruby.Draw()
    pascal.Draw()
    for civilian in civilians:
        civilian.Draw(civilians)
    for tree in forest:
        tree.Draw()

def SetFireOnTree(forest, fire_cooldown, trees_qtt, trees_default_qtt):
    if fire_cooldown.IsReady():
        if trees_default_qtt > 0:
            tree_sorted = forest[randint(0,trees_qtt-1)]
            while (tree_sorted.state != "default" and tree_sorted.state != "with-monkey"):
                tree_sorted = forest[randint(0,trees_qtt-1)]
            
            tree_sorted.SetFire()
            trees_default_qtt -= 1
            fire_cooldown.Reset()
    
    return trees_default_qtt

def CharTrees(forest, monkeys_qtt, pascal, ruby, trees_chared_qtt, lost_point_audio):
    for tree in forest:
        if tree.char_cooldown.cooldown_duration > tree.min_char_time:
            tree.char_cooldown.cooldown_duration -= 0.001
        if tree.state == "on-fire" or tree.state == "on-fire-with-monkey":
            if tree.char_cooldown.IsReady():
                tree.Char()
                trees_chared_qtt += 1
                if tree.state == "on-fire-with-monkey":
                    monkeys_qtt -= 1
                    UpdateTotalScore(-60, pascal, ruby, lost_point_audio)
                else:
                    UpdateTotalScore(-30, pascal, ruby, lost_point_audio)

    return monkeys_qtt, trees_chared_qtt

def CalcDistance(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def CalcPivot(object):
    object_pivot = []
    object_pivot.append(object.x + object.width // 2)
    object_pivot.append(object.y + object.length // 2)
    return object_pivot

def CheckTreesDistances(firefighter, forest):
    for tree in forest:
        firefighter_pivot = CalcPivot(firefighter)
        tree_pivot = CalcPivot(tree)
        distance = CalcDistance(firefighter_pivot[0], firefighter_pivot[1], tree_pivot[0], tree_pivot[1])

        if distance <= 100:
            if tree not in firefighter.nearby_objects:
                firefighter.nearby_objects.append(tree)
        else:
            if tree in firefighter.nearby_objects:
                firefighter.nearby_objects.remove(tree)

def CheckShelterDistance(firefighter, shelter):
    firefighter_pivot = CalcPivot(firefighter)
    shelter_pivot = CalcPivot(shelter)
    distance = CalcDistance(firefighter_pivot[0], firefighter_pivot[1], shelter_pivot[0], shelter_pivot[1]+50)

    if distance <= 50:
        if shelter not in firefighter.nearby_objects:
            firefighter.nearby_objects.append(shelter)
    else:
        if shelter in firefighter.nearby_objects:
            firefighter.nearby_objects.remove(shelter)

def CheckWaterPumpDistance(firefighter, water_pump):
    firefighter_pivot = CalcPivot(firefighter)
    water_pump_pivot = CalcPivot(water_pump)
    distance = CalcDistance(firefighter_pivot[0], firefighter_pivot[1], water_pump_pivot[0], water_pump_pivot[1])

    if distance <= 50:
        if water_pump not in firefighter.nearby_objects:
            firefighter.nearby_objects.append(water_pump)
    else:
        if water_pump in firefighter.nearby_objects:
            firefighter.nearby_objects.remove(water_pump)

def CheckCivilianDistance(firefighter, civilians):
    for civilian in civilians:
        firefighter_pivot = CalcPivot(firefighter)
        civilian_pivot = CalcPivot(civilian)
        distance = CalcDistance(firefighter_pivot[0], firefighter_pivot[1], civilian_pivot[0], civilian_pivot[1])

        if distance <= 50:
            if civilian not in firefighter.nearby_civilians:
                if civilian.state != "rescued":
                    firefighter.nearby_civilians.append(civilian)
        else:
            if civilian in firefighter.nearby_civilians:
                firefighter.nearby_civilians.remove(civilian)

def CheckDistances(pascal, ruby, forest, shelter, water_pump, civilians):
    CheckTreesDistances(pascal, forest) 
    CheckTreesDistances(ruby, forest)
    CheckShelterDistance(pascal, shelter)
    CheckShelterDistance(ruby, shelter)
    CheckWaterPumpDistance(pascal, water_pump)
    CheckWaterPumpDistance(ruby, water_pump)
    CheckCivilianDistance(pascal, civilians)
    CheckCivilianDistance(ruby, civilians)

def SpawnMonkey(forest, monkey_cooldown, monkeys_qtt, trees_qtt, trees_default_qtt):
    if monkey_cooldown.IsReady():
        if trees_default_qtt > 0 and trees_default_qtt > monkeys_qtt:
            tree_sorted = forest[randint(0,trees_qtt-1)]
            while (tree_sorted.state != "default"):
                tree_sorted = forest[randint(0,trees_qtt-1)]
            
            tree_sorted.SpawnMonkey()
            monkeys_qtt += 1
            monkey_cooldown.Reset()

    return monkeys_qtt

def SpawnCivilian(civilian_cooldown, display, civilians, civilian_audio):
    if civilian_cooldown.IsReady():
        sorted_direction = randint(0,1)
        if sorted_direction == 0:
            direction = "right"
            x = 0
        else:
            direction = "left"
            x = WIDTH
        y = randint(0, HEIGHT-71)
        
        civilian_size = (35,71)
        new_civilian = Civilian(display, (x,y), (civilian_size[0], civilian_size[1]), direction)
        civilians.append(new_civilian)
        civilian_audio.play()
        civilian_cooldown.Reset()

def CheckCiviliansPosition(civilians, pascal, ruby, lost_point_audio):
    for civilian in civilians:
        if civilian.x < -35 or civilian.x > WIDTH:
            if civilian in pascal.nearby_civilians:
                pascal.nearby_civilians.remove(civilian)
            if civilian in ruby.nearby_civilians:
                ruby.nearby_civilians.remove(civilian)
            civilians.remove(civilian)
            UpdateTotalScore(-10, pascal, ruby, lost_point_audio)

def UpdateTotalScore(points, pascal, ruby, lost_point_audio):
    if points < 0:
        lost_point_audio.play()
    pascal.score += points // 2
    ruby.score += points // 2

def ShowScore(display, pascal, ruby, font):
    pascal_score = font.render(f"{pascal.score}", True, WHITE)
    total_score = font.render(f"{pascal.score + ruby.score}", True, WHITE)
    ruby_score = font.render(f"{ruby.score}", True, WHITE)
    
    pascal_width = pascal_score.get_width()
    total_width = total_score.get_width()
    ruby_width = ruby_score.get_width()

    margin = 8

    pascal_rect = pygame.Rect(50, 20 - margin, pascal_width + 2 * margin, pascal_score.get_height() + 2 * margin)
    total_rect = pygame.Rect((WIDTH // 2 - total_width // 2) - 5, 20 - margin, total_width + 2 * margin, total_score.get_height() + 2 * margin)
    ruby_rect = pygame.Rect(WIDTH - ruby_width - 50 - 5, 20 - margin, ruby_width + 2 * margin, ruby_score.get_height() + 2 * margin)

    pygame.draw.rect(display, RED, pascal_rect)
    pygame.draw.rect(display, LIGHT_GREEN, total_rect)
    pygame.draw.rect(display, YELLOW, ruby_rect)

    display.blit(pascal_score, (50 + margin, 20))
    display.blit(total_score, (total_rect.x + margin, 20))
    display.blit(ruby_score, (ruby_rect.x + margin, 20))

def RegisterScore(pascal, ruby, json_file_handler):
    last_score_data = {
        "score": pascal.score + ruby.score,
        "score_pascal": pascal.score,
        "score_ruby": ruby.score
    }
    json_file_handler.set("last_score", last_score_data)

def IsGameOver(trees_chared_qtt, trees_qtt, gameplay_state):
    if trees_chared_qtt >= trees_qtt:
        gameplay_state = "game-over"
    return gameplay_state

def EndGame(pascal, ruby, volume, end_game_audio, json_file_handler):
    if volume > 0:
        pygame.mixer.music.stop()
        end_game_audio.play()
    RegisterScore(pascal, ruby, json_file_handler)
    pygame.time.delay(2000)

def SetGameDifficulty(game_difficulty, pascal, ruby):
    score = pascal.score + ruby.score
    if "monkey" not in game_difficulty and score >= 50:
        game_difficulty.append("monkey")
    elif "civilian" not in game_difficulty and score >= 150:
        game_difficulty.append("civilian")
    return game_difficulty

def Gameplay(display, clock, font, volume):
    gameplay_state, game_difficulty, keys_pressed, trees_qtt, trees_chared_qtt, trees_default_qtt, fire_cooldown, monkeys_qtt, monkey_cooldown, civilians, civilian_cooldown, civilian_audio, lost_point_audio, end_game_audio, json_file_handler = Start(volume)
    lake, shelter, water_pump, pascal, ruby, forest  = CreateObjects(display, trees_qtt, volume)

    while True:
        gameplay_state = IsGameOver(trees_chared_qtt, trees_qtt, gameplay_state)
        if gameplay_state == "game-over":
            EndGame(pascal, ruby, volume, end_game_audio, json_file_handler)
            return "game-over", False
        elif gameplay_state == "menu":
            return "main-menu", False
        
        trees_default_qtt, monkeys_qtt, gameplay_state = HandleEvents(keys_pressed, pascal, ruby, trees_default_qtt, monkeys_qtt, gameplay_state)
        MoveFireFighters(keys_pressed, pascal, ruby)
        CheckDistances(pascal, ruby, forest, shelter, water_pump, civilians)

        game_difficulty = SetGameDifficulty(game_difficulty, pascal, ruby)
        if "fire" in game_difficulty:
            trees_default_qtt = SetFireOnTree(forest, fire_cooldown, trees_qtt, trees_default_qtt)
            monkeys_qtt, trees_chared_qtt = CharTrees(forest, monkeys_qtt, pascal, ruby, trees_chared_qtt, lost_point_audio)
        if "monkey" in game_difficulty:
            monkeys_qtt = SpawnMonkey(forest, monkey_cooldown, monkeys_qtt, trees_qtt, trees_default_qtt)
        if "civilian" in game_difficulty:
            SpawnCivilian(civilian_cooldown, display, civilians, civilian_audio)
            CheckCiviliansPosition(civilians, pascal, ruby, lost_point_audio)

        display.fill(GREEN)
        DrawObjects(lake, shelter, water_pump, ruby, pascal, civilians, forest)
        ShowScore(display, pascal, ruby, font)

        clock.tick(60)
        pygame.display.update()