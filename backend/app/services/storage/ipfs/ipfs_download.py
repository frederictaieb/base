import requests
from app.config.settings import settings
from app.config.logging_config import setup_logging
import logging

IPFS_GATEWAY_URL = settings.IPFS_GATEWAY_URL
IPFS_TIMEOUT = settings.IPFS_TIMEOUT

setup_logging()
logger = logging.getLogger(__name__)

def download_file(cid, output_path):
    if not cid:
        raise ValueError("CID manquant")
    try:
        url = f"{IPFS_GATEWAY_URL.rstrip('/')}/ipfs/{cid}"
        logger.info(f"Downloading file from {url}")
        response = requests.get(url, timeout=int(IPFS_TIMEOUT))
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur IPFS (download) : {e}")