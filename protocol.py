# ============================================================
# Protocol Class - بروتوكول الاتصال
# ============================================================
# الكلاس ده مسؤول عن إرسال واستقبال الرسائل بين الـ Client والـ Server
# بيستخدم طريقة Length-Prefix عشان يضمن وصول البيانات كاملة

import socket
import struct

class Protocol:
    """
    كلاس بيتعامل مع إرسال واستقبال الرسائل عبر الشبكة
    """
    
    @staticmethod
    def send_message(sock, message):
        """
        دالة لإرسال رسالة عبر الـ socket
        
        الفكرة:
        1. بنحول الرسالة لـ bytes
        2. بنحسب طول الرسالة ونبعته الأول (4 bytes)
        3. بعدين نبعت الرسالة نفسها
        
        ليه؟ عشان الطرف التاني يعرف قد إيه بيانات هيستقبل
        
        Parameters:
            sock: الـ socket اللي هنبعت عليه
            message: الرسالة (string)
            
        Returns:
            True: لو الإرسال نجح
            False: لو في مشكلة
        """
        try:
            # تحويل الرسالة من string لـ bytes
            data = message.encode('utf-8')
            
            # حساب طول البيانات وتحويله لـ 4 bytes
            # !I = unsigned int (4 bytes) في صيغة network byte order
            length = struct.pack('!I', len(data))
            
            # إرسال الطول + البيانات مع بعض
            sock.sendall(length + data)
            return True
            
        except Exception as e:
            print(f"[PROTOCOL] Error sending message: {e}")
            return False
    
    @staticmethod
    def receive_message(sock):
        """
        دالة لاستقبال رسالة من الـ socket
        
        الخطوات:
        1. نستقبل أول 4 bytes (الطول)
        2. نفك الطول عشان نعرف قد إيه بيانات جاية
        3. نستقبل البيانات على دفعات لحد ما نكمل كل حاجة
        
        Parameters:
            sock: الـ socket اللي هنستقبل منه
            
        Returns:
            الرسالة (string): لو الاستقبال نجح
            None: لو في مشكلة أو الاتصال قفل
        """
        try:
            # استقبال أول 4 bytes (الطول)
            raw_length = sock.recv(4)
            if not raw_length:
                return None  # الاتصال قفل
            
            # فك الطول من الـ 4 bytes
            length = struct.unpack('!I', raw_length)[0]
            
            # استقبال البيانات الفعلية
            data = b''  # bytes فاضية
            
            # نفضل نستقبل لحد ما نكمل كل البيانات
            while len(data) < length:
                # نستقبل على دفعات (chunks)
                # كل مرة نستقبل أقصى حاجة 4096 bytes أو الباقي
                chunk = sock.recv(min(length - len(data), 4096))
                
                if not chunk:
                    return None  # الاتصال قفل في النص
                
                data += chunk  # نضيف الـ chunk للبيانات
            
            # تحويل من bytes لـ string ونرجعها
            return data.decode('utf-8')
            
        except Exception as e:
            print(f"[PROTOCOL] Reception error: {e}")
            return None