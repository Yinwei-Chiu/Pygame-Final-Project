LEVELS = {
    1: {
        "background": "Image/road_background.png",
        "enemies": ["coffin_bread", "mango_ice"],  # 台南美食
        "boss": "Boss1",  # 只有一個Boss
        "boss_time": 5000,  # 5秒後Boss出現（改短一點方便測試）
        "enemy_delay": (1600, 3000)  # 刷新頻率*0.5 (原本800-1500，現在1600-3000)
    },
    # 第二關之後可以以後再加
    2: {
        "background": "Image/road_background.png", 
        "enemies": ["coffin_bread", "mango_ice"],
        "boss": "Boss1",  # 同樣的Boss
        "boss_time": 8000,  # 8秒後Boss出現
        "enemy_delay": (1200, 2400)  # 刷新頻率*0.5 (原本600-1200，現在1200-2400)
    }, 
    3: {
        "background": "Image/road_background.png",
        "enemies": ["coffin_bread", "mango_ice"],
        "boss": "Boss1",  # 同樣的Boss
        "boss_time": 6000,  # 6秒後Boss出現
        "enemy_delay": (1000, 2000)  # 刷新頻率*0.5 (原本500-1000，現在1000-2000)
    }
}