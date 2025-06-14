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


setup_logging()
logger = logging.getLogger(__name__)

SERVER_ADDRESS = settings.XRP_SERVER_WALLET_ADDR
XRP_WS_URI = settings.XRP_TESTNET_ADDR_WS

async def xrp_listener():
    from app.api.routes import add_marker 
    from app.models.markers import Location

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

                    if parsed_memos.get("json_hash"):
                        json_hash = parsed_memos.get("json_hash")
                        heatmap_hash = parsed_memos.get("heatmap_hash")
                        wisdom_0_hash = parsed_memos.get("wisdom_0_hash")
                        wisdom_1_hash = parsed_memos.get("wisdom_1_hash")
                        wisdom_2_hash = parsed_memos.get("wisdom_2_hash")

                        id = str(uuid.uuid4())
                        temp_dir = tempfile.mkdtemp(prefix=id)
                        json_path = os.path.join(temp_dir, "json_hash.json")
                        heatmap_path = os.path.join(temp_dir, "heatmap_hash.png")
                        wisdom_0_path = os.path.join(temp_dir, "wisdom_0_hash.mp3")
                        wisdom_1_path = os.path.join(temp_dir, "wisdom_1_hash.mp3")
                        wisdom_2_path = os.path.join(temp_dir, "wisdom_2_hash.mp3")
                        
                        download_file(json_hash,  json_path)
                        logger.info(f"Downloaded json file to {json_path}")
                        download_file(heatmap_hash, heatmap_path)
                        logger.info(f"Downloaded heatmap file to {heatmap_path}")
                        download_file(wisdom_0_hash, wisdom_0_path)
                        logger.info(f"Downloaded wisdom_0 file to {wisdom_0_path}")
                        download_file(wisdom_1_hash, wisdom_1_path)
                        logger.info(f"Downloaded wisdom_1 file to {wisdom_1_path}")
                        download_file(wisdom_2_hash, wisdom_2_path)
                        logger.info(f"Downloaded wisdom_2 file to {wisdom_2_path}")

                        with open(json_path, "r") as f:
                            json_data = json.load(f)
                        logger.info(f"JSON data: {json_data}")

                        #with open(heatmap_path, "r") as f:
                        #    heatmap_data = json.load(f)
                        #logger.info(f"Heatmap data: {heatmap_data}")

                        location = json_data.get("location")
                        logger.info(f"Location: {location}")

                    await add_marker(Marker(
                        location=location,
                    ))
                    shutil.rmtree(temp_dir)
    except Exception as e:
        logger.error(f"❌ Error in XRP Listener : {e}")