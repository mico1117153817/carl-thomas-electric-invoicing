FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for weasyprint, fonts, and PDF generation
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libglib2.0-dev \
    libpangoftt-1.0-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    fontconfig-config

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY models.py .  
COPY database.py .
COPY schemas.py .
COPY frontend/index.html .

# Create database file in container
RUN touch invoice_portal.db

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
