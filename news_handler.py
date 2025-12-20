# ============================================================
# NewsHandler Class - معالج الأخبار
# ============================================================
# الكلاس ده مسؤول عن التواصل مع NewsAPI.org وجلب البيانات

import requests  # مكتبة لعمل HTTP requests
import json      # مكتبة للتعامل مع JSON
from config import NEWS_API_KEY, NEWS_API_BASE_URL  # جلب الإعدادات

class NewsHandler:
    """
    كلاس بيتعامل مع NewsAPI ويجيب الأخبار والمصادر
    """
    
    def __init__(self):
        """
        Constructor - بيتنفذ لما نعمل object من الكلاس
        بيحفظ الـ API key والـ base URL
        """
        self.api_key = NEWS_API_KEY
        self.base_url = NEWS_API_BASE_URL
    
    def get_headlines(self, **params):
        """
        دالة عامة لجلب الأخبار الرئيسية (headlines)
        
        Parameters:
            **params: أي parameters نعوز نبعتها للـ API
                     مثلاً: country='us', category='sports'
        
        Returns:
            dictionary فيه البيانات من الـ API
        """
        # بناء الـ URL الكامل
        url = f"{self.base_url}/top-headlines"
        
        # إضافة الـ API key للـ parameters
        params['apiKey'] = self.api_key
        
        # تحديد عدد النتائج بحد أقصى 15 (حسب المطلوب في المشروع)
        params['pageSize'] = 15
        
        try:
            # إرسال GET request للـ API
            response = requests.get(url, params=params)
            
            # التأكد إن الـ response نجح (status code 200)
            response.raise_for_status()
            
            # تحويل الـ response من JSON لـ Python dictionary
            return response.json()
            
        except Exception as e:
            # لو حصل error، نرجع رسالة خطأ
            return {"status": "error", "message": str(e)}
    
    def get_sources(self, **params):
        """
        دالة عامة لجلب مصادر الأخبار (sources)
        
        Parameters:
            **params: أي parameters (مثل category, country, language)
        
        Returns:
            dictionary فيه بيانات المصادر
        """
        url = f"{self.base_url}/top-headlines/sources"
        params['apiKey'] = self.api_key
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ============================================================
    # دوال البحث في الأخبار - Headlines Search Functions
    # ============================================================
    
    def search_headlines_by_keyword(self, keyword, country=None):
        """
        البحث في الأخبار باستخدام كلمة مفتاحية
        مثال: البحث عن "football"
        
        Parameters:
            keyword: الكلمة اللي هنبحث عنها
            country: البلد (اختياري)
        """
        params = {'q': keyword}  # q = query (استعلام)
        if country:
            params['country'] = country
        return self.get_headlines(**params)
    
    def get_headlines_by_category(self, category, country='us'):
        """
        جلب الأخبار حسب الفئة
        مثال: أخبار رياضية (sports)
        
        Parameters:
            category: الفئة (business, sports, technology, etc.)
            country: البلد (default: us)
        """
        params = {'category': category, 'country': country}
        return self.get_headlines(**params)
    
    def get_headlines_by_country(self, country):
        """
        جلب الأخبار حسب البلد
        مثال: أخبار من السعودية (sa)
        
        Parameters:
            country: كود البلد (sa, us, ae, etc.)
        """
        params = {'country': country}
        return self.get_headlines(**params)
    
    def get_all_headlines(self, country='us'):
        """
        جلب كل الأخبار الرئيسية بدون تصفية
        
        Parameters:
            country: البلد (default: us)
        """
        params = {'country': country}
        return self.get_headlines(**params)
    
    # ============================================================
    # دوال البحث في المصادر - Sources Search Functions
    # ============================================================
    
    def get_sources_by_category(self, category):
        """
        جلب المصادر حسب الفئة
        مثال: مصادر تقنية (technology)
        """
        params = {'category': category}
        return self.get_sources(**params)
    
    def get_sources_by_country(self, country):
        """
        جلب المصادر حسب البلد
        مثال: مصادر من الإمارات (ae)
        """
        params = {'country': country}
        return self.get_sources(**params)
    
    def get_sources_by_language(self, language):
        """
        جلب المصادر حسب اللغة
        مثال: مصادر عربية (ar) أو إنجليزية (en)
        """
        params = {'language': language}
        return self.get_sources(**params)
    
    def get_all_sources(self):
        """
        جلب كل المصادر المتاحة بدون تصفية
        """
        return self.get_sources()
    
    # ============================================================
    # حفظ البيانات - Save Data Function
    # ============================================================
    
    def save_to_json(self, data, filename):
        """
        حفظ البيانات في ملف JSON
        
        الفكرة: كل ما client يطلب بيانات، نحفظها في ملف
        اسم الملف: ClientName_option_GroupID.json
        
        Parameters:
            data: البيانات (dictionary)
            filename: اسم الملف
        
        Returns:
            True: لو الحفظ نجح
            False: لو في مشكلة
        """
        try:
            # فتح الملف للكتابة (w = write)
            with open(filename, 'w', encoding='utf-8') as f:
                # تحويل dictionary لـ JSON وكتابته في الملف
                # ensure_ascii=False: عشان ندعم العربي
                # indent=4: عشان الملف يكون منسق وسهل القراءة
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error in saving JSON: {e}")
            return False