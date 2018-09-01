import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from back_ground import BackGround
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
from game_functions import check_events,updata_screen,update_bullets,create_fleet
from game_functions import update_aliens

def run_game():
    # 初始化游戏并创建一个屏幕对象
    ai_settings=Settings()
    pygame.init()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    play_button=Button(ai_settings,screen,"Play")
    stats=GameStats(ai_settings)
    score_board=ScoreBoard(ai_settings,screen,stats)
    ship=Ship(ai_settings,screen)
    alien=Alien(ai_settings,screen)
    back_ground=BackGround(screen)
    bullets=Group()
    aliens=Group()

    create_fleet(ai_settings,screen,ship,aliens)

    # 开始游戏的主循环 
    while True:
        check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,score_board)
        if stats.game_active:
            ship.update()
            update_bullets(ai_settings,screen,ship,aliens,bullets,stats,score_board)
            update_aliens(ai_settings,stats,screen,ship,aliens,bullets,score_board)
        updata_screen(ai_settings,screen,stats,ship,back_ground,aliens,bullets,play_button,score_board)

run_game()
