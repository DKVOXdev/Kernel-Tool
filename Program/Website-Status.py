from Config.Util import *
from Config.Config import *

try:
    import requests
    from urllib.parse import urlparse
    import re
    try:
        from bs4 import BeautifulSoup
        BEAUTIFULSOUP_AVAILABLE = True
    except ImportError:
        BEAUTIFULSOUP_AVAILABLE = False
except Exception as e:
    ErrorModule(e)

Title("Website Status")

try:
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    def CheckWebsiteStatus(url):
        try:
            # Extract domain from URL
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split('/')[0]
            
            # Remove www. prefix for checking
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Remove port if present
            if ':' in domain:
                domain = domain.split(':')[0]
            
            if not domain:
                print(f"{BEFORE + AFTER} {ERROR} Invalid URL: {white}{url}{red}")
                return
            
            print(f"{BEFORE + AFTER} {WAIT} Checking status of {white}{domain}{green}...")
            
            # Check via isitdownrightnow.com
            check_url = f"https://www.isitdownrightnow.com/{domain}.html"
            
            try:
                response = requests.get(check_url, timeout=15, headers=headers, allow_redirects=True)
                
                if response.status_code == 200:
                    # Parse the HTML response
                    if BEAUTIFULSOUP_AVAILABLE:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        page_text = soup.get_text()
                    else:
                        # Fallback: use regex to extract text content
                        page_text = re.sub(r'<script[^>]*>.*?</script>', '', response.text, flags=re.DOTALL | re.IGNORECASE)
                        page_text = re.sub(r'<style[^>]*>.*?</style>', '', page_text, flags=re.DOTALL | re.IGNORECASE)
                        page_text = re.sub(r'<[^>]+>', ' ', page_text)
                        page_text = ' '.join(page_text.split())
                    
                    # Check for "is up" or "is down" patterns
                    if re.search(r'is\s+up\.', page_text, re.IGNORECASE):
                        status = "UP"
                        status_color = green
                        status_icon = GEN_VALID
                    elif re.search(r'is\s+down\.', page_text, re.IGNORECASE):
                        status = "DOWN"
                        status_color = red
                        status_icon = ERROR
                    else:
                        # Try alternative method - check if we can reach the actual website
                        try:
                            test_response = requests.get(f"https://{domain}", timeout=10, headers=headers, allow_redirects=True)
                            if test_response.status_code < 500:
                                status = "UP"
                                status_color = green
                                status_icon = GEN_VALID
                            else:
                                status = "DOWN"
                                status_color = red
                                status_icon = ERROR
                        except:
                            status = "DOWN"
                            status_color = red
                            status_icon = ERROR
                    
                    # Extract "Last checked" time
                    last_checked_match = re.search(r'Last checked\s+(\d+\s+(?:second|sec|minute|min|hour|hr)s?\s+ago)', page_text, re.IGNORECASE)
                    if last_checked_match:
                        last_checked = last_checked_match.group(1)
                    else:
                        last_checked = "Just now"
                    
                    # Display results
                    print(f"{BEFORE_GREEN + AFTER_GREEN} {status_icon} Website: {white}{domain}{status_color}")
                    print(f"{BEFORE_GREEN + AFTER_GREEN} {status_icon} Status: {white}{status}{status_color}")
                    print(f"{BEFORE_GREEN + AFTER_GREEN} {status_icon} Last Checked: {white}{last_checked}{status_color}")
                    print(f"{BEFORE_GREEN + AFTER_GREEN} {status_icon} Source: {white}isitdownrightnow.com{status_color}")
                    
                    # Additional check - verify directly
                    print(f"\n{BEFORE + AFTER} {WAIT} Verifying directly...")
                    try:
                        direct_url = f"https://{domain}" if not domain.startswith('http') else domain
                        direct_response = requests.get(direct_url, timeout=10, headers=headers, allow_redirects=True)
                        
                        if direct_response.status_code < 500:
                            print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Direct Check: {white}Accessible{green} Status Code: {white}{direct_response.status_code}{green}")
                        else:
                            print(f"{BEFORE + AFTER} {ERROR} Direct Check: {white}Error{red} Status Code: {white}{direct_response.status_code}{red}")
                    except Exception as e:
                        print(f"{BEFORE + AFTER} {ERROR} Direct Check: {white}Failed{red} Error: {white}{str(e)[:50]}{red}")
                    
                else:
                    print(f"{BEFORE + AFTER} {ERROR} Failed to check status: {white}HTTP {response.status_code}{red}")
                    # Fallback: try direct connection
                    print(f"{BEFORE + AFTER} {WAIT} Attempting direct connection...")
                    try:
                        direct_url = f"https://{domain}" if not domain.startswith('http') else domain
                        direct_response = requests.get(direct_url, timeout=10, headers=headers, allow_redirects=True)
                        if direct_response.status_code < 500:
                            print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Website: {white}{domain}{green} Status: {white}UP{green}")
                        else:
                            print(f"{BEFORE + AFTER} {ERROR} Website: {white}{domain}{red} Status: {white}DOWN{red} Status Code: {white}{direct_response.status_code}{red}")
                    except:
                        print(f"{BEFORE + AFTER} {ERROR} Website: {white}{domain}{red} Status: {white}DOWN{red}")
                        
            except requests.exceptions.RequestException as e:
                print(f"{BEFORE + AFTER} {ERROR} Connection Error: {white}{str(e)[:50]}{red}")
                # Fallback: try direct connection
                print(f"{BEFORE + AFTER} {WAIT} Attempting direct connection...")
                try:
                    direct_url = f"https://{domain}" if not domain.startswith('http') else domain
                    direct_response = requests.get(direct_url, timeout=10, headers=headers, allow_redirects=True)
                    if direct_response.status_code < 500:
                        print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Website: {white}{domain}{green} Status: {white}UP{green}")
                    else:
                        print(f"{BEFORE + AFTER} {ERROR} Website: {white}{domain}{red} Status: {white}DOWN{red}")
                except:
                    print(f"{BEFORE + AFTER} {ERROR} Website: {white}{domain}{red} Status: {white}DOWN{red}")
                    
        except Exception as e:
            print(f"{BEFORE + AFTER} {ERROR} Error checking website status: {white}{str(e)[:50]}{red}")

    print(f"{BEFORE + AFTER} {INFO} Selected User-Agent: {white + user_agent}")
    website_url = input(f"{BEFORE + AFTER} {INPUT} Website Url -> {reset}")
    Censored(website_url)

    if not website_url:
        print(f"{BEFORE + AFTER} {ERROR} No URL provided{red}")
        Continue()
        Reset()
    else:
        CheckWebsiteStatus(website_url)
        Continue()
        Reset()

except Exception as e:
    Error(e)

