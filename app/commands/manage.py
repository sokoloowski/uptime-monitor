import click
from flask import Blueprint, current_app

from app.app import db
from app.models import Host
from app.utils.discord import notify_new_host, notify_removed_host

bp = Blueprint('manage', __name__)


@bp.cli.command("add")
@click.argument("ipaddress")
@click.option("--name", default=None)
def cmd_add_device(ipaddress, name):
    host = Host(ipaddress=ipaddress, name=name)
    db.session.add(host)
    db.session.commit()
    notify_new_host(current_app.config["DISCORD_NOTIFICATION_WEBHOOK"], host)


@bp.cli.command("set-name")
@click.argument("name")
@click.option("--to", default=None)
def cmd_set_name(name, to):
    host = db.session.query(Host).filter(Host.ipaddress == to).one_or_none()
    if host is None:
        return
    host.name = name
    db.session.commit()


@bp.cli.command("remove")
@click.argument("ipaddress")
def cmd_remove_device(ipaddress):
    host = db.session.query(Host).filter(Host.ipaddress == ipaddress).one_or_none()
    if host is None:
        return
    db.session.delete(host)
    db.session.commit()
    notify_removed_host(current_app.config["DISCORD_NOTIFICATION_WEBHOOK"], host)
