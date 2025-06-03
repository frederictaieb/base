import asyncio
import websockets
import json
import logging
import os
from dotenv import load_dotenv
from app.config.settings import settings
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

SERVER_ADDRESS = settings.XRP_SERVER_WALLET_ADDR
XRP_WS_URI = settings.XRP_TESTNET_ADDR_WS



def parse_memo(memos: List[dict]) -> Dict[str, Any]:
    """
    Parse a list of XRPL memos and return a merged dictionary of all memo data.
    Each memo is expected to be a dict with a 'Memo' key containing 'MemoData' in hex.
    """
    report = {}
    if memos and len(memos) > 0:
        for memo in memos:
            memo_data_hex = memo.get("Memo", {}).get("MemoData")
            if memo_data_hex:
                try:
                    # Decode hex to utf-8 string
                    memo_data_json = bytes.fromhex(memo_data_hex).decode("utf-8")
                    # Parse JSON string to dict
                    memo_data_object = json.loads(memo_data_json)
                    # Merge into report
                    report.update(memo_data_object)
                except Exception as e:
                    print(f"Error decoding memo: {e}")
            else:
                print("No MemoData found.")
        return report
    else:
        print("No memos found in the transaction.")
        return report


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

    except Exception as e:
        logger.error(f"❌ Error in XRP Listener : {e}")
