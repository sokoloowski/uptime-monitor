import os

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")


# Flask quickstart:
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
# Flask factory pattern:
# https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
def create_app():
    # Create and configure the app
    app = Flask(__name__)

    # Load config from file config.py
    app.config.from_pyfile("config.py")
    app.config.from_pyfile("../config.local.py")

    # Ensure the instance folder exists - nothing interesting
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize SQLAlchemy
    db.init_app(app)

    from app.models import Host, HostHistory

    with app.app_context():
        db.create_all()
        db.session.commit()

    # Initialize Socket.io
    socketio.init_app(app)

    @socketio.on("*")
    def handle_my_custom_event(json):
        print("received json: " + str(json))

    # Setup custom "Not found" page
    # https://flask.palletsprojects.com/en/2.0.x/errorhandling/#custom-error-pages
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({
            "message": "not found",
            "code": "404"
        }), 404

    # Register blueprints (views)
    # https://flask.palletsprojects.com/en/2.0.x/blueprints/
    from app.views.index import bp as bp_index
    app.register_blueprint(bp_index)

    from app.api.index import bp as bp_api_index
    app.register_blueprint(bp_api_index)

    from app.commands.manage import bp as bp_manage
    app.register_blueprint(bp_manage)

    from app.commands.ping import bp as bp_ping
    app.register_blueprint(bp_ping)

    return app
