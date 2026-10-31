# Changelog / سجل التغييرات

All notable changes to **SINGULARITY** will be documented in this file.  
يتم توثيق كافة التغييرات والتحسينات الملحوظة لمشروع **SINGULARITY** في هذا الملف.

[English](#english) | [العربية](#العربية)

---

## English

### [1.0.0] - 2026-10-31

#### Added
- **Core Engine & Architecture**:
  - Full real-time relativistic simulation built on `pygame-ce` and `numpy`.
  - Unified spatial coordinate scale using the Schwarzschild radius ($R_s$) as standard length unit.
  - Full 3D camera projection with continuous yaw rotation, pitch inclination, and perspective depth ordering.
- **Astrophysics & Relativistic Dynamics**:
  - Exact event horizon boundary at $1.0 \, R_s$ with dynamic particle absorption.
  - Photon sphere ring at $1.5 \, R_s$ with luminous unstable photon orbit rendering.
  - Innermost Stable Circular Orbit (ISCO) at $3.0 \, R_s$ via Paczyński-Wiita pseudo-Newtonian potential.
  - Shakura-Sunyaev radial temperature profile: $T(r) \propto r^{-3/4} [1 - \sqrt{r_{\text{in}}/r}]^{1/4}$.
  - Relativistic Doppler beaming asymmetry ($\delta^3$) amplifying approaching disk matter.
  - Screen-space gravitational lensing deflection bending background stars and far-disk halo arc.
  - **Gravitational Wave Ripples**: Relativistic spacetime metric perturbations expanding outward on mass absorption.
- **Arabic Typography System**:
  - Contextual glyph reshaping and BiDi layout via `arabic-reshaper` and `python-bidi`.
  - 4 typography modes: `letters` (28 alphabet letters), `words`, `phrases`, and `mixed`.
  - Characters align tangentially along orbital velocity streamlines ($\theta_{\text{flow}}$).
  - 2-tier quantized glyph cache maintaining 60 FPS on standard CPUs.
- **Cinematic & UI Features**:
  - **Cinematic Auto-Tour Mode (`[C]`)**: Smooth autonomous 360° orbital camera with pitch oscillation and breathing zoom.
  - Glassmorphic telemetry HUD with live FPS, frame times, particle diagnostics, and interactive parameter sliders.
  - 5 curated color presets: Solar Orange, Deep Blue, Purple Nebula, Monochrome White, and Emerald Singularity.
- **Verification & Testing**:
  - 40 automated unit tests covering geometry, physics, typography, and camera projection.
  - Headless benchmark mode (`--benchmark`) for automated performance analysis.

---

## العربية

### [الإصدار 1.0.0] - 31 أكتوبر 2026

#### الإضافات والميزات الجديدة
- **المحرك المعماري الأساسي**:
  - محاكاة نسبية متكاملة في الوقت الفعلي مبنية باستخدام `pygame-ce` و `numpy`.
  - نظام إحداثيات فراغي موحد بالكامل يعتمد على نصف قطر شفارتزشيلد ($R_s$) كوحدة طول أساسية.
  - كاميرا ثلاثية الأبعاد كاملة تتيح الدوران حول المحور الرأسي (Yaw)، والميلان (Pitch)، وإسقاط المنظور وترتيب العمق.
- **الفيزياء الفلكية والديناميكا النسبية**:
  - أفق حدث شفارتزشيلد بدقة عند $1.0 \, R_s$ مع آلية ابتلاع ديناميكية للجسيمات.
  - كرة الفوتونات (Photon Sphere) عند $1.5 \, R_s$ مع تصيير حلقة الضوء المتوهجة.
  - المدار الدائري المستقر الداخلي (ISCO) عند $3.0 \, R_s$ اعتماداً على جهد باتشينسكي-فيتا النسبي.
  - توزيع حراري شعاعي لقرص التزويد مطابق لنموذج شاكورا-سونيايف القياسي.
  - تأثير دوبلر النسبي (Doppler Beaming) المسبب لعدم التماثل البصري وإضاءة الجانب المقترب.
  - عدسة جاذبية فضائية ثنائية تحني النجوم الخلفية وتُظهر الجزء البعيد من القرص كقوس علوي وسفلي.
  - **تموجات أمواج الجاذبية**: نبضات تموجية تتوسع في مستوى القرص كقطع ناقص ثلاثي الأبعاد فور سقوط المادة داخل الثقب الأسود.
- **نظام التيبوغرافيا والخط العربي**:
  - معالجة تشكيل الحروف العربية واتصالها وانسيابية الاتجاه من اليمين لليسار عبر `arabic-reshaper` و `python-bidi`.
  - 4 أوضاع للكتابة: الحروف المنفردة (`letters` - 28 حرفاً)، الكلمات (`words`)، العبارات الكونية (`phrases`)، والوضع المختلط (`mixed`).
  - توجيه الحروف مماسياً ومطابقتها لخطوط تدفق السرعة المدارية.
  - نظام كاش مزدوج للرموز يحافظ على أداء 60 إطاراً في الثانية حتى على المعالجات العادية.
- **الميزات البصرية وواجهة المستخدم**:
  - **نمط الجولة السينمائية التلقائية (`[C]`)**: كاميرا مدارية ذاتية التحكم تدور 360 درجة مع تذبذب انسيابي لزاوية الميلان وزووم تنفسي.
  - لوحة معلومات بيانية شفافة (Glassmorphic HUD) مع قياسات دقيقة لمعدل الإطارات وزمن الإطار وتعداد الجسيمات.
  - 5 لوحات ألوان فلكية مختارة: البرتقالي الشمسي، الأزرق العميق، السديم الأرجواني، الأبيض الأحادي، والزمرد الكوني.
- **الاختبارات والتحقق الآلي**:
  - 40 اختباراً وحدوياً تغطي النسب الهندسية، المعادلات الفيزيائية، كاش الخطوط، وإسقاط الكاميرا.
  - نمط قياس أداء بدون واجهة رسومية (`--benchmark`) للتحقق السريع.
