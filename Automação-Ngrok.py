import subprocess
import time
import requests
import os
import platform
import urllib.request
from twilio.rest import Client

def download_ngrok():
    print("Baixando o ngrok...")
    os_type = platform.system().lower()
    ngrok_url = ""
    
    if os_type == "windows":
        ngrok_url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip"
        download_path = "ngrok.zip"
    elif os_type == "linux":
        ngrok_url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
        download_path = "ngrok.zip"
    elif os_type == "darwin":
        ngrok_url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip"
        download_path = "ngrok.zip"
    else:
        print("Sistema operacional não suportado.")
        return
    
    urllib.request.urlretrieve(ngrok_url, download_path)
    print("Descompactando o ngrok...")
    subprocess.run(["unzip", download_path], check=True)
    os.remove(download_path)
    print("Ngrok baixado e descompactado com sucesso!")

def start_ngrok(port):
    ngrok_path = "./ngrok" 
    if not os.path.exists(ngrok_path):
        print("Ngrok não encontrado. Iniciando o download...")
        download_ngrok()
    
    print(f"Iniciando o ngrok na porta {port}...")
    subprocess.Popen([ngrok_path, "http", str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) 

def get_ngrok_url():
  
    NGROK_API_URL = "http://127.0.0.1:4040/api/tunnels"
    try:
        response = requests.get(NGROK_API_URL).json()
        public_url = response['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        print(f"Erro ao capturar a URL do ngrok: {e}")
        return None

def update_env_file(url, env_file_path):

    try:
        with open(env_file_path, "w") as file:
            file.write(f"NGROK_URL={url}\n")
        print(f".env atualizado com sucesso em {env_file_path} com a URL: {url}")
    except Exception as e:
        print(f"Erro ao atualizar o arquivo .env: {e}")

def send_whatsapp_message(account_sid, auth_token, from_whatsapp, to_whatsapp, message):

    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            from_=f"whatsapp:{from_whatsapp}",
            body=message,
            to=f"whatsapp:{to_whatsapp}"
        )
        print(f"Mensagem enviada com sucesso via WhatsApp! SID: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem via WhatsApp: {e}")

def main():
    PORT = 3000

    # ----------   Modificar caminho para chegar na pasta do .env do projeto  ---------
    env_file_path = r"C:\xampp\htdocs\Sistema_de_Sao_Jorge\.env"
    # ----------------------------------------------------------------------------------

    account_sid = "0000000000000000000"
    auth_token = "000000000000000000000"
    from_whatsapp = "0000000000000000"
    to_whatsapp = "0000000000000000000"

    start_ngrok(PORT)
    
    url = None
    while not url:
        print("Tentando capturar a URL do ngrok...")
        url = get_ngrok_url()
        if not url:
            time.sleep(2)

    print(f"URL pública do ngrok: {url}")
    update_env_file(url, env_file_path)

    whatsapp_message = f"A URL pública do servidor é: {url}"
    send_whatsapp_message(account_sid, auth_token, from_whatsapp, to_whatsapp, whatsapp_message)

if __name__ == "__main__":
    main()
