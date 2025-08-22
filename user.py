import json
import os

class User():
    def __init__(self):
        self.money = 0
        self.level = 1
        self.max_level = 3
        self.load_data()

    def level_up(self):
        # (3)---滿足條件時self.level+=1---
        # (3)---self.level不能超過self.max_level---
        if self.level < self.max_level:
            self.level += 1


    def save_data(self):
        # (2)---儲存使用者的資料---
        # (2)---需要儲存的有self.money、self.level---
        # (2)---被儲存的位置在資料夾的User_data---
        print("Saving user data...")
        data = {
            "money": self.money,
            "level": self.level
        }
        
        if not os.path.exists("User_data"):
            os.makedirs("User_data")
        
        with open("User_data/user_data.json", "w") as f:
            json.dump(data, f)


    def load_data(self):
        # (2)---讀取使用者的資料---
        # (2)---如果沒有儲存過的資料(第一次玩)，那就使用money=0、level=1---
        print("Loading user data...")
        try:
            with open("User_data/user_data.json", "r") as f:
                data = json.load(f)
                self.money = data["money"]
                self.level = data["level"]
        except (FileNotFoundError, json.JSONDecodeError):
            self.money = 0
            self.level = 1