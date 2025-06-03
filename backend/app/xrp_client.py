
import os
from dotenv import load_dotenv
import logging
from xrpl.wallet import Wallet
from xrpl.constants import CryptoAlgorithm
from xrpl.clients import WebsocketClient
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.transaction import autofill_and_sign
from xrpl.transaction import submit_and_wait


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
client_wallet_seed = os.getenv("XRP_CLIENT_WALLET_SEED")
server_wallet_addr = os.getenv("XRP_SERVER_WALLET_ADDR")

test_wallet = Wallet.from_seed(seed=client_wallet_seed, algorithm=CryptoAlgorithm.ED25519)
logger.info(f"Client wallet address: {test_wallet.address}")

client = WebsocketClient(os.getenv("XRP_TESTNET_ADDR_WS"))
client.open()

try:
    my_payment = Payment(
        account=test_wallet.address,
        amount=xrp_to_drops(1),
        destination=server_wallet_addr,
    )
    logger.info(f"Payment object: {my_payment}")

    signed_tx = autofill_and_sign(my_payment, client, test_wallet)
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







