import asyncio
import websockets
import json
import logging
from app.config.settings import settings
from app.models.markers import Marker
from app.utils.utils import parse_memo
from app.api.routes import add_marker

logger = logging.getLogger(__name__)

SERVER_ADDRESS = settings.XRP_SERVER_WALLET_ADDR
XRP_WS_URI = settings.XRP_TESTNET_ADDR_WS

async def xrp_listener():
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

                    await add_marker(Marker(
                        gps=Gps(
                            lat=parsed_memos["lat"],
                            lng=parsed_memos["lng"],
                        ),
                        emotions=Emotions(
                            joy=parsed_memos["joy"],
                            sadness=parsed_memos["sadness"],
                            anger=parsed_memos["anger"],
                            fear=parsed_memos["fear"],
                        ),
                        wisdom=Wisdom(
                            sentence_1=parsed_memos["sentence_1"],
                            sentence_2=parsed_memos["sentence_2"],
                            sentence_3=parsed_memos["sentence_3"],
                        ),
                    ))
    except Exception as e:
        logger.error(f"❌ Error in XRP Listener : {e}")