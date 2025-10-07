from playwright.sync_api import sync_playwright
import random
import time
from typing import List
from urllib.parse import quote_plus

from .schema import TrendItem
from .utils import save_trends_data

# Google Trends URL
GOOGLE_TRENDS_URL = "https://trends.google.com.tw/trending?geo=TW&hours=4"
OUTPUT_FILENAME = "google-trends.json"

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:124.0) Gecko/20100101 Firefox/124.0',
]

def fetch_google_trends():
    """使用 Playwright 抓取 Google Trends，參考有效的 TS 腳本邏輯"""
    print("開始使用 Playwright (新策略) 抓取 Google Trends 資料...")

    with sync_playwright() as p:
        browser = None
        try:
            random_user_agent = random.choice(USER_AGENTS)
            print(f"使用 User-Agent: {random_user_agent}")

            browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            context = browser.new_context(user_agent=random_user_agent)
            page = context.new_page()

            # 隨機延遲 3~13 秒
            random_delay = random.randint(3000, 13000)
            print(f"隨機延遲 {random_delay / 1000:.2f} 秒...")
            time.sleep(random_delay / 1000)

            print(f"正在導航至: {GOOGLE_TRENDS_URL}")
            page.goto(GOOGLE_TRENDS_URL, wait_until="domcontentloaded", timeout=30000)

            # 再次隨機延遲
            post_load_delay = random.randint(3000, 8000)
            print(f"頁面載入後額外延遲 {post_load_delay / 1000:.2f} 秒...")
            time.sleep(post_load_delay / 1000)

            try:
                print("等待表格元素 'td' 載入...")
                page.wait_for_selector('td', timeout=10000)
                print("表格元素已載入。")
            except Exception:
                print("等待元素載入超時，可能頁面沒有資料或結構已更改。")

            # 移植自成功的 TS 腳本的 page.evaluate 邏輯
            raw_trends = page.evaluate('''
                () => {
                    const allRows = Array.from(document.querySelectorAll('tbody tr'));
                    const dataRows = allRows.filter((row) => {
                        const cells = row.querySelectorAll('td');
                        return cells.length > 3;
                    });

                    const tableData = dataRows.map((row) => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        const trendCell = cells[1];
                        const countCell = cells[2];

                        if (trendCell && countCell) {
                            const trendDivs = Array.from(trendCell.querySelectorAll('div'));
                            let trendText = '';
                            for (const div of trendDivs) {
                                const text = div.textContent?.trim() || '';
                                if (text && !text.includes('次搜尋') && !text.includes('活躍') && !text.includes('持續時間') && !text.includes('·')) {
                                    trendText = text;
                                    break;
                                }
                            }

                            const countCellText = countCell.textContent?.trim() || '';
                            const countMatches = countCellText.match(/(\d+[\d,]*\+)/g) || [];
                            const searchCount = countMatches.find((match) => match.match(/^\d+[\d,]*\+$/)) || '';

                            if (trendText && searchCount) {
                                return {
                                    googleTrend: trendText,
                                    searchVolume: searchCount,
                                };
                            }
                        }
                        return null;
                    }).filter((row) => row !== null);

                    return tableData;
                }
            ''')

            trends: List[TrendItem] = []
            for item in raw_trends:
                title = item.get('googleTrend')
                if not title:
                    continue
                
                trend_item: TrendItem = {
                    "title": title,
                    "url": f"https://www.google.com/search?q={quote_plus(title)}",
                    "score": item.get('searchVolume'),
                    "image_url": None,
                    "timestamp": None,
                }
                trends.append(trend_item)

            if not trends:
                print("警告: 未能從頁面解析出任何趨勢資料。")

            save_trends_data(OUTPUT_FILENAME, trends)
            print(f"成功抓取並儲存 {len(trends)} 筆 Google 趨勢資料。")

        except Exception as e:
            print(f"處理 Google Trends 時發生錯誤: {e}")
            save_trends_data(OUTPUT_FILENAME, []) # 錯誤發生時儲存空列表
            raise
        finally:
            if browser:
                browser.close()

if __name__ == '__main__':
    fetch_google_trends()
