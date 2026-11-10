# SINGULARITY // Arabic Gravitational Art Engine
### محرك المحاكاة الفلكية والفن التوليدي النسبي للثقب الأسود بالحروف العربية
### Relativistic Black Hole Generative-Art Simulation in Arabic Typography

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pytest: 40 Passed](https://img.shields.io/badge/tests-40%20passed-brightgreen.svg)]()
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%99%A5-red.svg)](LICENSE)
[![Dual Language](https://img.shields.io/badge/Docs-العربية%20%7C%20English-blue.svg)](#-التوثيق-باللغة-العربية)

---

### اختر لغة التوثيق / Choose Documentation Language:
> **[🇸🇦 التوثيق باللغة العربية (Arabic Documentation)](#-التوثيق-باللغة-العربية)**  
> **[🇬🇧 English Documentation (التوثيق باللغة الإنجليزية)](#-english-documentation)**

---

<br>

# 🇸🇦 التوثيق باللغة العربية

> **SINGULARITY** هو محرك فن توليدي فلكي ومحاكاة نسبية في الوقت الحقيقي، يُصيّر الزمكان المنحني، وحركة قرص التزويد، وعدسة الجاذبية للثقب الأسود باستخدام **الحروف والكلمات العربية** كجوهر للمادة المرئية.

---

## فهرس المحتويات (العربية)
1. [نظرة عامة](#نظرة-عامة)
2. [الأسس الفيزيائية والرياضية المعتمدة](#الأسس-الفيزيائية-والرياضية-المعتمدة)
3. [نظام الخط والتيبوغرافيا العربية](#نظام-الخط-والتيبوغرافيا-العربية)
4. [الميزات البصرية والحركية](#الميزات-البصرية-والحركية)
5. [المتطلبات والبيئة البرمجية](#المتطلبات-والبيئة-البرمجية)
6. [دليل التثبيت خطوة بخطوة](#دليل-التثبيت-خطوة-بخطوة)
7. [طريقة التشغيل وخيارات سطر الأوامر](#طريقة-التشغيل-وخيارات-سطر-الأوامر)
8. [التحكم التفاعلي ولوحة القياسات](#التحكم-التفاعلي-ولوحة-القياسات)
9. [معمارية وبنية المشروع](#معمارية-وبنية-المشروع)
10. [الاختبارات الآلية](#الاختبارات-الآلية)
11. [الرخصة](#الرخصة)

---

## نظرة عامة

بدلاً من الاعتماد على الأشكال الهندسية التقليدية أو المضلعات المكسوة بالخامات، يقوم **SINGULARITY** ببناء الشكل الفلكي للثقب الأسود من آلاف **الحروف والكلمات العربية**. تدور الحروف وتتسارع وتنجذب وفقاً لقوانين النسبية العامة، متحاذية مع خطوط التدفق المدارية وكأنها خطوط عربية مضيئة تسبح في الفضاء الكوني.

يتميز المحرك بأسلوب بصري سينمائي يبتعد عن الشاشات الطرفية النمطية، ويحقق أداءً سلساً بمعدل **60 إطاراً في الثانية (60 FPS)** على الحواسيب العادية بفضل المعالجة الشعاعية عبر NumPy ونظام كاش الحروف المزدوج.

---

## الأسس الفيزيائية والرياضية المعتمدة

تعتمد المحاكاة على تقريبات فيزيائية دقيقة مستمدة من النسبية العامة والفيزياء الفلكية:

### 1. مقياس فراغي موحد يعتمد على نصف قطر شفارتزشيلد ($R_s$)
تستخدم جميع العناصر في المحاكاة إحداثيات عالمية ثلاثية الأبعاد منسوبة إلى $R_s$:
* **أفق الحدث (Event Horizon):** يقع عند $1.0 \, R_s$. كل جسيم يعبر هذا الحد يتم ابتلاعه وسحبه للداخل.
* **كرة الفوتونات (Photon Sphere):** تقع عند $1.5 \, R_s$. المدار الحرج غير المستقر للضوء الذي يشكل حلقة الإضاءة المركزية.
* **المدار الدائري المستقر الداخلي (ISCO):** يقع عند $3.0 \, R_s$. تسقط المادة داخله بشكل حلزوني سريع نحو الثقب الأسود.
* **قرص التزويد (Accretion Disk):** يمتد من $3.0 \, R_s$ حتى $20.0 \, R_s$.
* **السمك الرأسي للقرص:** يتبع هندسة قرص الغاز الواقعية $H(r) = 0.03 \, r$.

### 2. التوزيع الحراري الشعاعي (شاكورا-سونيايف)
يتبع إشعاع القرص نموذج القرص الرقيق الفيزيائي القياسي:
$$T(r) = T_{\text{peak}} \cdot \left(\frac{r}{r_{\text{in}}}\right)^{-3/4} \left[1 - \sqrt{\frac{r_{\text{in}}}{r}}\right]^{1/4}$$
تصل درجة الحرارة ذروتها عند $r \approx 4.08 \, R_s$ مع تدرج لوني ينتقل من الأبيض الساطع في المركز إلى البرتقالي الشمسي والقرمزي عند الأطراف.

### 3. الديناميكا المدارية لباتشينسكي-فيتا
تُحاكي السرعة الزاوية المدارية النسبية باستخدام جهد باتشينسكي-فيتا:
$$\Omega(r) = \frac{\sqrt{GM}}{r^{1/2}(r - R_s)}$$
مما يمنح الحروف القريبة من الأفق حركة حلزونية متسارعة تلتف بعنف حول المركز، بينما تدور الأطراف الخارجية بهدوء كبلري.

### 4. تأثير دوبلر النسبي (Doppler Beaming)
المادة التي تدور باتجاه زاوية رؤية الكاميرا تتضاعف إضاءتها وفق معامل التعزيز النسبي $\delta^3$:
$$\delta = \frac{1}{\gamma (1 - \beta \cos\theta)}$$
مما يُنتج عدم تماثل السطوع الشهير المشاهد في صور تلسكوب أفق الحدث (EHT).

### 5. عدسة الجاذبية (Gravitational Lensing)
ينحني ضوء النجوم الخلفية والجانب البعيد من القرص بفعل انحناء الزمكان، ليظهر كقوس مضيء أعلى وأسفل الثقب الأسود.

### 6. تموجات أمواج الجاذبية (Gravitational Wave Ripples)
عند ابتلاع أي جسيم وعبروره أفق الحدث ($r \le R_s$)، ينطلق نبض تموجي نسبي كقطع ناقص ثلاثي الأبعاد متوافق مع زاوية ميلان الكاميرا ويتلاشى تدريجياً.

---

## نظام الخط والتيبوغرافيا العربية

* **28 حرفاً من الحروف الهجائية:** تتكون البلازما الأساسية للقرص من حروف الأبجدية العربية المنفردة.
* **اتصال الحروف وانسيابية الاتجاه (BiDi):** معالجة تشكيل الكلمات والعبارات بالكامل عبر `arabic-reshaper` ومكتبة `python-bidi`.
* **المحاذاة المماسية لخطوط التدفق:** تدور الحروف تلقائياً لتتوازى مع اتجاه السرعة المدارية:
  $$\theta_{\text{flow}} = 90^\circ + \arctan2(v_z, v_x)$$
* **أوضاع النص الأربعة:**
  * **حروف منفردة (`letters`):** الحروف الـ 28 كاملة.
  * **كلمات فلكية (`words`):** كلمات متصلة مثل: *جاذبية، أفق الحدث، ثقب أسود، تفرد، نور، سرمدي، زمكان*.
  * **عبارات كونية (`phrases`):** عبارات مثل: *في فلك يسبحون، والنجم إذا هوى*.
  * **وضع مختلط (`mixed`):** تدفق ديناميكي يجمع بين الحروف والكلمات والعبارات.

---

## الميزات البصرية والحركية

* **نمط الجولة السينمائية التلقائية (`[C]`):** كاميرا ذاتية القيادة تدور 360 درجة حول الثقب الأسود مع تذبذب زاوية الميلان وزووم تنفسي هادئ.
* **تموجات أمواج الجاذبية:** نبضات دائرية متوهجة تنبعث عند ابتلاع المادة.
* **لوحة قياسات تفاعلية (Glassmorphic HUD):** متابعة فورية للإطارات في الثانية (FPS)، وزمن الإطار، ونسبة الجسيمات المبتلعة.
* **5 لوحات ألوان متكاملة:** البرتقالي الشمسي، الأزرق العميق، السديم الأرجواني، الأبيض الأحادي، والزمرد الكوني.
* **توهج متراكم متعدد المراحل (Additive Bloom):** لمعان وانعكاسات ضوئية بدون هبوط في الأداء.

---

## المتطلبات والبيئة البرمجية

* **بايثون:** الإصدار 3.11 أو أحدث (تم التحقق والتوافق الكامل مع Python 3.14).
* **نظام التشغيل:** ويندوز 10/11، لينكس، أو ماك أو إس.
* **المكتبات الأساسية:**
  * `pygame-ce >= 2.5.0`
  * `numpy >= 2.0.0`
  * `numba >= 0.60.0`
  * `pillow >= 10.0.0`
  * `arabic-reshaper >= 3.0.0`
  * `python-bidi >= 0.4.2`

---

## دليل التثبيت خطوة بخطوة

### على ويندوز (PowerShell):
```powershell
# 1. الدخول إلى مجلد المشروع
cd G:\python_ascii

# 2. إنشاء البيئة الافتراضية وتفعيلها
python -m venv .venv
.\.venv\Scripts\activate

# 3. تثبيت المتطلبات الأساسية والتطويرية
pip install -e ".[dev]"
```

### على لينكس / ماك:
```bash
# 1. إنشاء البيئة الافتراضية وتفعيلها
python3 -m venv .venv
source .venv/bin/activate

# 2. تثبيت الحزم
pip install -e ".[dev]"
```

---

## طريقة التشغيل وخيارات سطر الأوامر

### التشغيل المباشر:
```powershell
python main.py
```

### خيارات سطر الأوامر المتاحة:
```powershell
# التشغيل بلوحة ألوان معينة ونمط كلمات
python main.py --preset solar_orange --mode words

# التشغيل في وضع ملء الشاشة بجودة فائقة
python main.py --fullscreen --quality HIGH

# ضبط عدد الجسيمات الأولي
python main.py --particles 10000

# تشغيل فحص الأداء الآلي بدون واجهة (Headless Benchmark)
python main.py --benchmark 120
```

---

## التحكم التفاعلي ولوحة القياسات

| المفتاح / التحكم | الوظيفة |
| :--- | :--- |
| **`C`** | تشغيل / إيقاف نمط الجولة السينمائية التلقائية |
| **سحب الفأرة الأيسر** | تدوير الكاميرا حول الثقب الأسود (Yaw & Pitch) |
| **سحب الفأرة الأيمن** | تحريك موضع مركز الرؤية (Pan) |
| **عجلة الفأرة** | تقريب / إبعاد الكاميرا (Zoom) |
| **`H`** | إظهار / إخفاء واجهة التحكم وشريط المعلومات |
| **`F`** | تبديل وضع ملء الشاشة (Fullscreen) |
| **`Space`** | إيقاف مؤقت / استئناف حركة المحاكاة |
| **`R`** | إعادة تعيين الجسيمات وموقع الكاميرا |
| **`P`** | حفظ لقطة شاشة بدقة فائقة داخل مجلد `screenshots/` |
| **`Esc`** | الخروج من البرنامج بأمان وحفظ الإعدادات |

---

## معمارية وبنية المشروع

```text
singularity/
├── src/singularity/
│   ├── core/           # إدارة المحرك، الإعدادات، والحالة العامة
│   ├── physics/        # نسبية شفارتزشيلد، شاكورا-سونيايف، وعدسة الجاذبية
│   ├── particles/      # حوض الجسيمات المهيكل وقنوات الانبعاث
│   ├── typography/     # تشكيل الحروف العربية، اتجاه BiDi، وكاش الرموز
│   ├── rendering/      # كاميرا 3D، تصيير النجوم، التوهج، وأمواج الجاذبية
│   ├── ui/             # لوحة التحكم الزجاجية وشاشة البيانات التفاعلية
│   └── utilities/      # التنميط الرياضي والتحسين الحسابي
├── tests/              # 40 اختباراً وحدوياً مؤتمتاً
├── LICENSE             # رخصة MIT الرسمية والترجمة العربية
├── CONTRIBUTING.md     # دليل المساهمة الثنائي
├── CHANGELOG.md        # سجل التحديثات
└── pyproject.toml      # إعدادات الحزمة وبيئة الاختبارات
```

---

## الاختبارات الآلية

يحتوي المشروع على **40 اختباراً وحدوياً** تغطي كافة الجوانب الفيزيائية والهندسية والتيبوغرافية:
```powershell
pytest
```
*جميع الاختبارات تجتاز بنجاح بنسبة 100% في أقل من ثانيتين.*

---

<br>
<hr>
<br>

# 🇬🇧 English Documentation

> **SINGULARITY** is an interactive, real-time generative-art engine and relativistic astrophysical simulation that renders curved spacetime, accretion disk dynamics, and gravitational lensing primarily through **Arabic typography** as the visual matter.

---

## Table of Contents (English)
1. [Overview](#overview-1)
2. [Astrophysical & Mathematical Foundations](#astrophysical--mathematical-foundations-1)
3. [Arabic Typography System](#arabic-typography-system-1)
4. [Key Features & Visual Effects](#key-features--visual-effects-1)
5. [Prerequisites & Environment](#prerequisites--environment-1)
6. [Step-by-Step Installation](#step-by-step-installation-1)
7. [Running & CLI Usage](#running--cli-usage-1)
8. [Interactive Controls & HUD](#interactive-controls--hud-1)
9. [Architecture & Repository Structure](#architecture--repository-structure-1)
10. [Automated Testing](#automated-testing-1)
11. [License](#license-1)

---

## Overview

Rather than relying on conventional textured polygons or wireframe meshes, **SINGULARITY** constructs the celestial geometry of a Schwarzschild black hole from thousands of active **Arabic characters**. Characters rotate, plunge, and stretch in accordance with relativistic gravitational dynamics, aligning with orbital stream lines like luminous cosmic calligraphy.

The visual identity is cinematic, scientific, and elegant—deliberately avoiding generic green terminal clichés. The simulation achieves **60 FPS** on standard hardware through vectorized Struct-of-Arrays (SoA) particle pools and a quantized glyph cache.

---

## Astrophysical & Mathematical Foundations

The simulation implements real general-relativistic approximations:

### 1. Unified Spatial Scale ($R_s$)
All scene entities adhere to a single unified coordinate scale governed by the **Schwarzschild radius ($R_s$)**:
* **Event Horizon:** Fixed at $1.0 \, R_s$ (consuming boundary).
* **Photon Sphere:** Positioned at $1.5 \, R_s$ where unstable circular photon orbits create the luminous ring.
* **Innermost Stable Circular Orbit (ISCO):** Positioned at $3.0 \, R_s$. Matter crossing inside ISCO plunges rapidly into the event horizon.
* **Accretion Disk:** Extends from $3.0 \, R_s$ to $20.0 \, R_s$.
* **Vertical Scale Height:** Follows physical gas disk geometry $H(r) = 0.03 \, r$.

### 2. Shakura-Sunyaev Temperature Profile
Disk emission and radiation follow the standard thin-disk model:
$$T(r) = T_{\text{peak}} \cdot \left(\frac{r}{r_{\text{in}}}\right)^{-3/4} \left[1 - \sqrt{\frac{r_{\text{in}}}{r}}\right]^{1/4}$$
Reaching peak temperature at $r \approx 4.08 \, R_s$, smoothly transitioning from incandescent white-gold core to solar orange and deep crimson rim.

### 3. Paczyński-Wiita Orbital Dynamics
Pseudo-Newtonian relativistic angular velocity reproduces circular orbits:
$$\Omega(r) = \frac{\sqrt{GM}}{r^{1/2}(r - R_s)}$$
Causing characters near the horizon to whip in tight, accelerating relativistic spirals.

### 4. Relativistic Doppler Beaming
Matter orbiting toward the line of sight is amplified by the relativistic beaming factor $\delta^3$:
$$\delta = \frac{1}{\gamma (1 - \beta \cos\theta)}$$
Creating the signature Event Horizon Telescope (EHT) brightness asymmetry.

### 5. Gravitational Lensing & Far-Disk Elevation
Light from the far side of an inclined accretion disk bends over the top and bottom of the event horizon, rendering the iconic halo arc.

### 6. Gravitational Wave Ripples
Whenever matter crosses the event horizon, a quasinormal spacetime metric perturbation expands outward across the disk plane, dissipating at relativistic speeds.

---

## Arabic Typography System

* **28 Alphabet Glyphs by Default:** The core plasma is composed of pure isolated Arabic letters.
* **Contextual Reshaping & BiDi Layout:** Uses `arabic-reshaper` and `python-bidi` for full right-to-left glyph connectivity when rendering words and phrases.
* **Tangential Flow Alignment:** Character rotation angles dynamically align with orbital velocity streamlines:
  $$\theta_{\text{flow}} = 90^\circ + \arctan2(v_z, v_x)$$
* **Typography Modes:**
  * **Letters (`letters`):** All 28 Arabic alphabet characters.
  * **Words (`words`):** Cosmological terms (*جاذبية، أفق الحدث، ثقب أسود، تفرد، نور، سرمدي، زمكان*).
  * **Phrases (`phrases`):** Astronomical and philosophical verses (*في فلك يسبحون، والنجم إذا هوى*).
  * **Mixed (`mixed`):** A dynamic composite stream.

---

## Key Features & Visual Effects

* **Cinematic Auto-Tour Mode (`[C]`):** Hands-free autonomous orbital camera that glides 360° around the black hole while smoothly oscillating between face-on circular view and edge-on lensing halo.
* **Gravitational Wave Ripples:** Relativistic ripple emissions upon particle absorption.
* **Glassmorphic Telemetry HUD:** Real-time diagnostics for FPS, absorbed matter, active particles, and parameter sliders.
* **5 Color Presets:** Solar Orange, Deep Blue, Purple Nebula, Monochrome, and Emerald Singularity.
* **Additive Multi-Pass Bloom & Phosphorescent Trails:** Smooth downscaled glow and motion blur.

---

## Prerequisites & Step-by-Step Installation

### Prerequisites
* Python 3.11 or higher (Python 3.14 fully supported).
* Operating System: Windows 10/11, Linux, or macOS.

### Installation
```bash
# Clone repository
git clone https://github.com/MR-SPH/singularity.git
cd singularity-art

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies in editable mode
pip install -e ".[dev]"
```

---

## Running & CLI Usage

```bash
# Default launch
python main.py

# Custom preset and typography mode
python main.py --preset solar_orange --mode words

# Launch in Fullscreen with HIGH quality
python main.py --fullscreen --quality HIGH

# Headless performance benchmark (60 frames)
python main.py --benchmark 60
```

---

## Interactive Controls & HUD

| Key / Input | Action |
| :--- | :--- |
| **`C`** | Toggle Cinematic Auto-Tour Mode |
| **Left Click + Drag** | Orbit camera around black hole (Yaw & Pitch) |
| **Right Click + Drag**| Pan camera center |
| **Scroll Wheel** | Zoom camera in / out |
| **`H`** | Toggle HUD & glassmorphic control dock |
| **`F`** | Toggle Fullscreen mode |
| **`Space`** | Pause / Resume simulation |
| **`R`** | Reset simulation and camera |
| **`P`** | Save high-resolution screenshot to `screenshots/` |
| **`Esc`** | Safely save configuration and exit |

---

## Architecture & Repository Structure

```text
singularity/
├── src/singularity/
│   ├── core/           # Engine lifecycle, config, and state
│   ├── physics/        # General relativistic gravity, Shakura-Sunyaev, lensing
│   ├── particles/      # Vectorized SoA particle pools and emitters
│   ├── typography/     # Arabic reshaping, BiDi, and glyph caching
│   ├── rendering/      # 3D camera, starfield, bloom, and gravitational ripples
│   ├── ui/             # Glassmorphic control dock and telemetry HUD
│   └── utilities/      # Math utilities and profiler
├── tests/              # 40 automated unit tests
├── LICENSE             # Bilingual MIT License
├── CONTRIBUTING.md     # Bilingual Contribution Guide
├── CHANGELOG.md        # Bilingual Version History
└── pyproject.toml      # Packaging & pytest configuration
```

---

## Automated Testing

Run the test suite with:
```bash
pytest
```
*40/40 tests pass in ~1.3 seconds across all modules.*

---

## License

This project is licensed under the [MIT License](LICENSE) — free for academic, artistic, and commercial use.
