// config.example.js — انسخ هذا الملف إلى `config.js` محليًا واملأ القيم (لا ترفع المفاتيح الحقيقية إلى المستودع العام)
// يمكنك أيضاً استخدام متغيرات البيئة في منصة النشر (Vercel) بدلًا من وضع المفاتيح هنا.

window.APP_CONFIG = window.APP_CONFIG || {
  // URL لمشروع Supabase الخاص بك، مثال: https://abcde12345.supabase.co
  SUPABASE_URL: 'https://your-project-id.supabase.co',

  // المفتاح العام (anon) من Supabase — استخدم المفتاح العام فقط في المتصفح
  SUPABASE_ANON_KEY: 'your-anon-key-here',

  // اسم الـ bucket الذي أنشأته في Storage (مثال: student-uploads)
  SUPABASE_BUCKET: 'student-uploads',

  // اختياري: احتفظ بعنوان الخادم الاحتياطي إن وُجد
  // SERVER_URL: 'https://your-server.example.com/send-message'
};
