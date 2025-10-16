import time
import schedule
from datetime import datetime
from main import main as run_scrapers

def scheduled_scraper_job():
    """定時執行的爬蟲任務"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🕐 [{current_time}] 開始執行定時爬蟲任務...")
    
    try:
        run_scrapers()
        print(f"✅ [{current_time}] 爬蟲任務執行完成")
    except Exception as e:
        print(f"❌ [{current_time}] 爬蟲任務執行失敗: {e}")

def main():
    """Worker服務主程式"""
    print("🚀 World Trend Scraper Worker 服務啟動")
    print("⏰ 設定每小時執行一次爬蟲任務")
    
    # 設定每小時執行一次
    schedule.every().hour.do(scheduled_scraper_job)
    
    # 啟動時立即執行一次
    print("🔄 啟動時執行初始爬蟲任務...")
    scheduled_scraper_job()
    
    # 持續運行排程
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分鐘檢查一次

if __name__ == "__main__":
    main()
