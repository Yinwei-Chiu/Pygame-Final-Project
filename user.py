import json
import os

class User():
    def __init__(self):
        self.money = 0
        self.level = 1
        self.max_level = 3
        self.best_time = 0  # 最佳時間（毫秒）
        self.load_data()

    def level_up(self):
        # 滿足條件時self.level+=1
        # self.level不能超過self.max_level
        if self.level < self.max_level:
            self.level += 1

    def save_data(self):
        # 儲存使用者的資料
        # 需要儲存的有self.money、self.level、self.best_time
        # 被儲存的位置在資料夾的User_data
        print("Saving user data...")
        data = {
            "money": self.money,
            "level": self.level,
            "best_time": self.best_time
        }
        
        if not os.path.exists("User_data"):
            os.makedirs("User_data")
        
        with open("User_data/user_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        # 讀取使用者的資料
        # 如果沒有儲存過的資料(第一次玩)，那就使用money=0、level=1、best_time=0
        print("Loading user data...")
        try:
            with open("User_data/user_data.json", "r") as f:
                data = json.load(f)
                self.money = data.get("money", 0)
                self.level = data.get("level", 1)
                self.best_time = data.get("best_time", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.money = 0
            self.level = 1
            self.best_time = 0

    def get_best_time_text(self):
        """獲得最佳時間的顯示文字"""
        if self.best_time == 0:
            return "No record yet"
        else:
            return f"{self.best_time/1000:.1f}s"