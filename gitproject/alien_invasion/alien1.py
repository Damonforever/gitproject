import pygame
from pygame.sprite import Sprite
class Alien1(Sprite):
    """表示单个外星人1的类"""
    def __init__(self,ai_settings,screen,boss):
        """初始化外星人1并设置其起始位置"""
        super(Alien1,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人1图像，并设置其rect属性
        self.image = pygame.image.load('images/alien1.bmp')
        self.rect = self.image.get_rect()

        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人1的精确位置
        self.rect.centerx = boss.rect.centerx
        self.rect.top = boss.rect.bottom

        #存储用小数表示的外星人1的位置
        self.center = float(self.rect.centerx)
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.alien1_speed_factor

    def check_edges(self):
            """如果alien1位于屏幕边缘，就返回TRUE"""
            screen_rect = self.screen.get_rect()
            if self.rect.right >= screen_rect.right:
                return True
            elif self.rect.left <= 0:
                return True

    def update(self):
        #向右或者向左移动alien1
        self.center += (self.ai_settings.alien1_speed_factor * self.ai_settings.alien1_direction)
        # 根据self.center更新rect对象
        self.rect.centerx = self.center
        self.y +=self.speed_factor *0.1
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)