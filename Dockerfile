FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for weasyprint, fonts, PDF generation
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libglib2.0-dev \
    pango \
    freetype6 \
    fontconfig \
    pkg-config

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY models.py .
COPY database.py .
COPY schemas.py .
COPY frontend/index.html .

touch invoice_portal.db

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
