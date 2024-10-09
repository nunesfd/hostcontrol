
import re
import socket

def is_valid_ipv4(ip: str) -> bool:
    """Valida um endereço IPv4."""
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False

def is_valid_ipv6(ip: str) -> bool:
    """Valida um endereço IPv6."""
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except socket.error:
        return False
    
def is_valid_ip(ip: str) -> bool:
    """Valida um endereço IPv4 ou IPv6."""
    return is_valid_ipv4(ip) or is_valid_ipv6(ip)

def is_valid_hostname(hostname: str) -> bool:
    """Valida um hostname de acordo com as regras do DNS."""
    
    if len(hostname) > 255:
        return False
    
    if hostname.endswith('.'):
        hostname = hostname[:-1]
    
    labels = hostname.split('.')
    
    hostname_regex = re.compile(r'^[a-zA-Z0-9-]{1,63}$')
    
    for label in labels:
        if not label or not hostname_regex.match(label):
            return False
        
        if label.startswith('-') or label.endswith('-'):
            return False
    
    return True
