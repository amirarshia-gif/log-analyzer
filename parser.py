import re

LOG_PATTERN = re.compile(r'(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+) (\S+)" (\d{3}) (\S+)')


def parse_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    ip, timestamp, method, endpoint, protocol, status, size = match.groups()

    return {
        "ip": ip,
        "timestamp": timestamp,
        "method": method,
        "endpoint": endpoint,
        "protocol": protocol,
        "status": int(status),
        "size": size,
    }



if __name__ == "__main__":
    sample = '203.0.113.42 - - [01/Jun/2026:09:14:22 +0000] "GET /products/1877 HTTP/1.1" 200 5324 "-" "Mozilla/5.0"'

    result = parse_line(sample)

    print(result)