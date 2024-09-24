FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libegl1 \
    libdbus-1-3 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb-cursor0 \
    libxcb-cursor-dev \
    libxcb-xinerama0 \
    ffmpeg \
    libxcb-keysyms1 \
    qt6-base-dev \
    libxcb-image0 \
    libxcb-shm0 \
    libxcb-icccm4 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libx11-dev \
    libxkbcommon-x11-dev \
    libx11-xcb1 \
    libgl1-mesa-dev \
    && apt-get clean

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p /logs

COPY . .

EXPOSE 8085

CMD ["python", "app/app.py"]