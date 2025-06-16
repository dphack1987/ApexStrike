#!/usr/bin/env python3
import socket
import threading
import time
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.lock = threading.Lock()

    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                with self.lock:
                    service = self._get_service_name(port)
                    banner = self._get_banner(sock)
                    self.open_ports.append((port, service, banner))
                    print(f"{Fore.GREEN}[+] Port {port} is open - Service: {service} - Banner: {banner}{Style.RESET_ALL}")
            sock.close()
        except:
            pass

    def _get_service_name(self, port):
        """Get service name for a port"""
        try:
            service = socket.getservbyport(port)
            return service
        except:
            return "unknown"

    def _get_banner(self, sock):
        """Attempt to grab service banner"""
        try:
            sock.send(b'GET / HTTP/1.1\r\n\r\n')
            banner = sock.recv(1024).decode().strip()
            return banner[:40] + '...' if len(banner) > 40 else banner
        except:
            return "No banner"

    def run_scan(self, start_port, end_port, threads=100):
        """Run port scan with multiple threads"""
        print(f"\n{Fore.YELLOW}[*] Starting port scan on {self.target}{Style.RESET_ALL}")
        try:
            target_ip = socket.gethostbyname(self.target)
            print(f"{Fore.GREEN}[+] Target IP: {target_ip}{Style.RESET_ALL}")

            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(self.scan_port, range(start_port, end_port + 1))

            duration = time.time() - start_time
            print(f"\n{Fore.CYAN}[*] Scan completed in {duration:.2f} seconds{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Found {len(self.open_ports)} open ports{Style.RESET_ALL}")

            return self.open_ports

        except socket.gaierror:
            print(f"{Fore.RED}[!] Hostname could not be resolved{Style.RESET_ALL}")
            return []
        except socket.error:
            print(f"{Fore.RED}[!] Could not connect to server{Style.RESET_ALL}")
            return []
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}[!] Scan interrupted by user{Style.RESET_ALL}")
            return self.open_ports
