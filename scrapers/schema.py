from typing import TypedDict, Optional

class TrendItem(TypedDict):
    """
    統一的趨勢項目資料結構。
    所有爬蟲都應將其結果轉換為此格式的列表。
    """
    title: str          # 標題
    url: str            # 原始連結
    score: Optional[str]   # 熱度/分數/推文數
    image_url: Optional[str] # 縮圖 URL
    timestamp: Optional[str] # 發布時間 (ISO 格式)
