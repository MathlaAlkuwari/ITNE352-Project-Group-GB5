# ============================================================
# Client Script - Procedural Programming (Non-OOP)
# ============================================================
# السكريبت ده بيشغل الـ Client بطريقة procedural (بدون OOP)
# الفرق بينه وبين client_oop.py: هنا كل حاجة functions منفصلة، مش classes

import socket       # للتعامل مع الشبكة
import json         # للتعامل مع JSON
import struct       # لحزم البيانات
from datetime import datetime  # للتعامل مع التواريخ

# ============================================================
# الإعدادات والثوابت - Settings and Constants
# ============================================================
HOST = '127.0.0.1'  # عنوان الـ Server
PORT = 5000         # رقم المنفذ

# القوائم الثابتة
COUNTRIES = ['au', 'ca', 'jp', 'ae', 'sa', 'kr', 'us', 'ma']
LANGUAGES = ['ar', 'en']
CATEGORIES = ['business', 'general', 'health', 'science', 'sports', 'technology']

# ============================================================
# دوال الاتصال - Communication Functions
# ============================================================

def send_message(sock, message):
    """
    إرسال رسالة للـ Server
    
    Parameters:
        sock: الـ socket
        message: الرسالة (string)
    
    Returns:
        True: لو الإرسال نجح
        False: لو في مشكلة
    """
    try:
        data = message.encode('utf-8')
        length = struct.pack('!I', len(data))
        sock.sendall(length + data)
        return True
    except Exception as e:
        print(f"Send error: {e}")
        return False

def receive_message(sock):
    """
    استقبال رسالة من الـ Server
    
    Parameters:
        sock: الـ socket
    
    Returns:
        الرسالة (string): لو الاستقبال نجح
        None: لو في مشكلة
    """
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

# ============================================================
# دوال عرض القوائم - Menu Display Functions
# ============================================================

