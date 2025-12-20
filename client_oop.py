# ============================================================
# Client Script - Object Oriented Programming
# ============================================================
# السكريبت ده بيشغل الـ Client اللي بيتصل بالـ Server

import socket       # للتعامل مع الشبكة
import json         # للتعامل مع JSON
import struct       # لحزم البيانات
from datetime import datetime  # للتعامل مع التواريخ
from protocol import Protocol  # كلاس البروتوكول

# ============================================================
# MenuDisplay Class - عرض القوائم
# ============================================================

class MenuDisplay:
    """
    الكلاس ده مسؤول عن عرض القوائم والواجهة للمستخدم
    فصلناه في class منفصل عشان الكود يكون منظم (OOP)
    """
    
    # ============================================================
    # الثوابت - Constants
    # ============================================================
    # القوائم دي ثابتة ومش هتتغير، عشان كده عملناها class attributes
    
    COUNTRIES = ['au', 'ca', 'jp', 'ae', 'sa', 'kr', 'us', 'ma']
    # أستراليا، كندا، اليابان، الإمارات، السعودية، كوريا، أمريكا، المغرب
    
    LANGUAGES = ['ar', 'en']
    # عربي، إنجليزي
    
    CATEGORIES = ['business', 'general', 'health', 'science', 'sports', 'technology']
    # أعمال، عام، صحة، علوم، رياضة، تكنولوجيا
    
    # ============================================================
    # دوال العرض - Display Functions
    # ============================================================
    
    @staticmethod
    def print_header(title):
        """
        طباعة عنوان منسق
        @staticmethod: دالة ثابتة مش محتاجة object
        """
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    @staticmethod
    def display_main_menu():
        """عرض القائمة الرئيسية"""
        MenuDisplay.print_header("MAIN MENU")
        print("1. Search for headlines")
        print("2. List of sources")
        print("3. Quit")
        print("-" * 60)
    
    @staticmethod
    def display_headlines_menu():
        """عرض قائمة الأخبار"""
        MenuDisplay.print_header("HEADLINES MENU")
        print("1. Search by keyword")
        print("2. Search by category")
        print("3. Search by country")
        print("4. List all headlines")
        print("5. Back to main menu")
        print("-" * 60)
    
    @staticmethod
    def display_sources_menu():
        """عرض قائمة المصادر"""
        MenuDisplay.print_header("SOURCES MENU")
        print("1. Search by category")
        print("2. Search by country")
        print("3. Search by language")
        print("4. List all sources")
        print("5. Back to main menu")
        print("-" * 60)
    
    @staticmethod
    def display_categories():
        """عرض الفئات المتاحة"""
        print("\nAvailable categories:")
        for i, cat in enumerate(MenuDisplay.CATEGORIES, 1):
            print(f"{i}. {cat}")
    
    @staticmethod
    def display_countries():
        """عرض الدول المتاحة"""
        print("\nAvailable countries:")
        # قاموس لترجمة أكواد الدول
        countries_map = {
            'au': 'Australia',
            'ca': 'Canada',
            'jp': 'Japan',
            'ae': 'UAE',
            'sa': 'Saudi Arabia',
            'kr': 'South Korea',
            'us': 'USA',
            'ma': 'Morocco'
        }
        for i, code in enumerate(MenuDisplay.COUNTRIES, 1):
            print(f"{i}. {countries_map[code]} ({code})")
    
    @staticmethod
    def display_languages():
        """عرض اللغات المتاحة"""
        print("\nAvailable languages:")
        print("1. Arabic (ar)")
        print("2. English (en)")


# ============================================================
# NewsDisplay Class - عرض الأخبار
# ============================================================

