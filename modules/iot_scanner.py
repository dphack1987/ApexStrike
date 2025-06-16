#!/usr/bin/env python3
import socket
import requests
import threading
import paho.mqtt.client as mqtt
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

class IoTScanner:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []
        self.devices = []
        self.lock = threading.Lock()
        
    def scan_iot_device(self):
        """Scan IoT device for common vulnerabilities"""
        print(f"\n{Fore.YELLOW}[*] Starting IoT device scan on {self.target}{Style.RESET_ALL}")
        
        # Test common IoT protocols
        self._test_mqtt()
        self._test_coap()
        self._test_telnet()
        self._test_default_credentials()
        
        return self.vulnerabilities, self.devices

    def _test_mqtt(self):
        """Test MQTT protocol vulnerabilities"""
        print(f"\n{Fore.CYAN}[*] Testing MQTT protocol...{Style.RESET_ALL}")
        
        # Common MQTT ports
        mqtt_ports = [1883, 8883]
        
        for port in mqtt_ports:
            try:
                client = mqtt.Client()
                client.connect(self.target, port, 5)
                
                # Test anonymous access
                try:
                    client.connect(self.target, port, 5)
                    self._add_vulnerability("MQTT", f"Anonymous access allowed on port {port}")
                except:
                    pass
                
                # Test default credentials
                default_creds = [
                    ('admin', 'admin'),
                    ('mqtt', 'mqtt'),
                    ('root', 'root'),
                    ('test', 'test')
                ]
                
                for username, password in default_creds:
                    try:
                        client.username_pw_set(username, password)
                        client.connect(self.target, port, 5)
                        self._add_vulnerability("MQTT", 
                            f"Default credentials work: {username}:{password} on port {port}")
                    except:
                        continue
                        
            except Exception as e:
                print(f"{Fore.RED}[!] Error testing MQTT on port {port}: {str(e)}{Style.RESET_ALL}")

    def _test_coap(self):
        """Test CoAP protocol vulnerabilities"""
        print(f"\n{Fore.CYAN}[*] Testing CoAP protocol...{Style.RESET_ALL}")
        
        # CoAP default port
        coap_port = 5683
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            
            # Simple CoAP discovery message
            discovery_msg = b'\x40\x01\x00\x01\xbb\x2e\x77\x65\x6c\x6c\x2d\x6b\x6e\x6f\x77\x6e\x04\x63\x6f\x72\x65'
            
            sock.sendto(discovery_msg, (self.target, coap_port))
            data, addr = sock.recvfrom(1024)
            
            if data:
                self._add_device("CoAP", f"CoAP service running on port {coap_port}")
                
                # Check if device responds to unauthorized requests
                if len(data) > 0:
                    self._add_vulnerability("CoAP", 
                        "Device responds to unauthorized CoAP discovery")
                    
        except Exception as e:
            print(f"{Fore.RED}[!] Error testing CoAP: {str(e)}{Style.RESET_ALL}")

    def _test_telnet(self):
        """Test Telnet vulnerabilities"""
        print(f"\n{Fore.CYAN}[*] Testing Telnet...{Style.RESET_ALL}")
        
        telnet_port = 23
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.target, telnet_port))
            
            if result == 0:
                self._add_vulnerability("Telnet", 
                    "Telnet port open - Consider using SSH instead")
                
                # Test default credentials
                self._test_default_credentials()
                
        except Exception as e:
            print(f"{Fore.RED}[!] Error testing Telnet: {str(e)}{Style.RESET_ALL}")

    def _test_default_credentials(self):
        """Test for default credentials on various services"""
        print(f"\n{Fore.CYAN}[*] Testing default credentials...{Style.RESET_ALL}")
        
        default_creds = [
            ('admin', 'admin'),
            ('root', 'root'),
            ('admin', 'password'),
            ('administrator', 'admin'),
            ('user', 'user'),
            ('default', 'default'),
            ('admin', ''),
            ('root', ''),
        ]
        
        # Test HTTP basic auth
        for username, password in default_creds:
            try:
                response = requests.get(f'http://{self.target}', 
                    auth=(username, password), timeout=5)
                
                if response.status_code == 200:
                    self._add_vulnerability("Default Credentials", 
                        f"HTTP Basic Auth credentials work: {username}:{password}")
            except:
                continue

    def scan_network(self, subnet):
        """Scan network for IoT devices"""
        print(f"\n{Fore.YELLOW}[*] Scanning network {subnet} for IoT devices{Style.RESET_ALL}")
        
        # Common IoT ports
        iot_ports = [80, 443, 1883, 5683, 8883, 23, 2323, 8080]
        
        try:
            # Parse subnet (e.g., 192.168.1.0/24)
            network = subnet.split('/')[0]
            bits = int(subnet.split('/')[1])
            
            # Calculate network range
            network_addr = network.split('.')
            start_ip = '.'.join(network_addr[:-1]) + '.1'
            end_ip = '.'.join(network_addr[:-1]) + '.254'
            
            def scan_host(ip):
                for port in iot_ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result = sock.connect_ex((ip, port))
                        
                        if result == 0:
                            self._add_device("Network", 
                                f"Device found at {ip}:{port}")
                            
                            # Try to get device info
                            if port in [80, 8080]:
                                try:
                                    response = requests.get(f'http://{ip}:{port}', timeout=5)
                                    server = response.headers.get('Server', '')
                                    if server:
                                        self._add_device("HTTP", 
                                            f"Server at {ip}:{port} - {server}")
                                except:
                                    pass
                                    
                        sock.close()
                    except:
                        continue
            
            # Scan hosts in parallel
            with ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(scan_host, [f"{'.'.join(network_addr[:-1])}.{i}" 
                    for i in range(1, 255)])
                
        except Exception as e:
            print(f"{Fore.RED}[!] Error scanning network: {str(e)}{Style.RESET_ALL}")

    def _add_vulnerability(self, vuln_type, description):
        """Add found vulnerability to the list"""
        with self.lock:
            self.vulnerabilities.append({
                'type': vuln_type,
                'description': description
            })
            print(f"{Fore.RED}[!] Found {vuln_type}: {description}{Style.RESET_ALL}")

    def _add_device(self, device_type, description):
        """Add found device to the list"""
        with self.lock:
            self.devices.append({
                'type': device_type,
                'description': description
            })
            print(f"{Fore.GREEN}[+] Found {device_type}: {description}{Style.RESET_ALL}")

    def generate_report(self):
        """Generate a detailed report of findings"""
        report = {
            'target': self.target,
            'vulnerabilities': self.vulnerabilities,
            'devices': self.devices
        }
        
        return report
