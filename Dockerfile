FROM python:3.9-slim

WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Installation de Playwright
RUN pip install playwright && playwright install

# Copie du code de l'application
COPY . .

# Crée le répertoire de sortie
RUN mkdir -p output

# Crée un fichier inputs.txt vide s'il n'existe pas
RUN touch inputs.txt

# Expose le port sur lequel l'API Flask s'exécute
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["python", "app.py"]
