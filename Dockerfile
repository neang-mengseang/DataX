FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for Playwright
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip git \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libasound2 libxtst6 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libgtk-3-0 libnspr4 libdbus-1-3 \
    libatspi2.0-0 libx11-6 libxext6 libxfixes3 libxcb1 libxkbcommon0 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install

# Copy the full app source
COPY . .

# Expose port for Railway or other cloud hosting
EXPOSE 8080

# Run the Flask app via Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.app:app"]
