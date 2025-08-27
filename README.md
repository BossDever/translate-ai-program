# 🌐 Gemini AI Translator

Repository: BossDever/translate-ai-program

แอพพลิเคชันแปลภาษาด้วย AI ที่ใช้ Google Gemini API พร้อมระบบตรวจจับภาษาอัตโนมัติและ UI 

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ คุณสมบัติเด่น

- 🤖 **การแปลด้วย AI**: ใช้ Google Gemini 2.0 Flash เพื่อความแม่นยำสูง
- 🔍 **ตรวจจับภาษาอัตโนมัติ**: ไม่ต้องเลือกภาษาต้นทาง ระบบจะตรวจจับให้อัตโนมัติ
- ⚡ **การทำงานแบบ Asynchronous**: UI ไม่ค้างขณะแปลภาษา
- 🎯 **ผลลัพธ์สะอาด**: แสดงเฉพาะคำแปล ไม่มีคำอธิบายเพิ่มเติม
- 📱 **รองรับ DPI สูง**: ใช้งานได้ดีกับหน้าจอความละเอียดสูง

## 🌍 ภาษาที่รองรับ

- 🇹🇭 **ไทย** (Thai)
- 🇺🇸 **อังกฤษ** (English) 
- 🇯🇵 **ญี่ปุ่น** (Japanese)
- 🇨🇳 **จีน** (Chinese)
- 🇰🇷 **เกาหลี** (Korean)

## 🚀 การติดตั้งและใช้งาน

### ขั้นตอนที่ 1: Clone โปรเจกต์
```bash
git clone https://github.com/BossDever/translate-ai-program.git
cd translate-ai-program
```

### ขั้นตอนที่ 2: ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### ขั้นตอนที่ 3: ตั้งค่า API Key

1. **สร้างไฟล์ .env**:
```bash
cp .env.example .env
```

2. **รับ Gemini API Key**:
   - ไปที่ [Google AI Studio](https://makersuite.google.com/app/apikey)
   - สร้าง API Key ใหม่
   - คัดลอก API Key

3. **แก้ไขไฟล์ .env**:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### ขั้นตอนที่ 4: รันแอพพลิเคชัน
```bash
python app.py
```

## 📖 วิธีใช้งาน

1. **เปิดแอพ** - หน้าต่างจะเปิดกลางหน้าจออัตโนมัติ
2. **เลือกภาษาปลายทาง** - เลือกภาษาที่ต้องการแปลเป็น
3. **พิมพ์ข้อความ** - ใส่ข้อความที่ต้องการแปลในช่องซ้าย
4. **กดปุ่ม "แปลภาษา"** - รอผลลัพธ์ในช่องขวา
5. **ใช้ปุ่ม "ลบข้อความ"** - เพื่อล้างข้อความทั้งหมด

### 🔥 ฟีเจอร์พิเศษ: การตรวจจับภาษาอัตโนมัติ

แอพจะตรวจจับภาษาต้นทางอัตโนมัติ:
- พิมพ์ **"สวัสดี"** → ตรวจจับเป็นภาษาไทย
- พิมพ์ **"Hello"** → ตรวจจับเป็นภาษาอังกฤษ  
- พิมพ์ **"こんにちは"** → ตรวจจับเป็นภาษาญี่ปุ่น
- พิมพ์ **"你好"** → ตรวจจับเป็นภาษาจีน
- พิมพ์ **"안녕하세요"** → ตรวจจับเป็นภาษาเกาหลี

## 🛠️ โครงสร้างโปรเจกต์

```
translate-ai-program/
├── 📄 app.py              # ไฟล์หลักของแอพพลิเคชัน
├── 📄 dpi_set.py          # จัดการ DPI สำหรับหน้าจอความละเอียดสูง
├── 📄 requirements.txt    # รายการ dependencies
├── 📄 .env               # ไฟล์ environment variables (ไม่อัปโหลดไป Git)
├── 📄 .env.example       # ตัวอย่างไฟล์ .env
├── 📄 .gitignore         # ไฟล์ที่ไม่ต้องการอัปโหลดไป Git
└── 📄 README.md          # คู่มือการใช้งาน (ไฟล์นี้)
```

## ⚙️ ข้อกำหนดระบบ

- **Python**: 3.7 หรือสูงกว่า
- **ระบบปฏิบัติการ**: Windows, macOS, Linux
- **การเชื่อมต่ออินเทอร์เน็ต**: จำเป็นสำหรับการเรียกใช้ API
- **RAM**: อย่างน้อย 512 MB
- **พื้นที่ว่าง**: อย่างน้อย 100 MB

## 🔧 การแก้ไขปัญหา

### ❌ ปัญหา: Import Error
```bash
# แก้ไข: ติดตั้ง dependencies ใหม่
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ ปัญหา: API Key ไม่ทำงาน
1. ✅ ตรวจสอบว่า API Key ถูกต้อง
2. ✅ ตรวจสอบว่าไฟล์ `.env` อยู่ในโฟลเดอร์เดียวกันกับ `app.py`
3. ✅ ตรวจสอบว่าไม่มีช่องว่างหรืออักขระพิเศษใน API Key
4. ✅ ตรวจสอบโควต้า API ที่ Google AI Studio

### ❌ ปัญหา: แอพไม่เปิด
```bash
# แก้ไข: ตรวจสอบ Python version
python --version

# ถ้า Python < 3.7 ให้อัปเกรด Python
```

### ❌ ปัญหา: การแปลช้า
- ✅ ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ✅ ลองใช้ข้อความสั้นๆ ก่อน
- ✅ ตรวจสอบสถานะ API ที่ Google

## 📋 Dependencies

```txt
python-dotenv  # สำหรับจัดการ environment variables
requests       # สำหรับเรียกใช้ API
```

## 🔒 ความปลอดภัย

⚠️ **ข้อสำคัญ**: 
- **อย่าแชร์ API Key** ของคุณให้ใครฟัง
- ไฟล์ `.env` จะไม่ถูกอัปโหลดไป GitHub เพื่อความปลอดภัย
- เก็บ API Key ไว้เป็นความลับ

## 🤝 การมีส่วนร่วม

หากพบข้อผิดพลาดหรือต้องการเสนอแนะ:
1. เปิด Issue ใน GitHub
2. ส่ง Pull Request
3. ติดต่อผู้พัฒนา

## 📄 License

โปรเจกต์นี้ใช้ MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) file

## 👨‍💻 ผู้พัฒนา

สร้างด้วย ❤️ โดยผู้พัฒนาคนไทย

---

⭐ **ถ้าโปรเจกต์นี้มีประโยชน์ อย่าลืมกด Star ให้ด้วยนะครับ!** ⭐
