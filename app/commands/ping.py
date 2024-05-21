import subprocess
import sys

import click
import requests
from flask import Blueprint, current_app

from app.app import db
from app.models import Host, HostHistory
from app.utils.discord import notify_up, notify_down

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
    if host.up != (is_down == 0):
        host.notified = False
    host.up = (is_down == 0)
    if not host.notified:
        if host.up:
            r = notify_up(current_app.config["DISCORD_NOTIFICATION_WEBHOOK"], host)
        else:
            r = notify_down(current_app.config["DISCORD_NOTIFICATION_WEBHOOK"], host)
        if r == 204:
            # Successfully sent notification
            host.notified = True
    db.session.add(host_history)
    db.session.commit()
    requests.post(f"http://{current_app.config['APP_HOST']}:{current_app.config['APP_PORT']}/api/{ip_addr}",
                  json={"status": is_down})


@bp.cli.command("ping")
@click.option("--ip", default=None)
def cmd_ping_all(ip):
    if ip is not None:
        ping_host(ip)
    else:
        hosts = db.session.query(Host).all()
        for host in hosts:
            ping_host(host.ipaddress)
