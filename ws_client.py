import websocket
import threading
import json

def on_message(ws, message):
    print("Geldi:", message)

def on_error(ws, error):
    print("Hata:", error)

def on_close(ws):
    print("Bağlantı kapandı.")

def on_open(ws):
    print("Bağlanıldı.")
    ws.send("Merhaba!")

ws = websocket.WebSocketApp(
    "ws://localhost:5000/ws",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)


# Client'i thread'de başlatan fonksiyon
def start_ws():
    ws.on_open = on_open
    ws.run_forever()

# Thread başlat
ws_thread = threading.Thread(target=start_ws)
ws_thread.daemon = True

# Veriyi gönderme fonksiyonu
def send_data(data: dict):
    if ws.sock and ws.sock.connected:  # Bağlantı açık mı kontrol et
        ws.send(json.dumps(data))
        