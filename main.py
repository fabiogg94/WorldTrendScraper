import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 從中央設定檔導入不重複的爬蟲任務列表
from config import UNIQUE_SCRAPERS

def main():
    """並行執行所有爬蟲任務"""
    start_time = time.time()
    print(f"🚀 開始執行 {len(UNIQUE_SCRAPERS)} 個爬蟲任務...")

    # 使用 ThreadPoolExecutor 來並行處理 I/O 密集的網路請求
    with ThreadPoolExecutor(max_workers=len(UNIQUE_SCRAPERS)) as executor:
        # 提交所有任務
        future_to_scraper = {executor.submit(scraper["func"]): scraper for scraper in UNIQUE_SCRAPERS}
        
        results = {}
        for future in as_completed(future_to_scraper):
            scraper_name = future_to_scraper[future]["name"]
            try:
                # 獲取任務結果 (雖然我們的函式沒有返回值，但這可以觸發異常)
                future.result()
                results[scraper_name] = "✅ 成功"
            except Exception as exc:
                results[scraper_name] = f"❌ 失敗: {exc}"

    print('\n' + '-'*30)
    print('🏁 所有任務執行完畢！')
    
    for name, result in results.items():
        print(f"- {name}: {result}")

    end_time = time.time()
    print(f"\n總耗時: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main()