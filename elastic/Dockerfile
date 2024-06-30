# Utilisez une image de base Python
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Configuration des proxies
ENV http_proxy=http://DMZ-PXSERVER.APPS.PARIS.MDP:8080/
ENV https_proxy=http://DMZ-PXSERVER.APPS.PARIS.MDP:8080/
ENV no_proxy=ressources.paris.mdp,cmp.paris.mdp

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