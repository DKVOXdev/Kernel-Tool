from Config.Util import *
from Config.Config import *

try:
    import requests
    import ssl
    import socket
    import time
    from urllib.parse import urlparse
    from datetime import datetime
except Exception as e:
    ErrorModule(e)

Title("Website Strength Scanner")

try:
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    def CheckSSL(url):
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            if not hostname:
                return
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    subject = dict(x[0] for x in cert.get('subject', []))
                    
                    # Check certificate validity
                    not_after = cert.get('notAfter')
                    not_before = cert.get('notBefore')
                    
                    if not_after:
                        expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                        days_until_expiry = (expiry_date - datetime.now()).days
                        
                        if days_until_expiry > 30:
                            print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} SSL Certificate: {white}Valid{green} Expires in: {white}{days_until_expiry} days{green} Issuer: {white}{issuer.get('organizationName', 'Unknown')}")
                        elif days_until_expiry > 0:
                            print(f"{BEFORE + AFTER} {WAIT} SSL Certificate: {white}Expiring Soon{green} Expires in: {white}{days_until_expiry} days{green} Issuer: {white}{issuer.get('organizationName', 'Unknown')}")
                        else:
                            print(f"{BEFORE + AFTER} {ERROR} SSL Certificate: {white}Expired{red} Expired: {white}{days_until_expiry} days ago{red}")
                    
                    # Check SSL version
                    version = ssock.version()
                    if version in ['TLSv1.2', 'TLSv1.3']:
                        print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} SSL Version: {white}{version}{green} Status: {white}Secure{green}")
                    else:
                        print(f"{BEFORE + AFTER} {ERROR} SSL Version: {white}{version}{red} Status: {white}Weak{red}")
        except Exception as e:
            print(f"{BEFORE + AFTER} {ERROR} SSL Check: {white}Failed{red} Error: {white}{str(e)[:50]}{red}")

    def CheckSecurityHeaders(url):
        try:
            response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
            headers_dict = response.headers
            
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'CSP',
                'X-Frame-Options': 'X-Frame-Options',
                'X-Content-Type-Options': 'X-Content-Type-Options',
                'X-XSS-Protection': 'X-XSS-Protection',
                'Referrer-Policy': 'Referrer-Policy',
                'Permissions-Policy': 'Permissions-Policy'
            }
            
            found_headers = []
            missing_headers = []
            
            for header, name in security_headers.items():
                if header in headers_dict:
                    found_headers.append(name)
                    value = headers_dict[header][:60] if len(headers_dict[header]) > 60 else headers_dict[header]
                    print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Security Header: {white}{name}{green} Status: {white}Present{green} Value: {white}{value}{green}")
                else:
                    missing_headers.append(name)
                    print(f"{BEFORE + AFTER} {ERROR} Security Header: {white}{name}{red} Status: {white}Missing{red}")
            
            if found_headers:
                print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Security Headers Found: {white}{len(found_headers)}/{len(security_headers)}{green}")
            if missing_headers:
                print(f"{BEFORE + AFTER} {ERROR} Security Headers Missing: {white}{len(missing_headers)}/{len(security_headers)}{red}")
                
        except Exception as e:
            print(f"{BEFORE + AFTER} {ERROR} Security Headers Check: {white}Failed{red} Error: {white}{str(e)[:50]}{red}")

    def CheckServerResponse(url):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            status_code = response.status_code
            server = response.headers.get('Server', 'Unknown')
            powered_by = response.headers.get('X-Powered-By', 'Not Disclosed')
            
            if response_time < 500:
                print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Response Time: {white}{response_time:.2f}ms{green} Status: {white}Fast{green}")
            elif response_time < 2000:
                print(f"{BEFORE + AFTER} {WAIT} Response Time: {white}{response_time:.2f}ms{green} Status: {white}Moderate{green}")
            else:
                print(f"{BEFORE + AFTER} {ERROR} Response Time: {white}{response_time:.2f}ms{red} Status: {white}Slow{red}")
            
            if status_code == 200:
                print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} HTTP Status: {white}{status_code}{green} Status: {white}OK{green}")
            elif status_code in [301, 302, 307, 308]:
                print(f"{BEFORE + AFTER} {WAIT} HTTP Status: {white}{status_code}{green} Status: {white}Redirect{green}")
            else:
                print(f"{BEFORE + AFTER} {ERROR} HTTP Status: {white}{status_code}{red} Status: {white}Error{red}")
            
            if server != 'Unknown':
                print(f"{BEFORE + AFTER} {INFO} Server: {white}{server}{green}")
            if powered_by != 'Not Disclosed':
                print(f"{BEFORE + AFTER} {INFO} Powered By: {white}{powered_by}{green}")
                
        except Exception as e:
            print(f"{BEFORE + AFTER} {ERROR} Server Response Check: {white}Failed{red} Error: {white}{str(e)[:50]}{red}")

    def CheckHTTPS(url):
        try:
            parsed = urlparse(url)
            scheme = parsed.scheme.lower()
            
            if scheme == 'https':
                print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Protocol: {white}HTTPS{green} Status: {white}Secure{green}")
            elif scheme == 'http':
                print(f"{BEFORE + AFTER} {ERROR} Protocol: {white}HTTP{red} Status: {white}Insecure{red}")
            else:
                print(f"{BEFORE + AFTER} {ERROR} Protocol: {white}{scheme}{red} Status: {white}Unknown{red}")
        except Exception as e:
            print(f"{BEFORE + AFTER} {ERROR} Protocol Check: {white}Failed{red} Error: {white}{str(e)[:50]}{red}")

    def CheckContentSecurity(url):
        try:
            response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
            content = response.text.lower()
            
            # Check for sensitive information exposure
            sensitive_patterns = {
                'password': 'Password Field',
                'api_key': 'API Key',
                'secret': 'Secret Key',
                'token': 'Token',
                'database': 'Database Info',
                'config': 'Config File'
            }
            
            found_patterns = []
            for pattern, name in sensitive_patterns.items():
                if pattern in content[:50000]:  # Check first 50KB
                    found_patterns.append(name)
            
            if found_patterns:
                print(f"{BEFORE + AFTER} {WAIT} Content Security: {white}Potential Sensitive Data Found{green} Patterns: {white}{', '.join(found_patterns[:3])}{green}")
            else:
                print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Content Security: {white}No Obvious Sensitive Data{green} Status: {white}Clean{green}")
                
        except Exception as e:
            print(f"{BEFORE + AFTER} {ERROR} Content Security Check: {white}Failed{red} Error: {white}{str(e)[:50]}{red}")

    print(f"{BEFORE + AFTER} {INFO} Selected User-Agent: {white + user_agent}")
    website_url = input(f"{BEFORE + AFTER} {INPUT} Website Url -> {reset}")
    Censored(website_url)

    print(f"{BEFORE + AFTER} {WAIT} Analyzing website strength...")
    if "https://" not in website_url and "http://" not in website_url:
        website_url = "https://" + website_url

    CheckHTTPS(website_url)
    CheckSSL(website_url)
    CheckServerResponse(website_url)
    CheckSecurityHeaders(website_url)
    CheckContentSecurity(website_url)
    Continue()
    Reset()

except Exception as e:
    Error(e)

