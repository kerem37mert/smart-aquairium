import websocket
import threading
import json

# =====================
# CALLBACKLER
# =====================

def on_message(ws, message):
    try:
        data = json.loads(message)
        msg_type = data.get("type")

        if msg_type == "command":
            command = data["payload"]["name"]
            print("Komut geldi:", command)

            if command == "feed":
                print("Yem ver komutu alındı")
                # burada istersen fish_tank.feed_fish() tetiklenir
            elif command == "water_change":
                print("Su değiştir komutu alındı")

    except Exception as e:
        print("Mesaj parse hatası:", e)


def on_error(ws, error):
    print("WS hata:", error)


def on_close(ws):
    print("WS bağlantı kapandı")


def on_open(ws):
    print("WS bağlandı")

    # Backend'e kendini TANIT
    ws.send(json.dumps({
        "client": "desktop"
    }))

# =====================
# WS APP
# =====================

ws = websocket.WebSocketApp(
    "ws://localhost:5000/ws",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

def start_ws():
    ws.run_forever()

# main.py burayı çağırıyor
ws_thread = threading.Thread(target=start_ws, daemon=True)

# =====================
# DIŞARIDAN ÇAĞRILAN
# =====================

def send_data(data: dict):
    """
    main.py içinden çağrılıyor
    aquarium_data -> backend formatına çevrilir
    """
    if ws.sock and ws.sock.connected:
        payload = {
            "type": "sensor_data",
            "payload": data
        }
        ws.send(json.dumps(payload))
