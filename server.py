# ============================================================
# Server Script - Procedural Programming (Non-OOP)
# ============================================================
# السكريبت ده بيشغل الـ Server بطريقة procedural (بدون OOP)
# الفرق بينه وبين server_oop.py: هنا كل حاجة functions منفصلة، مش classes

import socket     # للتعامل مع الشبكة
import threading  # للتعامل مع أكتر من client في نفس الوقت
import json       # للتعامل مع JSON
import struct     # لحزم البيانات
from news_handler import NewsHandler  # كلاس جلب الأخبار

# ============================================================
# الإعدادات - Settings
# ============================================================
HOST = '127.0.0.1'  # عنوان الـ IP (localhost)
PORT = 5000         # رقم المنفذ
GROUP_ID = "GB5"    # رقم المجموعة

# إنشاء object من NewsHandler (هنستخدمه في كل الدوال)
news_handler = NewsHandler()

# ============================================================
# دوال الاتصال - Communication Functions
# ============================================================

def send_message(client_socket, message):
    """
    إرسال رسالة للـ client
    
    الفكرة: نبعت طول الرسالة الأول (4 bytes) عشان الـ client يعرف قد إيه بيانات جاية
    
    Parameters:
        client_socket: الـ socket الخاص بالـ client
        message: الرسالة (string)
    
    Returns:
        True: لو الإرسال نجح
        False: لو في مشكلة
    """
    try:
        # تحويل الرسالة من string لـ bytes
        data = message.encode('utf-8')
        
        # حساب طول البيانات وتحويله لـ 4 bytes
        length = struct.pack('!I', len(data))
        
        # إرسال الطول + البيانات مع بعض
        client_socket.sendall(length + data)
        return True
    except Exception as e:
        print(f"[PROTOCOL] Send error: {e}")
        return False

def receive_message(client_socket):
    """
    استقبال رسالة من الـ client
    
    الخطوات:
    1. نستقبل أول 4 bytes (الطول)
    2. نفك الطول
    3. نستقبل البيانات الفعلية على دفعات
    
    Parameters:
        client_socket: الـ socket الخاص بالـ client
    
    Returns:
        الرسالة (string): لو الاستقبال نجح
        None: لو في مشكلة أو الاتصال قفل
    """
    try:
        # استقبال أول 4 bytes (الطول)
        raw_length = client_socket.recv(4)
        if not raw_length:
            return None  # الاتصال قفل
        
        # فك الطول من الـ 4 bytes
        length = struct.unpack('!I', raw_length)[0]
        
        # استقبال البيانات الفعلية
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
# معالجة قائمة الأخبار - Headlines Menu Handler
# ============================================================

def handle_headlines_menu(client_socket, client_name):
    """
    دالة بتتعامل مع طلبات قائمة الأخبار
    
    Parameters:
        client_socket: الـ socket
        client_name: اسم الـ client
    """
    while True:
        # استقبال اختيار الـ client
        choice = receive_message(client_socket)
        if not choice:
            break
        
        print(f"[{client_name}] Headlines request: {choice}")
        
        # ============================================================
        # الاختيار 1: بحث بكلمة مفتاحية
        # ============================================================
        if choice == '1':
            send_message(client_socket, "READY")  # إشارة للـ client: أنا جاهز
            keyword = receive_message(client_socket)  # استقبال الكلمة
            if not keyword:
                break
            
            print(f"[{client_name}] Searching headlines for keyword: {keyword}")
            
            # جلب البيانات من NewsAPI
            data = news_handler.search_headlines_by_keyword(keyword)
            
            # حفظ البيانات في JSON file
            # اسم الملف: ClientName_keyword_GroupID.json
            filename = f"{client_name}_keyword_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)
            
            # إرسال البيانات للـ client
            send_message(client_socket, json.dumps(data))
        
        # ============================================================
        # الاختيار 2: بحث حسب الفئة
        # ============================================================
        elif choice == '2':
            send_message(client_socket, "READY")
            category = receive_message(client_socket)  # استقبال الفئة
            if not category:
                break
            
            print(f"[{client_name}] Searching headlines by category: {category}")
            
            # جلب الأخبار حسب الفئة
            data = news_handler.get_headlines_by_category(category)
            filename = f"{client_name}_category_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)
            
            send_message(client_socket, json.dumps(data))
        
        # ============================================================
        # الاختيار 3: بحث حسب البلد
        # ============================================================
        elif choice == '3':
            send_message(client_socket, "READY")
            country = receive_message(client_socket)  # استقبال كود البلد
            if not country:
                break
            
            print(f"[{client_name}] Searching headlines by country: {country}")
            
            # جلب أخبار البلد
            data = news_handler.get_headlines_by_country(country)
            filename = f"{client_name}_country_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)
            
            send_message(client_socket, json.dumps(data))
        
        # ============================================================
        # الاختيار 4: كل الأخبار
        # ============================================================
        elif choice == '4':
            print(f"[{client_name}] Fetching all headlines")
            
            # جلب كل الأخبار
            data = news_handler.get_all_headlines()
            filename = f"{client_name}_all_headlines_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)
            
            send_message(client_socket, json.dumps(data))
        
        # ============================================================
        # الاختيار 5: رجوع للقائمة الرئيسية
        # ============================================================
        elif choice == '5':
            break  # نخرج من الـ loop
        
        else:
            send_message(client_socket, "ERROR")

# ============================================================
# معالجة قائمة المصادر - Sources Menu Handler
# ============================================================

