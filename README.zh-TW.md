[English](./README.md)

# 核心爬蟲與趨勢檢視器

---

一個基於 Python 的網路應用程式，它從多個線上來源（Google 趨勢、BBC 新聞、Reddit、PTT）抓取熱門話題，並在一個統一、乾淨的網路介面中顯示它們。

![image](home_zh.png)

## ✨ 功能特性

- **多來源爬取**: 從 Google 趨勢、BBC 新聞、Reddit 和 PTT 收集資料。
- **統一資料管道**: 所有爬取的資料都被標準化為一致的 `TrendItem` 結構，便於處理。
- **Flask 網頁介面**: 使用輕量級的 Flask 網頁伺服器來呈現資料。
- **現代化且響應式的 UI**: 前端使用 Bootstrap 建構，確保在桌面和行動裝置上都有乾淨的視覺效果。
- **通用卡片佈局**: 所有趨勢項目都使用單一、一致的卡片元件顯示，提供統一的使用者體驗。
- **可設定的架構**: 透過編輯中央 `config.py` 檔案，可以輕鬆新增或移除資料來源。

## 🛠️ 技術棧

- **後端**: Python, Flask
- **爬蟲**: Playwright, Requests, Feedparser, BeautifulSoup
- **前端**: HTML, CSS, Bootstrap, Jinja2
- **包管理**: `uv`

## 🚀 開始使用

請按照以下說明在您的本機電腦上取得並執行專案的副本。

### 先決條件

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (一個快速的 Python 包安裝與解析器)

### 安裝

1.  **克隆儲存庫:**
    ```sh
    git clone https://github.com/LayorX/core-scraper.git
    cd core-scraper
    ```

2.  **建立虛擬環境:**
    ```sh
    uv venv
    ```
    *之後您可能需要啟動它，例如在 Windows 上執行 `.venv\Scripts\activate`。*

3.  **安裝依賴:**
    ```sh
    uv pip sync pyproject.toml
    ```

4.  **安裝 Playwright 瀏覽器二進位檔案:**
    (這是 Google 趨勢爬蟲所必需的)
    ```sh
    uv run playwright install
    ```

## 🏃 如何使用

1.  **爬取資料**

    要執行 `config.py` 中定義的所有爬蟲並更新 `/data` 目錄中的 JSON 檔案，請執行：
    ```sh
    uv run -m main
    ```

2.  **執行網頁應用程式**

    執行批次腳本以啟動 Flask 伺服器：
    ```sh
    .\run-website.bat
    ```
    應用程式將在 `http://127.0.0.1:5000` 上可用。

## 📁 專案結構

```
core-scraper/
├── .venv/                  # 虛擬環境
├── data/                   # 儲存爬取資料的 JSON 檔案
├── scrapers/               # 各來源的獨立爬蟲模組
│   ├── __init__.py
│   ├── schema.py           # 定義統一的 TrendItem 資料結構
│   └── ...                 # bbc.py, google.py, etc.
├── static/                 # 靜態資源 (CSS, JS, 圖片)
├── templates/              # Jinja2 HTML 模板
│   ├── index.html          # 包含通用卡片的主頁面模板
│   └── layout.html         # 基礎佈局
├── .gitignore
├── app.py                  # 主要的 Flask 應用程式檔案
├── config.py               # 資料來源的中央設定檔
├── main.py                 # 觸發所有爬蟲的主腳本
├── pyproject.toml          # 專案元資料與依賴
├── README.md               # 英文版說明
├── README.zh-TW.md         # 本檔案
└── run-website.bat         # 執行網頁伺服器的腳本
```
