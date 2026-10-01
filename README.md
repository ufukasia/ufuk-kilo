# Ufuk ASIL Kaç Santim, Kaç Kilo? — Sınıf İçi Tahmin Oyunu

Derste "kolektif akıl" (kalabalığın ortalama tahmini) fikrini göstermek için hazırlanmış tek sayfalık bir Streamlit uygulaması. Öğrenciler hocanın boyunu ve kilosunu tahmin eder; tahminler anonim olarak kaydedilir ve istenildiğinde sınıf ortalaması gösterilir.

## Özellikler

- Boy (cm, 100–999) ve kilo (kg, 10–999) için tam sayı tahmin formu.
- **Kolektif akıl perdesini aç** düğmesiyle tahminci sayısı, ortalama boy ve ortalama kilo.
- Onay kutusuyla korunan "tüm tahminleri sil" düğmesi.
- Tahminler yalnızca boy, kilo ve kayıt zamanı olarak `ufuk_asil_tahminleri.sqlite3` dosyasında tutulur; isim veya öğrenci numarası istenmez.

## Kurulum ve çalıştırma

```bash
pip install -r requirements.txt
streamlit run app.py
```

Veritabanı dosyası ve tablo ilk çalıştırmada otomatik oluşturulur.

## Proje yapısı

```
ufuk-kilo/
├── app.py                         # Uygulama
├── requirements.txt               # streamlit
└── ufuk_asil_tahminleri.sqlite3   # Tahmin veritabanı
```

## İletişim

Dr. Öğr. Üyesi Ufuk Asil, Ostim Teknik Üniversitesi.
