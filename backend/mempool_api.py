import requests

def get_btc_fees():
    #Receives current Bitcoin network fees from mempool.space
    url = "https://mempool.space/api/v1/fees/recommended"
    
    try:
        # Making a request to the API
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Checking for errors (404, 500)
        data = response.json()
        
        # Return a dictionary with data
        return {
            "fastestFee": data.get("fastestFee"),
            "halfHourFee": data.get("halfHourFee"),
            "hourFee": data.get("hourFee"),
            "minimumFee": data.get("minimumFee")
        }
        
    except Exception as e:
        print(f"[ERROR] Ошибка при получении данных мемпула: {e}")
        return None


if __name__ == "__main__":
    print("Собираем данные из Mempool...")
    fees = get_btc_fees()
    
    if fees:
        print(f"🔥 Быстрая транзакция: {fees['fastestFee']} sat/vB")
        print(f"⏳ Обычная (30 мин): {fees['halfHourFee']} sat/vB")
        print(f"🐢 Медленная (1 час): {fees['hourFee']} sat/vB")