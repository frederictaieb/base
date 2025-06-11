import os
import requests
from app.config.settings import settings
import ipfshttpclient

IPFS_API_URL = settings.IPFS_API_URL
IPFS_GATEWAY_URL = settings.IPFS_GATEWAY_URL
TIMEOUT = settings.TIMEOUT
IPFS_IP = settings.IPFS_IP
IPFS_PORT = settings.IPFS_PORT

def upload_directory(directory_path):
    client = ipfshttpclient.connect(f"/ip4/{IPFS_IP}/tcp/{IPFS_PORT}/http")
    res = client.add(directory_path, recursive=True)
    root = res[-1]
    return root["Hash"]


def upload_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(
                f"{IPFS_API_URL}/api/v0/add",
                files={'file': file},
                timeout=int(TIMEOUT)
            )
        response.raise_for_status()
        data = response.json()
        return data['Hash']
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur IPFS (upload) : {e}")


def download_file(cid, output_path):
    if not cid:
        raise ValueError("CID manquant")
    try:
        url = f"{IPFS_GATEWAY_URL.rstrip('/')}/{cid}"
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur IPFS (download) : {e}")
