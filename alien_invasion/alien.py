import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen=screen
        self.ai_settings=ai_settings

        self.image=pygame.image.load("images/alien.bmp")
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        self.x=float(self.rect.x)
        self.y=float(self.rect.y)
        self.xcenter=float(self.rect.centerx)
        self.ycenter=float(self.rect.centery)


    def update(self):
        """向右移动外星人"""
        self.x+= self.ai_settings.fleet_direction*self.ai_settings.alien_speed_factor
        self.rect.x=self.x

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def check_edge(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True
   
