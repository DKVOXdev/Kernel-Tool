# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ------------------------------------------------------------------------------------------------
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner,
#       but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le
#       propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.
# ------------------------------------------------------------------------------------------------

import requests
import random
import os
import hashlib
import re

from Config.Util import *
from Config.Config import *

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

user_agent = random.choice(user_agents)

def Instagram(email):
    session = requests.Session()
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.instagram.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.instagram.com/'
    }
    response = session.get('https://www.instagram.com/accounts/emailsignup/', headers=headers)
    if response.status_code != 200:
        return False
    token = session.cookies.get('csrftoken')
    if not token:
        return False
    headers['x-csrftoken'] = token
    headers['Referer'] = 'https://www.instagram.com/accounts/emailsignup/'
    response = session.post(
        url='https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/',
        headers=headers,
        data={'email': email}
    )
    if response.status_code == 200:
        return 'Another account is using the same email.' in response.text or 'email_is_taken' in response.text
    return False

def Twitter(email):
    response = requests.get(
        'https://api.twitter.com/i/users/email_available.json',
        params={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('taken', False)
    return False

def Pinterest(email):
    response = requests.get(
        'https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/',
        params={'source_url': '/', 'data': '{"options": {"email": "' + email + '"}, "context": {}}'}
    )
    if response.status_code == 200:
        data = response.json()['resource_response']
        if data['message'] == 'Invalid email.':
            return False
        return data['data'] is not False
    return False

def Imgur(email):
    response = requests.post(
        'https://imgur.com/signin/ajax_email_available',
        headers={'User-Agent': user_agent},
        data={'email': email}
    )
    if response.status_code == 200:
        return not response.json()['data']['available']
    return False

def Spotify(email):
    response = requests.get(
        'https://spclient.wg.spotify.com/signup/public/v1/account',
        headers={'User-Agent': user_agent},
        params={'validate': '1', 'email': email}
    )
    if response.status_code == 200:
        return response.json().get('status') == 20
    return False

def FireFox(email):
    response = requests.post(
        'https://api.accounts.firefox.com/v1/account/status',
        data={'email': email}
    )
    if response.status_code == 200:
        return 'false' not in response.text
    return False

def LastPass(email):
    response = requests.get(
        'https://lastpass.com/create_account.php',
        params={'check': 'avail', 'username': email}
    )
    if response.status_code == 200:
        return 'no' in response.text
    return False

def Archive(email):
    response = requests.post(
        'https://archive.org/account/signup',
        data={'input_name': 'username', 'input_value': email, 'input_validator': 'true', 'submit_by_js': 'true'}
    )
    if response.status_code == 200:
        return 'is already taken.' in response.text
    return False

def ProtonMail(email):
    response = requests.post(
        'https://account.proton.me/api/users/exists',
        json={'Address': email}
    )
    if response.status_code == 200:
        return response.json().get('Exists', False)
    return False

def Github(email):
    response = requests.get('https://github.com/signup', headers={'User-Agent': user_agent})
    if response.status_code != 200:
        return False
    match = re.search(r'name="authenticity_token" value="([^"]+)"', response.text)
    if not match:
        return False
    r2 = requests.post(
        'https://github.com/signup/email',
        headers={'User-Agent': user_agent},
        data={'authenticity_token': match.group(1), 'email': email}
    )
    return 'Email is already taken' in r2.text or 'email_already_taken' in r2.text

def Gravatar(email):
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    response = requests.get(
        f'https://en.gravatar.com/{email_hash}.json',
        headers={'User-Agent': user_agent}
    )
    return response.status_code == 200

def Duolingo(email):
    response = requests.get(
        'https://www.duolingo.com/2017-06-30/users',
        headers={'User-Agent': user_agent},
        params={'email': email, 'fields': 'email'}
    )
    if response.status_code == 200:
        return len(response.json().get('users', [])) > 0
    return False

def Snapchat(email):
    response = requests.post(
        'https://accounts.snapchat.com/accounts/get_teaser_user_status',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('status') == 'USER_FOUND'
    return False

def Airbnb(email):
    response = requests.get(
        'https://api.airbnb.com/v2/email_availability',
        headers={'User-Agent': user_agent, 'X-Airbnb-API-Key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20'},
        params={'email': email}
    )
    if response.status_code == 200:
        return not response.json().get('email_available', True)
    return False

def Ebay(email):
    response = requests.get(
        'https://reg.ebay.com/reg/IdentityAjaxServlet',
        headers={'User-Agent': user_agent},
        params={'userid': email, 'email': email, 'siteid': '0'}
    )
    if response.status_code == 200:
        return 'emailTaken' in response.text
    return False

def Samsung(email):
    response = requests.post(
        'https://account.samsung.com/accounts/v1/SEAO/signInGate',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'loginId': email}
    )
    if response.status_code == 200:
        return response.json().get('resultCode') == '200'
    return False

def Freelancer(email):
    response = requests.get(
        'https://www.freelancer.com/api/users/0.1/users',
        headers={'User-Agent': user_agent},
        params={'email': email, 'compact': True}
    )
    if response.status_code == 200:
        return len(response.json().get('result', {}).get('users', {})) > 0
    return False

def Patreon(email):
    response = requests.post(
        'https://www.plurk.com/Users/isEmailFound',
        headers={'User-Agent': user_agent},
        data={'email': email}
    )
    if response.status_code == 200:
        return 'True' in response.text
    return False

def Dropbox(email):
    response = requests.post(
        'https://www.dropbox.com/ajax_login',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'login_email': email, 'login_password': 'wrongpassword123', 'is_xhr': 'true'}
    )
    if response.status_code == 200:
        return 'No account found' not in response.text and 'wrong password' in response.text.lower()
    return False

def Reddit(email):
    response = requests.post(
        'https://www.reddit.com/api/check_username.json',
        headers={'User-Agent': user_agent},
        data={'user': email}
    )
    if response.status_code == 200:
        return response.json().get('taken', False)
    return False

def Tumblr(email):
    response = requests.post(
        'https://www.tumblr.com/register/account/email',
        headers={'User-Agent': user_agent},
        data={'email': email}
    )
    if response.status_code == 200:
        return 'This email is taken.' in response.text or 'email_taken' in response.text
    return False

def Wordpress(email):
    response = requests.post(
        'https://public-api.wordpress.com/rest/v1.1/signup/validation/user',
        headers={'User-Agent': user_agent},
        data={'email': email, 'user_name': '', 'password': ''}
    )
    if response.status_code == 200:
        return 'email' in response.json().get('errors', {})
    return False

def Zoom(email):
    response = requests.post(
        'https://zoom.us/signup/checkEmail',
        headers={'User-Agent': user_agent},
        data={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('exist', False)
    return False

def Linkedin(email):
    response = requests.get(
        'https://www.linkedin.com/uas/request-password-reset',
        headers={'User-Agent': user_agent},
        params={'email': email}
    )
    return response.status_code == 200 and 'member-id' in response.text

def Microsoft(email):
    response = requests.post(
        'https://login.live.com/GetCredentialType.srf',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'username': email, 'isOtherIdpSupported': True, 'checkPhones': False,
              'isRemoteNGCSupported': False, 'isCookieBannerShown': False,
              'isFidoSupported': False, 'flowToken': ''}
    )
    if response.status_code == 200:
        return response.json().get('IfExistsResult', 1) == 0
    return False

def Apple(email):
    response = requests.post(
        'https://iforgot.apple.com/iforgot/phone/verifyAccount.do',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'emailAddress': email}
    )
    return response.status_code == 200 and 'error' not in response.text.lower()

def Google(email):
    session = requests.Session()
    session.get('https://accounts.google.com/signin/v1/lookup', headers={'User-Agent': user_agent})
    response = session.post(
        'https://accounts.google.com/signin/v1/lookup',
        headers={'User-Agent': user_agent},
        data={'Email': email, 'next': 'https://accounts.google.com/ManageAccount'}
    )
    return 'Wrong password' in response.text or 'password' in response.text.lower()

def Yahoo(email):
    session = requests.Session()
    session.get('https://login.yahoo.com/', headers={'User-Agent': user_agent})
    response = session.post(
        'https://login.yahoo.com/account/challenge/username',
        headers={'User-Agent': user_agent},
        data={'username': email, 'browser-fp-raw-json': '{}'}
    )
    return 'password' in response.text.lower() or 'That Yahoo ID' not in response.text

def Netflix(email):
    response = requests.post(
        'https://www.netflix.com/api/shakti/mre/login',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'userLoginId': email, 'password': 'wrongpassword123', 'flow': 'websiteSignUp',
              'mode': 'login', 'action': 'loginAction', 'withFields': 'rememberMe,nextPage,userLoginId,password'}
    )
    if response.status_code == 200:
        return 'incorrect password' in response.text.lower()
    return False

