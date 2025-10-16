
import feedparser
from datetime import datetime
from time import mktime
from typing import List

from .schema import TrendItem
from .utils import save_trends_data, take_screenshot

def fetch_rss_trends(url: str, output_filename: str):
    """通用 RSS Feed 爬蟲，抓取指定 URL 並儲存至指定檔案"""
    print(f"🚀 開始抓取 RSS feed: {url}")
    trends: List[TrendItem] = []

    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            raise ValueError(f"RSS feed 格式不正確: {feed.bozo_exception}")
        
        if not feed.entries:
            print(f"⚠️ 警告: RSS feed 中沒有找到任何條目: {url}")
            save_trends_data(output_filename, trends)
            return

        print(f"📰 頻道: {feed.feed.get('title', 'N/A')} - 找到 {len(feed.entries)} 條新聞")

        for entry in feed.entries:
            timestamp = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                    timestamp = dt.isoformat()
                except (TypeError, ValueError):
                    print(f"⚠️ 警告: 無法解析時間戳: {entry.published_parsed}")
                    pass

            image_url = None
            if 'media_thumbnail' in entry and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get('url')

            trend_item: TrendItem = {
                "title": entry.get('title', '無標題'),
                "url": entry.get('link', ''),
                "score": None,
                "image_url": image_url, # Will be updated below if needed
                "timestamp": timestamp,
            }

            # If no image was found in the RSS feed, take a screenshot
            if not trend_item["image_url"]:
                trend_item["image_url"] = take_screenshot(trend_item["url"])
            
            trends.append(trend_item)

    except Exception as e:
        print(f"❌ 爬取 RSS ({url}) 時發生嚴重錯誤: {e}")
        save_trends_data(output_filename, [])
        raise

    save_trends_data(output_filename, trends)
    print(f"✅ 成功抓取並儲存 {len(trends)} 筆趨勢資料到 {output_filename}。")
