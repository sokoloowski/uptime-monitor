import subprocess
import sys

import click
import requests
from flask import Blueprint

from app.app import db
from app.models import Host, HostHistory

bp = Blueprint('iputils', __name__)


def ping_host(ip_addr):
    host = db.session.query(Host).filter(Host.ipaddress == ip_addr).one_or_none()
    if host is None:
        return
    c = "-n" if sys.platform.lower() == 'win32' else '-c'
    is_down = subprocess.run(["ping", c, "1", ip_addr],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL).returncode
    host_history = HostHistory(host_id=host.id, up=(is_down == 0))
    host.up = (is_down == 0)
    db.session.add(host_history)
    db.session.commit()
    requests.post("http://127.0.0.1:5000/api/" + ip_addr, json={"status": is_down})


@bp.cli.command("ping")
@click.argument("host")
def cmd_ping_host(host):
    ping_host(host)


@bp.cli.command("ping")
def cmd_ping_all():
    hosts = db.session.query(Host).all()
    for host in hosts:
        ping_host(host.ipaddress)
