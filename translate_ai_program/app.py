from dpi_set import *
from tkinter import *
from tkinter import ttk
import os, requests
from dotenv import load_dotenv
import re
import tkinter as tk
import tkinter.messagebox as tkk
import threading

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"


#ขนาดหน้าต่าง
root = tk.Tk()
root.title("Gemini AI Translator")

# คำนวณตำแหน่งกลางหน้าจอ
window_width = 950
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)

root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.maxsize(950,600)
root.minsize(950,600)



#ตั้งค่า DPI
dpi = DpiManager()
dpi.enable_win_dpi_awareness(mode="system")  # หรือ "permonitor"
dpi.apply_tk_scaling(root)   # ตั้งสเกลครั้งแรก (ตาม DPI จอปัจจุบัน)
dpi.bind_auto_update(root)   # อัปเดตอัตโนมัติเมื่อย้ายหน้าต่าง/รีไซส์

# ...existing code...
language1 = StringVar(value="อัตโนมัติ")
language2 = StringVar(value="English")
#widget
# make combobox readonly so user cannot type arbitrary text
combo1 = ttk.Combobox(root, values=["อัตโนมัติ","Thai","English","Japanese","Chinese","Korean"], textvariable=language1, state="readonly")
combo1.pack(pady=10)
combo1.place(x=145,y=18)

label = Label(root, text="─────▶", font=("Sarabun", 16))
label.place(x=400, y=1)

combo2 = ttk.Combobox(root, values=["Thai","English","Japanese","Chinese","Korean"], textvariable=language2, state="readonly")
combo2.pack(pady=10)
combo2.place(x=620,y=18)

#เก็บข้อความที่พิมพ์ในช่องข้อความ
text1 = Text(root,font=("Sarabun",16),height=7,width=25)
text1.place(x=10,y=65)

text2 = Text(root,font=("Sarabun",16),height=7,width=25)
text2.place(x=485,y=65)


def _clean_output(s: str) -> str:
    """ทำความสะอาดผลลัพธ์ให้เหลือแค่คำแปลเปล่าๆ"""
    if not s:
        return ""
    
    # ลบประโยคคำนำต่างๆ ที่ AI ชอบใส่
    patterns_to_remove = [
        r'^\s*(that translates to|this translates to|translation|translated text|the translation is|in thai|in english|in japanese|in chinese|in korean)\s*:?\s*',
        r'^\s*(the most common.*?is|คำตอบควรออกมาแค่|ผลลัพธ์คือ)\s*:?\s*',
        r'^\s*(hello|สวัสดี)\s+(in|ใน)\s+\w+\s+(is|คือ)\s*:?\s*',
        r'^\s*"([^"]*)".*$',  # ถ้ามีเครื่องหมายคำพูด เอาเฉพาะข้างใน
    ]
    
    for pattern in patterns_to_remove:
        s = re.sub(pattern, r'\1' if '([^"]*)' in pattern else '', s, flags=re.I)
    
    # ลบ Markdown และเครื่องหมายพิเศษ
    s = re.sub(r'[*_`#]+', '', s)  # **bold**, *italic*, `code`, #header
    s = re.sub(r'^"+|"+$', '', s.strip())  # เครื่องหมายคำพูดหน้าหลัง
    s = re.sub(r'^\s*[-•]\s*', '', s)  # bullet points
    
    # เอาเฉพาะบรรทัดแรกที่มีเนื้อหา
    for line in s.splitlines():
        line = line.strip()
        if line and not line.startswith(('*', '-', '•', '#')):
            return line
    
    return s.strip()

def detect_language(text):
    """ตรวจจับภาษาอัตโนมัติจากข้อความ"""
    # ตรวจภาษาไทย
    thai_chars = sum(1 for c in text if '\u0e00' <= c <= '\u0e7f')
    # ตรวจภาษาจีน
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    # ตรวจภาษาญี่ปุ่น
    japanese_chars = sum(1 for c in text if '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff')
    # ตรวจภาษาเกาหลี
    korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7af')
    
    total_chars = len(text.replace(' ', ''))
    if total_chars == 0:
        return "English"
    
    # คำนวณเปอร์เซ็นต์
    thai_percent = (thai_chars / total_chars) * 100
    chinese_percent = (chinese_chars / total_chars) * 100
    japanese_percent = (japanese_chars / total_chars) * 100
    korean_percent = (korean_chars / total_chars) * 100
    
    # ถ้ามีตัวอักษรพิเศษมากกว่า 30% ถือว่าเป็นภาษานั้น
    if thai_percent > 30:
        return "Thai"
    elif chinese_percent > 30:
        return "Chinese"
    elif japanese_percent > 30:
        return "Japanese"
    elif korean_percent > 30:
        return "Korean"
    else:
        return "English"

def translate_api(src_text, src_lang, tgt_lang):
    """ฟังก์ชันสำหรับเรียก API แยกต่างหาก (ใช้ใน thread)"""
    # ถ้าเลือก "อัตโนมัติ" ให้ตรวจจับภาษาอัตโนมัติ
    if src_lang == "อัตโนมัติ":
        src_lang = detect_language(src_text)
    
    # Prompt ที่เน้นให้ตอบแค่คำแปลเปล่าๆ
    prompt = f"Translate this {src_lang} text to {tgt_lang}. Return only the translation, no explanations: {src_text}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 200,  # จำกัดความยาวผลลัพธ์
            "temperature": 0.1       # ลด randomness เพื่อความเร็ว
        }
    }

    try:
        r = requests.post(URL, json=payload, timeout=10)  # ลด timeout
        r.raise_for_status()
        data = r.json()
        
        translated_raw = data["candidates"][0]["content"]["parts"][0]["text"]
        return _clean_output(translated_raw)
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {e}"

def update_result(result):
    """อัปเดตผลลัพธ์ใน UI"""
    text2.delete("1.0","end")
    text2.insert("1.0", result)
    button1.config(state="normal", text="แปลภาษา")  # เปิดปุ่มกลับมา

def translate():
    src_text = text1.get("1.0","end-1c").strip()
    src_lang = language1.get()
    tgt_lang = language2.get()

    # ตรวจสอบข้อมูลก่อน (ไม่ต้องตรวจสอบภาษาต้นทางแล้ว เพราะมี "อัตโนมัติ")
    if not src_text:
        text2.delete("1.0","end")
        text2.insert("1.0", "⚠️ กรุณาใส่ข้อความก่อน")
        return

    # แสดงสถานะกำลังแปล
    text2.delete("1.0","end")
    text2.insert("1.0", "🔄 กำลังแปล...")
    button1.config(state="disabled", text="กำลังแปล...")  # ปิดปุ่มชั่วคราว
    
    # ใช้ threading เพื่อไม่ให้ UI หยุดทำงาน
    def translate_thread():
        result = translate_api(src_text, src_lang, tgt_lang)
        root.after(0, lambda: update_result(result))  # อัปเดต UI ใน main thread
    
    thread = threading.Thread(target=translate_thread, daemon=True)
    thread.start()


def delete():
    text1.delete("1.0","end")
    text2.delete("1.0","end")

#ปุ่มส่งข้อความ
button1 = Button(root,text="แปลภาษา",font=("Sarabun",16),command=translate)
button1.place(x=305,y=490)

#ปุ่มสำหรับลบข้อความ
button2 = Button(root,text="ลบข้อความ",font=("Sarabun",16),command=delete)
button2.place(x=485,y=490)

root.mainloop()