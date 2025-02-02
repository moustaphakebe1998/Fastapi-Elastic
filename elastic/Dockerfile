# Utilisez une image de base Python
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Configuration des proxies
ENV http_proxy=http://DMZ
ENV https_proxy=http://DMZ
ENV no_proxy=ressources.pa

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY ./requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copier le code de l'application
COPY ./app /app/app

# Exposer le port 80
EXPOSE 80

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# COPY ./app /app/app
# COPY ./cert /app/cert

# EXPOSE 8443

# Lancer l'application avec Uvicorns
