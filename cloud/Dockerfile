FROM python:3.10-slim

WORKDIR /app

COPY cloud_requirements.txt .

RUN pip install --no-cache-dir -r cloud_requirements.txt

COPY server.py gemini_handler.py eleven_labs_handler.py .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
