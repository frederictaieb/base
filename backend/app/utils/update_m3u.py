import os
import uuid
import tempfile
import shutil
import websockets
import json
import logging
from app.config.settings import settings
from app.config.logging_config import setup_logging
from app.models.markers import Marker
from app.utils.utils import parse_memo
from app.services.storage.ipfs.ipfs_download import download_file
import asyncio

setup_logging()
logger = logging.getLogger(__name__)

SERVER_ADDRESS = settings.XRP_SERVER_WALLET_ADDR
XRP_WS_URI = settings.XRP_TESTNET_ADDR_WS
IPFS_GATEWAY_URL = settings.IPFS_GATEWAY_URL

ipfs_gateway_root = IPFS_GATEWAY_URL.rstrip('/') + "/ipfs/"
logger.info(f"IPFS Gateway Root: {ipfs_gateway_root}")

async def xrp_wisdom_listener():
    if not SERVER_ADDRESS or not XRP_WS_URI:
        logger.error("❌ SERVER_ADDRESS ou XRP_WS_URI missing in .env")
        return

    try:
        async with websockets.connect(XRP_WS_URI) as websocket:
            subscribe_message = {
                "id": 1,
                "command": "subscribe",
                "accounts": [SERVER_ADDRESS]
            }
            await websocket.send(json.dumps(subscribe_message))
            logger.info(f"🛜 Listening to xrp transactions from {SERVER_ADDRESS}")

            while True:
                message = await websocket.recv()
                data = json.loads(message)

                if data.get("type") == "transaction":
                    tx_hash = data.get("transaction", {}).get("hash")
                    logger.info(f"✅ Transaction detected: {tx_hash[:21]}[...]")

                    parsed_memos = parse_memo(data["transaction"]["Memos"])
                    logger.info(f"📝 Parsed memo: {parsed_memos}")

                    with open("wisdom_hashes.txt", "a") as f:
                        for i in range(3):
                            key = f"wisdom_{i}_hash"
                            if parsed_memos.get(key):
                                hash_value = parsed_memos[key]
                                ipfs_cid = f"{ipfs_gateway_root}{hash_value}"
                                logger.info(f"*** WISDOM {i} IPFS_CID: {ipfs_cid} ***")
                                f.write(f"{ipfs_cid}\n")


    except Exception as e:
        logger.error(f"❌ Error in XRP Listener : {e}")

async def main():
    await xrp_wisdom_listener()

if __name__ == "__main__":
    asyncio.run(main())