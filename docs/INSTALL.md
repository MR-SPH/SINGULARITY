# Installation & Environment Requirements Guide
# دليل متطلبات وبيئة التشغيل والتثبيت

[English](#english) | [العربية](#العربية)

---

## English

### 1. System & Hardware Requirements

* **Operating System:** Windows 10/11, Linux (Ubuntu, Debian, Fedora, Arch), or macOS (11+).
* **Python Version:** Python 3.11 or higher (Python 3.14 is fully tested and supported).
* **Processor (CPU):** Any modern Dual-Core or Quad-Core 64-bit CPU.
* **Memory (RAM):** Minimum 2 GB RAM (4 GB recommended).
* **Graphics:** Any standard integrated or dedicated GPU supporting OpenGL / SDL2 windowing (no dedicated GPU compute shaders required).

---

### 2. Required Packages & Libraries

All runtime dependencies are defined in `requirements.txt` and `pyproject.toml`:

| Package | Minimum Version | Purpose |
| :--- | :--- | :--- |
| **`pygame-ce`** | `>=2.5.0` | Community Edition SDL2 windowing, 60 FPS event handling, and 2D surface blitting (replaces standard pygame with pre-built cp314 wheels). |
| **`numpy`** | `>=2.0.0` | High-performance vectorized numerical math, Struct-of-Arrays (SoA) particle pools, and matrix projections. |
| **`numba`** | `>=0.60.0` | JIT compilation acceleration for intensive mathematical loops. |
| **`pillow`** | `>=10.0.0` | High-resolution image manipulation and screenshot exports. |
| **`arabic-reshaper`** | `>=3.0.0` | Contextual Arabic typography glyph reconstruction (connecting isolated letters into cursive words). |
| **`python-bidi`** | `>=0.4.2` | Unicode Bidirectional algorithm handling for correct Right-to-Left (RTL) text layout. |
| **`pytest`** | `>=8.0.0` | *(Dev only)* Automated unit testing suite (40 unit tests). |

---

### 3. Step-by-Step Installation

#### Step 1: Open Terminal / PowerShell
Navigate to the project root directory:
```bash
cd G:\python_ascii
```

#### Step 2: Create a Dedicated Virtual Environment
Using a virtual environment isolates project dependencies:
```bash
# Windows
python -m venv .venv

# Linux / macOS
python3 -m venv .venv
```

#### Step 3: Activate the Virtual Environment
```powershell
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt (cmd):
.\.venv\Scripts\activate.bat

# Linux / macOS:
source .venv/bin/activate
```

#### Step 4: Upgrade pip & Install Dependencies
```bash
python -m pip install --upgrade pip

# Option A: Install from requirements.txt
pip install -r requirements.txt

# Option B: Install in editable mode with development/test dependencies
pip install -e ".[dev]"
```

---

### 4. Verification

Verify that your installation is working correctly by running the automated test suite:
```bash
pytest
```
*Expected output: `40 passed in ~1.5s`.*

---

<br>
<hr>
<br>

## العربية

### 1. متطلبات النظام والأجهزة

* **نظام التشغيل:** ويندوز 10 أو 11، أو لينكس (أي توزيعة)، أو ماك أو إس (11 فما فوق).
* **إصدار بايثون:** Python 3.11 أو أحدث (تم اختبار التوافقية الكاملة مع Python 3.14).
* **المعالج (CPU):** معالج ثنائي أو رباعي النواة بتردد حديث (لا يتطلب مواصفات خارقة).
* **الذاكرة العشوائية (RAM):** 2 جيجابايت كحد أدنى (4 جيجابايت موصى بها).
* **بطاقة الرسوميات (GPU):** أي بطاقة شاشة مدمجة أو منفصلة تدعم مكتبات SDL2 وعرض النوافذ (لا يلزم توفر كرت شاشة احترافي لأن المعالجة الرياضية تعتمد على NumPy و CPU).

---

### 2. المكتبات والحزم المطلوبة

تم حصر كافة الاعتماديات في ملفي `requirements.txt` و `pyproject.toml`:

| الحزمة (Package) | الإصدار الأدنى | الوظيفة وأهميتها في المشروع |
| :--- | :--- | :--- |
| **`pygame-ce`** | `>=2.5.0` | النسخة المجتمعية المتطورة من Pygame؛ توفر نافذة العرض، وإدارة الأحداث، والرسم بمعدل 60 إطاراً في الثانية، وتحتوي على ملفات جاهزة لـ Python 3.14. |
| **`numpy`** | `>=2.0.0` | إجراء الحسابات الرياضية الشعاعية المتزامنة لحركة آلاف الجسيمات في أجزاء من الميلي ثانية. |
| **`numba`** | `>=0.60.0` | تسريع الدوال الرياضية الثقيلة عبر التجميع اللحظي (JIT). |
| **`pillow`** | `>=10.0.0` | معالجة الصور وحفظ لقطات الشاشة عالية الدقة. |
| **`arabic-reshaper`** | `>=3.0.0` | تشكيل الحروف العربية وربطها سياقياً لتحويل الحروف المنفصلة إلى كلمات متصلة. |
| **`python-bidi`** | `>=0.4.2` | معالجة اتجاه النصوص ثنائية الاتجاه لضمان انسيابية الكتابة العربية من اليمين إلى اليسار. |
| **`pytest`** | `>=8.0.0` | *(للتطوير فقط)* بيئة الاختبارات الآلية التي تشغل كافة اختبارات المشروع الـ 40. |

---

### 3. خطوات التثبيت خطوة بخطوة

#### الخطوة 1: الدخول إلى مجلد المشروع
افتح موجه الأوامر (PowerShell أو Terminal) وانتقل للمجلد:
```powershell
cd G:\python_ascii
```

#### الخطوة 2: إنشاء بيئة افتراضية منعزلة (Virtual Environment)
```powershell
# على ويندوز:
python -m venv .venv

# على لينكس / ماك:
python3 -m venv .venv
```

#### الخطوة 3: تفعيل البيئة الافتراضية
```powershell
# على ويندوز (PowerShell):
.\.venv\Scripts\Activate.ps1

# على ويندوز (CMD):
.\.venv\Scripts\activate.bat

# على لينكس أو ماك:
source .venv/bin/activate
```

#### الخطوة 4: ترقية pip وتثبيت المكتبات
```powershell
python -m pip install --upgrade pip

# التثبيت المباشر:
pip install -r requirements.txt

# أو التثبيت مع أدوات التطوير والاختبارات:
pip install -e ".[dev]"
```

---

### 4. التحقق من نجاح التثبيت

تأكد من سلامة البيئة والمكتبات بتشغيل حزمة الاختبارات:
```powershell
pytest
```
*يجب أن تظهر لك النتيجة: `40 passed` باللون الأخضر.*

