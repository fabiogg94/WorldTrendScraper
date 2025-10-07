
from functools import partial
from scrapers.bbc import fetch_rss_trends
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
    # --- BBC 多來源設定 ---
    {
        "id": "bbc-trad",
        "name": "BBC 中文 (繁)",
        "fetch_func": partial(fetch_rss_trends, url="https://feeds.bbci.co.uk/zhongwen/trad/rss.xml", output_filename="bbc-trad-trends.json"),
        "filename": "bbc-trad-trends.json",
        "icon": "bi-globe2",
    },
    {
        "id": "bbc-jp",
        "name": "BBC 日本語",
        "fetch_func": partial(fetch_rss_trends, url="https://feeds.bbci.co.uk/japanese/rss.xml", output_filename="bbc-jp-trends.json"),
        "filename": "bbc-jp-trends.json",
        "icon": "bi-globe-asia-australia",
    },
    {
        "id": "bbc-news",
        "name": "BBC News (World)",
        "fetch_func": partial(fetch_rss_trends, url="http://feeds.bbci.co.uk/news/world/rss.xml", output_filename="bbc-news-trends.json"),
        "filename": "bbc-news-trends.json",
        "icon": "bi-globe-americas",
    },
    {
        "id": "bbc-ent",
        "name": "BBC Entertainment",
        "fetch_func": partial(fetch_rss_trends, url="http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml", output_filename="bbc-ent-trends.json"),
        "filename": "bbc-ent-trends.json",
        "icon": "bi-film",
    },
]

# 為了 main.py 執行方便，建立一個不重複的爬蟲函式列表
# 注意：每個 partial 物件都是獨立的，所以我們需要一個代表性的函式
def run_all_bbc_trends():
    """一個輔助函式，用於執行所有 BBC 相關的爬取任務"""
    for source in SOURCES:
        if source['id'].startswith('bbc-'):
            source['fetch_func']()

UNIQUE_SCRAPERS = [
    {"name": "Google", "func": fetch_google_trends},
    {"name": "PTT", "func": fetch_ptt_trends},
    {"name": "Reddit", "func": fetch_reddit_trends}, # 執行一次即可處理所有 Reddit 來源
    {"name": "BBC", "func": run_all_bbc_trends}, # 執行一次即可處理所有 BBC 來源
]
