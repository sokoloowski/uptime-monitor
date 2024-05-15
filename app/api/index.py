from flask import Blueprint, jsonify, request, abort

from app.app import socketio

bp = Blueprint("bp_api_index", __name__, url_prefix="/api")


# Here you can read about routing:
# https://flask.palletsprojects.com/en/2.0.x/api/#url-route-registrations
# https://hackersandslackers.com/flask-routes/
@bp.route('/<host>', methods=['POST'])
def index_post(host):
    if request.remote_addr != "127.0.0.1":
        return abort(403)
    status = request.json.get("status", None)
    if status is None:
        return abort(400)
    socketio.emit("history", {"host": host, "down": status > 0})
    return jsonify({"host": host, "status": "ok"})
