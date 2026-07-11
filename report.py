def print_report(data):

    print("=" * 65)

    print("Web Server Log Analysis Report")

    print("=" * 65)

    print(f"Total Requests : {data['total_requests']}")
    print(f"Malformed Lines: {data['malformed_lines']}")
    print(f"Unique IPs     : {data['unique_ips']}")

    if data["total_requests"] > 0:
        error_rate = (
            data["error_requests"]
            / data["total_requests"]
            * 100
        )
    else:
        error_rate = 0

    print(f"Error Rate     : {error_rate:.2f}%")

    print()

    print("Top Endpoints")
    print("-" * 60)

    for endpoint, count in data["top_endpoints"]:
        print(f"{endpoint:<40}{count}")

    print()


   
    print("Hourly Requests")

    print("-" * 60)

    max_requests = max(data["hourly_requests"].values(), default=1)

    for hour in sorted(data["hourly_requests"]):

        count = data["hourly_requests"][hour]

        bar_length = int((count / max_requests) * 40)

        bar = "█" * bar_length

        print(f"{hour}:00 | {bar:<40} ({count})")


    print()

    print("Suspicious Login Attempts")

    print("-" * 60)

    for ip, count in data["failed_login_ips"].most_common(10):

        if count >= 10:

         print(f"{ip:<20}{count}")    







