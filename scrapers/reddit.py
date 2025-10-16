import requests
from datetime import datetime
from typing import List

from .schema import TrendItem
from .utils import save_trends_data, take_screenshot

# 設定要抓取的 Reddit URL 列表
REDDIT_URLS = [
    {
        "url": "https://www.reddit.com/r/all/hot.json?limit=25",
        "filename": "reddit-all-hot.json",
        "description": "Reddit r/all 熱門文章",
    },
    {
        "url": "https://www.reddit.com/r/Taiwanese/hot.json?limit=25",
        "filename": "reddit-taiwanese-hot.json",
        "description": "Reddit r/Taiwanese 熱門文章",
    },
    {
        "url": "https://www.reddit.com/r/China_irl/hot.json?limit=25",
        "filename": "reddit-china-irl-hot.json",
        "description": "Reddit r/China_irl 熱門文章",
    },
]

BASE_URL = "https://www.reddit.com"

def fetch_reddit_trends():
    """使用 requests 抓取 Reddit JSON API 並轉換為標準格式"""
    print("🚀 開始抓取 Reddit JSON 資料...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for source in REDDIT_URLS:
        url = source["url"]
        filename = source["filename"]
        description = source["description"]

        try:
            print(f"\n--- 處理: {description} ---")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            raw_data = response.json()
            posts = raw_data.get('data', {}).get('children', [])
            
            trends: List[TrendItem] = []
            for post in posts:
                post_data = post.get('data', {})
                if not post_data:
                    continue

                # 處理縮圖，如果不是有效的 http 連結則設為 None
                thumbnail = post_data.get('thumbnail')
                image_url = thumbnail if thumbnail and thumbnail.startswith('http') else None

                # 將 UTC 時間戳轉換為 ISO 格式
                timestamp = None
                if post_data.get('created_utc'):
                    timestamp = datetime.fromtimestamp(post_data['created_utc']).isoformat()

                trend_item: TrendItem = {
                    "title": post_data.get('title', 'N/A'),
                    "url": f"{BASE_URL}{post_data.get('permalink', '')}",
                    "score": str(post_data.get('score', 0)),
                    "image_url": image_url, # Will be updated below if needed
                    "timestamp": timestamp,
                }

                # If no image was found, take a screenshot
                if not trend_item["image_url"]:
                    trend_item["image_url"] = take_screenshot(trend_item["url"])
                
                trends.append(trend_item)

            # 使用通用的儲存函式
            save_trends_data(filename, trends)

        except requests.RequestException as e:
            print(f"❌ 處理 {description} 時發生網路錯誤: {e}")
        except Exception as e:
            print(f"❌ 處理 {description} 時發生未知錯誤: {e}")

    print("\n📊 Reddit 抓取完成!")

if __name__ == '__main__':
    fetch_reddit_trends()

