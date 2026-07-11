import re

LOG_PATTERN = re.compile(
    r'(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+) (\S+)" (\d{3}) (\S+)'
)


def parse_line(line):
    match = LOG_PATTERN.match(line)

    if not match:
        return None

    ip, timestamp, method, endpoint, protocol, status, size = match.groups()

    try:
        size = 0 if size == "-" else int(size)
    except ValueError:
        size = 0

    return {
        "ip": ip,
        "timestamp": timestamp,
        "method": method,
        "endpoint": endpoint,
        "protocol": protocol,
        "status": int(status),
        "size": size,
    }