# ============================================================
# Server Script - Object Oriented Programming
# ============================================================
# This script runs the Server that accepts Clients

import socket     # For network communication
import threading  # To handle more than one client at the same time
import json       # For handling JSON
from news_handler import NewsHandler  # News fetching class
from protocol import Protocol          # Protocol class

# ============================================================
# ClientHandler Class - Client Handler
# ============================================================

class ClientHandler:
    """
    This class handles each client individually
    Each client runs in a separate thread
    """
    
    def __init__(self, client_socket, client_address, group_id):
        """
        Constructor - executed when a new object is created
        
        Parameters:
            client_socket: the client's socket
            client_address: client address (IP + Port)
            group_id: group ID (GB5)
        """
        self.socket = client_socket       # socket
        self.address = client_address     # address
        self.group_id = group_id          # group ID
        self.client_name = None           # client name (received later)
        self.news_handler = NewsHandler() # news handler object
        self.protocol = Protocol()        # communication protocol object
    
    def send(self, message):
        """Send a message to the client - wrapper function"""
        return self.protocol.send_message(self.socket, message)
    
    def receive(self):
        """Receive a message from the client - wrapper function"""
        return self.protocol.receive_message(self.socket)
    
    # ============================================================
    # Headlines Menu Handler
    # ============================================================
    
    def handle_headlines_menu(self):
        """
        Function that handles headlines menu requests
        The client can choose:
        1. Search by keyword
        2. Search by category
        3. Search by country
        4. All headlines
        5. Return to main menu
        """
        while True:  # Loop to keep receiving requests
            # Receive client choice
            choice = self.receive()
            if not choice:  # If connection is closed
                break
            
            # Print request on server screen
            print(f"[{self.client_name}] Headlines request: {choice}")
            
            # ============================================================
            # Option 1: Search by keyword
            # ============================================================
            if choice == '1':
                self.send("READY")  # Tell the client: I'm ready
                keyword = self.receive()  # Receive keyword
                if not keyword:
                    break
                
                print(f"[{self.client_name}] Searching headlines for keyword: {keyword}")
                
                # Fetch data from NewsAPI
                data = self.news_handler.search_headlines_by_keyword(keyword)
                
                # Save data to JSON file
                filename = f"{self.client_name}_keyword_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                # Send data to client
                self.send(json.dumps(data))
            
            # ============================================================
            # Option 2: Search by category
            # ============================================================
            elif choice == '2':
                self.send("READY")
                category = self.receive()  # Receive category (sports, business, etc.)
                if not category:
                    break
                
                print(f"[{self.client_name}] Searching headlines by category: {category}")
                
                data = self.news_handler.get_headlines_by_category(category)
                filename = f"{self.client_name}_category_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # ============================================================
            # Option 3: Search by country
            # ============================================================
            elif choice == '3':
                self.send("READY")
                country = self.receive()  # Receive country code (sa, us, ae, etc.)
                if not country:
                    break
                
                print(f"[{self.client_name}] Searching headlines by country: {country}")
                
                data = self.news_handler.get_headlines_by_country(country)
                filename = f"{self.client_name}_country_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # ============================================================
            # Option 4: All headlines
            # ============================================================
            elif choice == '4':
                print(f"[{self.client_name}] Fetching all headlines")
                
                data = self.news_handler.get_all_headlines()
                filename = f"{self.client_name}_all_headlines_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # ============================================================
            # Option 5: Return to main menu
            # ============================================================
            elif choice == '5':
                break  # Exit loop and return to main menu
            
            else:
                self.send("ERROR")
    
    # ============================================================
    # Sources Menu Handler
    # ============================================================
    
    def handle_sources_menu(self):
        """
        Function that handles sources menu requests
        The client can choose:
        1. Search by category
        2. Search by country
        3. Search by language
        4. All sources
        5. Return to main menu
        """
        while True:
            choice = self.receive()
            if not choice:
                break
            
            print(f"[{self.client_name}] Sources request: {choice}")
            
            # Option 1: Search by category
            if choice == '1':
                self.send("READY")
                category = self.receive()
                if not category:
                    break
                
                print(f"[{self.client_name}] Searching sources by category: {category}")
                
                data = self.news_handler.get_sources_by_category(category)
                filename = f"{self.client_name}_sources_category_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # Option 2: Search by country
            elif choice == '2':
                self.send("READY")
                country = self.receive()
                if not country:
                    break
                
                print(f"[{self.client_name}] Searching sources by country: {country}")
                
                data = self.news_handler.get_sources_by_country(country)
                filename = f"{self.client_name}_sources_country_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # Option 3: Search by language
            elif choice == '3':
                self.send("READY")
                language = self.receive()
                if not language:
                    break
                
                print(f"[{self.client_name}] Searching sources by language: {language}")
                
                data = self.news_handler.get_sources_by_language(language)
                filename = f"{self.client_name}_sources_language_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # Option 4: All sources
            elif choice == '4':
                print(f"[{self.client_name}] Fetching all sources")
                
                data = self.news_handler.get_all_sources()
                filename = f"{self.client_name}_all_sources_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # Option 5: Return to main menu
            elif choice == '5':
                break
            
            else:
                self.send("ERROR")
    
    # ============================================================
    # Main Client Handler
    # ============================================================
    
    def handle(self):
        """
        Main function that handles the client
        Runs in a separate thread for each client
        """
        print(f"[NEW CONNECTION] {self.address} connected")
        
        try:
            # ============================================================
            # Step 1: Receive client name
            # ============================================================
            self.client_name = self.receive()
            if not self.client_name:
                return
            
            print(f"[CLIENT NAME] {self.client_name} from {self.address}")
            self.send("CONNECTED")  # Connection confirmation
            
            # ============================================================
            # Step 2: Main Menu Loop
            # ============================================================
            while True:
                choice = self.receive()  # Receive choice
                if not choice:
                    break
                
                print(f"[{self.client_name}] Main menu choice: {choice}")
                
                # Option 1: Headlines menu
                if choice == '1':
                    self.send("HEADLINES")
                    self.handle_headlines_menu()
                
                # Option 2: Sources menu
                elif choice == '2':
                    self.send("SOURCES")
                    self.handle_sources_menu()
                
                # Option 3: Disconnect
                elif choice == '3':
                    print(f"[DISCONNECTED] {self.client_name} disconnected")
                    self.send("BYE")
                    break
                
                else:
                    self.send("ERROR")
        
        except Exception as e:
            print(f"[ERROR] {self.client_name if self.client_name else 'Unknown'}: {e}")
        
        finally:
            self.socket.close()
            print(f"[CLOSED] Connection with {self.client_name} closed")


