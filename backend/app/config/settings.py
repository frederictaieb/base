import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')

class Settings:
    XRP_SERVER_WALLET_ADDR = os.getenv("XRP_SERVER_WALLET_ADDR")
    XRP_TESTNET_ADDR_WS = os.getenv("XRP_TESTNET_ADDR_WS")
    IPFS_API_URL = os.getenv("IPFS_API_URL")
    IPFS_GATEWAY_URL = os.getenv("IPFS_GATEWAY_URL")
    TIMEOUT = os.getenv("TIMEOUT")
    IPFS_IP = os.getenv("IPFS_IP")
    IPFS_PORT = os.getenv("IPFS_PORT")

settings = Settings()