# News Service System - Client/Server Project

## Project Description
A Python-based client-server application that provides real-time news information using the NewsAPI.org service. The system allows multiple clients to simultaneously connect to a central server and retrieve news headlines and sources based on various search criteria including keywords, categories, countries, and languages.

The project implements network programming concepts including TCP socket communication, multithreading for concurrent client handling, JSON data processing, and RESTful API integration.

---

## Semester
**Semester 1, Academic Year 2025-2026**

---

## Group Information
- **Group Name:** GB5
- **Course Code:** ITNE352
- **Section:** [2]

### Team Members:
1. **Student Name:** Mathla Fadhel Alkuwari  
   **Student ID:** 202305249

2. **Student Name:** Noor Aljenaid  
   **Student ID:** 202109013

---

## Table of Contents
1. [Project Description](#project-description)
2. [Requirements](#requirements)
3. [How to Run](#how-to-run)
4. [The Scripts](#the-scripts)
5. [Additional Concept: OOP](#additional-concept-oop)
6. [Project Structure](#project-structure)
7. [Acknowledgments](#acknowledgments)
8. [Conclusion](#conclusion)

---

## Requirements

### Software Requirements:
- **Python 3.7+** (tested on Python 3.8 and above)
- **pip** (Python package manager)

### Python Libraries:
Install the required libraries using:
```bash
pip install requests
```

### NewsAPI Key:
1. Register at [https://newsapi.org/register](https://newsapi.org/register)
2. Obtain your free API key
3. Add it to `config.py` file

### File Structure:
Ensure you have the following files in your project directory:
```
ClientServer/
├── config.py
├── protocol.py
├── news_handler.py
├── server_oop.py
├── client_oop.py
├── server.py (optional - non-OOP version)
├── client.py (optional - non-OOP version)
└── README.md
```

---

## How to Run

### Step 1: Configure the API Key
Edit `config.py` and add your NewsAPI key:
```python
NEWS_API_KEY = "a7e07d89e99a46b7b42ef4d59655df86"
NEWS_API_BASE_URL = "https://newsapi.org/v2"
```

Also, set your group ID in `server_oop.py`:
```python
server = NewsServer(host='127.0.0.1', port=5000, group_id="GB5")
```

### Step 2: Start the Server
Open a terminal and run:
```bash
python server_oop.py
```

You should see:
```
============================================================
NEWS SERVICE SERVER (OOP) - Group GB5
============================================================
Server listening on 127.0.0.1:5000
Waiting for connections...
============================================================
```

### Step 3: Start the Client(s)
Open **another terminal** (or multiple terminals for testing concurrent connections) and run:
```bash
python client_oop.py
```

You will be prompted to:
1. Enter your name
2. Navigate through menus to search for news

### Step 4: Test Multithreading
To test concurrent connections, open **3 separate terminals** and run the client in each one simultaneously.

---

## The Scripts

### 1. `config.py`
**Purpose:** Configuration file storing API credentials and endpoints.

**Key Components:**
```python
NEWS_API_KEY = "a7e07d89e99a46b7b42ef4d59655df86"
NEWS_API_BASE_URL = "https://newsapi.org/v2"
```

---

### 2. `protocol.py`
**Purpose:** Handles network communication protocol with length-prefix messaging.

**Main Class:** `Protocol`

**Key Methods:**
- `send_message(sock, message)`: Sends messages with a 4-byte length prefix
- `receive_message(sock)`: Receives messages and reconstructs them from chunks

**How it works:**
```python
# Sending
data = message.encode('utf-8')
length = struct.pack('!I', len(data))  # 4-byte unsigned int
sock.sendall(length + data)

# Receiving
raw_length = sock.recv(4)
length = struct.unpack('!I', raw_length)[0]
# Then receive 'length' bytes of actual data
```

This ensures large JSON responses are transmitted correctly without truncation.

---

### 3. `news_handler.py`
**Purpose:** Handles all interactions with the NewsAPI service.

**Main Class:** `NewsHandler`

**Key Methods:**
- `get_headlines(**params)`: Fetch top headlines
- `get_sources(**params)`: Fetch news sources
- `search_headlines_by_keyword(keyword, country)`: Search news by keyword
- `get_headlines_by_category(category, country)`: Get headlines filtered by category
- `get_headlines_by_country(country)`: Get country-specific headlines
- `get_sources_by_category(category)`: Get sources by category
- `get_sources_by_language(language)`: Get sources by language
- `save_to_json(data, filename)`: Save API responses to JSON files

**Utilized Packages:**
- `requests`: For making HTTP requests to NewsAPI
- `json`: For parsing and saving JSON data

**Example Usage:**
```python
news = NewsHandler()
data = news.get_headlines_by_category('sports', 'us')
news.save_to_json(data, 'sports_headlines.json')
```

---

### 4. `server_oop.py`
**Purpose:** Main server script using Object-Oriented Programming.

**Main Classes:**

#### `ClientHandler`
Handles individual client connections in separate threads.

**Attributes:**
- `socket`: Client socket connection
- `address`: Client address
- `client_name`: Name of connected client
- `news_handler`: Instance of NewsHandler
- `protocol`: Instance of Protocol for communication

**Key Methods:**
- `handle()`: Main handler for client lifecycle
- `handle_headlines_menu()`: Process headlines-related requests
- `handle_sources_menu()`: Process sources-related requests
- `send(message)`: Wrapper for protocol send
- `receive()`: Wrapper for protocol receive

#### `NewsServer`
Main server class that manages connections.

**Attributes:**
- `host`: Server IP address (default: 127.0.0.1)
- `port`: Server port (default: 5000)
- `group_id`: Group identifier for file naming
- `server_socket`: Main server socket
- `is_running`: Server state flag

**Key Methods:**
- `start()`: Initialize and start the server
- `stop()`: Gracefully shutdown the server
- `print_banner()`: Display startup information

**Threading Implementation:**
```python
thread = threading.Thread(target=client_handler.handle)
thread.start()
```
Each client connection runs in its own thread, allowing concurrent handling of up to 3 clients.

**Utilized Packages:**
- `socket`: TCP socket programming
- `threading`: Concurrent client handling
- `json`: JSON data processing
- `struct`: Binary data packing for protocol

---

### 5. `client_oop.py`
**Purpose:** Client-side application using OOP principles.

**Main Classes:**

#### `MenuDisplay`
Handles all menu display and user interface formatting.

**Class Attributes:**
- `COUNTRIES`: List of supported country codes
- `LANGUAGES`: List of supported languages
- `CATEGORIES`: List of news categories

**Key Methods:**
- `display_main_menu()`: Show main menu
- `display_headlines_menu()`: Show headlines options
- `display_sources_menu()`: Show sources options
- `display_categories()`: Show available categories
- `display_countries()`: Show available countries
- `display_languages()`: Show available languages
- `print_header(title)`: Format section headers

#### `NewsDisplay`
Handles display of news data received from server.

**Key Methods:**
- `display_headlines_list(articles)`: Show list of articles
- `display_headline_details(article)`: Show detailed article info
- `display_sources_list(sources)`: Show list of sources
- `display_source_details(source)`: Show detailed source info

#### `NewsClient`
Main client class managing server connection and user interaction.

**Attributes:**
- `host`: Server IP address
- `port`: Server port
- `socket`: Client socket
- `protocol`: Protocol instance
- `client_name`: User's name
- `menu_display`: MenuDisplay instance
- `news_display`: NewsDisplay instance

**Key Methods:**
- `connect()`: Establish connection with server
- `disconnect()`: Close connection
- `run()`: Main client loop
- `handle_headlines_menu()`: Process headlines menu interactions
- `handle_sources_menu()`: Process sources menu interactions
- `process_headlines_response()`: Display headlines data
- `process_sources_response()`: Display sources data
- `send(message)`: Send message to server
- `receive()`: Receive message from server

**User Flow:**
1. Connect to server and authenticate with name
2. Navigate main menu (Headlines/Sources/Quit)
3. Select search criteria
4. View list of results (max 15)
5. Optionally view detailed information
6. Return to menus or quit

**Utilized Packages:**
- `socket`: Network communication
- `json`: Parse JSON responses
- `datetime`: Format publication dates/times
- `struct`: Binary data handling

---

## Additional Concept: OOP

### What is Object-Oriented Programming?

Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects" that contain data (attributes) and code (methods). It focuses on organizing code into reusable, modular structures.

### Core OOP Principles in Python:

#### 1. **Classes and Objects**
A class is a blueprint for creating objects.

```python
class NewsServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def start(self):
        # Server logic here
        pass
```

#### 2. **Encapsulation**
Bundling data and methods that operate on that data within a single unit (class).

```python
class ClientHandler:
    def __init__(self, socket, address):
        self.socket = socket      # Private data
        self.address = address    # Encapsulated
    
    def send(self, message):      # Public method
        # Only this class manages socket communication
        pass
```

#### 3. **Inheritance**
Creating new classes based on existing ones (not heavily used in this project but available).

```python
class BaseHandler:
    def log(self, message):
        print(message)

class ClientHandler(BaseHandler):  # Inherits from BaseHandler
    def handle(self):
        self.log("Handling client")  # Uses inherited method
```

#### 4. **Modularity**
Breaking code into separate, manageable pieces.

**Our Implementation:**
- `Protocol` class: Handles communication
- `NewsHandler` class: Handles API requests
- `ClientHandler` class: Handles individual clients
- `NewsServer` class: Manages the server
- `MenuDisplay` class: Handles UI
- `NewsDisplay` class: Handles data display
- `NewsClient` class: Manages client operations

### Benefits of OOP in Our Project:

1. **Code Reusability**
   - `Protocol` class is used by both server and client
   - Same methods for send/receive in both applications

2. **Easier Maintenance**
   - Need to change communication protocol? Only modify `Protocol` class
   - Need to update menu display? Only modify `MenuDisplay` class

3. **Better Organization**
   - Each class has a single, clear responsibility
   - Server logic is separate from client logic
   - Communication logic is separate from business logic

4. **Scalability**
   - Easy to add new menu options by extending `MenuDisplay`
   - Easy to add new API endpoints by extending `NewsHandler`
   - Easy to add new client types by inheriting from `NewsClient`

### Comparison: Procedural vs OOP

**Before (Procedural - `server.py`):**
```python
def send_message(socket, message):
    # send logic

def receive_message(socket):
    # receive logic

def handle_client(socket, address):
    # handle logic
    send_message(socket, "Hello")
    data = receive_message(socket)
```

**After (OOP - `server_oop.py`):**
```python
class ClientHandler:
    def __init__(self, socket, address):
        self.socket = socket
        self.protocol = Protocol()
    
    def handle(self):
        self.protocol.send_message(self.socket, "Hello")
        data = self.protocol.receive_message(self.socket)
```

The OOP version is more organized, with related data and functions grouped together.

### Class Diagram:

```
┌─────────────────┐
│   NewsServer    │
│─────────────────│
│ - host          │
│ - port          │
│ - server_socket │
│─────────────────│
│ + start()       │
│ + stop()        │
└────────┬────────┘
         │ creates
         ▼
┌─────────────────┐
│ ClientHandler   │
│─────────────────│
│ - socket        │
│ - address       │
│ - client_name   │
│─────────────────│
│ + handle()      │
│ + send()        │
│ + receive()     │
└────────┬────────┘
         │ uses
         ▼
┌─────────────────┐      ┌─────────────────┐
│   Protocol      │      │  NewsHandler    │
│─────────────────│      │─────────────────│
│ + send_message()│      │ + get_headlines()│
│ + receive()     │      │ + get_sources() │
└─────────────────┘      └─────────────────┘
```

---

## Project Structure

```
ClientServer/
│
├── config.py                 # API configuration
├── protocol.py               # Communication protocol (OOP)
├── news_handler.py           # NewsAPI handler (OOP)
│
├── server_oop.py            # Server with OOP implementation
├── client_oop.py            # Client with OOP implementation
│
├── server.py                # Server (procedural - optional)
├── client.py                # Client (procedural - optional)
│
├── test_api.py              # API testing script
│
├── README.md                # This file
│
└── Generated JSON files:
    ├── [ClientName]_keyword_[GroupID].json
    ├── [ClientName]_category_[GroupID].json
    ├── [ClientName]_country_[GroupID].json
    └── ... (other generated files)
```

---

## Acknowledgments

- **NewsAPI.org** for providing the news API service
- **Dr. Mohammed Almeer** for project guidance and instruction
- **University of Bahrain** - College of IT, Department of Computer Engineering
- **Python Documentation** for reference materials
- **Threading and Socket Programming tutorials** for implementation guidance

---

## Conclusion

This project successfully demonstrates the implementation of a client-server architecture using Python's socket programming capabilities. The system effectively handles multiple concurrent client connections through multithreading, retrieves real-time data from external APIs, and presents information in a user-friendly manner.

### Key Achievements:
-Implemented robust TCP socket communication with custom protocol  
-Successfully integrated NewsAPI for real-time data retrieval  
-Achieved concurrent client handling using Python threading  
-Applied Object-Oriented Programming principles for clean, maintainable code  
-Created intuitive user interface with organized menu navigation  
-Implemented proper error handling and connection management  

### Learning Outcomes:
Through this project, we gained hands-on experience in:
- Network programming and socket communication
- Multithreading and concurrent programming
- RESTful API integration and JSON processing
- Object-oriented design and implementation
- Client-server architecture patterns
- Protocol design and implementation

### Future Enhancements:
Potential improvements for future versions:
- Implement SSL/TLS for secure communication
- Add caching mechanism for frequently requested data
- Create a GUI using Tkinter or PyQt
- Implement user authentication and session management
- Add database storage for persistent data
- Support for more NewsAPI endpoints and features

---

**Course:** ITNE352 - Network Programming  
**Instructor:** Dr. Mohammed Almeer  
**Institution:** University of Bahrain - College of IT  
**Git-Hub:**  "https://github.com/MathlaAlkuwari/ITNE352-Project-Group-GB5.git" 
