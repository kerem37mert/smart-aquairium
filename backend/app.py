from flask import Flask
from flask_sock import Sock
from db import DB
import json

app = Flask(__name__)
sock = Sock(app)
db = DB()

@sock.route('/ws')
def websocket_route(ws):
    while True:
        raw = ws.receive()  # Client -> Sunucu
        if raw is None:
            break

        try:
            data = json.loads(raw)   # JSON -> Dict
        except json.JSONDecodeError:
            ws.send("Hatalı JSON")
            continue

        print("Gelen veri:", data)

        db.updateData(data)

        ws.send("Veri güncellendi")


# HTTP İLE
@app.route("/data")
def get_data():
    return db.getData()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
