# ============================================================
# Server Script - Procedural Programming (Non-OOP)
# ============================================================
# This script runs the Server in a procedural way (without OOP)
# The difference between it and server_oop.py:
# here everything is separate functions, not classes

import socket     # For network communication
import threading  # To handle multiple clients at the same time
import json       # For handling JSON
import struct     # For data packing
from news_handler import NewsHandler  # News fetching class

# ============================================================
# Settings
# ============================================================
HOST = '127.0.0.1'  # IP address (localhost)
PORT = 5000         # Port number
GROUP_ID = "GB5"    # Group ID

# Create an object from NewsHandler (used in all functions)
news_handler = NewsHandler()

# ============================================================
# Communication Functions
# ============================================================

def send_message(client_socket, message):
    """
    Send a message to the client

    Idea:
    Send the message length first (4 bytes) so the client knows
    how much data is coming

    Parameters:
        client_socket: the client's socket
        message: the message (string)

    Returns:
        True: if sending succeeded
        False: if there is a problem
    """
    try:
        # Convert message from string to bytes
        data = message.encode('utf-8')

        # Calculate data length and convert it to 4 bytes
        length = struct.pack('!I', len(data))

        # Send length + data together
        client_socket.sendall(length + data)
        return True
    except Exception as e:
        print(f"[PROTOCOL] Send error: {e}")
        return False

def receive_message(client_socket):
    """
    Receive a message from the client

    Steps:
    1. Receive the first 4 bytes (length)
    2. Unpack the length
    3. Receive the actual data in chunks

    Parameters:
        client_socket: the client's socket

    Returns:
        message (string): if successful
        None: if there is a problem or connection closed
    """
    try:
        # Receive first 4 bytes (length)
        raw_length = client_socket.recv(4)
        if not raw_length:
            return None  # Connection closed

        # Unpack the length
        length = struct.unpack('!I', raw_length)[0]

        # Receive the actual data
        data = b''
        while len(data) < length:
            chunk = client_socket.recv(min(length - len(data), 4096))
            if not chunk:
                return None
            data += chunk

        return data.decode('utf-8')
    except Exception as e:
        print(f"[PROTOCOL] Receive error: {e}")
        return None

# ============================================================
# Headlines Menu Handler
# ============================================================

def handle_headlines_menu(client_socket, client_name):
    """
    Function that handles headlines menu requests

    Parameters:
        client_socket: the socket
        client_name: client name
    """
    while True:
        # Receive client choice
        choice = receive_message(client_socket)
        if not choice:
            break

        print(f"[{client_name}] Headlines request: {choice}")

        # ============================================================
        # Option 1: Search by keyword
        # ============================================================
        if choice == '1':
            send_message(client_socket, "READY")  # Signal client: ready
            keyword = receive_message(client_socket)
            if not keyword:
                break

            print(f"[{client_name}] Searching headlines for keyword: {keyword}")

            # Fetch data from NewsAPI
            data = news_handler.search_headlines_by_keyword(keyword)

            # Save data to JSON file
            # Filename format: ClientName_keyword_GroupID.json
            filename = f"{client_name}_keyword_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)

            # Send data to client
            send_message(client_socket, json.dumps(data))

        # ============================================================
        # Option 2: Search by category
        # ============================================================
        elif choice == '2':
            send_message(client_socket, "READY")
            category = receive_message(client_socket)
            if not category:
                break

            print(f"[{client_name}] Searching headlines by category: {category}")

            data = news_handler.get_headlines_by_category(category)
            filename = f"{client_name}_category_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)

            send_message(client_socket, json.dumps(data))

        # ============================================================
        # Option 3: Search by country
        # ============================================================
        elif choice == '3':
            send_message(client_socket, "READY")
            country = receive_message(client_socket)
            if not country:
                break

            print(f"[{client_name}] Searching headlines by country: {country}")

            data = news_handler.get_headlines_by_country(country)
            filename = f"{client_name}_country_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)

            send_message(client_socket, json.dumps(data))

        # ============================================================
        # Option 4: All headlines
        # ============================================================
        elif choice == '4':
            print(f"[{client_name}] Fetching all headlines")

            data = news_handler.get_all_headlines()
            filename = f"{client_name}_all_headlines_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)

            send_message(client_socket, json.dumps(data))

        # ============================================================
        # Option 5: Return to main menu
        # ============================================================
        elif choice == '5':
            break

        else:
            send_message(client_socket, "ERROR")