def handle_sources_menu(client_socket, client_name):
    """
    دالة بتتعامل مع طلبات قائمة المصادر
    
    Parameters:
        client_socket: الـ socket
        client_name: اسم الـ client
    """
    while True:
        choice = receive_message(client_socket)
        if not choice:
            break
        
        print(f"[{client_name}] Sources request: {choice}")
        
        # الاختيار 1: بحث حسب الفئة
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
        
        # الاختيار 2: بحث حسب البلد
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
        
        # الاختيار 3: بحث حسب اللغة
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
        
        # الاختيار 4: كل المصادر
        elif choice == '4':
            print(f"[{client_name}] Fetching all sources")
            
            data = news_handler.get_all_sources()
            filename = f"{client_name}_all_sources_{GROUP_ID}.json"
            news_handler.save_to_json(data, filename)
            
            send_message(client_socket, json.dumps(data))
        
        # الاختيار 5: رجوع للقائمة الرئيسية
        elif choice == '5':
            break
        
        else:
            send_message(client_socket, "ERROR")

# ============================================================
# المعالج الرئيسي للـ Client - Main Client Handler
# ============================================================

def handle_client(client_socket, client_address):
    """
    الدالة الرئيسية اللي بتتعامل مع كل client
    بتشتغل في thread منفصل لكل client
    
    Parameters:
        client_socket: الـ socket الخاص بالـ client
        client_address: عنوان الـ client (IP + Port)
    """
    print(f"[NEW CONNECTION] {client_address} connected")
    
    # متغير لحفظ اسم الـ client
    client_name = None
    
    try:
        # ============================================================
        # الخطوة 1: استقبال اسم الـ Client
        # ============================================================
        client_name = receive_message(client_socket)
        if not client_name:
            return
        
        print(f"[CLIENT NAME] {client_name} from {client_address}")
        send_message(client_socket, "CONNECTED")  # تأكيد الاتصال
        
        # ============================================================
        # الخطوة 2: القائمة الرئيسية - Main Menu Loop
        # ============================================================
        while True:
            choice = receive_message(client_socket)
            if not choice:
                break
            
            print(f"[{client_name}] Main menu choice: {choice}")
            
            # الاختيار 1: قائمة الأخبار
            if choice == '1':
                send_message(client_socket, "HEADLINES")
                handle_headlines_menu(client_socket, client_name)
            
            # الاختيار 2: قائمة المصادر
            elif choice == '2':
                send_message(client_socket, "SOURCES")
                handle_sources_menu(client_socket, client_name)
            
            # الاختيار 3: إنهاء الاتصال
            elif choice == '3':
                print(f"[DISCONNECTED] {client_name} disconnected")
                send_message(client_socket, "BYE")
                break
            
            else:
                send_message(client_socket, "ERROR")
    
    except Exception as e:
        # لو حصل أي error
        print(f"[ERROR] {client_name if client_name else 'Unknown'}: {e}")
    
    finally:
        # في كل الأحوال، نقفل الـ socket
        client_socket.close()
        print(f"[CLOSED] Connection with {client_name if client_name else 'client'} closed")

# ============================================================
# دالة بداية الـ Server - Start Server Function
# ============================================================

def start_server():
    """
    الدالة الرئيسية لتشغيل الـ Server
    """
    # ============================================================
    # الخطوة 1: إنشاء الـ Socket
    # ============================================================
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR: عشان نقدر نعيد استخدام المنفذ بسرعة
    # مفيد لو قفلنا السيرفر وعايزين نشغله تاني بسرعة
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # ============================================================
    # الخطوة 2: ربط الـ Socket بالـ IP والـ Port
    # ============================================================
    server_socket.bind((HOST, PORT))
    
    # ============================================================
    # الخطوة 3: الاستماع للاتصالات
    # ============================================================
    # listen(3) = نقبل حد أقصى 3 clients في قائمة الانتظار
    server_socket.listen(3)
    
    # طباعة رسالة البداية
    print("=" * 60)
    print(f"NEWS SERVICE SERVER (Procedural) - Group {GROUP_ID}")
    print("=" * 60)
    print(f"Server listening on {HOST}:{PORT}")
    print("Waiting for connections...")
    print("=" * 60)
    
    try:
        # ============================================================
        # الخطوة 4: قبول الاتصالات (Loop لا نهائي)
        # ============================================================
        while True:
            # accept() بتستنى لحد ما client يتصل
            # بترجع: socket الـ client + عنوانه
            client_socket, client_address = server_socket.accept()
            
            # ============================================================
            # الخطوة 5: إنشاء Thread جديد لهذا الـ Client
            # ============================================================
            # كل client بيشتغل في thread منفصل
            # عشان نقدر نتعامل مع أكتر من client في نفس الوقت (Multithreading)
            thread = threading.Thread(
                target=handle_client,  # الدالة اللي هتشتغل في الـ thread
                args=(client_socket, client_address)  # الـ parameters
            )
            thread.start()  # بداية الـ thread
            
            # طباعة عدد الاتصالات النشطة
            # threading.active_count() - 1 لأن الـ main thread محسوب
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
    except KeyboardInterrupt:
        # لو المستخدم ضغط Ctrl+C
        print("\n[SHUTTING DOWN] Server closing...")
    
    finally:
        # في كل الأحوال، نقفل الـ server socket
        server_socket.close()
        print("[SERVER] Stopped")

# ============================================================
# نقطة البداية - Entry Point
# ============================================================

if __name__ == "__main__":
    """
    ده بيتنفذ لو شغلنا الملف مباشرة
    لو استوردنا الملف في ملف تاني، ده مش هيتنفذ
    """
    start_server()