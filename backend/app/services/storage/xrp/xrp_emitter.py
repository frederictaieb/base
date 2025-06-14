import os
import json
from dotenv import load_dotenv
from app.config.settings import settings

import logging
from app.config.logging_config import setup_logging

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

def xrp_emitter(json_hash, heatmap_hash, wisdom_0_hash, wisdom_1_hash, wisdom_2_hash):
    memo_data = {
        "json_hash": json_hash,
        "heatmap_hash": heatmap_hash,
        "wisdom_0_hash": wisdom_0_hash,
        "wisdom_1_hash": wisdom_1_hash,
        "wisdom_2_hash": wisdom_2_hash
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