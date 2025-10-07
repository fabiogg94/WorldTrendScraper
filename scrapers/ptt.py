from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
from typing import List

from .schema import TrendItem
from .utils import save_trends_data

# PTT Web URL
PTT_URL = "https://www.pttweb.cc/hot/all/today"
BASE_URL = "https://www.pttweb.cc"
OUTPUT_FILENAME = "ptt-trends.json"

def fetch_ptt_trends():
    """使用 requests 和 BeautifulSoup 抓取 PTT Web 熱門文章並轉換為標準格式"""
    print("🚀 開始抓取 PTT Web 資料...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(PTT_URL, headers=headers, timeout=30)
        response.raise_for_status()

        print("✅ 網頁內容下載完成，開始解析...")
        soup = BeautifulSoup(response.text, 'lxml')

        article_links = soup.select('a[href*="/bbs/"]')
        
        trends: List[TrendItem] = []
        seen_links = set()

        for link_tag in article_links:
            container = link_tag.find_parent(class_="e7-container")
            if not container:
                continue

            relative_link = link_tag.get('href')
            if not relative_link or relative_link in seen_links:
                continue
            
            seen_links.add(relative_link)

            try:
                title = ''
                for span in link_tag.find_all('span'):
                    if span.get_text(strip=True):
                        title = span.get_text(strip=True)
                        break
                if not title:
                    title = link_tag.get_text(strip=True)

                if not title or not relative_link:
                    continue

                score_tag = container.find(class_="e7-recommendScore")
                score = score_tag.get_text(strip=True) if score_tag else '0'

                time_tag = container.find(string=re.compile(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}'))
                timestamp = None
                if time_tag:
                    try:
                        # 轉換時間格式為 ISO 8601
                        dt_object = datetime.strptime(time_tag.strip(), '%Y/%m/%d %H:%M')
                        timestamp = dt_object.isoformat()
                    except ValueError:
                        # 如果格式不對，保留原始字串
                        timestamp = time_tag.strip()

                image_tag = container.select_one('.e7-preview img')
                image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else None

                trend_item: TrendItem = {
                    "title": title,
                    "url": f"{BASE_URL}{relative_link}",
                    "score": score,
                    "image_url": image_url,
                    "timestamp": timestamp,
                }
                trends.append(trend_item)

            except Exception as e:
                print(f"⚠️ 解析文章時出錯: {relative_link} -> {e}")
                continue
        
        # 取前 20 筆
        final_trends = trends[:20]

        # 使用通用的儲存函式
        save_trends_data(OUTPUT_FILENAME, final_trends)

    except requests.RequestException as e:
        print(f"❌ 抓取 PTT 時發生網路錯誤: {e}")
    except Exception as e:
        print(f"❌ 處理 PTT 時發生未知錯誤: {e}")

    print("\n📊 PTT 抓取完成!")

if __name__ == '__main__':
    fetch_ptt_trends()