import websockets
import json
import logging
from app.config.settings import settings
from app.config.logging_config import setup_logging
from app.models.markers import Marker
from app.utils.utils import parse_memo
#from app.api.routes import add_marker

import os
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

            #        await add_marker(Marker(
            #            gps=Gps(
            #                lat=parsed_memos["lat"],
            #                lng=parsed_memos["lng"],
            #            ),
            #            emotions=Emotions(
            #                joy=parsed_memos["joy"],
            #                sadness=parsed_memos["sadness"],
            #                anger=parsed_memos["anger"],
            #                fear=parsed_memos["fear"],
            #            ),
            #            wisdom=Wisdom(
            #                sentence_1=parsed_memos["sentence_1"],
            #                sentence_2=parsed_memos["sentence_2"],
            #                sentence_3=parsed_memos["sentence_3"],
            #            ),
            #        ))
    except Exception as e:
        logger.error(f"❌ Error in XRP Listener : {e}")


def xrp_emitter(json_hash, heatmap_hash):
    memo_data = {
        "json_hash": json_hash,
        "heatmap_hash": heatmap_hash
    }
    memo_json = json.dumps(memo_data)
    memo_hex = memo_json.encode('utf-8').hex()
    memo = Memo(memo_data=memo_hex) 
    logger.info(f"*** Memo: {memo}")
    
    load_dotenv()
    client_wallet_seed = os.getenv("XRP_CLIENT_WALLET_SEED")
    server_wallet_addr = os.getenv("XRP_SERVER_WALLET_ADDR")
    client_wallet = Wallet.from_seed(seed=client_wallet_seed, algorithm=CryptoAlgorithm.ED25519)
    client_wallet_addr = client_wallet.address
    logger.info(f"Client wallet address: {client_wallet.address}")

    client = WebsocketClient(os.getenv("XRP_TESTNET_ADDR_WS"))
    client.open()
    
    try:
        my_payment = Payment(
            account= client_wallet_addr,
            amount=xrp_to_drops(0.01),
            destination=server_wallet_addr,
            memos=[memo]
        )
        logger.info(f"Payment object: {my_payment}")

        signed_tx = autofill_and_sign(my_payment, client,  client_wallet)
        max_ledger = signed_tx.last_ledger_sequence
        tx_id = signed_tx.get_hash()
        logger.info(f"Transaction expires after ledger: {max_ledger}")
        logger.info(f"Identifying hash: {tx_id}")
        tx_response = submit_and_wait(signed_tx, client)
        logger.info(f"Transaction result: {tx_response.result['meta']['TransactionResult']}")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        client.close()