def Amazon(email):
    session = requests.Session()
    session.get('https://www.amazon.com/ap/signin', headers={'User-Agent': user_agent})
    response = session.post(
        'https://www.amazon.com/ap/signin',
        headers={'User-Agent': user_agent},
        data={'email': email, 'create': '0', 'password': 'wrongpassword', 'metadata1': ''}
    )
    return 'password' in response.text.lower() and 'No account found' not in response.text

def Paypal(email):
    response = requests.post(
        'https://www.paypal.com/auth/validatelogin',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('result', {}).get('isExistingAccount', False)
    return False

def Twitch(email):
    response = requests.get(
        'https://passport.twitch.tv/usernames/' + email,
        headers={'User-Agent': user_agent}
    )
    return response.status_code == 409

def Discord(email):
    response = requests.post(
        'https://discord.com/api/v9/auth/register',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'email': email, 'username': 'test', 'password': 'WrongPass123!', 'consent': True}
    )
    if response.status_code in [200, 400]:
        return 'email' in response.json() and 'already registered' in str(response.json().get('email', ''))
    return False

def Steam(email):
    response = requests.get(
        'https://store.steampowered.com/join/checkavail/',
        headers={'User-Agent': user_agent},
        params={'accountname': email, 'count': 1}
    )
    if response.status_code == 200:
        return not response.json().get('bAvail', True)
    return False

