# 🎯 Quick Import Data - Checklist (30 detik)

## ✅ Verifikasi 3 Hal

### 1️⃣ Spreadsheet Sudah Public?
```
Buka: https://docs.google.com/spreadsheets/d/1UxSvet7BwwgYec5b4kN4bT5zquYU2rOPSBNFXqVgJa4/
Klik: Share → "Anyone with the link can view" ✅
```

### 2️⃣ Kolom Data Benar?
```
Sheet: MASTER
Kolom C (index 2): NPSN
Kolom D (index 3): Nama Sekolah  
Kolom G (index 6): Status (cari: "Terpasang" atau "Belum Pasang")
Kolom H (index 7): Kendala/Detail
```

### 3️⃣ API_URL di HTML Sudah Benar?
```
Buka: Monitoring.html
Baris: 117
Value: const API_URL = 'https://script.google.com/macros/s/AKfycby-...../exec';
✅ Jika sudah ada URL Apps Script, DONE!
```

---

## 🚀 Cara Kerja (Otomatis)

```
1. Browser buka Monitoring.html
2. Setiap 30 detik → Fetch ke API_URL
3. Apps Script baca Spreadsheet MASTER
4. Return data dalam format JSON
5. Dashboard parse + tampilkan
6. Done! Update otomatis ✨
```

---

## 🔍 Test Cepat (Copy-Paste di Console)

Buka browser → F12 → Console tab → Paste:

```javascript
fetch('https://script.google.com/macros/s/AKfycby-HnH7NBFI9eLWNn2RVssnLr1DotsNicZUp5A_UNgWHQ5-69VyLdwGSyO7ohUtpJPd/exec')
  .then(r => r.json())
  .then(d => { console.log('Data:', d); console.table(d.rows); })
  .catch(e => console.error('ERROR:', e));
```

**Harusnya muncul:** Table dengan data dari Spreadsheet ✅

---

## ⚠️ Kalau Error

| Error | Solusi |
|-------|--------|
| "Failed to fetch" | Spreadsheet belum public |
| Empty data | Check kolom index (C, D, G, H) |
| "403 Forbidden" | Apps Script belum di-deploy atau authorize |
| CORS error | Coba pakai fallback CSV URL |

---

## 💡 Ganti Data Source

**Pakai Spreadsheet Lain:**

Buka `Monitoring.html` baris 114-115:
```javascript
const SPREADSHEET_ID = '1UxSvet7BwwgYec5b4kN4bT5zquYU2rOPSBNFXqVgJa4';  // ← Ganti ID
const SHEET_NAME = 'MASTER';  // ← Ganti nama sheet
```

Copy ID spreadsheet baru dari URL:
```
https://docs.google.com/spreadsheets/d/[COPY_INI]/edit
```

---

**Status:** ✅ SIAP PAKAI (Tinggal jamin Spreadsheet public!)
