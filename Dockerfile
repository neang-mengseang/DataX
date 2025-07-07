# Base Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 \
    libgtk-3-0 libxss1 libasound2 libxshmfence1 libgbm-dev libx11-xcb1 \
    libxcb1 libxcomposite1 libxdamage1 libxrandr2 libpangocairo-1.0-0 \
    libpangoft2-1.0-0 libatk1.0-0 libcups2 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirement files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browsers
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps

# Copy all source code
COPY . .

# Expose port (Railway uses PORT env var)
ENV PORT=5000
EXPOSE $PORT

# Set the default command
CMD ["python", "src/app.py"]
