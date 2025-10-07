import os
import json
from flask import Flask, render_template, request
from math import ceil

import subprocess

# 從中央設定檔導入所有資料來源設定
from config import SOURCES

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DATA_CACHE = {}

def install_playwright_browsers():
    """在應用程式啟動時，檢查並安裝 Playwright 瀏覽器"""
    print("🔧 正在檢查 Playwright 瀏覽器...")
    try:
        # 使用 subprocess 從程式內部執行指令，更穩健
        # capture_output=True 可以捕獲輸出，方便偵錯
        result = subprocess.run(
            ["uv", "run", "playwright", "install"],
            capture_output=True,
            text=True,
            check=True  # 如果指令失敗 (exit code 非 0)，會引發 CalledProcessError
        )
        print("✅ Playwright 瀏覽器已是最新狀態。")
        print(result.stdout)
    except FileNotFoundError:
        print("❌ 錯誤: 'uv' 指令不存在。請確保 uv 已安裝在環境中。")
        raise
    except subprocess.CalledProcessError as e:
        # 如果 playwright install 指令本身出錯
        print(f"❌ Playwright 瀏覽器安裝失敗，錯誤碼: {e.returncode}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        raise
    except Exception as e:
        print(f"❌ 發生未知錯誤: {e}")
        raise

class Pagination:
    """一個簡單的分頁物件"""
    def __init__(self, page, per_page, total_count, items):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.items = items

    @property
    def pages(self):
        return ceil(self.total_count / self.per_page)

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

def load_data_into_cache():
    """在應用程式啟動時讀取所有 JSON 檔案並存入記憶體快取"""
    print("🔄 正在載入資料到快取中...")
    for source in SOURCES:
        filename = source['filename']
        try:
            with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
                DATA_CACHE[source['id']] = json.load(f)
                print(f"  ✅ 已載入: {filename}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            DATA_CACHE[source['id']] = None # 即使檔案不存在或損毀也留個紀錄
            print(f"  ❌ 載入失敗: {filename} ({e})")
    print("✨ 快取載入完成!")

def paginate_from_cache(raw_data, slug):
    """從已載入的資料中進行分頁"""
    if not raw_data:
        return None

    all_items = raw_data.get('trends', [])

    per_page = request.args.get('per_page', 10, type=int)
    page_param = f"{slug}_page"
    page = request.args.get(page_param, 1, type=int)
    
    total_count = len(all_items)
    start = (page - 1) * per_page
    end = start + per_page
    items_on_page = all_items[start:end]

    pagination = Pagination(page, per_page, total_count, items_on_page)
    return pagination


@app.route('/')
def index():
    """主頁，從快取讀取所有資料並渲染模板"""
    all_data = []
    for source in SOURCES:
        raw_data = DATA_CACHE.get(source['id'])
        pagination = paginate_from_cache(raw_data, source['id'])
        
        if raw_data and pagination:
            all_data.append({
                "name": source['name'],
                "slug": source['id'],
                "icon": source['icon'],
                "updated": raw_data.get('updated', '1970-01-01'),
                "pagination": pagination
            })
    
    # 根據更新時間對來源進行排序，最新的在前
    sorted_data = sorted(all_data, key=lambda item: item['updated'], reverse=True)
    
    # 獲取全域 per_page 設定
    per_page_options = [5, 10, 20, 30, 50]
    current_per_page = request.args.get('per_page', 10, type=int)

    return render_template(
        'index.html', 
        sorted_data=sorted_data, 
        sources=sorted_data, # 側邊欄使用
        per_page_options=per_page_options,
        current_per_page=current_per_page,
        args=request.args # 用於構建分頁連結
    )

# 應用程式啟動時，依序執行準備工作
install_playwright_browsers()
load_data_into_cache()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)