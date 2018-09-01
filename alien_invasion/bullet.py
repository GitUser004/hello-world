import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_settings,screen,ship):
        super().__init__()
        self.screen=screen
        self.ai_settings=ai_settings

        self.rect=pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx=ship.rect.centerx
        self.rect.top=ship.rect.top

        self.x=float(self.rect.x)
        self.y=float(self.rect.y)
        self.xcenter=float(self.rect.centerx)
        self.ycenter=float(self.rect.centery)

        self.color=ai_settings.bullet_color
        self.speed_factor=ai_settings.bullet_speed_factor

        self.direction="UP"

    def update(self):
        if self.direction=="UP":
            self.rect=pygame.Rect(0,0,self.ai_settings.bullet_width,self.ai_settings.bullet_height)
            self.y-=self.speed_factor
            self.rect.x=self.x
            self.rect.y=self.y
        elif self.direction=="RIGHT":
            self.rect=pygame.Rect(0,0,self.ai_settings.bullet_height,self.ai_settings.bullet_width)
            self.xcenter+=self.speed_factor
            self.rect.centerx=self.xcenter
            self.rect.y=self.y
        elif self.direction=="LEFT":
            self.rect=pygame.Rect(0,0,self.ai_settings.bullet_height,self.ai_settings.bullet_width)
            self.xcenter-=self.speed_factor
            self.rect.centerx=self.xcenter
            self.rect.y=self.y


    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
