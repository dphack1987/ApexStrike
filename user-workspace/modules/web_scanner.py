#!/usr/bin/env python3
import requests
import threading
import queue
import json
from urllib.parse import urljoin
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

class WebScanner:
    def __init__(self, target):
        self.target = target if target.startswith(('http://', 'https://')) else f'http://{target}'
        self.vulnerabilities = []
        self.endpoints = []
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'PenTest-CLI/2.0',
            'Accept': '*/*',
            'Connection': 'close'
        }

    def test_endpoint(self, endpoint, method="GET", data=None):
        """Test a single endpoint for vulnerabilities"""
        url = urljoin(self.target, endpoint)
        try:
            response = self.session.request(method, url, data=data, timeout=5, verify=False)
            status_code = response.status_code
            
            with self.lock:
                if status_code == 200:
                    print(f"{Fore.GREEN}[+] Found: {url} - Status: {status_code}{Style.RESET_ALL}")
                    self._analyze_response(url, response)
                elif status_code in [401, 403]:
                    print(f"{Fore.YELLOW}[!] Protected: {url} - Status: {status_code}{Style.RESET_ALL}")
                    self.endpoints.append((url, status_code, "Protected endpoint"))
                return status_code
                
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Error testing {url}: {str(e)}{Style.RESET_ALL}")
            return None

    def _analyze_response(self, url, response):
        """Analyze response for potential vulnerabilities"""
        try:
            # Check for sensitive information in response
            sensitive_patterns = [
                'password', 'api_key', 'secret', 'token',
                'admin', 'root', 'config', 'database'
            ]
            
            content = response.text.lower()
            headers = str(response.headers).lower()
            
            # Check response headers
            if 'x-powered-by' in headers:
                self._add_vulnerability(url, "Information Disclosure", 
                                     f"Server technology revealed: {response.headers['X-Powered-By']}")
            
            # Check for missing security headers
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-XSS-Protection': 'XSS protection',
                'X-Content-Type-Options': 'MIME-type sniffing protection',
                'Content-Security-Policy': 'CSP',
                'Strict-Transport-Security': 'HSTS'
            }
            
            for header, description in security_headers.items():
                if header.lower() not in headers:
                    self._add_vulnerability(url, "Missing Security Header", 
                                         f"Missing {header} ({description})")
            
            # Check for sensitive information in response
            for pattern in sensitive_patterns:
                if pattern in content:
                    self._add_vulnerability(url, "Information Leakage", 
                                         f"Possible sensitive information disclosure: {pattern}")
            
            # Check for common vulnerabilities
            self._check_sql_injection(url)
            self._check_xss(url)
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error analyzing response from {url}: {str(e)}{Style.RESET_ALL}")

    def _add_vulnerability(self, url, vuln_type, description):
        """Add found vulnerability to the list"""
        with self.lock:
            self.vulnerabilities.append({
                'url': url,
                'type': vuln_type,
                'description': description
            })
            print(f"{Fore.RED}[!] Found {vuln_type}: {description}{Style.RESET_ALL}")

    def _check_sql_injection(self, url):
        """Basic SQL injection testing"""
        payloads = ["'", "1' OR '1'='1", "1; DROP TABLE users"]
        for payload in payloads:
            try:
                response = self.session.get(f"{url}?id={payload}", timeout=5)
                if any(error in response.text.lower() for error in ['sql', 'mysql', 'sqlite', 'postgresql']):
                    self._add_vulnerability(url, "Possible SQL Injection", 
                                         f"Database error revealed with payload: {payload}")
            except:
                continue

    def _check_xss(self, url):
        """Basic XSS testing"""
        payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
        for payload in payloads:
            try:
                response = self.session.get(f"{url}?q={payload}", timeout=5)
                if payload in response.text:
                    self._add_vulnerability(url, "Possible XSS", 
                                         f"Payload reflected in response: {payload}")
            except:
                continue

    def scan_api(self):
        """Scan for API endpoints and vulnerabilities"""
        print(f"\n{Fore.YELLOW}[*] Starting API scan on {self.target}{Style.RESET_ALL}")
        
        # Common API endpoints
        api_endpoints = [
            '/api', '/api/v1', '/api/v2', '/swagger', '/swagger.json',
            '/docs', '/graphql', '/graphiql', '/api/docs', '/openapi.json',
            '/api/auth', '/api/login', '/api/users', '/api/admin',
            '/api/data', '/api/config', '/api/settings', '/api/system'
        ]
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.test_endpoint, api_endpoints)
        
        return self.vulnerabilities, self.endpoints

    def scan_web(self, deep=False):
        """Scan for web vulnerabilities"""
        print(f"\n{Fore.YELLOW}[*] Starting web vulnerability scan on {self.target}{Style.RESET_ALL}")
        
        # Common web paths to test
        web_paths = [
            '/', '/admin', '/login', '/wp-admin', '/phpmyadmin',
            '/config', '/.env', '/.git/config', '/backup', '/debug',
            '/test', '/dev', '/api', '/console', '/admin/console',
            '/server-status', '/nginx_status', '/status', '/phpinfo.php',
            '/admin/phpinfo.php', '/info.php', '/admin/dashboard',
            '/administrator', '/admin/config', '/admin/db', '/db',
            '/wp-config.php', '/config.php', '/configuration.php',
            '/sites/default/settings.php', '/admin/web/config',
        ]
        
        if deep:
            web_paths.extend([
                '/backup/', '/bak/', '/old/', '/new/', '/temp/',
                '/dev/', '/development/', '/test/', '/testing/',
                '/_admin/', '/backend/', '/cms/', '/wp/', '/wordpress/',
                '/joomla/', '/drupal/', '/panel/', '/cpanel/', '/webadmin/',
                '/adminer/', '/mysql/', '/db/', '/database/', '/admin/db/',
                '/admin/backup/', '/admin/bak/', '/admin/old/', '/admin/new/',
                '/admin/temp/', '/admin/dev/', '/admin/test/', '/admin/beta/'
            ])
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.test_endpoint, web_paths)
        
        return self.vulnerabilities, self.endpoints

    def generate_report(self):
        """Generate a detailed report of findings"""
        report = {
            'target': self.target,
            'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'vulnerabilities': self.vulnerabilities,
            'endpoints': self.endpoints
        }
        
        return json.dumps(report, indent=2)
