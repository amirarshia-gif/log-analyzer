from collections import Counter

from parser import parse_line

import gzip

def analyze_log(file_path):
    total_requests = 0
    malformed_lines = 0
    error_requests = 0

    unique_ips = set()

    failed_login_ips = Counter()

    endpoints = Counter()

    hourly_requests = Counter()

    if file_path.endswith(".gz"):
        file = gzip.open(
        file_path,
        "rt",
        encoding="utf-8"
    )
    else:
        file = open(
        file_path,
        "r",
        encoding="utf-8"
    )

    with file:

        for line in file:

            log = parse_line(line)

            if log is None:
                malformed_lines += 1
                continue

            total_requests += 1

            unique_ips.add(log["ip"])

            endpoints[log["endpoint"]] += 1

            hour = log["timestamp"][12:14]

            hourly_requests[hour] += 1

            if log["status"] >= 400:
                error_requests += 1


            if (
                log["endpoint"] == "/login"
                and log["status"] == 401
            ):
                failed_login_ips[log["ip"]] += 1
            


    return {
        "total_requests": total_requests,
        "malformed_lines": malformed_lines,
        "unique_ips": len(unique_ips),
        "top_endpoints": endpoints.most_common(10),
        "hourly_requests": hourly_requests,
        "error_requests": error_requests,
        "failed_login_ips": failed_login_ips,
    }


