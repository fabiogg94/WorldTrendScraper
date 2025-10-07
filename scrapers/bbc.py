
import feedparser
from datetime import datetime
from time import mktime
from typing import List

from .schema import TrendItem
from .utils import save_trends_data

# BBC 中文 RSS Feed URL
BBC_RSS_URL = "https://feeds.bbci.co.uk/zhongwen/trad/rss.xml"
OUTPUT_FILENAME = "bbc-trends.json"

def fetch_bbc_trends():
    """使用 feedparser 抓取 BBC RSS feed 並轉換為標準格式"""
    print("🚀 開始抓取 BBC Chinese RSS feed...")

    try:
        feed = feedparser.parse(BBC_RSS_URL)

        if feed.bozo:
            print(f"⚠️  警告: RSS feed 可能格式不正確。錯誤: {feed.bozo_exception}")

        print(f"📰 頻道標題: {feed.feed.get('title', 'N/A')}")

        trends: List[TrendItem] = []
        for entry in feed.entries:
            # 從 media_thumbnail 中提取縮圖 URL
            image_url = None
            if 'media_thumbnail' in entry and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get('url')

            # 將 published_parsed (time.struct_time) 轉換為 ISO 格式字串
            timestamp = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                timestamp = dt.isoformat()

            trend_item: TrendItem = {
                "title": entry.get('title', 'N/A'),
                "url": entry.get('link', ''),
                "score": None,
                "image_url": image_url,
                "timestamp": timestamp or entry.get('published'),
            }
            trends.append(trend_item)

        # 使用通用的儲存函式
        save_trends_data(OUTPUT_FILENAME, trends)

    except Exception as e:
        print(f"❌ 爬取 BBC RSS 時發生錯誤: {e}")

    print("\n📊 BBC 抓取完成!")

if __name__ == '__main__':
    fetch_bbc_trends()
