from collections import Counter
from parser import parse_line
def analyze_log(file_path):
    total_requests = 0
    malformed_lines = 0

    unique_ips = set()

    endpoints = Counter()

    hourly_requests = Counter()

    error_requests = 0
    with open(file_path, "r", encoding="utf-8") as file:  
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
    return {
    "total_requests": total_requests,
    "malformed_lines": malformed_lines,
    "unique_ips": len(unique_ips),
    "top_endpoints": endpoints.most_common(10),
    "hourly_requests": hourly_requests,
    "error_requests": error_requests,
}            



if __name__ == "__main__":
    report = analyze_log("access.log")

    print(report)

