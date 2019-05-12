import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from sorceboard import  Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
from boss import Boss
from  musics import Musics
from  start_end import Start_end
def run_game():
    #初始化pygame、设置和屏幕对象
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    ms = Musics()
    ms.fplay()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Aline Invasion")
    #创建Play按钮
    play_button = Button(ai_settings,screen,"Play")
    #创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    #创建一艘飞船，一个用于存储子弹的编组和一个外星人编组
    ship = Ship(ai_settings,screen)
    boss = Boss(ai_settings,screen)
    sd = Start_end(ai_settings,screen)
    bullets = Group()
    aliens = Group()
    alien1s = Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    #获取当前系统的字体
    #print(pygame.font.get_fonts())
    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,
                        aliens,alien1s,bullets,ms)
        if stats.game_active:
            ship.update()
            boss.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,alien1s,ms)
            gf.update_aliens(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms)
            gf.update_alien1s(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms)
            gf.update_boss(ai_settings,stats,sb,boss,bullets,ms)
            gf.add_alien(ai_settings,screen,boss,aliens,alien1s)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,boss,
                         alien1s,play_button,sd)

run_game()