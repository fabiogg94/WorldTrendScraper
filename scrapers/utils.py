
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Define the data directory relative to the scrapers package
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

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
