import socket

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024


def start_client():
    """Connect to the TCP server and exchange messages."""

    # Create a TCP/IPv4 socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            print(f"Connecting to {HOST}:{PORT}...")

            # Attempt to connect to the server.
            client_socket.connect((HOST, PORT))

            print("Successfully connected to the server.")
            print("Type 'quit' to disconnect.")

            while True:
                message = input("Enter message: ").strip()

                if not message:
                    print("Please enter a message.")
                    continue

                # Send the user's message to the server.
                client_socket.sendall(message.encode("utf-8"))

                # Receive the server's response.
                response = client_socket.recv(BUFFER_SIZE)
                print(f"Server: {response.decode('utf-8')}")

                if message.lower() == "quit":
                    print("Disconnected from server.")
                    break

        except ConnectionRefusedError:
            print(
                "Connection failed: the server is not running "
                "or is not accepting connections."
            )

        except OSError as error:
            print(f"Client error: {error}")

        finally:
            print("Client shut down.")


if __name__ == "__main__":
    start_client()