# ============================================================
# Sources Menu Handler
# ============================================================

def handle_sources_menu(client_socket, client_name):
    """
    Function that handles sources menu requests

    Parameters:
        client_socket: the socket
        client_name: client name
    """
    while True:
        choice = receive_message(client_socket)
        if not choice:
            break

        print(f"[{client_name}] Sources request: {choice}")

        # Option 1: Search by category
        if choice == '1':
            send_message(client_socket, "READY")
            category = receive_message(client_socket)
            if not category:
                break

            print(f"[{client_name}] Searching sources by category: {category}")

            data = news_handler.get_sources_by_category(category)
            filename = f"{client_name}_sources_category_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)

            send_message(client_socket, json.dumps(data))

        # Option 2: Search by country
        elif choice == '2':
            send_message(client_socket, "READY")
            country = receive_message(client_socket)
            if not country:
                break

            print(f"[{client_name}] Searching sources by country: {country}")

            data = news_handler.get_sources_by_country(country)
            filename = f"{client_name}_sources_country_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)

            send_message(client_socket, json.dumps(data))

        # Option 3: Search by language
        elif choice == '3':
            send_message(client_socket, "READY")
            language = receive_message(client_socket)
            if not language:
                break

            print(f"[{client_name}] Searching sources by language: {language}")

            data = news_handler.get_sources_by_language(language)
            filename = f"{client_name}_sources_language_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)

            send_message(client_socket, json.dumps(data))

        # Option 4: All sources
        elif choice == '4':
            print(f"[{client_name}] Fetching all sources")

            data = news_handler.get_all_sources()
            filename = f"{client_name}_all_sources_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)

            send_message(client_socket, json.dumps(data))

        # Option 5: Return to main menu
        elif choice == '5':
            break

        else:
            send_message(client_socket, "ERROR")

# ============================================================
# Main Client Handler
# ============================================================

def handle_client(client_socket, client_address):
    """
    Main function that handles each client
    Runs in a separate thread per client

    Parameters:
        client_socket: client socket
        client_address: client address (IP + Port)
    """
    print(f"[NEW CONNECTION] {client_address} connected")

    client_name = None

    try:
        # Step 1: Receive client name
        client_name = receive_message(client_socket)
        if not client_name:
            return

        print(f"[CLIENT NAME] {client_name} from {client_address}")
        send_message(client_socket, "CONNECTED")

        # Step 2: Main menu loop
        while True:
            choice = receive_message(client_socket)
            if not choice:
                break

            print(f"[{client_name}] Main menu choice: {choice}")

            if choice == '1':
                send_message(client_socket, "HEADLINES")
                handle_headlines_menu(client_socket, client_name)

            elif choice == '2':
                send_message(client_socket, "SOURCES")
                handle_sources_menu(client_socket, client_name)

            elif choice == '3':
                print(f"[DISCONNECTED] {client_name} disconnected")
                send_message(client_socket, "BYE")
                break

            else:
                send_message(client_socket, "ERROR")

    except Exception as e:
        print(f"[ERROR] {client_name if client_name else 'Unknown'}: {e}")

    finally:
        client_socket.close()
        print(f"[CLOSED] Connection with {client_name if client_name else 'client'} closed")

# ============================================================
# Start Server Function
# ============================================================

def start_server():
    """
    Main function to start the server
    """
    # Step 1: Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow fast port reuse
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Step 2: Bind socket to IP and Port
    server_socket.bind((HOST, PORT))

    # Step 3: Listen for connections
    server_socket.listen(3)

    print("=" * 60)
    print(f"NEWS SERVICE SERVER (Procedural) - Group {GROUP_ID}")
    print("=" * 60)
    print(f"Server listening on {HOST}:{PORT}")
    print("Waiting for connections...")
    print("=" * 60)

    try:
        # Step 4: Accept connections
        while True:
            client_socket, client_address = server_socket.accept()

            # Step 5: Create a new thread for this client
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\n[SHUTTING DOWN] Server closing...")

    finally:
        server_socket.close()
        print("[SERVER] Stopped")

# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    """
    Executed only when the file is run directly
    Not executed if the file is imported
    """
    start_server()
