# 🚨 Deprem Alarmı

![Python](https://img.shields.io/badge/Python-3.10+-blue)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
![Status](https://img.shields.io/badge/Status-Active-success)
![Interface](https://img.shields.io/badge/Interface-GUI-lightgrey)
[![Author](https://img.shields.io/badge/Author-yok1rai-brown?logo=github)](https://github.com/yok1rai)

**Deprem Alarmı**, Türkiye ve çevresindeki depremleri **USGS üzerinden gerçek zamanlı olarak izleyen**, belirlenen büyüklük eşiğinin üzerindeki **yeni depremler için otomatik sesli alarm veren**, Python tabanlı **masaüstü (GUI) deprem alarm uygulamasıdır**.

Uygulama, **alarm spam’ini engelleyen durum temelli bir mantık**, **SQLite destekli geçmiş kaydı** ve **stabil ses sistemi** ile çalışır.

---

## ✨ Özellikler

- 📡 USGS Earthquake API’den canlı veri çekme  
- 🖥️ **Tkinter tabanlı GUI (masaüstü uygulaması)**  
- 🔔 Eşik aşımı durumunda **3 kez sesli alarm**
- 🚫 Aynı deprem için tekrar alarm çalmaz
- 🧠 Deprem ID bazlı durum kontrolü
- 🗄️ SQLite ile lokal deprem geçmişi
- 🔊 `pygame.mixer` ile stabil ses oynatma
- 🧩 Modüler ve genişletilebilir mimari

---

## 🖼️ Arayüz Genel Bakış

GUI aşağıdaki bileşenleri içerir:

- **Başlat / Durdur** kontrol paneli
- Alarm eşiği (büyüklük) giriş alanı
- Canlı olarak güncellenen:
  - Konum listesi
  - Büyüklük listesi
  - Durum mesajları
  - Alarm durumu

Veriler **5 saniyede bir** otomatik olarak güncellenir.

---

## 📂 Proje Yapısı

```text
DepremAlarmi/
├── assets/
│   └── sounds/
│       └── anons.wav
├── data/
│   └── earthquakes.db        # Çalışma sırasında oluşur
├── deprecated/
│   └── cli.py                # ❌ Artık kullanılmıyor (deprecated)
├── src/
│   └── deprem_alarmi/
│       ├── main.py           # Tkinter GUI + uygulama döngüsü
│       ├── fetcher.py        # USGS API veri çekme
│       ├── processor.py     # En güncel depremi ayrıştırma
│       ├── alarm/
│       │   ├── alarm.py     # Alarm kontrol mantığı
│       │   ├── rules.py     # Eşik kuralları
│       │   └── sound.py     # Pygame ses sistemi
│       └── storage/
│           └── sqlite.py    # SQLite veri katmanı
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

---

## ⚠️ CLI Durumu (Deprecated)

Bu projede daha önce **CLI tabanlı** bir sürüm bulunmaktaydı:

```text
deprecated/cli.py
```

- ❌ **Artık aktif olarak kullanılmıyor**
- ❌ GUI sürümüyle aynı davranışı garanti etmez
- ❌ Gelecekte tamamen kaldırılabilir

CLI dosyası **referans / arşiv** amacıyla tutulmaktadır.  
Güncel ve desteklenen arayüz **GUI (Tkinter)** sürümüdür.

---

## ⚙️ Kurulum

> **Python 3.10 veya üzeri gereklidir**

```bash
git clone https://github.com/yok1rai/DepremAlarmi.git
cd DepremAlarmi
pip install .
```

---

## ▶️ Çalıştırma

```bash
python -m deprem_alarmi.main
```

Uygulama açıldığında:

1. Alarm eşiğini gir (örn. `4.0`)
2. **Başlat** butonuna bas
3. Sistem otomatik olarak izlemeye başlar

---

## 🔁 Çalışma Mantığı

1. USGS API’den bölgesel deprem verisi çekilir  
2. En güncel deprem seçilir  
3. Deprem daha önce kaydedilmemişse:
   - SQLite veritabanına eklenir  
   - Büyüklük eşiği kontrol edilir  
4. Şartlar sağlanıyorsa alarm **3 kez çalar**  
5. Aynı deprem tekrar alarm üretmez  

Sorgulama aralığı: **5 saniye**

---

## 🗄️ Veritabanı (SQLite)

- Dosya yolu: `data/earthquakes.db`
- Lokal olarak oluşturulur
- GitHub repository’sine dahil edilmez

Amaç:
- Deprem geçmişini tutmak
- Aynı deprem için tekrar alarm çalmasını önlemek

---

## 🧠 Kullanılan Teknolojiler

- Python 3.10+
- Tkinter (GUI)
- pygame.mixer (ses sistemi)
- SQLite
- USGS Earthquake API

---

## 📜 Lisans

Bu proje **Apache License 2.0** ile lisanslanmıştır.  
Detaylar için `LICENSE` dosyasına bakınız.

---

## 👤 Yazar

**yok1rai**  
GitHub: https://github.com/yok1rai

---

## ⚠️ Yasal Uyarı

Bu proje **eğitim, deney ve kişisel kullanım** amaçlıdır.  
**Resmî afet uyarı sistemlerinin yerine geçmez.**