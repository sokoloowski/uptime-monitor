import requests

from app.models import Host

COLOR_RED = 15548997
COLOR_GREEN = 5763719
COLOR_BLUE = 5793266


def send_embed(webhook: str, message: str, description: str, color: int) -> int:
    if webhook is None:
        return -1

    r = requests.post(webhook, json={
        "username": "UptimeMonitor",
        "embeds": [
            {
                "title": message,
                "description": description,
                "type": "rich",
                "color": color
            }
        ]
    })

    return r.status_code


def notify_up(webhook: str, host: Host) -> int:
    return send_embed(webhook,
                      f"Host {host} is up",
                      f"UptimeMonitor got a response from `{host.ipaddress}`",
                      COLOR_GREEN)


def notify_down(webhook: str, host: Host) -> int:
    return send_embed(webhook,
                      f"Host {host} is down",
                      f"UptimeMonitor was unable to ping `{host.ipaddress}`",
                      COLOR_RED)


def notify_new_host(webhook: str, host: Host) -> int:
    return send_embed(webhook,
                      f"Added {host} to monitoring",
                      f"UptimeMonitor will now monitor `{host.ipaddress}`",
                      COLOR_BLUE)


def notify_removed_host(webhook: str, host: Host) -> int:
    return send_embed(webhook,
                      f"Removed {host} from monitoring",
                      f"UptimeMonitor will no longer monitor `{host.ipaddress}`",
                      COLOR_BLUE)