class NewsDisplay:
    """
    الكلاس ده مسؤول عن عرض بيانات الأخبار والمصادر
    منفصل عن MenuDisplay عشان كل واحد ليه مسؤولية واحدة (OOP Principle)
    """
    
    @staticmethod
    def display_headlines_list(articles):
        """
        عرض قائمة الأخبار
        
        Parameters:
            articles: list فيها الأخبار (من الـ API)
        
        Returns:
            list: أول 15 خبر بس (حسب المطلوب في المشروع)
        """
        MenuDisplay.print_header("HEADLINES")
        
        if not articles:
            print("No articles found.")
            return []
        
        # عرض أول 15 خبر فقط
        for i, article in enumerate(articles[:15], 1):
            print(f"\n{i}. Title: {article.get('title', 'N/A')}")
            print(f"   Source: {article.get('source', {}).get('name', 'N/A')}")
            print(f"   Author: {article.get('author', 'N/A')}")
            print("-" * 60)
        
        return articles[:15]
    
    @staticmethod
    def display_headline_details(article):
        """
        عرض تفاصيل خبر واحد
        
        Parameters:
            article: dictionary فيه بيانات الخبر
        """
        MenuDisplay.print_header("HEADLINE DETAILS")
        print(f"Title: {article.get('title', 'N/A')}")
        print(f"Source: {article.get('source', {}).get('name', 'N/A')}")
        print(f"Author: {article.get('author', 'N/A')}")
        print(f"Description: {article.get('description', 'N/A')}")
        print(f"URL: {article.get('url', 'N/A')}")
        
        # التعامل مع تاريخ النشر
        published_at = article.get('publishedAt', 'N/A')
        if published_at != 'N/A':
            try:
                # تحويل النص لـ datetime object
                dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                print(f"Published Date: {dt.strftime('%Y-%m-%d')}")
                print(f"Published Time: {dt.strftime('%H:%M:%S')}")
            except:
                # لو فشل التحويل، نعرض النص زي ما هو
                print(f"Published: {published_at}")
        print("=" * 60)
    
    @staticmethod
    def display_sources_list(sources):
        """
        عرض قائمة المصادر
        
        Parameters:
            sources: list فيها المصادر
        
        Returns:
            list: أول 15 مصدر
        """
        MenuDisplay.print_header("SOURCES")
        
        if not sources:
            print("No sources found.")
            return []
        
        # عرض أول 15 مصدر فقط
        for i, source in enumerate(sources[:15], 1):
            print(f"{i}. {source.get('name', 'N/A')}")
            print("-" * 60)
        
        return sources[:15]
    
    @staticmethod
    def display_source_details(source):
        """
        عرض تفاصيل مصدر واحد
        
        Parameters:
            source: dictionary فيه بيانات المصدر
        """
        MenuDisplay.print_header("SOURCE DETAILS")
        print(f"Name: {source.get('name', 'N/A')}")
        print(f"Country: {source.get('country', 'N/A').upper()}")
        print(f"Description: {source.get('description', 'N/A')}")
        print(f"URL: {source.get('url', 'N/A')}")
        print(f"Category: {source.get('category', 'N/A')}")
        print(f"Language: {source.get('language', 'N/A')}")
        print("=" * 60)


# ============================================================
# NewsClient Class - الـ Client الرئيسي
# ============================================================

