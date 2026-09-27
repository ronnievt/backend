from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

server = Flask(__name__)
CORS(server)

STORAGE = "data.txt"


@server.route("/api/city", methods=["POST"])
def add_city():
    payload = request.get_json(silent=True) or {}
    user_city = str(payload.get("city", "")).strip()

    if len(user_city) == 0:
        return jsonify({"status": "error", "message": "Поле города пустое"}), 400

    stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    record = "{} | Город: {}\n".format(stamp, user_city)

    try:
        with open(STORAGE, "a", encoding="utf-8") as f:
            f.write(record)
    except OSError as err:
        return jsonify({"status": "error", "message": "Сбой записи: {}".format(err)}), 500

    return jsonify({"status": "ok", "message": "Город {} добавлен".format(user_city)}), 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)