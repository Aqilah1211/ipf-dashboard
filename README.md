# 📚 Dokumentasi Lengkap - IFP Monitoring Dashboard

## 🎯 Ringkas: Cara Kerja Import Data

**Data TIDAK di-import manual** — sistem **otomatis fetch dari Spreadsheet** setiap 30 detik.

### 3 Langkah Cepat:
1. ✅ Spreadsheet dibuat public (Share → Anyone)
2. ✅ API_URL sudah ter-set di Monitoring.html (baris 117)
3. ✅ Selesai! Auto-fetch dimulai

---

## 📖 File Dokumentasi

| File | Tujuan | Untuk Siapa |
|------|--------|------------|
| **[QUICK_IMPORT.md](QUICK_IMPORT.md)** | ⚡ Checklist 30 detik | Yang ingin langsung coba |
| **[IMPORT_DATA_GUIDE.md](IMPORT_DATA_GUIDE.md)** | 📊 Panduan detail + troubleshoot | Yang ingin paham cara kerjanya |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 🏗️ Diagram flow + sequence | Developer / yang ingin detail teknis |
| **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)** | 🚀 Setup Google Apps Script | Deploy pertama kali |
| **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** | ✅ Checklist lengkap | QA / verification |

---

## 🚀 Mulai dari Sini

### Pilihan A: Saya ingin langsung coba
→ Baca: **[QUICK_IMPORT.md](QUICK_IMPORT.md)** (5 menit)

### Pilihan B: Saya ingin paham cara kerjanya
→ Baca: **[IMPORT_DATA_GUIDE.md](IMPORT_DATA_GUIDE.md)** (10 menit)
→ Lihat: **[ARCHITECTURE.md](ARCHITECTURE.md)** (diagram + flow)

### Pilihan C: Saya belum deploy Apps Script
→ Baca: **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)** (15 menit step-by-step)

---

## 📊 Data Flow (Ultra-Ringkas)

```
Spreadsheet (MASTER sheet)
    ↑ (auto-sync)
    │
Google Apps Script (API)
    ↑ (FETCH setiap 30s)
    │
Monitoring.html Dashboard
    ↓
Browser → Tampilkan data
```

**Poin Penting:**
- ✅ Spreadsheet HARUS public (Share)
- ✅ Sheet harus bernama `MASTER`
- ✅ Kolom C=NPSN, D=Nama, G=Status, H=Kendala
- ✅ API_URL sudah benar di HTML (baris 117)

---

## 🔧 File Sumber Kode

| File | Fungsi | Lokasi |
|------|--------|--------|
| `GAS_Code.gs` | Server code (Google Apps Script) | `/GAS_Code.gs` |
| `Monitoring.html` | Frontend dashboard | `/Monitoring.html` |
| `run_server.py` | Local HTTP server runner | `/run_server.py` |

---

## ✨ Fitur Siap Pakai

- ✅ Real-time dashboard dengan 4 statistik
- ✅ Tabel kendala dengan highlight baru
- ✅ Auto-refresh 30 detik (bisa di-pause)
- ✅ Search/filter by NPSN atau Nama
- ✅ Timestamp "Last Updated"
- ✅ Responsive design (mobile-friendly)
- ✅ Hash-based change detection (hemat bandwidth)

---

## 🎯 Checklist Jika Ada Masalah

### Data tidak muncul?
```
□ Spreadsheet sudah public? (Share → Anyone)
□ Sheet bernama "MASTER"?
□ Kolom C,D,G,H ada data?
□ API_URL di HTML correct? (test di console)
□ Klik refresh atau tunggu 30 detik
```

### Ingin ganti Spreadsheet lain?
```
Buka Monitoring.html → baris 114-115
const SPREADSHEET_ID = '[GANTI_INI]';
const SHEET_NAME = 'MASTER';
```

### Ingin cek data langsung?
```javascript
// Buka browser → F12 → Console, paste:
fetch('https://script.google.com/macros/s/AKfycby-HnH7NBFI9eLWNn2RVssnLr1DotsNicZUp5A_UNgWHQ5-69VyLdwGSyO7ohUtpJPd/exec')
  .then(r => r.json())
  .then(d => console.table(d.rows));
```

---

## 📞 Referensi Cepat

**Test Server:**
```powershell
python -m http.server 8000
# Buka: http://localhost:8000/Monitoring.html
```

**Deploy Apps Script:**
```
1. Buka script.google.com
2. New project → Copy GAS_Code.gs
3. Deploy → Web App (Anyone, even anonymous)
4. Copy URL → Update API_URL di HTML
```

**Struktur Spreadsheet yang Diperlukan:**
```
Sheet: MASTER
Kolom C (idx 2):  NPSN
Kolom D (idx 3):  Nama Sekolah
Kolom G (idx 6):  Status ("Terpasang" / "Belum Pasang")
Kolom H (idx 7):  Kendala/Detail
```

---

## 🎓 Belajar Lebih Lanjut

Untuk modifikasi advanced (ganti kolom, ubah polling interval, dll):
1. Edit [GAS_Code.gs](GAS_Code.gs) → Deploy ulang
2. Edit [Monitoring.html](Monitoring.html) → Refresh browser

---

**Status: ✅ SIAP PAKAI**

Tinggal jamin Spreadsheet public dan mulai tracking! 🎉

Pertanyaan? Check dokumentasi sesuai topik di atas.
