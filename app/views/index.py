import subprocess
import sys

from flask import Blueprint, jsonify, request, render_template

from app.app import db
from app.models import Host

bp = Blueprint("bp_index", __name__)


# Here you can read about routing:
# https://flask.palletsprojects.com/en/2.0.x/api/#url-route-registrations
# https://hackersandslackers.com/flask-routes/
@bp.route('/')
def index_get():
    hosts = db.session.query(Host).all()
    return render_template("index.html.jinja", hosts=hosts)
