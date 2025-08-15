FROM python:3.11-slim
LABEL authors="nkhimin"

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full app
COPY . .

EXPOSE 8501

# Run Streamlit app directly
CMD ["streamlit", "run", "src/app.py"]