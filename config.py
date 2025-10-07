
from scrapers.bbc import fetch_bbc_trends
from scrapers.google import fetch_google_trends
from scrapers.ptt import fetch_ptt_trends
from scrapers.reddit import fetch_reddit_trends

# 單一事實來源 (Single Source of Truth)
# 所有爬蟲和網站的設定都從這裡讀取
SOURCES = [
    {
        "id": "google",
        "name": "Google Trends",
        "fetch_func": fetch_google_trends,
        "filename": "google-trends.json",
        "icon": "bi-google",
    },
    {
        "id": "ptt",
        "name": "PTT 熱門文章",
        "fetch_func": fetch_ptt_trends,
        "filename": "ptt-trends.json",
        "icon": "bi-chat-square-text-fill",
    },
    {
        "id": "reddit_all",
        "name": "Reddit 全站熱門",
        # Reddit 爬蟲會處理多個來源，但我們只需要一個代表性的函式
        "fetch_func": fetch_reddit_trends, 
        "filename": "reddit-all-hot.json",
        "icon": "bi-reddit",
    },
    {
        "id": "reddit_tw",
        "name": "Reddit 台灣社群",
        "fetch_func": fetch_reddit_trends,
        "filename": "reddit-taiwanese-hot.json",
        "icon": "bi-reddit",
    },
    {
        "id": "reddit_cn",
        "name": "Reddit 華語社群",
        "fetch_func": fetch_reddit_trends,
        "filename": "reddit-china-irl-hot.json",
        "icon": "bi-reddit",
    },
    {
        "id": "bbc",
        "name": "BBC 中文",
        "fetch_func": fetch_bbc_trends,
        "filename": "bbc-trends.json",
        "icon": "bi-globe2",
    },
]

# 為了 main.py 執行方便，建立一個不重複的爬蟲函式列表
# 注意：fetch_reddit_trends 只需執行一次
UNIQUE_SCRAPERS = [
    {"name": "Google", "func": fetch_google_trends},
    {"name": "PTT", "func": fetch_ptt_trends},
    {"name": "Reddit", "func": fetch_reddit_trends}, # 執行一次即可處理所有 Reddit 來源
    {"name": "BBC", "func": fetch_bbc_trends},
]
