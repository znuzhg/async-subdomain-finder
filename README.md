# 🚀 async-subdomain-finder  
Yüksek performanslı **asenkron subdomain bulucu**.  
`aiohttp + asyncio` kullanarak aynı anda yüzlerce isteği paralel yapar.  
Hızlı, hafif ve pentest odaklı bir keşif aracıdır.

---

## 📌 Özellikler
- ⚡ **Async IO** sayesinde ultra hızlı tarama  
- 🌐 Aynı anda **100+ eşzamanlı istek**  
- 📁 Bulunan subdomain'leri otomatik olarak `found.txt` dosyasına kaydeder  
- 🧵 Güvenli dosya yazımı için **asyncio.Lock()**  
- 🔒 Sessiz mod: hatalar loglanmaz, sadece bulunanlar gösterilir  
- 🛠 Minimal, okunabilir ve modüler Python tasarımı  

---

## 📦 Kurulum

### 1) Depoyu klonla
```bash
git clone https://github.com/<username>/async-subdomain-finder.git
cd async-subdomain-finder
```
2) Gerekli kütüphaneyi yükle
```bash
pip install aiohttp
```
▶️ Kullanım
1) wordlist.txt dosyanı oluştur

Her satıra bir subdomain yaz:
```bash
www
mail
ftp
api
dev
test
stage
```
2) Scripti çalıştır
```bash
python3 finder.py
```
3) Sonuçlar nereye kaydediliyor?

Başarılı bulunan subdomain’ler şu dosyada tutulur:
```bash
found.txt
```

Format:
```bash
[+] Bulundu: http://api.example.com (HTTP 200)
```
🧠 Çalışma Mantığı
---
Araç:

wordlist.txt listesini okur

Her kelime için http://sub.example.com URL’si oluşturur

asyncio.Semaphore ile aynı anda en fazla 100 istek gönderir

HTTP durumu < 400 ise geçerli kabul edip çıktı ve dosya kaydı yapar

Hataları sessizce geçer (isteğe göre açılabilir)
---
🧩 Kod Mantığı (Özet)
sem = asyncio.Semaphore(100)
write_lock = asyncio.Lock()

async def subDomain_kontrol(session, word):
    async with sem:
        async with session.get(url) as response:
            if response.status < 400:
                async with write_lock:
                    # found.txt dosyasına yaz
---
