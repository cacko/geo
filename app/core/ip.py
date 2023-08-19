import ipaddress
import httpx


def get_remote_ip(req_ip, forward_ip=None):
    try:
        ipv4 = ipaddress.IPv4Address(req_ip)
        if ipv4.is_private:
            return httpx.get("https://checkip.amazonaws.com").text.strip()
        if forward_ip:
            return forward_ip
    except Exception:
        pass
    return req_ip
