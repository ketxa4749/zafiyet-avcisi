#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import json
import re
from datetime import datetime

# Renkler
KIRMIZI = "\033[91m"
YESIL = "\033[92m"
SARI = "\033[93m"
MAVI = "\033[94m"
RESET = "\033[0m"

def banner():
    print(f"""{MAVI}
    ############################################################
    #                                                          #
    #                  ZAFİYET ve EXPLOIT AVCISI (v2.0)        #
    #                                                          #
    #    Hedef sistemde Nmap ile zafiyet tarar ve Searchsploit #
    #             ile uygun exploit'leri arar.                 #
    #                                                          #
    ############################################################
    {RESET}""")

def arac_kontrolu(arac_adi, arac_yolu):
    """Verilen aracın sistemde kurulu olup olmadığını kontrol eder."""
    print(f"{SARI}[*] '{arac_adi}' kontrol ediliyor...{RESET}")
    if os.path.isfile(arac_yolu) and os.access(arac_yolu, os.X_OK):
        print(f"{YESIL}[+] '{arac_adi}' bulundu: {arac_yolu}{RESET}")
        return True
    else:
        print(f"{KIRMIZI}[-] HATA: '{arac_adi}' bulunamadı veya çalıştırılabilir değil: {arac_yolu}{RESET}")
        if sys.platform.startswith("linux"):
             print(f"{MAVI}[INFO] Termux için kurulum: pkg install {arac_adi}{RESET}")
             print(f"{MAVI}[INFO] Debian/Ubuntu için kurulum: sudo apt-get install {arac_adi} (exploitdb için 'exploitdb' paketi){RESET}")
        return False


