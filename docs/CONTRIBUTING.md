# Contributing to SINGULARITY / دليل المساهمة في المشروع

[English](#english) | [العربية](#العربية)

---

## English

Thank you for your interest in contributing to **SINGULARITY: Arabic Gravitational Art Engine**! We welcome contributions ranging from relativistic physics enhancements and calligraphy typography to performance optimizations and documentation.

### How to Contribute

1. **Fork the Repository**: Create your own fork on GitHub.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Set Up Development Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   pip install -e ".[dev]"
   ```
4. **Code Standards**:
   - Write clean, type-annotated Python code following PEP 8.
   - Use vectorized NumPy operations rather than Python loops for particle dynamics and rendering.
   - Ensure Arabic typography shaping respects Right-to-Left (BiDi) contexts.
5. **Run Automated Tests**:
   Before submitting your PR, ensure all 40 tests pass:
   ```bash
   pytest
   ```
6. **Commit & Open Pull Request**:
   Use conventional commits (`feat:`, `fix:`, `docs:`, `perf:`). Provide a clear summary and screenshots/GIFs for visual changes.

### Future Exploration Ideas
- Custom Arabic calligraphy font integrations (Kufic, Naskh, Diwani).
- OpenCL / Metal compute shader backends for high-density particle counts (>100k).
- Audio-reactive gravitational pulsation / cosmological acoustics.

---

## العربية

يسعدنا ويشرفنا اهتمامك بالمساهمة في مشروع **SINGULARITY: محرك الفن التوليدي والمحاكاة الفلكية النسبية بالحروف العربية**! نرحب بكافة المساهمات، سواء في تحسين الفيزياء النسبية، أو الخطوط والتيبوغرافيا العربية، أو تحسين الأداء، أو التوثيق.

### خطوات المساهمة

1. **نسخ المستودع (Fork):** أنشئ نسختك الخاصة من المستودع على GitHub.
2. **إنشاء فرع للميزة (Feature Branch):**
   ```bash
   git checkout -b feature/اسم-الميزة
   ```
3. **تجهيز بيئة التطوير:**
   ```bash
   python -m venv .venv
   # تفعيل البيئة على ويندوز:
   .\.venv\Scripts\activate
   # أو على لينكس/ماك:
   source .venv/bin/activate

   pip install -e ".[dev]"
   ```
4. **معايير كتابة الشيفرة البرمجية:**
   - كتابة شيفرة بايثون نظيفة ومنظمة وفق معايير PEP 8 مع تدوين الأنواع (Type Annotations).
   - استخدام المعالجة الشعاعية عبر NumPy (Vectorized Operations) في حركة الجسيمات وتجنب الحلقات التكرارية البطيئة.
   - الحفاظ على اتصال الحروف العربية واتجاه الكتابة السليم (BiDi RTL).
5. **إجراء الاختبارات الآلية:**
   تأكد من اجتياز جميع الاختبارات الأربعين بنجاح قبل إرسال التعديل:
   ```bash
   pytest
   ```
6. **إنشاء طلب السحب (Pull Request):**
   استخدم رسائل إيداع واضحة، وأرفق صوراً أو لقطات متحركة عند تعديل المظهر البصري.

### مجالات مقترحة للتطوير
- دعم خطوط عربية كلاسيكية متنوعة (كوفي، رقعة، ديواني).
- مسرعات حوسبة باستخدام OpenCL أو Compute Shaders لرفع كثافة الجسيمات إلى أكثر من 100,000 جسيم.
- تفاعل موجي صوتي مع نبضات الثقب الأسود (Cosmological Audio-reactive acoustics).
