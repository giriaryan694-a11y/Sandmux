import argparse
import socket
import threading
import select
import subprocess
import sys
import os

# New UI Imports
import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama to auto-reset colors after each print statement
init(autoreset=True)

def print_banner():
    """Displays the Sandmux ASCII banner and credits."""
    banner = pyfiglet.figlet_format("Sandmux")
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + "Made By Aryan Giri | giriaryan694-a11y")
    print(Fore.MAGENTA + "-" * 55)

# --- PROXY SERVER LOGIC ---

def load_list(filepath):
    """Loads a list of domains/IPs from a file."""
    if not filepath or not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as f:
        return set(line.strip().lower() for line in f if line.strip() and not line.startswith('#'))

def is_allowed(host, allowlist, denylist):
    """Determines if a host should be allowed through the proxy."""
    if host in denylist:
        return False
    if allowlist:
        return host in allowlist
    return False

def handle_client(client_socket, allowlist, denylist):
    """Handles an incoming proxy connection."""
    try:
        request = client_socket.recv(4096)
        if not request:
            return

        first_line = request.split(b'\n')[0].decode('utf-8', errors='ignore')
        method, url, _ = first_line.split(' ')

        if method == 'CONNECT':
            host, port_str = url.split(':')
            port = int(port_str)
        else:
            url_parts = url.replace("http://", "").split('/')
            host_port = url_parts[0].split(':')
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else 80

        host = host.lower()

        if not is_allowed(host, allowlist, denylist):
            print(Fore.RED + f"[BLOCKED] Connection to {host}:{port} denied by policy.")
            client_socket.close()
            return
        
        print(Fore.GREEN + f"[ALLOWED] Connection to {host}:{port}")

        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, port))

        if method == 'CONNECT':
            client_socket.send(b'HTTP/1.1 200 Connection Established\r\n\r\n')
        else:
            remote_socket.send(request)

        sockets = [client_socket, remote_socket]
        while True:
            read_sockets, _, error_sockets = select.select(sockets, [], sockets, 10)
            if error_sockets:
                break
            
            for sock in read_sockets:
                other_sock = remote_socket if sock is client_socket else client_socket
                data = sock.recv(4096)
                if data:
                    other_sock.send(data)
                else:
                    return 

    except Exception:
        pass 
    finally:
        client_socket.close()

def start_proxy(port, allowlist, denylist):
    """Starts the proxy server loop."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(10)
    print(Fore.BLUE + f"[*] Secure Proxy running on 127.0.0.1:{port}")
    
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(
            target=handle_client, 
            args=(client_socket, allowlist, denylist)
        )
        client_thread.daemon = True
        client_thread.start()

# --- SANDBOX LIFECYCLE & LAUNCHER LOGIC ---

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Sandmux - Termux Isolated Python Sandbox")
    parser.add_argument('--allowlist', type=str, help='File containing allowed domains/IPs')
    parser.add_argument('--denylist', type=str, help='File containing blocked domains/IPs')
    parser.add_argument('--port', type=int, default=8080, help='Local proxy port (default: 8080)')
    parser.add_argument('--delete', action='store_true', help='Delete the Ubuntu sandbox and exit')
    parser.add_argument('--reset', action='store_true', help='Wipe and reinstall the Ubuntu sandbox before launching')
    args = parser.parse_args()

    # Handle Sandbox Deletion
    if args.delete:
        print(Fore.RED + "[*] Deleting the Ubuntu sandbox...")
        subprocess.run(["proot-distro", "remove", "ubuntu"])
        print(Fore.GREEN + "[*] Sandbox successfully deleted.")
        sys.exit(0)

    # Handle Sandbox Reset
    if args.reset:
        print(Fore.YELLOW + "[*] Resetting sandbox: Removing existing Ubuntu environment...")
        subprocess.run(["proot-distro", "remove", "ubuntu"])
        print(Fore.YELLOW + "[*] Resetting sandbox: Reinstalling fresh Ubuntu environment...")
        subprocess.run(["proot-distro", "install", "ubuntu"])
        print(Fore.GREEN + "[*] Sandbox successfully reset.")

    # Proceed to launch
    allowlist = load_list(args.allowlist)
    denylist = load_list(args.denylist)

    if not allowlist:
        print(Fore.YELLOW + Style.BRIGHT + "[!] WARNING: No allowlist provided. All network traffic will be blocked.")

    # 1. Start Proxy
    proxy_thread = threading.Thread(target=start_proxy, args=(args.port, allowlist, denylist))
    proxy_thread.daemon = True
    proxy_thread.start()

    # 2. Launch proot-distro
    proxy_url = f"http://127.0.0.1:{args.port}"
    proot_cmd = [
        "proot-distro", "login", "ubuntu",
        "--isolated",
        "--shared-tmp",
        "--env", f"http_proxy={proxy_url}",
        "--env", f"https_proxy={proxy_url}",
        "--env", f"HTTP_PROXY={proxy_url}",
        "--env", f"HTTPS_PROXY={proxy_url}"
    ]

    print(Fore.BLUE + Style.BRIGHT + "[*] Launching isolated Ubuntu sandbox...")
    try:
        subprocess.run(proot_cmd)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[*] Exiting sandbox.")
    
    print(Fore.GREEN + "[*] Sandbox closed. Shutting down proxy.")
    sys.exit(0)

if __name__ == "__main__":
    main()
