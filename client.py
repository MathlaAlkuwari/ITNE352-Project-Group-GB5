import socket
import struct
import json
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

# Constant option lists
COUNTRIES = ['au', 'ca', 'jp', 'ae', 'sa', 'kr', 'us', 'ma']
LANGUAGES = ['ar', 'en']
CATEGORIES = ['business', 'general', 'health', 'science', 'sports', 'technology']


def send_message(sock, message):
    """Send a length-prefixed UTF-8 message through the socket."""
    try:
        data = message.encode('utf-8')
        length = struct.pack('!I', len(data))
        sock.sendall(length + data)
        return True
    except Exception as e:
        print(f"Send error: {e}")
        return False


def receive_message(sock):
    """Receive a length-prefixed UTF-8 message from the socket."""
    try:
        raw_length = sock.recv(4)
        if not raw_length:
            return None
        length = struct.unpack('!I', raw_length)[0]
        
        data = b''
        while len(data) < length:
            chunk = sock.recv(min(length - len(data), 4096))
            if not chunk:
                return None
            data += chunk
        
        return data.decode('utf-8')
    except Exception as e:
        print(f"Receive error: {e}")
        return None


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def display_main_menu():
    print_header("MAIN MENU")
    print("1. Search for headlines")
    print("2. List of sources")
    print("3. Quit")
    print("-" * 60)


def display_headlines_menu():
    print_header("HEADLINES MENU")
    print("1. Search by keyword")
    print("2. Search by category")
    print("3. Search by country")
    print("4. List all headlines")
    print("5. Back to main menu")
    print("-" * 60)


def display_sources_menu():
    print_header("SOURCES MENU")
    print("1. Search by category")
    print("2. Search by country")
    print("3. Search by language")
    print("4. List all sources")
    print("5. Back to main menu")
    print("-" * 60)


def display_categories():
    print("\nAvailable categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")


def display_countries():
    print("\nAvailable countries:")
    countries_map = {
        'au': 'Australia', 'ca': 'Canada', 'jp': 'Japan', 'ae': 'UAE',
        'sa': 'Saudi Arabia', 'kr': 'South Korea', 'us': 'USA', 'ma': 'Morocco'
    }
    for i, code in enumerate(COUNTRIES, 1):
        print(f"{i}. {countries_map[code]} ({code})")


def display_languages():
    print("\nAvailable languages:")
    print("1. Arabic (ar)")
    print("2. English (en)")


def display_headlines_list(articles):
    """Print a numbered list of up to 15 headlines."""
    print_header("HEADLINES")
    
    if not articles:
        print("No articles found.")
        return []
    
    for i, article in enumerate(articles[:15], 1):
        print(f"\n{i}. Title: {article.get('title', 'N/A')}")
        print(f"   Source: {article.get('source', {}).get('name', 'N/A')}")
        print(f"   Author: {article.get('author', 'N/A')}")
        print("-" * 60)
    
    return articles[:15]


def display_headline_details(article):
    """Print detailed information for a single article."""
    print_header("HEADLINE DETAILS")
    print(f"Title: {article.get('title', 'N/A')}")
    print(f"Source: {article.get('source', {}).get('name', 'N/A')}")
    print(f"Author: {article.get('author', 'N/A')}")
    print(f"Description: {article.get('description', 'N/A')}")
    print(f"URL: {article.get('url', 'N/A')}")
    
    published_at = article.get('publishedAt', 'N/A')
    if published_at != 'N/A':
        try:
            dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            print(f"Published Date: {dt.strftime('%Y-%m-%d')}")
            print(f"Published Time: {dt.strftime('%H:%M:%S')}")
        except:
            print(f"Published: {published_at}")
    print("=" * 60)


def display_sources_list(sources):
    """Print a numbered list of up to 15 sources."""
    print_header("SOURCES")
    
    if not sources:
        print("No sources found.")
        return []
    
    for i, source in enumerate(sources[:15], 1):
        print(f"{i}. {source.get('name', 'N/A')}")
        print("-" * 60)
    
    return sources[:15]


def display_source_details(source):
    """Print detailed information for a single source."""
    print_header("SOURCE DETAILS")
    print(f"Name: {source.get('name', 'N/A')}")
    print(f"Country: {source.get('country', 'N/A').upper()}")
    print(f"Description: {source.get('description', 'N/A')}")
    print(f"URL: {source.get('url', 'N/A')}")
    print(f"Category: {source.get('category', 'N/A')}")
    print(f"Language: {source.get('language', 'N/A')}")
    print("=" * 60)


