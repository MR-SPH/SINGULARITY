# SINGULARITY — Quick Start & User Guide
# دليل التشغيل السريع للمستخدم

[🇸🇦 العربية](#-دليل-التشغيل-باللغة-العربية) | [🇬🇧 English](#-english-quick-start)

---

# 🇸🇦 دليل التشغيل باللغة العربية

مرحباً بك في **SINGULARITY: محرك المحاكاة الفلكية والفن التوليدي للثقب الأسود بالحروف العربية**.  
تم تجهيز هذا المشروع ليعمل فورياً وبضغطة زر واحدة (Turnkey & Fail-safe) على أي جهاز.

---

### 🚀 الطريقة الأسهل (بدون أي أوامر):

#### على نظام ويندوز (Windows):
1. انقر نقراً مزدوجاً (Double Click) على ملف:
   👉 **`run.bat`**
2. سيقوم الملف تلقائياً بفحص بايثون، إنشاء البيئة الافتراضية، تثبيت المكتبات وتشغيل المحاكاة فوراً!

#### تشغيل كبرنامج مستقل (.exe) بدون بايثون نهائياً:
البرنامج مبني ومجهز مسبقاً داخل مجلد `dist`:
1. انقر نقراً مزدوجاً مباشرة على:
   👉 **`dist\Run_App.bat`** (أو **`dist\SINGULARITY\SINGULARITY.exe`**)
2. سيعمل البرنامج فورياً على أي جهاز ويندوز دون الحاجة لتثبيت بايثون!
*(ملاحظة: إذا أردت إعادة بناء التطبيق التنفيذي من الكود المصدري في أي وقت، فقط شغل `build_windows.bat`).*

---

### 💻 أوامر جاهزة للنسخ واللصق (للمبرمجين ومستخدمي الطرفية):

#### خيار 1: عبر Windows PowerShell
```powershell
# 1. الدخول لمجلد المشروع
cd singularity

# 2. التشغيل التلقائي المباشر
.\run.bat
```

#### خيار 2: عبر موجه أوامر الويندوز (CMD)
```cmd
cd singularity
run.bat
```

#### خيار 3: عبر لينكس أو ماك (Linux / macOS)
```bash
# إعطاء صلاحية التشغيل أول مرة ثم الإطلاق
chmod +x run.sh
./run.sh
```

---

### ⚠️ ملاحظة هامة جداً عند تثبيت بايثون لأول مرة:
إذا لم يكن بايثون مثبتاً على جهازك من قبل:
1. حمّل بايثون من الموقع الرسمي: [python.org/downloads](https://www.python.org/downloads/) (إصدار 3.11 أو أحدث).
2. **خطوة حرجة أثناء التثبيت:** في أول نافذة تظهر لك، احرص على تفعيل الخيار في الأسفل:  
   ✅ **`Add Python to PATH`**  
   *(هذا الخيار ضروري حتى يتعرف النظام على بايثون من أي مكان).*

---

### 🎮 أزرار التحكم داخل المحاكاة:

| الزر / التحكم | الوظيفة |
| :--- | :--- |
| **`C`** | **تشغيل / إيقاف الجولة السينمائية التلقائية (Cinematic Auto-Tour 360°)** |
| **سحب الفأرة الأيسر** | تدوير الكاميرا حول الثقب الأسود (Yaw / Pitch) |
| **عجلة الفأرة** | تقريب المنظور وإبعاده (Zoom) |
| **سحب الفأرة الأيمن** | تحريك مركز المشهد (Pan) |
| **`Space`** | إيقاف مؤقت / استئناف حركة الجسيمات |
| **`H`** | إظهار / إخفاء لوحة التحكم والبيانات (HUD) |
| **`F`** | ملء الشاشة (Fullscreen) |
| **`R`** | إعادة ضبط الكاميرا والجسيمات |
| **`P`** | حفظ لقطة شاشة عالية الدقة داخل مجلد `screenshots/` |
| **`Esc`** | الخروج الآمن وحفظ الإعدادات |

---

<br>
<hr>
<br>

# 🇬🇧 English Quick Start

Welcome to **SINGULARITY: Arabic Gravitational Art Engine**.  
This project is engineered to run out of the box with one click (Turnkey & Fail-safe) on any system.

---

### 🚀 Easiest Method (One-Click Launch):

#### On Windows:
1. Simply double-click:
   👉 **`run.bat`**
2. The script will automatically verify Python, set up `.venv`, install requirements, and launch the black hole simulation!

#### Run as Standalone Executable (.exe without Python):
The standalone build is already prepared and ready inside the `dist` directory:
1. Double-click directly on:
   👉 **`dist\Run_App.bat`** (or **`dist\SINGULARITY\SINGULARITY.exe`**)
2. The simulation will launch immediately on any Windows machine—no Python installation needed!
*(Note: To re-compile the standalone executable from source at any time, run `build_windows.bat`).*

---

### 💻 Copy & Paste Terminal Commands:

#### Windows PowerShell:
```powershell
.\run.bat
```

#### Windows Command Prompt (CMD):
```cmd
run.bat
```

#### Linux & macOS Terminal:
```bash
chmod +x run.sh
./run.sh
```

---

### ⚠️ Important Note When Installing Python:
If Python is not yet installed:
1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/).
2. **Critical Step:** In the installer's first screen, make sure to check:  
   ✅ **`Add Python to PATH`**

---

### 🎮 In-App Controls:

| Input | Action |
| :--- | :--- |
| **`C`** | **Toggle Cinematic Auto-Tour (Autonomous 360° Orbit)** |
| **Left Click + Drag** | Orbit camera around the black hole |
| **Mouse Wheel** | Zoom in / out |
| **Right Click + Drag**| Pan camera center |
| **`Space`** | Pause / Resume simulation |
| **`H`** | Toggle HUD & Control Panel |
| **`F`** | Toggle Fullscreen |
| **`R`** | Reset simulation and camera |
| **`P`** | Save high-resolution screenshot to `screenshots/` |
| **`Esc`** | Save settings and exit |

