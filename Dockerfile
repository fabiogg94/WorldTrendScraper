# 1. Base Image: Use a slim Python image that matches your local environment
FROM python:3.10-slim

# 2. Environment Variables: For better logging and organization
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
WORKDIR $APP_HOME

# 3. Install uv: The project's package manager
RUN pip install uv

# 4. Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# 5. Install dependencies using uv
RUN uv sync --no-cache

# 6. Copy the rest of the application code
COPY . .

# 7. REMOVED: Do not run scraper during build, as it will be hidden by the volume.
# RUN uv run python main.py

# 8. Expose the port the app runs on
EXPOSE 8000

# 9. Command to run the application
# On start, first run the scraper to populate the volume, 
# then start the web server. The worker service will handle subsequent updates.
CMD ["sh", "-c", "uv run python main.py && uv run gunicorn app:app --bind 0.0.0.0:8000"]
