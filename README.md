# Zafiyet ve Exploit Avcısı

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)

Bu araç, hedef bir sistem üzerinde **Nmap** kullanarak otomatik olarak zafiyet taraması yapar ve bulunan servis/versiyon bilgilerine göre **Exploit-DB** üzerinden potansiyel exploitleri arar. Süreci otomatikleştirerek sızma testi ve güvenlik analizlerinde zaman kazandırmayı hedefler.

## 🚀 Temel Özellikler

- **Otomatik Nmap Taraması**: Hedef sistemde `nmap -sV --script vuln` komutunu çalıştırarak servisleri, versiyonları ve bilinen zafiyetleri tespit eder.
- **Akıllı Exploit Arama**: Nmap çıktısını analiz ederek potansiyel anahtar kelimeler (örn: `vsftpd 2.3.4`, `apache`, `openssh 8.2`) çıkarır.
- **Exploit-DB Entegrasyonu**: Çıkarılan anahtar kelimeler ile Exploit-DB web sitesi üzerinde arama yapar ve ilgili arama URL'lerini kaydeder.
- **Düzenli Çıktı Yönetimi**: Her tarama için `scan_results_hedef_tarih` formatında ayrı bir klasör oluşturur ve tüm sonuçları bu klasörde saklar.
- **Renkli ve Anlaşılır Arayüz**: Konsol çıktılarını renklendirerek süreci daha kolay takip etmenizi sağlar.
- **Bağımlılık Kontrolü**: Çalıştırmadan önce gerekli olan `nmap` gibi araçların sistemde kurulu olup olmadığını kontrol eder.

## 🛠️ Kurulum ve Gereksinimler

Aracı çalıştırmadan önce sisteminizde aşağıdaki araçların ve kütüphanelerin kurulu olması gerekmektedir:

1.  **Python 3**:
    *   Araç Python 3 ile yazılmıştır. Sisteminizde kurulu değilse resmi sitesinden indirebilirsiniz.

2.  **Nmap**:
    *   **Debian/Ubuntu**: `sudo apt-get update && sudo apt-get install nmap`
    *   **Termux**: `pkg install nmap`

3.  **Python Kütüphaneleri**:
    *   Gerekli olan `requests` kütüphanesini pip ile kurun:
        ```bash
        pip install requests
        ```

## 🏃‍♂️ Nasıl Kullanılır?

Aracı kullanmak oldukça basittir. Terminal veya komut satırını açın ve aşağıdaki komutu çalıştırın:

```bash
python3 zafiyet_avcisi.py <hedef_ip_veya_url>
```

**Örnek Kullanım:**
```bash
python3 zafiyet_avcisi.py 192.168.1.10
```
veya
```bash
python3 zafiyet_avcisi.py example.com
```

Araç çalışmaya başladığında adımları konsolda size bildirecektir.

## 📂 Çıktı Dosyaları

Tarama tamamlandığında, sonuçlar projenin ana dizininde oluşturulan `scan_results_...` adlı bir klasörün içinde yer alır.

-   `nmap_scan.txt`: Nmap taramasının ham çıktısını içerir. Tüm açık portlar, servisler, versiyonlar ve zafiyet scriptlerinin sonuçları bu dosyada bulunur.
-   `searchsploit_results.json`: Nmap çıktısından tespit edilen servislere yönelik Exploit-DB arama sonuçlarını (URL'lerini) içeren JSON formatındaki dosyadır.

## ⚠️ Yasal Uyarı

Bu araç sadece **yasal ve etik** amaçlar için tasarlanmıştır. Sadece test etme yetkinizin olduğu sistemlerde kullanın. İzinsiz sistemlerde tarama yapmak yasa dışıdır ve ciddi sonuçlar doğurabilir. Geliştirici, aracın yasa dışı kullanımından sorumlu tutulamaz.

---
*Geliştiren: ketxa4749*
