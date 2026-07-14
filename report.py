def print_summary(data):
    """Print total requests, malformed lines, unique IPs, and error rate."""
    print("=" * 65)
    print("Web Server Log Analysis Report")
    print("=" * 65)

    if data["total_requests"] > 0:
        error_rate = (
            data["error_requests"]
            / data["total_requests"]
            * 100
        )
    else:
        error_rate = 0

    print(f"Total Requests  : {data['total_requests']} requests")
    print(f"Malformed Lines : {data['malformed_lines']} lines skipped")
    print(f"Unique IPs      : {data['unique_ips']} distinct visitors")
    print(f"Error Rate      : {error_rate:.2f}% of requests were 4xx/5xx")
    print()


def print_endpoints(data):
    """Print the 10 most requested endpoints."""
    print("Top Endpoints")
    print("-" * 60)

    for endpoint, count in data["top_endpoints"]:
        print(f"  {endpoint:<40}{count:>6} requests")
    print()


def print_suspicious(data):
    """Print IPs with 10+ failed /login attempts (possible brute force)."""
    print("Suspicious Login Attempts")
    print("-" * 60)

    flagged = [
        (ip, count)
        for ip, count in data["failed_login_ips"].most_common(10)
        if count >= 10
    ]

    if not flagged:
        print("  None detected (no IP had 10+ failed /login attempts).")
    else:
        print("  IPs below made repeated failed login attempts,")
        print("  which can indicate a brute-force attack attempt:\n")
        for ip, count in flagged:
            print(f"  {ip:<20} {count} failed login attempts")
    print()


def print_report(data):
    """Print the full report: every section, in order."""
    print_summary(data)
    print_endpoints(data)
    print_hourly_chart(data)
    print_suspicious(data)


def print_hourly_chart(data, chart_height=10):
    """Print a vertical bar chart of requests per hour: one column per
    hour, the exact count written above each bar, scale 0 to max."""
    hourly_requests = data["hourly_requests"]

    print("Hourly Requests")
    print("-" * 60)

    if not hourly_requests:
        print("  No hourly data available.\n")
        return

    hours = sorted(hourly_requests)
    max_count = max(hourly_requests.values())

    # column needs to be wide enough to fit the longest number, plus padding
    col_width = max(len(str(max_count)) + 2, 8)

    # bar height in rows, scaled so the busiest hour reaches chart_height
    bar_heights = {
        hour: max(1, round(hourly_requests[hour] / max_count * chart_height))
        for hour in hours
    }

    label_rows = 1  # one row reserved for the number, right above the bar
    total_rows = label_rows + chart_height

    for row in range(total_rows):
        line = ""
        for hour in hours:
            bar_top_row = label_rows + (chart_height - bar_heights[hour])
            label_row = bar_top_row - 1

            if row == label_row:
                cell = str(hourly_requests[hour])
            elif row >= bar_top_row:
                cell = "██"
            else:
                cell = ""
            line += f"{cell:^{col_width}}"
        print(line)

    print(f"0 |{'-' * (col_width * len(hours) - 2)}")
    axis_line = "".join(f"{hour + ':00':^{col_width}}" for hour in hours)
    print(f"  {axis_line}")
    print(f"\n  (scale: 0 to {max_count} requests, "
          f"peak hour: {max(hourly_requests, key=hourly_requests.get)}:00)\n")