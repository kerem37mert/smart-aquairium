from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@sock.route('/ws')
def websocket_route(ws):
    while True:
        data = ws.receive()  # Client'tan veri al
        if data is None:     # Client bağlantıyı kapattıysa
            break
        print("Client'tan gelen veri:", data)
        # İstersen geri cevap da gönderebilirsin
        ws.send(f"Sunucu aldı: {data}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)