def handle_headlines_menu(sock):
    """Handle the headlines submenu loop."""
    while True:
        display_headlines_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice not in ['1', '2', '3', '4', '5']:
            print("Invalid choice. Please try again.")
            continue
        
        if not send_message(sock, choice):
            print("Connection error")
            return
        
        if choice == '5':
            break

        if choice == '1':
            receive_message(sock)  # wait for READY
            keyword = input("Enter keyword: ").strip()
            if not send_message(sock, keyword):
                print("Connection error")
                return
        
        elif choice == '2':
            receive_message(sock)
            display_categories()
            cat_choice = input("Select category number: ").strip()
            try:
                category = CATEGORIES[int(cat_choice) - 1]
                if not send_message(sock, category):
                    print("Connection error")
                    return
            except:
                print("Invalid choice.")
                continue
        
        elif choice == '3':
            receive_message(sock)
            display_countries()
            country_choice = input("Select country number: ").strip()
            try:
                country = COUNTRIES[int(country_choice) - 1]
                if not send_message(sock, country):
                    print("Connection error")
                    return
            except:
                print("Invalid choice.")
                continue
        
        print("\nFetching data from server...")
        response = receive_message(sock)
        
        if not response:
            print("Error: No response from server")
            continue
        
        try:
            data = json.loads(response)
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                article_list = display_headlines_list(articles)
                
                if article_list:
                    detail_choice = input(
                        "\nEnter article number for details (or press Enter to skip): "
                    ).strip()
                    if detail_choice.isdigit():
                        idx = int(detail_choice) - 1
                        if 0 <= idx < len(article_list):
                            display_headline_details(article_list[idx])
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON response - {e}")
        
        input("\nPress Enter to continue...")


def handle_sources_menu(sock):
    """Handle the sources submenu loop."""
    while True:
        display_sources_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice not in ['1', '2', '3', '4', '5']:
            print("Invalid choice. Please try again.")
            continue
        
        if not send_message(sock, choice):
            print("Connection error")
            return
        
        if choice == '5':
            break

        if choice == '1':
            receive_message(sock)
            display_categories()
            cat_choice = input("Select category number: ").strip()
            try:
                category = CATEGORIES[int(cat_choice) - 1]
                if not send_message(sock, category):
                    print("Connection error")
                    return
            except:
                print("Invalid choice.")
                continue
        
        elif choice == '2':
            receive_message(sock)
            display_countries()
            country_choice = input("Select country number: ").strip()
            try:
                country = COUNTRIES[int(country_choice) - 1]
                if not send_message(sock, country):
                    print("Connection error")
                    return
            except:
                print("Invalid choice.")
                continue
        
        elif choice == '3':
            receive_message(sock)
            display_languages()
            lang_choice = input("Select language number: ").strip()
            try:
                language = LANGUAGES[int(lang_choice) - 1]
                if not send_message(sock, language):
                    print("Connection error")
                    return
            except:
                print("Invalid choice.")
                continue
        
        print("\nFetching data from server...")
        response = receive_message(sock)
        
        if not response:
            print("Error: No response from server")
            continue
        
        try:
            data = json.loads(response)
            
            if data.get('status') == 'ok':
                sources = data.get('sources', [])
                source_list = display_sources_list(sources)
                
                if source_list:
                    detail_choice = input(
                        "\nEnter source number for details (or press Enter to skip): "
                    ).strip()
                    if detail_choice.isdigit():
                        idx = int(detail_choice) - 1
                        if 0 <= idx < len(source_list):
                            display_source_details(source_list[idx])
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON response - {e}")
        
        input("\nPress Enter to continue...")


def start_client():
    """Create the client socket and run the main interaction loop."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"Connecting to server at {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Connected!")
        
        client_name = input("Enter your name: ").strip()
        if not send_message(client_socket, client_name):
            print("Failed to send name")
            return
        
        response = receive_message(client_socket)
        if not response or response != "CONNECTED":
            print("Connection failed")
            return
        
        print(f"Welcome {client_name}!")

        while True:
            display_main_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice not in ['1', '2', '3']:
                print("Invalid choice. Please try again.")
                continue
            
            if not send_message(client_socket, choice):
                print("Connection error")
                break
            
            if choice == '1':
                response = receive_message(client_socket)
                if response == "HEADLINES":
                    handle_headlines_menu(client_socket)
            
            elif choice == '2':
                response = receive_message(client_socket)
                if response == "SOURCES":
                    handle_sources_menu(client_socket)
            
            elif choice == '3':
                receive_message(client_socket)
                print("\nGoodbye!")
                break
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client_socket.close()


if __name__ == "__main__":
    # This block runs only when the file is executed directly
    start_client()
