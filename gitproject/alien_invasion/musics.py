import pygame
class Musics():
    """游戏音效"""
    def __init__(self):
        self.hit_sound = pygame.mixer.Sound("hit.wav")
        #音量设置
        self.hit_sound.set_volume(0.2)
        self.bullet_sound = pygame.mixer.Sound("bullet.wav")
        self.bullet_sound.set_volume(0.5)
    def fplay(self):
        self.fight_sound = pygame.mixer.Sound("fight.ogg")
        #音量设置
        self.fight_sound.set_volume(0.2)
        #设置游戏背景音乐无限循环
        self.fight_sound.play(-1)