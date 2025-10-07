# Core Scraper & Trend Viewer

---

A Python-based web application that scrapes trending topics from various online sources (Google Trends, BBC News, Reddit, PTT) and displays them in a unified, clean web interface.

![image](https://github.com/LayorX/core-scraper/assets/16933433/2613450a-0b69-409c-a0b9-91722053b83c)

## ✨ Features

- **Multi-Source Scraping**: Gathers data from Google Trends, BBC News, Reddit, and PTT.
- **Unified Data Pipeline**: All scraped data is standardized into a consistent `TrendItem` schema for easy processing.
- **Flask Web Interface**: A lightweight web server built with Flask to present the data.
- **Modern & Responsive UI**: The frontend is built with Bootstrap, ensuring a clean look on both desktop and mobile.
- **Universal Card Layout**: All trend items are displayed using a single, consistent card component for a unified user experience.
- **Configurable Architecture**: Easily add or remove data sources by editing the central `config.py` file.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Scraping**: Playwright, Requests, Feedparser, BeautifulSoup
- **Frontend**: HTML, CSS, Bootstrap, Jinja2
- **Package Management**: `uv`

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (A fast Python package installer and resolver)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/LayorX/core-scraper.git
    cd core-scraper
    ```

2.  **Create a virtual environment:**
    ```sh
    uv venv
    ```
    *You may need to activate it afterwards, e.g., `.venv\Scripts\activate` on Windows.*

3.  **Install dependencies:**
    ```sh
    uv pip sync pyproject.toml
    ```

4.  **Install Playwright browser binaries:**
    (This is required for the Google Trends scraper)
    ```sh
    uv run playwright install
    ```

## 🏃 Usage

1.  **Scrape Data**

    To run all scrapers defined in `config.py` and update the JSON files in the `/data` directory, execute:
    ```sh
    uv run -m main
    ```

2.  **Run the Web Application**

    Execute the batch script to start the Flask server:
    ```sh
    .\run-website.bat
    ```
    The application will be available at `http://127.0.0.1:5000`.

## 📁 Project Structure

```
core-scraper/
├── .venv/                  # Virtual environment
├── data/                   # Stores scraped data in JSON format
├── scrapers/               # Individual scraper modules for each source
│   ├── __init__.py
│   ├── schema.py           # Defines the unified TrendItem data structure
│   └── ...                 # bbc.py, google.py, etc.
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # Jinja2 HTML templates
│   ├── index.html          # Main page template with universal card
│   └── layout.html         # Base layout
├── .gitignore
├── app.py                  # Main Flask application file
├── config.py               # Central configuration for data sources
├── main.py                 # Main script to trigger all scrapers
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
└── run-website.bat         # Script to run the web server
```
