import socket

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024


def start_server():
    """Start a TCP server and communicate with one client."""

    # Create a TCP/IPv4 socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            # Allow the address to be reused shortly after the server closes.
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind the server to localhost and the selected port.
            server_socket.bind((HOST, PORT))

            # Listen for incoming client connections.
            server_socket.listen(1)

            print(f"Server is listening on {HOST}:{PORT}...")

            # Wait for a client to connect.
            connection, address = server_socket.accept()

            with connection:
                print(f"Connected by {address}")

                while True:
                    data = connection.recv(BUFFER_SIZE)

                    # An empty result means the client disconnected.
                    if not data:
                        print("Client disconnected.")
                        break

                    message = data.decode("utf-8")
                    print(f"Client: {message}")

                    # Allow the client to gracefully end the session.
                    if message.lower() == "quit":
                        response = "Connection closing. Goodbye!"
                        connection.sendall(response.encode("utf-8"))
                        print("Closing client connection.")
                        break

                    response = f"Server received: {message}"
                    connection.sendall(response.encode("utf-8"))

        except OSError as error:
            print(f"Server error: {error}")

        finally:
            print("Server shut down.")


if __name__ == "__main__":
    start_server()