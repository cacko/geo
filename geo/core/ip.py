from email import message
import ipaddress
import logging
from turtle import st
import validators
import httpx
import socket

from geo.core import IPError


def get_remote_ip(req_ip, forward_ip=None):
    try:
        ipv4 = ipaddress.IPv4Address(req_ip)
        if ipv4.is_private:
            return httpx.get("https://checkip.amazonaws.com").text.strip()
        if forward_ip:
            return forward_ip
    except Exception as e:
        logging.exception(e)
        pass
    return req_ip

def resolve_hostname(hostname: str) -> str:
    try:
        assert validators.hostname(hostname, skip_ipv4_addr=True, skip_ipv6_addr=True)
        return socket.gethostbyname(hostname)
    except AssertionError as e:
        raise IPError(message="Not valid input") 
    except socket.gaierror as e:
        raise IPError(message=e.strerror)

def get_ip_from_input(input: str) -> str:
    try:
        assert validators.ip_address.ipv4(input)
        return input
    except AssertionError:
        try:
            return resolve_hostname(input) 
        except IPError as e:
            raise e
