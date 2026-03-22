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

def get_btc_fees():
    url = "https://mempool.space/api/v1/fees/recommended"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Ошибка при получении данных: {e}")
        return None

def save_to_db(fees):
    if not fees:
        return

    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO btc_mempool (fastest_fee, half_hour_fee, hour_fee, minimum_fee)
            VALUES (%s, %s, %s, %s)
            """
            

            values = (
                fees.get('fastestFee'),
                fees.get('halfHourFee'),
                fees.get('hourFee'),
                fees.get('minimumFee')
            )
            
            cursor.execute(sql, values)
        
        connection.commit()
        print(f"✅ Успех! Комиссии сохранены в базу данных. (Fastest: {fees.get('fastestFee')} sat/vB)")

    except Exception as e:
        print(f"[ERROR] Ошибка при работе с базой данных: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    print("Собираем данные из Mempool...")
    current_fees = get_btc_fees()
    
    if current_fees:
        save_to_db(current_fees)