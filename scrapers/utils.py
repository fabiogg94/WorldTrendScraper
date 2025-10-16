import json
import os
from datetime import datetime
from typing import List, Dict, Any
import hashlib
from playwright.sync_api import sync_playwright

# Define the data directory relative to the scrapers package
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
SCREENSHOT_DIR = os.path.join(STATIC_DIR, 'screenshots')


def save_trends_data(filename: str, trends_list: List[Dict[str, Any]]):
    """
    Saves a list of trends to a JSON file with a standardized structure.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, filename)

    output_data = {
        "updated": datetime.now().isoformat(),
        "trends": trends_list
    }

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 爬取完成，總共找到 {len(trends_list)} 個趨勢")
        print(f"💾 已保存到: {output_path}")

    except Exception as e:
        print(f"❌ 寫入檔案 {output_path} 時發生錯誤: {e}")

def take_screenshot(url: str) -> str:
    """
    Takes a screenshot of a given URL if it doesn't already exist and returns the local path.
    The path returned is relative to the static folder for use in HTML templates.
    """
    if not url or not url.startswith('http'):
        return "" # Return empty if no valid URL is provided

    # Create a unique, stable filename from the URL
    filename = hashlib.md5(url.encode()).hexdigest() + '.png'
    screenshot_path = os.path.join(SCREENSHOT_DIR, filename)
    
    # This is the path that will be used in the HTML template (e.g., /static/screenshots/file.png)
    template_path = f"/static/screenshots/{filename}"

    if os.path.exists(screenshot_path):
        return template_path

    print(f"🚀 正在為 {url} 截圖...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                viewport={'width': 1280, 'height': 720},
                device_scale_factor=1,
            )
            # Navigate to the page, wait for it to be idle
            page.goto(url, wait_until='networkidle', timeout=20000)
            
            # A generic attempt to dismiss cookie banners or modals
            try:
                # Look for common cookie consent button texts
                buttons = page.locator(
                    'button:has-text("Accept"), button:has-text("Agree"), '
                    'button:has-text("Confirm"), button:has-text("OK"), '
                    'button:has-text("I understand"), button:has-text("Close")'
                )
                # Click the first visible one
                if buttons.count() > 0:
                    first_visible_button = buttons.first
                    if first_visible_button.is_visible(timeout=1000):
                        first_visible_button.click(timeout=1000)
                        # Wait a moment for any overlay to disappear
                        page.wait_for_timeout(500)
            except Exception:
                # If no button is found or it fails, just continue.
                pass

            # Take the screenshot of the viewport
            page.screenshot(path=screenshot_path, full_page=False)
            browser.close()
            print(f"✅ 截圖成功: {template_path}")
            return template_path
    except Exception as e:
        print(f"❌ 截圖失敗 {url}: {e}")
        # In case of failure, return an empty string.
        # The frontend will need to handle this gracefully.
        return ""