import subprocess, time, requests,threading, psutil, socket

MAIN_URL = "gpa.tolife.app"
LOCAL_URL = "http://127.0.0.1:8080"
CHECK_INTERVAL = 10
#OFFLINE_LIMIT = 300
OFFLINE_LIMIT = 5

server_process = None
browser_process = None

def internet_ok():
    """Testa internet tentando acessar a página do google"""
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False
    
    
def start_server():
    global server_process
    if server_process is None:
        server_process = subprocess.Popen(
            ["python3", "server.py"]
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Servidor HTTP iniciado")




        
    