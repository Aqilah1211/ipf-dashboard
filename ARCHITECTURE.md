# 🏗️ Arsitektur Data Flow - IFP Monitoring

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BROWSER / DASHBOARD                          │
│                      (Monitoring.html)                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Stats Cards (4 cards)                                      │   │
│  │ • Total Sekolah  • Terpasang  • Belum Pasang  • Trouble   │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              ↑                                      │
│                              │                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Trouble Table                                              │   │
│  │ NPSN | Nama Sekolah | Status | Detail Kendala             │   │
│  │ 1037 | SD Maju      | Trouble| Layar rusak                │   │
│  │ 1038 | SMP Jaya     | Trouble| Delay pengiriman           │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              ↑                                      │
│                              │                                      │
│  fetchSheetData() every 30s   │   Manual refresh (klik ⟳)         │
│  │                            │                                    │
└──┼────────────────────────────┼────────────────────────────────────┘
   │                            │
   └─────────────┬──────────────┘
                 │
                 │ FETCH REQUEST (with optional hash param)
                 │
                 ↓
┌──────────────────────────────────────────────────────────────────────┐
│            GOOGLE APPS SCRIPT WEB APP (doGet)                        │
│         https://script.google.com/macros/s/[ID]/exec                │
│                                                                      │
│  Input:  ?hash=abc123... (untuk change detection)                   │
│  Process:                                                            │
│    1. Open Spreadsheet (SPREADSHEET_ID)                             │
│    2. Get Sheet MASTER                                              │
│    3. Get all data (getDataRange().getValues())                     │
│    4. Compute MD5 hash                                              │
│    5. If hash != client hash → changed=true, return full data       │
│       Else → changed=false, return empty rows (hemat bandwidth)     │
│                                                                      │
│  Output: JSON                                                        │
│  {                                                                   │
│    "rows": [                                                         │
│      ["Header", "NPSN", "Nama", ..., "Status", "Kendala"],         │
│      ["", "10370001", "SD Maju", ..., "Terpasang", "-"],            │
│      ["", "10370002", "SMP Jaya", ..., "Belum Pasang", "-"],        │
│      ...                                                             │
│    ],                                                                │
│    "hash": "md5hashABC123...",                                      │
│    "changed": true                                                  │
│  }                                                                   │
└──────────────────────────────────────────────────────────────────────┘
                 ↑
                 │
        SPREADSHEET UPDATE
                 │
                 ↓
┌──────────────────────────────────────────────────────────────────────┐
│          GOOGLE SHEETS (Spreadsheet)                                 │
│   https://docs.google.com/spreadsheets/d/[ID]/                      │
│                                                                      │
│  Sheet: MASTER (REQUIRED)                                           │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Col A | Col B | Col C    | Col D      | ... | G     | H   │   │
│  │       |       | NPSN     | Nama       |     | Status| Ket │   │
│  │───────┼───────┼──────────┼────────────┼─────┼───────┼─────│   │
│  │       |       | 10370001 | SD Maju    | ... | Terp. | -   │   │
│  │       |       | 10370002 | SMP Jaya   | ... | Belum | -   │   │
│  │       |       | 10370003 | SMA Harap  | ... | Terp. | Lag │   │
│  │       |       | 10370004 | SMK Modar  | ... | Belum | Var │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Permissions: ✅ Public (Anyone can view)                           │
│  Last Edit: [User edit data here]                                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Mapping

### Kolom yang Digunakan:

```javascript
// Row Index → Spreadsheet Column
rows[i][0]  → A (skipped / header)
rows[i][1]  → B 
rows[i][2]  → C (NPSN) ✅ Primary key
rows[i][3]  → D (Nama Sekolah) ✅ Display
rows[i][4]  → E
rows[i][5]  → F
rows[i][6]  → G (Status) ✅ Filter: "terpasang" / "belum pasang"
rows[i][7]  → H (Kendala/Detail) ✅ Show in table if not empty
```

### Logika Filtering:

```javascript
// Setiap row diproses:
- Mulai dari i=1 (skip header)
- Skip jika kolom NPSN (C) kosong
- Count sebagai "total"
- If status (G) contains "terpasang" AND tidak contains "belum" → "installed"
- Else → "pending"
- If kendala (H) ada isinya → Tambah ke "trouble" list + highlight
```

---

## 🔄 Change Detection (Hash-Based)

**Tujuan:** Hemat bandwidth — tidak kirim data penuh jika tidak ada perubahan

**Cara Kerja:**

1. **Browser hitung hash** dari data terakhir
2. **Kirim hash** ke Apps Script: `?hash=abc123...`
3. **Apps Script hitung hash** data terbaru
4. **Compare:**
   - ✅ Sama → return `{changed: false, rows: []}` (kosong)
   - ❌ Beda → return `{changed: true, rows: [...]}` (data penuh)

**Benefit:**
- Auto-refresh 30 detik tapi tidak boros bandwidth
- Hanya transmit data kecil (hash) jika tidak berubah
- Full data hanya kirim saat ada perubahan

---

## 🎯 Flow Diagram (Sequence)

```
Time    Browser                 Apps Script         Spreadsheet
──────  ──────────────────────  ──────────────────  ─────────────
00:00   ├─ Load Monitoring.html
        ├─ fetchSheetData()
        │  └─ FETCH /exec      ──→ 
        │                          ├─ Open Sheet
        │                          ├─ Read data
        │                          ├─ Hash = MD5(data)
        │                          ├─ Send JSON
        │  ←──── JSON ────────────┤
        ├─ Parse rows
        ├─ Update cards & table
        ├─ Display ✅
        │
30:00   ├─ Auto-refresh
        ├─ fetchSheetData()
        │  └─ FETCH /exec?hash=abc123
        │                         ├─ Read data
        │                         ├─ Hash = MD5(data)
        │                         ├─ Hash == param?
        │                         ├─ Changed=false
        │                         ├─ rows=[] (kosong)
        │                         ├─ Send (hanya hash)
        │  ←──── {changed:false,rows:[]}
        ├─ Skip update (no change)
        │                             [User edit cell H7]
        │                             ← cell updated
        │
60:00   ├─ Auto-refresh
        ├─ fetchSheetData()
        │  └─ FETCH /exec?hash=abc123 ──→
        │                         ├─ Read data
        │                         ├─ Hash = MD5(data) = XYZ789
        │                         ├─ Hash != param? ✅
        │                         ├─ Changed=true
        │                         ├─ Send full rows
        │  ←──── {changed:true,rows:[...]}
        ├─ Parse rows
        ├─ Update cards & table ✨
        ├─ Highlight new trouble
        └─ Display ✅
```

---

## 🔧 Troubleshooting Berdasarkan Flow

**Problem:** Data tidak muncul
- **Check:** Apakah Spreadsheet public? (Share permission)
- **Check:** Apakah kolom C,D,G,H ada data?
- **Check:** Apakah Apps Script sudah di-authorize?

**Problem:** Data lama, tidak update
- **Check:** Apakah auto-refresh aktif? (icon jam terang)
- **Check:** Apakah data di Spreadsheet sudah berubah?
- **Manual:** Klik refresh button (⟳)

**Problem:** Rows kosong tapi tidak error
- **Likely:** Hash match, data unchanged (normal!)
- **Check:** Edit Spreadsheet, wait 30s

---

**Kesimpulan:** Semua otomatis! Tinggal jamin Spreadsheet public + API_URL benar 👍
