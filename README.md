# Yee — واجهة التفاعل الصفية (Student Activity Portal)

تطبيق ويب بسيط يسمح للطلاب بالتقاط صور/تسجيلات صوتية وإرسالها إلى Supabase Storage أو إلى خادم احتياطي.

ملاحظة: لا تقم بوضع مفاتيح سرية في هذا المستودع.

## ما تم إضافته
- `index.html`: واجهة تفاعلية مُحسّنة لالتقاط صور/صوت وإرسالها إلى Supabase.
- `teacher.html`: صفحة عرض للمدرّس لعرض الملفات المخزنة في Supabase.
- `config.example.js`: نموذج تهيئة لتعبئة SUPABASE_URL و SUPABASE_ANON_KEY و SUPABASE_BUCKET.

## خطوات الإعداد السريع
1. أنشئ مشروعًا في Supabase (https://supabase.com) واحصل على:
   - SUPABASE_URL
   - SUPABASE_ANON_KEY (مفتاح anon العام فقط — آمن للاستخدام من المتصفح)

2. إنشاء bucket في Storage باسم `student-uploads` أو أي اسم تفضله.
   - إذا أردت روابط صور عامة، اجعل الـ bucket `public`.

3. إنشاء جدول metadata (اختياري لكن من الأفضل) عبر SQL Editor في Supabase:

```sql
create table if not exists submissions (
  id bigserial primary key,
  filename text,
  message text,
  created_at timestamptz default now(),
  user_agent text
);
```

4. اضبط التهيئة محليًا:
   - انسخ `config.example.js` إلى `config.js` واملأ القيم (لا ترفع `config.js` إلى المستودع العام).

5. نشر الواجهة:
   - GitHub Pages: ارفع الملفات، ثم فعّل Pages في إعدادات المستودع.
   - Vercel: اربط المستودع واستخدم متغيرات البيئة لحماية المفاتيح.

## تشغيل محلي للاختبار
- افتح `index.html` في متصفح يدعم getUserMedia (Chrome/Firefox) عبر خادم محلي (مثلاً `npx http-server` أو `python -m http.server 8000`).

## ملاحظات أمان وخصوصية
- استخدم `anon` key فقط في واجهة المستخدم؛ لا تضع `service_role` في المتصفح.
- أطّلع الطلاب وأحصل منهم على موافقة قبل التقاط أي بيانات شخصية.

