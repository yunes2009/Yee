// server-example.js - مثال بسيط لمختبر محلي لاستقبال الطلبات بأمان (لا تستخدمه للإنتاج دون تحسينات)
const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const app = express();
const upload = multer({ dest: path.join(__dirname,'uploads/'), limits: { fileSize: 5 * 1024 * 1024 } }); // حد 5MB

const API_KEY = process.env.API_KEY || 'local-test-key';

app.post('/send-message', upload.single('image'), (req, res) => {
  const key = req.header('x-api-key');
  if (key !== API_KEY) return res.status(401).json({ ok:false, error:'unauthorized' });

  const meta = {
    time: new Date().toISOString(),
    ip: req.ip,
    message: req.body.message || '',
    filename: req.file ? req.file.filename : null,
    originalname: req.file ? req.file.originalname : null,
    size: req.file ? req.file.size : 0,
    mimetype: req.file ? req.file.mimetype : null
  };

  // احفظ الميتاداتا لتحليل آمن في المختبر
  fs.appendFileSync(path.join(__dirname,'requests.log'), JSON.stringify(meta) + '\n');

  res.json({ ok: true, meta });
});

app.listen(3000, () => console.log('Test server running on http://localhost:3000'));
