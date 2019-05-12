import pygame
class Boss():
    def __init__(self,ai_settings,screen):
        """初始化boss并设置其初始位置"""
        self.screen = screen
        self.ai_settings = ai_settings

        #加载boss图像，并获取其外接矩形
        self.image = pygame.image.load('images/alien2.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将boss放在屏幕顶端中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top + 70

        # 在boss的属性center中存储小数值
        self.center = float(self.rect.centerx)

    def check_edges(self):
        """如果boss位与屏幕边缘，就返回TRUE"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """调整boss的位置"""
        #向右或者向左移动boss
        self.center += (self.ai_settings.boss_speed_factor * self.ai_settings.boss_direction)

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitem(self):
        """在指定位置绘制boss"""
        self.screen.blit(self.image,self.rect)