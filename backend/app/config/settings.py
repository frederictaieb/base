import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')

class Settings:
    XRP_SERVER_WALLET_ADDR = os.getenv("XRP_SERVER_WALLET_ADDR")
    XRP_TESTNET_ADDR_WS = os.getenv("XRP_TESTNET_ADDR_WS")

settings = Settings()