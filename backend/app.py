from flask import Flask, request, jsonify
from flask_sock import Sock
from flask_cors import CORS
from db import DB
import json

app = Flask(__name__)
CORS(app)  # CORS'u etkinleştir
sock = Sock(app)
db = DB()

desktop_clients = set()
web_clients = set()

@sock.route('/ws')
def websocket_route(ws):
    try:
        # İlk mesaj: client tanıtımı
        raw = ws.receive()
        if raw is None:
            return

        hello = json.loads(raw)
        client_type = hello.get("client")

        if client_type == "desktop":
            desktop_clients.add(ws)
            print("Desktop bağlandı")
        elif client_type == "web":
            web_clients.add(ws)
            print("Web bağlandı")
        else:
            ws.send("client type eksik")
            return

        # Ana mesaj döngüsü
        while True:
            raw = ws.receive()
            if raw is None:
                break

            data = json.loads(raw)
            msg_type = data.get("type")

            # Masaüstünden sensör verisi
            if msg_type == "sensor_data":
                db.updateData(data["payload"])

                # Web clientlara yayınla
                for client in list(web_clients):
                    try:
                        client.send(json.dumps({
                            "type": "sensor_update",
                            "payload": data["payload"]
                        }))
                    except:
                        web_clients.discard(client)

            # Web'den komut
            elif msg_type == "command":
                for client in list(desktop_clients):
                    try:
                        client.send(json.dumps({
                            "type": "command",
                            "payload": data["payload"]
                        }))
                    except:
                        desktop_clients.discard(client)

    except Exception as e:
        print("WS hata:", e)

    finally:
        desktop_clients.discard(ws)
        web_clients.discard(ws)
        print("Bağlantı kapandı")

# HTTP İLE
@app.route("/data")
def get_data():
    return db.getData()

# Login endpoint
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # Şimdilik herhangi bir kullanıcı adı ve şifre kabul edilir
    if username and password:
        return jsonify({
            "success": True,
            "message": "Giriş başarılı"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Kullanıcı adı ve şifre gerekli"
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