class NewsClient:
    """
    الكلاس الرئيسي للـ Client
    بيتعامل مع الاتصال بالـ Server والتفاعل مع المستخدم
    """
    
    def __init__(self, host='127.0.0.1', port=5000):
        """
        Constructor
        
        Parameters:
            host: عنوان الـ Server (localhost)
            port: رقم المنفذ (5000)
        """
        self.host = host
        self.port = port
        self.socket = None                    # الـ socket (هيتعمل في connect)
        self.protocol = Protocol()            # object للاتصال
        self.client_name = None               # اسم المستخدم
        self.menu_display = MenuDisplay()     # object لعرض القوائم
        self.news_display = NewsDisplay()     # object لعرض الأخبار
    
    def send(self, message):
        """إرسال رسالة للـ Server - wrapper function"""
        return self.protocol.send_message(self.socket, message)
    
    def receive(self):
        """استقبال رسالة من الـ Server - wrapper function"""
        return self.protocol.receive_message(self.socket)
    
    # ============================================================
    # الاتصال بالـ Server - Connection
    # ============================================================
    
    def connect(self):
        """
        الاتصال بالـ Server
        
        Returns:
            True: لو الاتصال نجح
            False: لو فشل
        """
        try:
            # إنشاء socket جديد
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            print(f"Connecting to server at {self.host}:{self.port}...")
            
            # محاولة الاتصال
            self.socket.connect((self.host, self.port))
            print("Connected!")
            
            # طلب اسم المستخدم
            self.client_name = input("Enter your name: ").strip()
            
            # إرسال الاسم للـ Server
            if not self.send(self.client_name):
                print("Failed to send name")
                return False
            
            # انتظار تأكيد من الـ Server
            response = self.receive()
            if not response or response != "CONNECTED":
                print("Connection failed")
                return False
            
            print(f"Welcome {self.client_name}!")
            return True
        
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """قطع الاتصال من الـ Server"""
        if self.socket:
            self.socket.close()
    
    # ============================================================
    # معالجة قائمة الأخبار - Headlines Menu
    # ============================================================
    
    def handle_headlines_menu(self):
        """
        التعامل مع قائمة الأخبار
        الـ user يقدر يبحث بطرق مختلفة
        """
        while True:
            # عرض القائمة
            self.menu_display.display_headlines_menu()
            choice = input("Enter your choice: ").strip()
            
            # التحقق من صحة الاختيار
            if choice not in ['1', '2', '3', '4', '5']:
                print("Invalid choice. Please try again.")
                continue
            
            # إرسال الاختيار للـ Server
            if not self.send(choice):
                print("Connection error")
                return
            
            # الاختيار 5 = رجوع
            if choice == '5':
                break
            
            # ============================================================
            # معالجة الاختيارات المختلفة
            # ============================================================
            
            # الاختيار 1: بحث بكلمة مفتاحية
            if choice == '1':
                self.receive()  # انتظار READY من الـ Server
                keyword = input("Enter keyword: ").strip()
                if not self.send(keyword):
                    print("Connection error")
                    return
            
            # الاختيار 2: بحث حسب الفئة
            elif choice == '2':
                self.receive()  # انتظار READY
                self.menu_display.display_categories()
                cat_choice = input("Select category number: ").strip()
                try:
                    # تحويل الرقم لاسم الفئة
                    category = self.menu_display.CATEGORIES[int(cat_choice) - 1]
                    if not self.send(category):
                        print("Connection error")
                        return
                except:
                    print("Invalid choice.")
                    continue
            
            # الاختيار 3: بحث حسب البلد
            elif choice == '3':
                self.receive()  # انتظار READY
                self.menu_display.display_countries()
                country_choice = input("Select country number: ").strip()
                try:
                    # تحويل الرقم لكود البلد
                    country = self.menu_display.COUNTRIES[int(country_choice) - 1]
                    if not self.send(country):
                        print("Connection error")
                        return
                except:
                    print("Invalid choice.")
                    continue
            
            # ============================================================
            # استقبال وعرض النتائج
            # ============================================================
            self.process_headlines_response()
    
    def process_headlines_response(self):
        """
        معالجة وعرض نتائج الأخبار
        دالة منفصلة عشان الكود يكون منظم
        """
        print("\nFetching data from server...")
        response = self.receive()
        
        if not response:
            print("Error: No response from server")
            return
        
        try:
            # تحويل JSON لـ dictionary
            data = json.loads(response)
            
            # التحقق من نجاح العملية
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                
                # عرض قائمة الأخبار
                article_list = self.news_display.display_headlines_list(articles)
                
                if article_list:
                    # السؤال عن عرض تفاصيل خبر معين
                    detail_choice = input("\nEnter article number for details (or press Enter to skip): ").strip()
                    
                    if detail_choice.isdigit():
                        idx = int(detail_choice) - 1
                        # التحقق من صحة الرقم
                        if 0 <= idx < len(article_list):
                            self.news_display.display_headline_details(article_list[idx])
            else:
                # عرض رسالة الخطأ
                print(f"Error: {data.get('message', 'Unknown error')}")
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON response - {e}")
        
        input("\nPress Enter to continue...")
    
    # ============================================================
    # معالجة قائمة المصادر - Sources Menu
    # ============================================================
    
    def handle_sources_menu(self):
        """
        التعامل مع قائمة المصادر
        نفس فكرة قائمة الأخبار لكن للمصادر
        """
        while True:
            self.menu_display.display_sources_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice not in ['1', '2', '3', '4', '5']:
                print("Invalid choice. Please try again.")
                continue
            
            if not self.send(choice):
                print("Connection error")
                return
            
            if choice == '5':  # رجوع
                break
            
            # معالجة الاختيارات
            if choice == '1':  # حسب الفئة
                self.receive()
                self.menu_display.display_categories()
                cat_choice = input("Select category number: ").strip()
                try:
                    category = self.menu_display.CATEGORIES[int(cat_choice) - 1]
                    if not self.send(category):
                        print("Connection error")
                        return
                except:
                    print("Invalid choice.")
                    continue
            
            elif choice == '2':  # حسب البلد
                self.receive()
                self.menu_display.display_countries()
                country_choice = input("Select country number: ").strip()
                try:
                    country = self.menu_display.COUNTRIES[int(country_choice) - 1]
                    if not self.send(country):
                        print("Connection error")
                        return
                except:
                    print("Invalid choice.")
                    continue
            
            elif choice == '3':  # حسب اللغة
                self.receive()
                self.menu_display.display_languages()
                lang_choice = input("Select language number: ").strip()
                try:
                    language = self.menu_display.LANGUAGES[int(lang_choice) - 1]
                    if not self.send(language):
                        print("Connection error")
                        return
                except:
                    print("Invalid choice.")
                    continue
            
            # عرض النتائج
            self.process_sources_response()
    
    def process_sources_response(self):
        """
        معالجة وعرض نتائج المصادر
        """
        print("\nFetching data from server...")
        response = self.receive()
        
        if not response:
            print("Error: No response from server")
            return
        
        try:
            data = json.loads(response)
            
            if data.get('status') == 'ok':
                sources = data.get('sources', [])
                source_list = self.news_display.display_sources_list(sources)
                
                if source_list:
                    detail_choice = input("\nEnter source number for details (or press Enter to skip): ").strip()
                    
                    if detail_choice.isdigit():
                        idx = int(detail_choice) - 1
                        if 0 <= idx < len(source_list):
                            self.news_display.display_source_details(source_list[idx])
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON response - {e}")
        
        input("\nPress Enter to continue...")
    
    # ============================================================
    # الدالة الرئيسية - Main Loop
    # ============================================================
    
    def run(self):
        """
        الدالة الرئيسية لتشغيل الـ Client
        بتتعامل مع القائمة الرئيسية والاختيارات
        """
        # محاولة الاتصال
        if not self.connect():
            return
        
        try:
            # ============================================================
            # القائمة الرئيسية - Main Menu Loop
            # ============================================================
            while True:
                self.menu_display.display_main_menu()
                choice = input("Enter your choice: ").strip()
                
                # التحقق من صحة الاختيار
                if choice not in ['1', '2', '3']:
                    print("Invalid choice. Please try again.")
                    continue
                
                # إرسال الاختيار للـ Server
                if not self.send(choice):
                    print("Connection error")
                    break
                
                # الاختيار 1: قائمة الأخبار
                if choice == '1':
                    response = self.receive()
                    if response == "HEADLINES":
                        self.handle_headlines_menu()
                
                # الاختيار 2: قائمة المصادر
                elif choice == '2':
                    response = self.receive()
                    if response == "SOURCES":
                        self.handle_sources_menu()
                
                # الاختيار 3: إنهاء
                elif choice == '3':
                    self.receive()
                    print("\nGoodbye!")
                    break
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            # في كل الأحوال، نقطع الاتصال
            self.disconnect()


# ============================================================
# Main Function - نقطة البداية
# ============================================================

def main():
    """
    الدالة الرئيسية - نقطة بداية البرنامج
    """
    # إنشاء object من NewsClient
    client = NewsClient(host='127.0.0.1', port=5000)
    
    # بداية تشغيل الـ Client
    client.run()


# ============================================================
# تشغيل البرنامج
# ============================================================
if __name__ == "__main__":
    # ده بيتنفذ لو شغلنا الملف مباشرة
    main()