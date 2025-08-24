LEVELS = {
    1: {
        "background": "Image/background/Million.png",
        "enemies": ["Tea", "mango_ice"],  # 保持原名稱以維持兼容性，實際是台南美食
        "boss": "Boss",  # 只有一個Boss
        "boss_time": 5000,  # 5秒後Boss出現
        "enemy_delay": (1500, 2500)  # 食物刷新間隔
    },
    2: {
        "background": "Image/background/Lindepartment.png", 
        "enemies": ["noodle", "oyster_omlet"],
        "boss": "Boss",
        "boss_time": 8000,  # 8秒後Boss出現
        "enemy_delay": (1200, 2000)  # 食物刷新間隔
    }, 
    3: {
        "background": "Image/background/kom_temple.png",
        "enemies": ["rice_cake", "shrimp_rool"],
        "boss": "Boss",
        "boss_time": 6000,  # 6秒後Boss出現
        "enemy_delay": (1000, 1800)  # 食物刷新間隔
    }
}