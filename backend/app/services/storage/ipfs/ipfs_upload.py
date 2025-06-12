import os
import requests
from app.config.settings import settings

IPFS_API_URL = settings.IPFS_API_URL
IPFS_TIMEOUT = settings.IPFS_TIMEOUT

def upload_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(
                f"{IPFS_API_URL}/api/v0/add",
                files={'file': file},
                timeout=int(IPFS_TIMEOUT)
            )
        response.raise_for_status()
        data = response.json()
        return data['Hash']
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur IPFS (upload) : {e}")