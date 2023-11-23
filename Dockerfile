# Utilisez une image de base avec Python préinstallé
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /SEB
WORKDIR /SEB

RUN pip install --upgrade sip

# Installez les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    libpython3-dev \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    python3-pyqt6 \
    libqt6widgets5 \
    # Ajoutez d'autres dépendances système nécessaires
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y xvfb

ENV DISPLAY=:99
COPY requirements.txt /SEB

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /SEB

# Exécutez votre script Python
CMD ["python", "main.py"]
