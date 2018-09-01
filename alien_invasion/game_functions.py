import sys,pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_keydown_event(event,ai_settings,screen,ship,bullets,stats,aliens,score_board):
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True
    elif event.key==pygame.K_UP:
        ship.moving_up=True
    elif event.key==pygame.K_DOWN:
        ship.moving_down=True
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key==pygame.K_q:
        sys.exit()
    elif event.key==pygame.K_p:
        if not stats.game_active:
            start_game(ai_settings,screen,stats,ship,aliens,bullets,score_board)

def check_keyup_event(event,ship):
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT:
        ship.moving_left=False
    elif event.key==pygame.K_UP:
        ship.moving_up=False
    elif event.key==pygame.K_DOWN:
        ship.moving_down=False

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,score_board):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        #print(event)
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_event(event,ai_settings,screen,ship,bullets,stats,aliens,score_board)
        elif event.type==pygame.KEYUP:
            check_keyup_event(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y,score_board)

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y,score_board):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings,screen,stats,ship,aliens,bullets,score_board)

def start_game(ai_settings,screen,stats,ship,aliens,bullets,score_board):
        pygame.mouse.set_visible(False) # 隐藏光标

        stats.reset_stats()
        stats.game_active=True

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        ai_settings.initialize_dynamic_settings()

        score_board.prep_score()
        score_board.prep_high_score()
        score_board.prep_level()
        score_board.prep_ships()

def updata_screen(ai_settings,screen,stats,ship,back_ground,aliens,bullets,play_button,score_board):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕 
    screen.fill(ai_settings.bg_color)
    #back_ground.blitme()
    ship.blitme()
    aliens.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    score_board.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings,screen,ship,aliens,bullets,stats,score_board):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0 or bullet.rect.right<0 or bullet.rect.left>bullet.screen.get_width():
            bullets.remove(bullet)
    check_bullet_alien_collisons(ai_settings,screen,ship,aliens,bullets,stats,score_board)
    

def check_bullet_alien_collisons(ai_settings,screen,ship,aliens,bullets,stats,score_board):
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisons=pygame.sprite.groupcollide(bullets,aliens,False,True)

    if collisons:
        for aliens in collisons.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            score_board.prep_score()
        check_high_score(stats,score_board)

    if len(aliens)==0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        stats.level+=1
        score_board.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets)<ai_settings.bullets_allowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        new_bullet.direction="UP"
        bullets.add(new_bullet)
        #new_bullet=Bullet(ai_settings,screen,ship)
        #new_bullet.direction="RIGHT"
        #bullets.add(new_bullet)
        #new_bullet=Bullet(ai_settings,screen,ship)
        #new_bullet.direction="LEFT"
        #bullets.add(new_bullet)


def get_number_alien_x(ai_settings,alien_width):
    available_space_x=ai_settings.screen_width-2*alien_width
    number_alien_x=int(available_space_x/(2*alien_width))
    return number_alien_x

def get_number_alien_rows(ai_settings,ship_height,alien_height):
    available_space_y=ai_settings.screen_height-3*alien_height-ship_height
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien=Alien(ai_settings,screen)
    alien.x=alien_width+2*alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
      """创建外星人群"""
      # 创建一个外星人，并计算一行可容纳多少个外星人
      # # 外星人间距为外星人宽度
      alien=Alien(ai_settings,screen)
      number_alien_x=get_number_alien_x(ai_settings,alien.rect.width)
      number_rows=get_number_alien_rows(ai_settings,ship.rect.height,alien.rect.height)

      for row_number in range(number_rows):
          for alien_number in range(number_alien_x):
             create_alien(ai_settings,screen,aliens,alien_number,row_number)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,score_board):
    """相应外星人撞到飞船"""
    if stats.ships_left>0:
        stats.ships_left-=1
        # 更新记分牌
        score_board.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_alens_bottom(ai_settings,stats,screen,ship,aliens,bullets,score_board):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets,score_board)
            break

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets,score_board):
    """
    检查是否有外星人到达屏幕边缘
    然后更新所有外星人的位置
    """
    check_fleet_edge(ai_settings,aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,score_board)
    check_alens_bottom(ai_settings,stats,screen,ship,aliens,bullets,score_board)

def check_fleet_edge(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_frop_speed
    ai_settings.fleet_direction*=-1

def check_high_score(stats, score_board):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()