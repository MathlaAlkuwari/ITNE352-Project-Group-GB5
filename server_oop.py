# ============================================================
# Server Script - Object Oriented Programming
# ============================================================
# السكريبت ده بيشغل الـ Server اللي بيستقبل الـ Clients

import socket     # للتعامل مع الشبكة
import threading  # للتعامل مع أكتر من client في نفس الوقت
import json       # للتعامل مع JSON
from news_handler import NewsHandler  # كلاس جلب الأخبار
from protocol import Protocol          # كلاس البروتوكول

# ============================================================
# ClientHandler Class - معالج الـ Client
# ============================================================

class ClientHandler:
    """
    الكلاس ده بيتعامل مع كل client لوحده
    كل client بيشتغل في thread منفصل
    """
    
    def __init__(self, client_socket, client_address, group_id):
        """
        Constructor - بيتنفذ لما نعمل object جديد
        
        Parameters:
            client_socket: الـ socket الخاص بالـ client
            client_address: عنوان الـ client (IP + Port)
            group_id: رقم المجموعة (GB5)
        """
        self.socket = client_socket       # الـ socket
        self.address = client_address     # العنوان
        self.group_id = group_id          # رقم المجموعة
        self.client_name = None           # اسم الـ client (هنستقبله لاحقاً)
        self.news_handler = NewsHandler() # object لجلب الأخبار
        self.protocol = Protocol()        # object للاتصال
    
    def send(self, message):
        """إرسال رسالة للـ client - wrapper function"""
        return self.protocol.send_message(self.socket, message)
    
    def receive(self):
        """استقبال رسالة من الـ client - wrapper function"""
        return self.protocol.receive_message(self.socket)
    
    # ============================================================
    # معالجة قائمة الأخبار - Headlines Menu Handler
    # ============================================================
    
    def handle_headlines_menu(self):
        """
        دالة بتتعامل مع طلبات قائمة الأخبار
        الـ client ممكن يختار:
        1. بحث بكلمة مفتاحية
        2. بحث حسب الفئة
        3. بحث حسب البلد
        4. كل الأخبار
        5. رجوع للقائمة الرئيسية
        """
        while True:  # Loop عشان نفضل نستقبل طلبات
            # استقبال اختيار الـ client
            choice = self.receive()
            if not choice:  # لو الاتصال قفل
                break
            
            # طباعة الطلب على شاشة الـ Server
            print(f"[{self.client_name}] Headlines request: {choice}")
            
            # ============================================================
            # الاختيار 1: بحث بكلمة مفتاحية
            # ============================================================
            if choice == '1':
                self.send("READY")  # نقول للـ client: أنا جاهز
                keyword = self.receive()  # استقبال الكلمة المفتاحية
                if not keyword:
                    break
                
                print(f"[{self.client_name}] Searching headlines for keyword: {keyword}")
                
                # جلب البيانات من NewsAPI
                data = self.news_handler.search_headlines_by_keyword(keyword)
                
                # حفظ البيانات في JSON file
                filename = f"{self.client_name}_keyword_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                # إرسال البيانات للـ client
                self.send(json.dumps(data))
            
            # ============================================================
            # الاختيار 2: بحث حسب الفئة
            # ============================================================
            elif choice == '2':
                self.send("READY")
                category = self.receive()  # استقبال الفئة (sports, business, etc.)
                if not category:
                    break
                
                print(f"[{self.client_name}] Searching headlines by category: {category}")
                
                # جلب الأخبار حسب الفئة
                data = self.news_handler.get_headlines_by_category(category)
                filename = f"{self.client_name}_category_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # ============================================================
            # الاختيار 3: بحث حسب البلد
            # ============================================================
            elif choice == '3':
                self.send("READY")
                country = self.receive()  # استقبال كود البلد (sa, us, ae, etc.)
                if not country:
                    break
                
                print(f"[{self.client_name}] Searching headlines by country: {country}")
                
                # جلب أخبار البلد
                data = self.news_handler.get_headlines_by_country(country)
                filename = f"{self.client_name}_country_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # ============================================================
            # الاختيار 4: كل الأخبار
            # ============================================================
            elif choice == '4':
                print(f"[{self.client_name}] Fetching all headlines")
                
                # جلب كل الأخبار
                data = self.news_handler.get_all_headlines()
                filename = f"{self.client_name}_all_headlines_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # ============================================================
            # الاختيار 5: رجوع للقائمة الرئيسية
            # ============================================================
            elif choice == '5':
                break  # نخرج من الـ loop ونرجع للقائمة الرئيسية
            
            else:
                # اختيار غلط
                self.send("ERROR")
    
    # ============================================================
    # معالجة قائمة المصادر - Sources Menu Handler
    # ============================================================
    
    def handle_sources_menu(self):
        """
        دالة بتتعامل مع طلبات قائمة المصادر
        الـ client ممكن يختار:
        1. بحث حسب الفئة
        2. بحث حسب البلد
        3. بحث حسب اللغة
        4. كل المصادر
        5. رجوع للقائمة الرئيسية
        """
        while True:
            choice = self.receive()
            if not choice:
                break
            
            print(f"[{self.client_name}] Sources request: {choice}")
            
            # الاختيار 1: بحث حسب الفئة
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
            
            # الاختيار 2: بحث حسب البلد
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
            
            # الاختيار 3: بحث حسب اللغة
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
            
            # الاختيار 4: كل المصادر
            elif choice == '4':
                print(f"[{self.client_name}] Fetching all sources")
                
                data = self.news_handler.get_all_sources()
                filename = f"{self.client_name}_all_sources_{self.group_id}.json"
                self.news_handler.save_to_json(data, filename)
                
                self.send(json.dumps(data))
            
            # الاختيار 5: رجوع للقائمة الرئيسية
            elif choice == '5':
                break
            
            else:
                self.send("ERROR")
    
    # ============================================================
    # المعالج الرئيسي للـ Client - Main Handler
    # ============================================================
    
    def handle(self):
        """
        الدالة الرئيسية اللي بتتعامل مع الـ client
        بتشتغل في thread منفصل لكل client
        """
        print(f"[NEW CONNECTION] {self.address} connected")
        
        try:
            # ============================================================
            # الخطوة 1: استقبال اسم الـ Client
            # ============================================================
            self.client_name = self.receive()
            if not self.client_name:
                return
            
            print(f"[CLIENT NAME] {self.client_name} from {self.address}")
            self.send("CONNECTED")  # تأكيد الاتصال
            
            # ============================================================
            # الخطوة 2: القائمة الرئيسية - Main Menu Loop
            # ============================================================
            while True:
                choice = self.receive()  # استقبال الاختيار
                if not choice:
                    break
                
                print(f"[{self.client_name}] Main menu choice: {choice}")
                
                # الاختيار 1: قائمة الأخبار
                if choice == '1':
                    self.send("HEADLINES")
                    self.handle_headlines_menu()  # ندخل على قائمة الأخبار
                
                # الاختيار 2: قائمة المصادر
                elif choice == '2':
                    self.send("SOURCES")
                    self.handle_sources_menu()  # ندخل على قائمة المصادر
                
                # الاختيار 3: إنهاء الاتصال
                elif choice == '3':
                    print(f"[DISCONNECTED] {self.client_name} disconnected")
                    self.send("BYE")
                    break  # نخرج من الـ loop
                
                else:
                    self.send("ERROR")
        
        except Exception as e:
            # لو حصل أي error، نطبعه
            print(f"[ERROR] {self.client_name if self.client_name else 'Unknown'}: {e}")
        
        finally:
            # في كل الأحوال، نقفل الـ socket
            self.socket.close()
            print(f"[CLOSED] Connection with {self.client_name} closed")