def Tiktok(email):
    response = requests.post(
        'https://www.tiktok.com/passport/web/account/check/email/',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('data', {}).get('email_registered', False)
    return False

def Badoo(email):
    response = requests.post(
        'https://badoo.com/api/login/email_exists/',
        headers={'User-Agent': user_agent},
        json={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('exists', False)
    return False

def Soundcloud(email):
    response = requests.get(
        'https://api.soundcloud.com/email_taken',
        headers={'User-Agent': user_agent},
        params={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('taken', False)
    return False

def Vimeo(email):
    response = requests.post(
        'https://vimeo.com/_next/api/proxy/users?action=email_available',
        headers={'User-Agent': user_agent},
        json={'email': email}
    )
    if response.status_code == 200:
        return not response.json().get('available', True)
    return False

def Hubspot(email):
    response = requests.post(
        'https://app.hubspot.com/signup-api/v1/lookup',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('exists', False)
    return False

def Gitlab(email):
    response = requests.post(
        'https://gitlab.com/users/sign_in',
        headers={'User-Agent': user_agent},
        data={'user[login]': email, 'user[password]': 'wrongpassword'}
    )
    return 'Invalid Login or password' in response.text

def Envato(email):
    response = requests.post(
        'https://account.envato.com/sign_in',
        headers={'User-Agent': user_agent},
        data={'login[email]': email, 'login[password]': 'wrongpassword'}
    )
    return 'Invalid password' in response.text or 'password' in response.text.lower()

def Kickstarter(email):
    response = requests.post(
        'https://www.kickstarter.com/signup/email_check',
        headers={'User-Agent': user_agent},
        data={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('taken', False)
    return False

def Fiverr(email):
    response = requests.post(
        'https://www.fiverr.com/users/api/v2/check-user',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('emailExists', False)
    return False

def Skype(email):
    response = requests.post(
        'https://login.skype.com/login/oauth/microsoft',
        headers={'User-Agent': user_agent},
        data={'username': email}
    )
    return 'password' in response.text.lower()

def Adobe(email):
    response = requests.get(
        'https://auth.services.adobe.com/imsapis/v1/sso/social/api/v1/social_provider/social_user_info',
        headers={'User-Agent': user_agent, 'X-IMS-CLIENTID': 'adobedotcom2'},
        params={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('existing_user', False)
    return False

def Weibo(email):
    response = requests.get(
        'https://weibo.com/signup/signup.php',
        headers={'User-Agent': user_agent},
        params={'email': email}
    )
    if response.status_code == 200:
        return 'email_used' in response.text or 'already exists' in response.text.lower()
    return False

def OKCupid(email):
    response = requests.post(
        'https://www.okcupid.com/graphql',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'query': 'mutation { checkEmail(email: "' + email + '") { exists } }'}
    )
    if response.status_code == 200:
        return response.json().get('data', {}).get('checkEmail', {}).get('exists', False)
    return False

def Meetup(email):
    response = requests.post(
        'https://api.meetup.com/2/member/check',
        headers={'User-Agent': user_agent},
        data={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('found', False)
    return False

def StackOverflow(email):
    response = requests.get(
        'https://api.stackexchange.com/2.3/users',
        params={'site': 'stackoverflow', 'filter': 'total', 'inname': email}
    )
    if response.status_code == 200:
        return response.json().get('total', 0) > 0
    return False

def HackerRank(email):
    response = requests.post(
        'https://www.hackerrank.com/auth/login',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'login': email, 'password': 'wrongpassword'}
    )
    if response.status_code in [200, 401, 422]:
        text = response.text.lower()
        return 'invalid password' in text or 'incorrect password' in text
    return False

def Xing(email):
    response = requests.post(
        'https://www.xing.com/app/user',
        headers={'User-Agent': user_agent},
        data={'op': 'login', 'dest': '/home', 'login_user_name': email, 'login_password': 'wrongpassword'}
    )
    return 'wrong password' in response.text.lower() or 'incorrect password' in response.text.lower()

def Bitbucket(email):
    response = requests.post(
        'https://bitbucket.org/api/internal/signup/check-email',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('taken', False)
    return False

def DevTo(email):
    response = requests.post(
        'https://dev.to/users',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'user': {'email': email}}
    )
    if response.status_code in [200, 422]:
        return 'already been taken' in response.text or 'taken' in response.text
    return False

def HackerOne(email):
    response = requests.post(
        'https://hackerone.com/users/sign_in',
        headers={'User-Agent': user_agent},
        data={'user[email]': email, 'user[password]': 'wrongpassword'}
    )
    return 'Invalid email or password' in response.text

def Bugcrowd(email):
    response = requests.post(
        'https://bugcrowd.com/user/sign_in',
        headers={'User-Agent': user_agent},
        data={'user[email]': email, 'user[password]': 'wrongpassword'}
    )
    return 'Invalid email or password' in response.text

def HackTheBox(email):
    response = requests.post(
        'https://app.hackthebox.com/api/v4/login',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'email': email, 'password': 'wrongpassword', 'remember': True}
    )
    if response.status_code in [200, 401, 422]:
        return 'password' in response.text.lower() or 'credentials' in response.text.lower()
    return False

def Trello(email):
    response = requests.post(
        'https://trello.com/1/authentication',
        headers={'User-Agent': user_agent},
        data={'email': email, 'password': 'wrongpassword'}
    )
    return 'Invalid password' in response.text or 'password' in response.text.lower()

def OpenSea(email):
    response = requests.post(
        'https://api.opensea.io/api/v1/user/check_email',
        headers={'User-Agent': user_agent, 'Content-Type': 'application/json'},
        json={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('exists', False)
    return False

def Foursquare(email):
    response = requests.post(
        'https://foursquare.com/ajax/checkEmail',
        headers={'User-Agent': user_agent},
        data={'email': email}
    )
    if response.status_code == 200:
        return response.json().get('taken', False)
    return False

sites = [
    Instagram, Twitter, Pinterest, Imgur, Spotify, FireFox,
    LastPass, Archive, ProtonMail, Github, Gravatar, Duolingo,
    Snapchat, Airbnb, Ebay, Samsung, Freelancer, Patreon,
    Dropbox, Reddit, Tumblr, Wordpress, Zoom, Linkedin, Microsoft,
    Apple, Google, Yahoo, Netflix, Amazon, Paypal, Twitch, Discord,
    Steam, Tiktok, Badoo, Soundcloud, Vimeo, Hubspot, Gitlab,
    Envato, Kickstarter, Fiverr, Skype, Adobe, Weibo,
    OKCupid, Meetup, StackOverflow, HackerRank, Xing, Bitbucket,
    DevTo, HackerOne, Bugcrowd, HackTheBox, Trello, OpenSea, Foursquare
]

def email_tracker():
    Reset()
    Title("Email Tracker")
    print(email_tracker_banner)
    print(f"{LC}=== Email Tracker ==={RS}")
    email = input(f"{LC}Enter email -> {RS}")
    print()

    found     = []
    not_found = []
    errors    = []

    for site in sites:
        try:
            result = site(email)
            if result:
                print(f"{LC}  [FOUND]     {site.__name__}{RS}")
                found.append(site.__name__)
            else:
                print(f"\033[31m  [NOT FOUND] {site.__name__}{RS}")
                not_found.append(site.__name__)
        except Exception:
            print(f"\033[33m  [ERROR]     {site.__name__}{RS}")
            errors.append(site.__name__)

    print(f"{LC}\n" + "─" * 60)
    print(f"{LC}  Total Sites  : {len(sites)}{RS}")
    print(f"{LC}  Found        : {len(found)}{RS}")
    print(f"\033[31m  Not Found    : {len(not_found)}{RS}")
    print(f"\033[33m  Errors       : {len(errors)}{RS}")

    if found:
        print(f"{LC}\n  [+] Accounts found on :{RS}")
        for name in found:
            print(f"{LC}      - {name}{RS}")

    print(f"{LC}" + "─" * 60 + f"\n{RS}")
    input(f"{LC}  Press Enter to exit...{RS}")

if __name__ == '__main__':
    email_tracker()
