class GameStats():
    """跟踪游戏的统计数据"""
    def __init__(self,ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #游戏刚启动时处于非活动状态
        self.game_active = False
        #在任何情况下都不应该重置最高分
        filename = 'highscore.txt'
        with open(filename) as file_object:
            for b in file_object:
                self.high_score = int(b)
        self.level = 1

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的数据"""
        self.ships_left = self.ai_settings.ship_limit
        self.boss_left = self.ai_settings.boss_life
        self.score = 0