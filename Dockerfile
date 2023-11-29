FROM python:3.8.12
RUN apt-get update && apt-get install -y \
    libasound-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8111", "--access-logfile", "logs/access.log", "--error-logfile", "logs/error.log", "app:app"]