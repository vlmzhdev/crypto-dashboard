import requests
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Connection settings to our local database
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

def get_btc_fees():
    #Gets current Bitcoin network fees from mempool.space
    url = "https://mempool.space/api/v1/fees/recommended"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Ошибка при получении данных: {e}")
        return None

def save_to_db(fees):
    #Saves received commissions to MySQL
    if not fees:
        return

    try:
        # Establishing a connection to the database
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            # SQL query to add a new row
            # %s are safe placeholders to avoid SQL injections.
            sql = """
            INSERT INTO btc_mempool (fastest_fee, half_hour_fee, hour_fee, minimum_fee)
            VALUES (%s, %s, %s, %s)
            """
            
            # Substitute real values ​​from the API dictionary
            values = (
                fees.get('fastestFee'),
                fees.get('halfHourFee'),
                fees.get('hourFee'),
                fees.get('minimumFee')
            )
            
            cursor.execute(sql, values)
        
        # We be sure to confirm the changes.
        connection.commit()
        print(f"✅ Успех! Комиссии сохранены в базу данных. (Fastest: {fees.get('fastestFee')} sat/vB)")

    except Exception as e:
        print(f"[ERROR] Ошибка при работе с базой данных: {e}")
    finally:
        # In any case, we close the connection so as not to overload the server.
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    print("Собираем данные из Mempool...")
    current_fees = get_btc_fees()
    
    if current_fees:
        save_to_db(current_fees)