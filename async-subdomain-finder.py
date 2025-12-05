import aiohttp
import asyncio

target = "example.com"
MAX_CONCURRENCY = 100  

sem = asyncio.Semaphore(MAX_CONCURRENCY)
write_lock = asyncio.Lock()

async def subDomain_kontrol(session, word):
    word = word.strip()
    url = f"http://{word}.{target}"

    async with sem:
        try:
            async with session.get(url) as response:
                if response.status < 400:
                    print(f"[+] Bulundu: {url} (HTTP {response.status})")

                    async with write_lock:
                        with open("found.txt", "a") as f:
                            f.write(f"[+] Bulundu: {url} (HTTP {response.status})\n")
                else:
                    print(f"[-] HTTP {response.status}: {url}")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            pass
            # print(f"[-] Yok: {url} ({e.__class__.__name__})")
        except Exception as e:
            pass
            # print(f"[!] Beklenmeyen hata {url} -> {e}")

async def main():
    with open("wordlist.txt", "r") as subdomain:
        words = subdomain.read().splitlines()

    timeout = aiohttp.ClientTimeout(total=3)
    connector = aiohttp.TCPConnector(limit=100)  # TCP bağlantı limiti

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [subDomain_kontrol(session, word) for word in words]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
