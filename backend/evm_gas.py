import requests
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}


NETWORKS = {
    'ethereum': 'https://eth.drpc.org',
    'bsc':      'https://bsc-dataseed.binance.org',
    'polygon':  'https://polygon-mainnet.gateway.tatum.io',
}

def get_gas(network, rpc_url):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_gasPrice",
        "params": [],
        "id": 1
    }
    try:
        response = requests.post(rpc_url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        hex_price = data.get('result')
        
        if hex_price is None:
            error_msg = data.get('error', {}).get('message', 'Unknown RPC error')
            print(f"[DEBUG] {network} RPC error: {error_msg}")
            return None

        gwei = int(hex_price, 16) / 1e9
        return round(gwei, 2)
    except Exception as e:
        print(f"[ERROR] {network}: {e}")
        return None

def save_to_db(network, gwei):
    if gwei is None:
        return
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO evm_gas (network, low, average, high)
            VALUES (%s, %s, %s, %s)
            """
            values = (
                network,
                round(gwei * 0.9, 4),
                round(gwei, 4),
                round(gwei * 1.2, 4)
            )
            cursor.execute(sql, values)
        connection.commit()
        print(f"✅ {network}: {gwei} gwei сохранён в БД")
    except Exception as e:
        print(f"[ERROR] БД ({network}): {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    print("Собираем EVM газ...")
    for network, rpc_url in NETWORKS.items():
        gwei = get_gas(network, rpc_url)
        save_to_db(network, gwei)
