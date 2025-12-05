![Python](https://img.shields.io/badge/Python-3.10+-blue)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
![Status](https://img.shields.io/badge/Status-Active-success)
![Interface](https://img.shields.io/badge/Interface-CLI-lightgrey)
[![Author](https://img.shields.io/badge/Author-yok1rai-brown?logo=github)](https://github.com/yok1rai)

# 🚨 Deprem alarmı

Türkiye ve çevresindeki depremleri **gerçek zamanlı olarak takip eden**, belirlenen şiddet eşiğinin üzerindeki depremleri **otomatik sesli alarm veren** Python tabanlı bir **CLI deprem alarm sistemidir**.

---

## ✨ Özellikler

- 📡 Canlı deprem verisi çekme
- 🧠 Akıllı alarm mantığı (durum temelli)
- 🔔 Alarm tetiklendiğinde **3 kez sesli uyarı**
- 🚫 Aynı deprem için tekrar alarm verilmez
- 🧩 Modüler yapı
- `pygame.mixer` tabanlı stabil ses sistemi

## 📂 Proje yapısı

```text
Deprem alarmı/
├── assets/
│   └── sounds/
│       └── anons.wav
├── data/
│   └── earthquakes.db       # Çalışma sırasında oluşur (git'e girmez)
├── src/
│   └── deprem_alarmi/
│       ├── fetcher.py       # Global deprem API kaynağı
│       ├── processor.py     # Veri işleme / filtreleme
│       ├── main.py          # Uygulama orkestrasyonu
│       ├── alarm/
│       │   ├── alarm.py     # Alarm davranışı
│       │   ├── rules.py     # Eşik kuralları
│       │   └── sound.py     # Ses işlemleri
│       └── storage/
│           └── sqlite.py    # Lokal SQLite kayıt katmanı
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## ⚙️ Kurulum

> Python **3.10 veya üzeri** gereklidir

### 1 — Depoyu klonla

```bash
git clone https://github.com/yok1rai/DepremAlarmi.git
cd DepremAlarmi
```

### 2 — Gerekli paketleri yükle

#### Kullanıcılar için

```bash
pip install .
```

#### Geliştiriciler için

```bash
pip install -e .
```

### 3 — Çalıştırma

```bash
python -m deprem_alarmi.main
```

## 🔁 Çalışma mantığı

1. Global deprem API’sinden canlı veri çeker
2. En güncel deprem verisini işler
3. Deprem SQLite veritabanında yoksa:
    - Kaydeder
    - Eşik değerini kontrol eder
    - Alarmı 3 kez sesli uyarı olarak çalıştırır
4. Aynı deprem tekrar geldiğinde alarm verilmez


## 🛎️ Alarm mantığı

- Alarm **tek seferlik bir olaydır**, sürekli çalmaz
- Şarta bağlı, **deprem ID bazlı** kontrol mekanizması kullanır
- Geçmiş kayıtlar **SQLite’ta** tutulur

> Alarm sesi varsayılan olarak **3 tekrar** olacak şekilde ayarlanmıştır.
> Bu davranış `alarm/alarm.py` üzerinden değiştirilebilir.


|Durum|Alarm Davranışı|
|:--|:---|
|Yeni deprem ≥ eşik|🔔 3 kez çalar|
|Yeni deprem < eşik|❌ Alarm yok|
|Aynı deprem ID|🔇 Tekrar çalmaz|
|Veri yok|❌ Alarm yok|

Bu sayede:

- Alarm spam yapmaz
- Aynı depremde tekrar tekrar çalmaz

## 🗄️ Veritabanı (SQLite)

- Veriler çalışma sırasında `data/earthquakes.db` dosyasına yazılır
- Bu dosya **yereldir** ve **GitHub repository’sine dahil edilmez**
- Her kullanıcıda veritabanı ayrı tutulur

SQLite yalnızca:
- Deprem geçmişini tutmak
- Aynı deprem için tekrar alarm verilmesini önlemek

amacıyla kullanılır.

## 🔧 Eşik değeri

Varsayılan alarm eşiği:

```text
4.5
```

Değiştirmek için `alarm/rules.py`'deki `def should_alarm(quake, threshold=4.5):`'un **threshold** değerini değiştirebilirsiniz

## 🧠 Kullanılan teknolojiler

- Python 3.10+
- pygame.mixer (ses sistemi)
- CLI tabanlı yapı
- Modüler mimari

## 📜 Lisans

Bu proje Apache License 2.0 ile lisanslanmıştır.
Detaylar için: LICENSE

## 👤 Yazar

[yok1rai](https://github.com/yok1rai) tarafından yapılmıştır

## ℹ️ Dipnot

*Bu proje eğitim, test ve kişisel kullanım amaçlıdır.* <br>
*Resmî afet kurumlarının yerine geçmez*
