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
from dotenv import load_dotenv
from xrpl.wallet import Wallet
from xrpl.constants import CryptoAlgorithm
from xrpl.clients import WebsocketClient
from xrpl.models.transactions import Payment, Memo
from xrpl.utils import xrp_to_drops
from xrpl.transaction import autofill_and_sign
from xrpl.transaction import submit_and_wait

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

                        id = str(uuid.uuid4())
                        temp_dir = tempfile.mkdtemp(prefix=id)
                        json_path = os.path.join(temp_dir, "json_hash.json")
                        heatmap_path = os.path.join(temp_dir, "heatmap_hash.png")
                        
                        download_file(json_hash,  json_path)
                        logger.info(f"Downloaded json file to {json_path}")
                        download_file(heatmap_hash, heatmap_path)
                        logger.info(f"Downloaded heatmap file to {heatmap_path}")
                        
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