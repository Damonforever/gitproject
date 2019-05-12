import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien
from alien1 import Alien1
def check_keydown_events(event,ai_settings,screen,ship,bullets,stats,ms):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        ms.bullet_sound.play()
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        filename = 'highscore.txt'
        with open(filename,'w') as file_object:
            file_object.write(str(stats.high_score))
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
     #创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def add_alien(ai_settings,screen,boss,aliens,alien1s):
    screen_rect = screen.get_rect()
    #当外星人的数量少于一定数目时，随机生成新的外星人
    if len(aliens)+len(alien1s) < ai_settings.aliens_allowed:
        #只有boss的位置在屏幕的120--1080之间才可以生成新的外星人
        if boss.rect.left > screen_rect.left+120 and boss.rect.right < \
                screen_rect.right-120:
            new_alien1 = Alien1(ai_settings,screen,boss)
            alien1s.add(new_alien1)

def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,
                 aliens,alien1s,bullets,ms):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,stats,ms)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,
                              aliens,alien1s,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,alien1s,
                      bullets,mouse_x,mouse_y):
    """在玩家单击Play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        sb.prep_boss()
        #清空外星人列表和子弹列表
        aliens.empty()
        alien1s.empty()
        bullets.empty()
        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,alien1s,ms):
    """更新子弹位置，并删除已消失的子弹"""
    #更新子弹位置
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,
                                  aliens,bullets,alien1s,ms)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,
                                  aliens,bullets,alien1s,ms):
    #检查是否有子弹击中外星人，击中则双消
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    collision1s = pygame.sprite.groupcollide(bullets,alien1s,True,True)
    if collisions:
        ms.hit_sound.play()
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    if collision1s:
        ms.hit_sound.play()
        for alien1s in collision1s.values():
            stats.score += ai_settings.alien_points * len(alien1s)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens) == 0:
        #删除现有的子弹，加快游戏节奏，并建成一群外星人,提高现有等级
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level +=1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)

def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可以容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可以容纳多少外星人"""
    available_space_y = (ai_settings.screen_height
                         -(3 * alien_height) - ship_height)
    # 减3为了屏幕外星人数量看起来更加和谐
    number_rows = int (available_space_y/(2 * alien_height)) - 2
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height  + 2 * alien.rect.height * (row_number+1)
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可以容纳多少个外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def update_screen(ai_settings,screen,stats,sb,ship,alines,bullets,boss,
                  alien1s,play_button,sd):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都会重绘屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitem()
    boss.blitem()
    alien1s.draw(screen)
    alines.draw(screen)
    #显示得分
    sb.show_score()
    #如果游戏处于非活跃状态，就绘制Play按钮
    if not stats.game_active:
        if stats.boss_left <= 0:
            sd.blitem1()
        if stats.ships_left <= 0:
            sd.blitem2()
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def check_fleet_edges(ai_settings,aliens):
    #有外星人到达边缘采取相应措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    #将整群外星人下移，并改变他们的方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_boss_collisions(stats,sb,boss,bullets,ms):
    #响应子弹击中boss
    collisions = pygame.sprite.spritecollideany(boss,bullets)
    if collisions and stats.boss_left > 0:
        ms.hit_sound.play()
        #将boss_left减1
        stats.boss_left -= 1
        sb.prep_boss()
        bullets.empty()
    else:
        filename = 'highscore.txt'
        with open(filename,'w') as file_object:
            file_object.write(str(stats.high_score))

        stats.game_active = False
        pygame.mouse.set_visible(True)

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0 :
        ms.hit_sound.play()
        #将ships_left减1
        stats.ships_left -= 1
        #更新记分牌
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        alien1s.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #暂停0.5秒
        sleep(0.5)
    else:
        filename = 'highscore.txt'
        with open(filename,'w') as file_object:
            file_object.write(str(stats.high_score))
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样处理
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms)
            break
    for alien1 in alien1s.sprites():
        if alien1.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms)
            break

def update_aliens(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms):
    """更新外星人群中所有外星人位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms)
    check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms)

def update_alien1s(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms):
    check_alien1s_edges(ai_settings,alien1s)
    alien1s.update()
    if pygame.sprite.spritecollideany(ship,alien1s):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms)
    check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,alien1s,bullets,ms)

def check_boss_edges(ai_settings,boss):
    if boss.check_edges():
        ai_settings.boss_direction *= -1

def check_alien1s_edges(ai_settings,alien1s):
    for alien1 in alien1s.sprites():
        if alien1.check_edges():
            ai_settings.alien1_direction *= -1

def update_boss(ai_settings,stats,sb,boss,bullets,ms):
#boss移动
    check_boss_edges(ai_settings,boss)
    boss.update()
    if pygame.sprite.spritecollideany(boss,bullets):
        check_bullet_boss_collisions(stats,sb,boss,bullets,ms)

def check_high_score(stats,sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()