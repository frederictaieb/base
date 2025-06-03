import asyncio
import websockets
import json
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SERVER_ADDRESS  = os.getenv("XRP_SERVER_WALLET_ADDR")
async def listen_xrp_transactions():
    uri = os.getenv("XRP_TESTNET_ADDR_WS")


    async with websockets.connect(uri) as websocket:
        # S'abonner aux transactions concernant l'adresse
        subscribe_message = {
            "id": 1,
            "command": "subscribe",
            "accounts": [SERVER_ADDRESS]
        }
        await websocket.send(json.dumps(subscribe_message))
        print(f"✅ Abonné au wallet {SERVER_ADDRESS}")

        # Écouter en boucle les messages du réseau
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                # Affiche seulement les transactions
                if data.get("type") == "transaction":
                    print("💸 Nouvelle transaction détectée :")
                    print(json.dumps(data, indent=2))
            except Exception as e:
                print(f"Erreur : {e}")
                break

if __name__ == "__main__":
    asyncio.run(listen_xrp_transactions())
