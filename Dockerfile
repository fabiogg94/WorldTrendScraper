# 1. 基底映像：選擇一個輕量的 Python 映像
FROM python:3.11-slim

# 2. 設定工作目錄
WORKDIR /app

# 3. 安裝 uv
# 我們先安裝 uv，以便後續用它來管理 Python 套件
RUN pip install uv

# 4. 複製依賴相關檔案
# 這樣可以利用 Docker 的層快取機制，如果依賴沒變，就不用重新安裝
COPY pyproject.toml uv.lock .python-version* ./

# 5. 安裝依賴
# 使用 uv sync 來根據 lock 檔案安裝精確版本的依賴
RUN uv pip install . --system

# 6. 安裝 Playwright 瀏覽器核心 (這是關鍵修復)
# 使用 python -m playwright 來確保指令能被找到
# --with-deps 會一併安裝作業系統所需的依賴
RUN python -m playwright install --with-deps

# 7. 複製所有剩餘的應用程式碼
COPY . .

# 8. Zeabur 會自動使用 Procfile 中的指令，所以 CMD 不是必須的
# 但如果需要，可以取消註解以下這行
# CMD ["gunicorn", "app:app"]