# ============================================================
# NewsServer Class - Main Server
# ============================================================

class NewsServer:
    """
    Main Server class
    Responsible for accepting connections and creating threads for clients
    """
    
    def __init__(self, host='127.0.0.1', port=5000, group_id="GB5"):
        """
        Constructor
        
        Parameters:
            host: IP address (localhost = 127.0.0.1)
            port: port number (5000)
            group_id: group ID (GB5)
        """
        self.host = host
        self.port = port
        self.group_id = group_id
        self.server_socket = None
        self.is_running = False
    
    def start(self):
        """
        Start the server
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(3)
        self.is_running = True
        
        self.print_banner()
        
        try:
            while self.is_running:
                client_socket, client_address = self.server_socket.accept()
                
                client_handler = ClientHandler(
                    client_socket,
                    client_address,
                    self.group_id
                )
                
                thread = threading.Thread(target=client_handler.handle)
                thread.start()
                
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        
        except KeyboardInterrupt:
            print("\n[SHUTTING DOWN] Server closing...")
            self.stop()
        
        except Exception as e:
            print(f"[SERVER ERROR] {e}")
            self.stop()
    
    def stop(self):
        """
        Stop the server
        """
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        print("[SERVER] Stopped")
    
    def print_banner(self):
        """
        Print server startup banner
        """
        print("=" * 60)
        print(f"NEWS SERVICE SERVER (OOP) - Group {self.group_id}")
        print("=" * 60)
        print(f"Server listening on {self.host}:{self.port}")
        print("Waiting for connections...")
        print("=" * 60)


# ============================================================
# Main Function - Entry Point
# ============================================================

def main():
    """
    Main function - program entry point
    """
    server = NewsServer(host='127.0.0.1', port=5000, group_id="GB5")
    server.start()


# ============================================================
# Program Execution
# ============================================================
if __name__ == "__main__":
    # Executed only when running this file directly
    # Not executed if the file is imported

    main()