# ============================================================
# NewsServer Class - السيرفر الرئيسي
# ============================================================

class NewsServer:
    """
    الكلاس الرئيسي للـ Server
    مسؤول عن قبول الاتصالات وإنشاء threads للـ clients
    """
    
    def __init__(self, host='127.0.0.1', port=5000, group_id="GB5"):
        """
        Constructor
        
        Parameters:
            host: عنوان الـ IP (localhost = 127.0.0.1)
            port: رقم المنفذ (5000)
            group_id: رقم المجموعة (GB5)
        """
        self.host = host
        self.port = port
        self.group_id = group_id
        self.server_socket = None  # الـ socket الرئيسي
        self.is_running = False    # حالة الـ Server (شغال / مش شغال)
    
    def start(self):
        """
        بداية تشغيل الـ Server
        """
        # ============================================================
        # الخطوة 1: إنشاء الـ Socket
        # ============================================================
        # AF_INET = IPv4, SOCK_STREAM = TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # SO_REUSEADDR: عشان نقدر نعيد استخدام المنفذ بسرعة
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # ============================================================
        # الخطوة 2: ربط الـ Socket بالـ IP والـ Port
        # ============================================================
        self.server_socket.bind((self.host, self.port))
        
        # ============================================================
        # الخطوة 3: الاستماع للاتصالات
        # ============================================================
        # listen(3) = نقبل حد أقصى 3 clients في قائمة الانتظار
        self.server_socket.listen(3)
        self.is_running = True
        
        # طباعة رسالة البداية
        self.print_banner()
        
        try:
            # ============================================================
            # الخطوة 4: قبول الاتصالات (Loop لا نهائي)
            # ============================================================
            while self.is_running:
                # accept() بتستنى لحد ما client يتصل
                # بترجع: socket الـ client + عنوانه
                client_socket, client_address = self.server_socket.accept()
                
                # ============================================================
                # الخطوة 5: إنشاء ClientHandler لهذا الـ Client
                # ============================================================
                client_handler = ClientHandler(
                    client_socket, 
                    client_address, 
                    self.group_id
                )
                
                # ============================================================
                # الخطوة 6: إنشاء Thread جديد لهذا الـ Client
                # ============================================================
                # كل client بيشتغل في thread منفصل
                # عشان نقدر نتعامل مع أكتر من client في نفس الوقت
                thread = threading.Thread(target=client_handler.handle)
                thread.start()  # بداية الـ Thread
                
                # طباعة عدد الاتصالات النشطة
                # threading.active_count() - 1 لأن الـ main thread محسوب
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        
        except KeyboardInterrupt:
            # لو المستخدم ضغط Ctrl+C
            print("\n[SHUTTING DOWN] Server closing...")
            self.stop()
        
        except Exception as e:
            print(f"[SERVER ERROR] {e}")
            self.stop()
    
    def stop(self):
        """
        إيقاف الـ Server
        """
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        print("[SERVER] Stopped")
    
    def print_banner(self):
        """
        طباعة رسالة بداية الـ Server
        """
        print("=" * 60)
        print(f"NEWS SERVICE SERVER (OOP) - Group {self.group_id}")
        print("=" * 60)
        print(f"Server listening on {self.host}:{self.port}")
        print("Waiting for connections...")
        print("=" * 60)


# ============================================================
# Main Function - نقطة البداية
# ============================================================

def main():
    """
    الدالة الرئيسية - نقطة بداية البرنامج
    """
    # إنشاء object من NewsServer
    server = NewsServer(host='127.0.0.1', port=5000, group_id="GB5")
    
    # بداية تشغيل الـ Server
    server.start()


# ============================================================
# تشغيل البرنامج
# ============================================================
if __name__ == "__main__":
    # ده بيتنفذ لو شغلنا الملف مباشرة
    # لو استوردنا الملف في ملف تاني، ده مش هيتنفذ
    main()