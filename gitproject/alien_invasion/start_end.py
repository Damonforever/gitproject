import pygame
from pygame.sprite import Sprite
class Start_end(Sprite):
    def __init__(self,ai_settings,screen):
        """初始化图片并加载其位置"""
        super(Start_end,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image1 = pygame.image.load('images/victor.bmp')
        self.image2 = pygame.image.load('images/defate.bmp')
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect1.right = self.screen_rect.right
        self.rect2.right = self.screen_rect.right
        self.rect1.bottom = self.screen_rect.bottom
        self.rect2.bottom = self.screen_rect.bottom

    def blitem1(self):
        self.screen.blit(self.image1,self.rect1)
    def blitem2(self):
        self.screen.blit(self.image2,self.rect2)