def nmap_tarama(hedef, cikti_dosyasi):
    """Nmap ile zafiyet taraması yapar."""
    print(f"\n{MAVI}[*] Nmap ile zafiyet taraması başlatılıyor: {hedef}{RESET}")
    print(f"{SARI}[INFO] Bu işlem uzun sürebilir...{RESET}")
    # -sV: Versiyon tespiti, --script vuln: Zafiyet scriptlerini çalıştırır
    komut = ["nmap", "-sV", "--script", "vuln", "-oN", cikti_dosyasi, hedef]
    print(f"{SARI}[CMD] Çalıştırılan komut: {' '.join(komut)}{RESET}")
    
    try:
        # Komutu shell=False (varsayılan) ile çalıştırmak daha güvenlidir
        subprocess.run(komut, check=True, text=True, stderr=subprocess.PIPE)
        print(f"{YESIL}[+] Nmap taraması tamamlandı. Sonuçlar '{cikti_dosyasi}' dosyasına kaydedildi.{RESET}")
        return True
    except FileNotFoundError:
        print(f"{KIRMIZI}[-] HATA: 'nmap' komutu bulunamadı. Sistemde kurulu olduğundan emin olun.{RESET}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"{KIRMIZI}[-] Nmap taraması sırasında bir hata oluştu:{RESET}")
        print(f"{KIRMIZI}{e.stderr}{RESET}")
        return False

import requests

def searchsploit_arama(anahtar_kelimeler, cikti_dosyasi):
    """Exploit-DB API'si üzerinden exploit araması yapar."""
    print(f"\n{MAVI}[*] Exploit-DB API'si ile exploit araması başlatılıyor...{RESET}")
    
    if not anahtar_kelimeler:
        print(f"{SARI}[-] Aranacak anahtar kelime bulunamadı.{RESET}")
        return

    benzersiz_kelimeler = sorted(list(set(anahtar_kelimeler)))
    print(f"{SARI}[INFO] Aranacak servisler/yazılımlar: {' '.join(benzersiz_kelimeler)}{RESET}")
    
    all_results = []
    for kelime in benzersiz_kelimeler:
        try:
            url = f"https://www.exploit-db.com/search?q={kelime}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status() # HTTP hatalarını kontrol et
            # Bu API doğrudan JSON sonucu vermez, bu yüzden sonuçları HTML'den ayrıştırmamız gerekir.
            # Bu, bu betiğin kapsamı dışındadır. Şimdilik, sadece arama URL'sini sağlayacağız.
            print(f"{YESIL}[+] '{kelime}' için arama URL'si: {url}{RESET}")
            all_results.append({"arama_terimi": kelime, "url": url})
        except requests.exceptions.RequestException as e:
            print(f"{KIRMIZI}[-] '{kelime}' için Exploit-DB araması sırasında bir hata oluştu: {e}{RESET}")

    if all_results:
        with open(cikti_dosyasi, 'w') as f:
            json.dump(all_results, f, indent=4)
        print(f"{YESIL}[+] Arama URL'leri '{cikti_dosyasi}' dosyasına kaydedildi.{RESET}")
    else:
        print(f"{SARI}[-] Exploit bulunamadı veya arama sırasında bir hata oluştu.{RESET}")


def nmap_ciktisini_analiz_et(nmap_dosyasi):
    """Nmap çıktı dosyasını okuyarak potansiyel arama terimleri çıkarır."""
    terimler = set()
    # Örnek: 21/tcp open  ftp     vsftpd 3.0.3
    # Örnek: 80/tcp open  http    Apache httpd 2.4.38 ((Debian))
    pattern = re.compile(r"^\d+/tcp\s+open\s+[^\s]+\s+(.*)", re.IGNORECASE)
    
    try:
        with open(nmap_dosyasi, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = pattern.search(line.strip())
                if match:
                    servis_bilgisi = match.group(1).lower().split()
                    # Genellikle ilk kelime ürün adıdır (örn: vsftpd, openssh, apache)
                    if len(servis_bilgisi) > 0:
                        urun = servis_bilgisi[0]
                        terimler.add(urun)
                        
                        # Versiyon numarası içeren sonraki kelimeleri bul
                        for kelime in servis_bilgisi[1:]:
                            if any(char.isdigit() for char in kelime):
                                versiyon = re.match(r"[\d\.]+", kelime)
                                if versiyon:
                                    terimler.add(f"{urun} {versiyon.group(0)}")
                                break # İlk versiyonu bulduktan sonra dur

        if terimler:
            print(f"{YESIL}[+] Nmap çıktısından potansiyel arama terimleri çıkarıldı: {list(terimler)}{RESET}")
        else:
            print(f"{SARI}[-] Nmap çıktısından potansiyel arama terimi çıkarılamadı.{RESET}")
        return list(terimler)
    except FileNotFoundError:
        print(f"{KIRMIZI}[-] Nmap çıktı dosyası bulunamadı: {nmap_dosyasi}{RESET}")
        return []


def main():
    banner()
    
    nmap_yolu = "/data/data/com.termux/files/usr/bin/nmap"

    if not arac_kontrolu('nmap', nmap_yolu):
        sys.exit(1)

    if len(sys.argv) < 2:
        print(f"{KIRMIZI}[-] HATA: Lütfen komut satırı argümanı olarak bir hedef IP veya URL belirtin.{RESET}")
        print(f"{MAVI}[INFO] Kullanım: python {sys.argv[0]} <hedef_ip_veya_url>{RESET}")
        sys.exit(1)
    
    hedef = sys.argv[1]

    # Çıktı dosyaları için isimlendirme
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Hedefteki geçersiz karakterleri temizle
    sadece_harf_rakam = re.sub(r'[^a-zA-Z0-9_.-]', '_', hedef)
    hedef_klasor = f"scan_results_{sadece_harf_rakam}_{timestamp}"
    
    try:
        if not os.path.exists(hedef_klasor):
            os.makedirs(hedef_klasor)
    except OSError as e:
        print(f"{KIRMIZI}[-] Sonuç klasörü oluşturulamadı: {e}{RESET}")
        sys.exit(1)
        
    nmap_cikti_dosyasi = os.path.join(hedef_klasor, f"nmap_scan.txt")
    searchsploit_cikti_dosyasi = os.path.join(hedef_klasor, f"searchsploit_results.json")

    if nmap_tarama(hedef, nmap_cikti_dosyasi):
        aranacak_terimler = nmap_ciktisini_analiz_et(nmap_cikti_dosyasi)
        if aranacak_terimler:
            searchsploit_arama(aranacak_terimler, searchsploit_cikti_dosyasi)
        else:
            print(f"{SARI}[INFO] Nmap çıktısından exploit aranacak bir servis/yazılım bilgisi otomatik olarak çıkarılamadı.{RESET}")
            print(f"{SARI}[INFO] Lütfen '{nmap_cikti_dosyasi}' dosyasını manuel olarak inceleyip 'searchsploit <anahtar_kelime>' komutunu çalıştırın.{RESET}")

    print(f"\n{YESIL}[*] İşlem tamamlandı. Tüm sonuçlar '{hedef_klasor}' klasöründe.{RESET}")

if __name__ == "__main__":
    main()
