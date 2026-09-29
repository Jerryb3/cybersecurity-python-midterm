import socket
import time
from datetime import datetime


# Only these targets are authorized for this assignment.
ALLOWED_TARGETS = {
    "127.0.0.1",
    "localhost",
    "scanme.nmap.org",
}

TIMEOUT = 1.0
DELAY = 0.1


def validate_port(port):
    """Check that a port number is within the valid TCP port range."""
    if port < 1 or port > 65535:
        raise ValueError("Port numbers must be between 1 and 65535.")


def scan_port(host, port):
    """Attempt a TCP connection and return True if the port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
            scanner.settimeout(TIMEOUT)
            result = scanner.connect_ex((host, port))
            return result == 0
    except socket.error:
        return False


def scan_ports(host, start_port, end_port):
    """Scan a range of TCP ports on an authorized target."""

    host = host.lower().strip()

    # Prevent scanning targets not authorized by the assignment.
    if host not in ALLOWED_TARGETS:
        print("Error: This target is not authorized for this assignment.")
        print("Allowed targets: localhost, 127.0.0.1, scanme.nmap.org")
        return

    try:
        validate_port(start_port)
        validate_port(end_port)

        if start_port > end_port:
            raise ValueError(
                "The starting port cannot be greater than the ending port."
            )

        # Resolve the hostname before beginning the scan.
        ip_address = socket.gethostbyname(host)

    except ValueError as error:
        print(f"Input error: {error}")
        return

    except socket.gaierror:
        print(f"Host error: Unable to resolve {host}.")
        return

    print("\n--- Python Port Scanner ---")
    print(f"Target: {host}")
    print(f"IP Address: {ip_address}")
    print(f"Port Range: {start_port}-{end_port}")
    print(f"Scan started: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")
    print("-" * 40)

    start_time = time.time()

    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            print(f"Port {port}: OPEN")
        else:
            print(f"Port {port}: CLOSED")

        # Small delay to avoid scanning too aggressively.
        time.sleep(DELAY)

    elapsed_time = time.time() - start_time

    print("-" * 40)
    print(f"Scan completed in {elapsed_time:.2f} seconds.")


def main():
    """Collect user input and start the port scan."""

    print("Authorized targets:")
    print("  localhost")
    print("  127.0.0.1")
    print("  scanme.nmap.org")

    try:
        host = input("\nEnter target: ").strip()
        start_port = int(input("Enter starting port: "))
        end_port = int(input("Enter ending port: "))

        scan_ports(host, start_port, end_port)

    except ValueError:
        print("Input error: Ports must be entered as whole numbers.")

    except KeyboardInterrupt:
        print("\nScan cancelled by user.")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()