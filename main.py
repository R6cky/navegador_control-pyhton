import subprocess, time, requests,threading, psutil, socket

MAIN_URL = "https://gpa.tolife.app"
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
            ["python3", "server.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Servidor HTTP iniciado")




def stop_server():
    global server_process
    if server_process:
        server_process.terminate()
        server_process = None
        print("Servidor HTTP está parado.")
        
        

def start_browser(url):
    global browser_process
    if browser_process:
        browser_process.terminate()
    
    
    browser_process = subprocess.Popen(
        ["qutebrowser", MAIN_URL],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Navegador iniciado em: {MAIN_URL}" )
    


def monitor():
    offline_time = 0
    global browser_process
    
    while True:
        if internet_ok():
            offline_time = 0
            
            if browser_process and MAIN_URL not in get_browser_url():
                print("Internet voltou, redirecionando...")
                start_browser(MAIN_URL)
                
            stop_server()
            
            
        else:
            offline_time += CHECK_INTERVAL
            print(f"Sem internet há {offline_time} segundos")
            
            if offline_time >= OFFLINE_LIMIT:
                print("5 minutos offline. Ativando servidor  + redirecionamento.")
                start_server()
                start_browser(LOCAL_URL)
                
        time.sleep(CHECK_INTERVAL)



def get_browser_url():
    """Obtem a url aberta no qutebrowser via socket rpc (mais leve)"""
            
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect("/run/user/1000/qutebrowser/ipc-0")
        s.send(b'{"command": ["tab-info"]}')
        resp = s.recv(4096).decode()
        s.close()

        if  '"url": "' in resp:
            return resp.split('"url": "')[1].split('"')[0]
    except:
        pass
    return ""



if __name__=="__main__":
    print("Iniciando sistema...")
    start_browser(MAIN_URL)
    
    
    monitor_tread = threading.Thread(target=monitor)
    monitor_tread.daemon = True
    monitor_tread.start()
    
    
# Mantém o script vivo
while True:
    time.sleep(1)
    