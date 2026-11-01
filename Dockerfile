# Image de départ : Python 3.12, version légère
FROM python:3.12-slim

# Dossier de travail de l'application dans le conteneur
WORKDIR /app

# Installer d'abord les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Puis copier le code de l'application
COPY app.py auth.py ./

# Faire tourner l'application avec un utilisateur sans droits d'administrateur
RUN useradd --create-home appuser \
    && chown -R appuser /app
USER appuser

# Port de l'application et commande de démarrage (serveur de production)
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
