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
├── src/
│   └── deprem_alarmi/
│       ├── fetcher.py
│       ├── processor.py
│       ├── main.py
│       ├── alarm/
│       │   ├── alarm.py
│       │   ├── rules.py
│       │   └── sound.py
│       └── storage/ (kullanılmıyor)
│           └── sqlite.py
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

1. Deprem verilerini çeker
2. Deprem verilerini filtreler
3. Deprem eşik değerini aşıyorsa, alarmı **3 kez** sesli uyarı olarak çalıştırır
4. Bu işlemleri `main.py` dosyasında birleştirir


## 🛎️ Alarm mantığı

- Alarm **tek seferlik bir olaydır**, sürekli çalmaz
- Şarta bağlı, **deprem ID bazlı** kontrol mekanizması kullanır

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
