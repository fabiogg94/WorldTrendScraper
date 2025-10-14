# 1. Base Image: Use a slim Python image that matches your local environment
FROM python:3.10-slim

# 2. Environment Variables: For better logging and organization
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
WORKDIR $APP_HOME

# 3. Install uv: The project's package manager
# We install it system-wide in the image to make it available for the next steps.
RUN pip install uv

# 4. Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# 5. Install dependencies using uv
# This creates a .venv and installs packages from uv.lock.
# --no-cache is used to ensure we get fresh packages if needed.
RUN uv sync --no-cache

# 6. Copy the rest of the application code
COPY . .

# 7. Initial Data Fetch: Run the scraper script during the build
# We use 'python main.py' which is more direct and robust than '-m main' inside Docker.
# The 'uv run' command ensures it executes within the created virtual environment.
RUN uv run python main.py

# 8. Expose the port the app runs on
# The Procfile uses gunicorn, which needs a port to listen on.
# Zeabur will map this to the public port 80/443.
# We use 8000 as a common default for gunicorn.
EXPOSE 8000

# 9. Command to run the application
# This is taken from the Procfile. 'uv run' ensures it uses the venv.
CMD ["uv", "run", "gunicorn", "app:app", "--bind", "0.0.0.0:8000"]