# Uptime Monitor

A simple uptime monitor that checks if a host is up or down.

## Inspiration

I wanted to monitor hosts in my network in similar way to how [UptimeRobot](https://uptimerobot.com) does it.

## Usage

Start service with WSGI. Also, remember to add following command to crontab to run the monitor every minute.

```
* * * * * /path/to/python -m flask --app /path/to/uptime-monitor/app/app.py iputils ping
```

## Management

All commands have to be run from the root of the project.

### Add a host

```bash
flask manage add <ip-address> [--name <friendly-name>]
```

### Update name of a host

```bash
flask manage set-name <new-name> --to <ip-address>
```
