import logging
from pathlib import Path


def get_logger(name=""):
    if "/" in name:
        name = Path(name).stem
    return logging.getLogger(f"quizify.{name}")


def get_request_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")
    if x_forwarded_for and x_forwarded_for[0]:
        login_ip = x_forwarded_for[0]
        if login_ip.count(":") == 1:
            # format: ipv4:port (non-standard X-Forwarded-For)
            login_ip = login_ip.split(":")[0]
        return login_ip

    return request.META.get("REMOTE_ADDR", "")


def bulk_get(d, keys, default=None):
    return [d.get(key, default) for key in keys]