def print_header(title):
    """طباعة عنوان منسق"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def display_main_menu():
    """عرض القائمة الرئيسية"""
    print_header("MAIN MENU")
    print("1. Search for headlines")
    print("2. List of sources")
    print("3. Quit")
    print("-" * 60)

def display_headlines_menu():
    """عرض قائمة الأخبار"""
    print_header("HEADLINES MENU")
    print("1. Search by keyword")
    print("2. Search by category")
    print("3. Search by country")
    print("4. List all headlines")
    print("5. Back to main menu")
    print("-" * 60)

def display_sources_menu():
    """عرض قائمة المصادر"""
    print_header("SOURCES MENU")
    print("1. Search by category")
    print("2. Search by country")
    print("3. Search by language")
    print("4. List all sources")
    print("5. Back to main menu")
    print("-" * 60)

def display_categories():
    """عرض الفئات المتاحة"""
    print("\nAvailable categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")

def display_countries():
    """عرض الدول المتاحة"""
    print("\nAvailable countries:")
    countries_map = {
        'au': 'Australia', 'ca': 'Canada', 'jp': 'Japan', 'ae': 'UAE',
        'sa': 'Saudi Arabia', 'kr': 'South Korea', 'us': 'USA', 'ma': 'Morocco'
    }
    for i, code in enumerate(COUNTRIES, 1):
        print(f"{i}. {countries_map[code]} ({code})")

def display_languages():
    """عرض اللغات المتاحة"""
    print("\nAvailable languages:")
    print("1. Arabic (ar)")
    print("2. English (en)")

# ============================================================
# دوال عرض البيانات - Data Display Functions
# ============================================================

def display_headlines_list(articles):
    """
    عرض قائمة الأخبار
    
    Parameters:
        articles: list فيها الأخبار
    
    Returns:
        list: أول 15 خبر
    """
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
    """
    عرض تفاصيل خبر واحد
    
    Parameters:
        article: dictionary فيه بيانات الخبر
    """
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
    """
    عرض قائمة المصادر
    
    Parameters:
        sources: list فيها المصادر
    
    Returns:
        list: أول 15 مصدر
    """
    print_header("SOURCES")
    
    if not sources:
        print("No sources found.")
        return []
    
    for i, source in enumerate(sources[:15], 1):
        print(f"{i}. {source.get('name', 'N/A')}")
        print("-" * 60)
    
    return sources[:15]

def display_source_details(source):
    """
    عرض تفاصيل مصدر واحد
    
    Parameters:
        source: dictionary فيه بيانات المصدر
    """
    print_header("SOURCE DETAILS")
    print(f"Name: {source.get('name', 'N/A')}")
    print(f"Country: {source.get('country', 'N/A').upper()}")
    print(f"Description: {source.get('description', 'N/A')}")
    print(f"URL: {source.get('url', 'N/A')}")
    print(f"Category: {source.get('category', 'N/A')}")
    print(f"Language: {source.get('language', 'N/A')}")
    print("=" * 60)

# ============================================================
# معالجة قائمة الأخبار - Headlines Menu Handler
# ============================================================

def handle_headlines_menu(sock):
    """
    التعامل مع قائمة الأخبار
    
    Parameters:
        sock: الـ socket المتصل بالـ Server
    """
    while True:
        display_headlines_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice not in ['1', '2', '3', '4', '5']:
            print("Invalid choice. Please try again.")
            continue
        
        if not send_message(sock, choice):
            print("Connection error")
            return
        
        if choice == '5':  # رجوع
            break
        
        # معالجة الاختيارات
        if choice == '1':  # بحث بكلمة مفتاحية
            receive_message(sock)  # انتظار READY
            keyword = input("Enter keyword: ").strip()
            if not send_message(sock, keyword):
                print("Connection error")
                return
        
        elif choice == '2':  # بحث حسب الفئة
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
        
        elif choice == '3':  # بحث حسب البلد
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
        
        # استقبال وعرض النتائج
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
                    detail_choice = input("\nEnter article number for details (or press Enter to skip): ").strip()
                    if detail_choice.isdigit():
                        idx = int(detail_choice) - 1
                        if 0 <= idx < len(article_list):
                            display_headline_details(article_list[idx])
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON response - {e}")
        
        input("\nPress Enter to continue...")

# ============================================================
# معالجة قائمة المصادر - Sources Menu Handler
# ============================================================

def handle_sources_menu(sock):
    """
    التعامل مع قائمة المصادر
    
    Parameters:
        sock: الـ socket المتصل بالـ Server
    """
    while True:
        display_sources_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice not in ['1', '2', '3', '4', '5']:
            print("Invalid choice. Please try again.")
            continue
        
        if not send_message(sock, choice):
            print("Connection error")
            return
        
        if choice == '5':  # رجوع
            break
        
        # معالجة الاختيارات
        if choice == '1':  # بحث حسب الفئة
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
        
        elif choice == '2':  # بحث حسب البلد
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
        
        elif choice == '3':  # بحث حسب اللغة
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
        
        # استقبال وعرض النتائج
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
                    detail_choice = input("\nEnter source number for details (or press Enter to skip): ").strip()
                    if detail_choice.isdigit():
                        idx = int(detail_choice) - 1
                        if 0 <= idx < len(source_list):
                            display_source_details(source_list[idx])
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON response - {e}")
        
        input("\nPress Enter to continue...")

# ============================================================
# الدالة الرئيسية - Main Client Function
# ============================================================

def start_client():
    """
    الدالة الرئيسية لتشغيل الـ Client
    """
    # إنشاء socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # الاتصال بالـ Server
        print(f"Connecting to server at {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Connected!")
        
        # إرسال اسم المستخدم
        client_name = input("Enter your name: ").strip()
        if not send_message(client_socket, client_name):
            print("Failed to send name")
            return
        
        # انتظار تأكيد
        response = receive_message(client_socket)
        if not response or response != "CONNECTED":
            print("Connection failed")
            return
        
        print(f"Welcome {client_name}!")
        
        # ============================================================
        # القائمة الرئيسية - Main Menu Loop
        # ============================================================
        while True:
            display_main_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice not in ['1', '2', '3']:
                print("Invalid choice. Please try again.")
                continue
            
            if not send_message(client_socket, choice):
                print("Connection error")
                break
            
            # الاختيار 1: قائمة الأخبار
            if choice == '1':
                response = receive_message(client_socket)
                if response == "HEADLINES":
                    handle_headlines_menu(client_socket)
            
            # الاختيار 2: قائمة المصادر
            elif choice == '2':
                response = receive_message(client_socket)
                if response == "SOURCES":
                    handle_sources_menu(client_socket)
            
            # الاختيار 3: إنهاء
            elif choice == '3':
                receive_message(client_socket)
                print("\nGoodbye!")
                break
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # قفل الاتصال
        client_socket.close()

# ============================================================
# نقطة البداية - Entry Point
# ============================================================

if __name__ == "__main__":
    """
    ده بيتنفذ لو شغلنا الملف مباشرة
    """
    start_client()