import time
import os
from requests import session
from urllib.parse import unquote
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import api

load_dotenv()
global PROXY_ENABLED, PROXY_HTTP, PROXY_HTTPS
PROXY_ENABLED = os.environ.get("proxy", "False").lower() == "true"
if PROXY_ENABLED:
    PROXY_HTTP = f"http://{os.environ.get('PROXY_HOST', '127.0.0.1')}:{os.environ.get('PROXY_PORT', '8080')}"
    PROXY_HTTPS = f"http://{os.environ.get('PROXY_HOST', '127.0.0.1')}:{os.environ.get('PROXY_PORT', '8080')}"
FLOWER_SEEDS = {
    "1": "2000001",
    "2": "2000002",
    "3": "2000003",
    "4": "2000004",
    "5": "2000005",
    "6": "2000006",
    "7": "2000007",
    "8": "2000008",
    "9": "2000009",
    "10": "2000010",
    "11": "2000011",
    "12": "2000012"
}

def refresh_session(session):
    session.headers.pop("Origin", None)
    session.headers.pop("Sec-Fetch-Site", None)
    url = "https://xsso.leagueoflegends.com/refresh"
    referer = "https://xsso.leagueoflegends.com/riot-owned-iframe"
    session.headers.update({
        "Referer": referer
    })
    if PROXY_ENABLED:
        session.get(url, proxies={"http": PROXY_HTTP, "https": PROXY_HTTPS}, verify=False)
    else:
        session.get(url, verify=False)

    # DOPO il refresh, pulisci i duplicati mantenendo solo l'ultimo di ogni nome
    for cookie_name in ["__Secure-access_token", "__Secure-session_expiry", "__Secure-refresh_token", "__Secure-id_hint"]:
        cookies_list = [c for c in session.cookies if c.name == cookie_name]
        if len(cookies_list) > 1:
            # Mantieni l'ultimo, cancella gli altri
            for cookie in cookies_list[:-1]:
                session.cookies.clear(cookie.domain, cookie.path, cookie.name)
    session.headers.pop("Referer")
    session.headers.update({
        "Origin": "https://crystalrosegame.wildrift.leagueoflegends.com",
        "Referer": "https://crystalrosegame.wildrift.leagueoflegends.com/"
    })
    return session

def prepare_session(session_expiry):
    this_session = session()
    this_session.cookies.update({
        "language": "it-IT",
        "__Secure-session_state": os.environ.get("SESSION_STATE"),
        "__Secure-access_token": os.environ.get("ACCESS_TOKEN"),
        "__Secure-session_expiry": session_expiry,
        "__Secure-refresh_token": os.environ.get("REFRESH_TOKEN"),
        "__Secure-refresh_token_presence": "1",
        "__Secure-id_token": os.environ.get("ID_TOKEN"),
        "__Secure-id_hint": os.environ.get("ID_HINT")
    })
    #"User-Agent": "WildRift/5.3.0.4096 (com.riotgames.league.wildrift; build:4096; iOS 14.8.0) Alamofire/5.6.1"
    this_session.headers.update({
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "Origin": "https://crystalrosegame.wildrift.leagueoflegends.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://crystalrosegame.wildrift.leagueoflegends.com/",
        "Accept-Language": "it-IT,it;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
        "Connection": "keep-alive"
    })
    return this_session

def is_harvestable(info, id):
    for land in info:
        if land.get("landIndex") == id and land.get("cropId") != 0:
            plant_time = land.get("plantTime")
            grow_time = land.get("cropDetail").get("growTime")
            sum = plant_time + grow_time
            current_time = int(time.time())
            #print(f"Land {id} - Plant time: {plant_time}, Grow time: {grow_time}, Sum: {sum}, Current time: {current_time}")
            if plant_time + grow_time <= current_time:
                #print(f"Land {id} is ready to harvest ({current_time} >= {sum})")
                return True        
    return False

def is_plantable(info, id):
    for land in info:    
        if land.get("landIndex") == id and land.get("cropId") == 0:
            return True        
    return False

def is_waterable(info, id):
    for land in info:    
        if land.get("landIndex") == id and land.get("cropId") != 0:
            now = int(time.time())
            last_water = int(land.get("wateringTime"))
            next_water = last_water + 1200  # 12 minutes (gameConfig farmEnterWaterDeficitCountdown value)
            if next_water <= now:
                #print(f"Land {id} is ready to water (now: {now} >= water: {land.get('wateringTime')})")
                return True        
    return False

def check_session_time(session_expiry):
    # URL decode the session_expiry string first
    decoded_expiry = unquote(session_expiry)
    time_struct = time.strptime(decoded_expiry, "%Y-%m-%dT%H:%M:%S.000Z")
    session_expiry_check = time.mktime(time_struct)
    now = time.time()
    if session_expiry_check - now < 300:
        return False
    return True

def print_farm_menu():
    print("=== Wild Rift Crystal Rose Farm Bot ===")
    print("""1. Input the flower corresponding number to plant:
    1) Skyglow Tulip
    2) Battle Rose
    3) Spirit Lotus
    4) Emerald Vine
    5) Fire Iris
    6) Desert Rose
    7) Voidbloom
    8) Thunder Iris
    9) Crystal Rose
    10) Aurora Icebloom
    11) Moonlight Lotus
    12) Starlight Lily
2. Ctrl+C to stop the bot.
""")

def farm_bot(this_session, session_expiry):
    print_farm_menu()
    seed_index = input("[+] Insert seed to plant: (default is SEED_ID from .env or Fire Iris)")
    if seed_index.strip() == "":
        seed_ID = os.environ.get("SEED_ID", "2000005")
    elif seed_index not in FLOWER_SEEDS:
        print("Invalid seed ID. Using default SEED_ID from .env or 2000005 - Fire Iris.")
        seed_ID = os.environ.get("SEED_ID", "2000005")
    else:
        seed_ID = FLOWER_SEEDS[seed_index]
    print(f"[+] Started bot")



    while True:
        if not check_session_time(session_expiry):
            this_session = refresh_session(this_session)
            session_expiry = next((c.value for c in this_session.cookies if c.name == "__Secure-session_expiry"), None)
        gardenInfo = api.get_garden_info(this_session)
        just_planted = False
        for land_index in range(1, 7):
            if is_harvestable(gardenInfo, land_index):
                api.harvest_crop(this_session, land_index, proxy_enabled=PROXY_ENABLED, http_proxy=PROXY_HTTP if PROXY_ENABLED else None, https_proxy=PROXY_HTTPS if PROXY_ENABLED else None)
            if is_plantable(gardenInfo, land_index):
                api.buy_seed(this_session, seed_ID, 1, proxy_enabled=PROXY_ENABLED, http_proxy=PROXY_HTTP if PROXY_ENABLED else None, https_proxy=PROXY_HTTPS if PROXY_ENABLED else None)
                api.plant_seed(this_session, seed_ID, land_index, proxy_enabled=PROXY_ENABLED, http_proxy=PROXY_HTTP if PROXY_ENABLED else None, https_proxy=PROXY_HTTPS if PROXY_ENABLED else None)
                just_planted = True
            if is_waterable(gardenInfo, land_index) and not just_planted:
                api.water_plants(this_session, land_index, proxy_enabled=PROXY_ENABLED, http_proxy=PROXY_HTTP if PROXY_ENABLED else None, https_proxy=PROXY_HTTPS if PROXY_ENABLED else None)
        time.sleep(60)  # Wait for 1 minutes before next cycle

def cheat_loop(this_session, session_expiry, gold_target=30000) -> None:
    seed_ID = "2000001"
    gained_gold = 0
    while gained_gold < gold_target:
        if not check_session_time(session_expiry):
            this_session = refresh_session(this_session)
            session_expiry = next((c.value for c in this_session.cookies if c.name == "__Secure-session_expiry"), None)
        api.buy_seed(this_session, seed_ID, proxy_enabled=PROXY_ENABLED, http_proxy=PROXY_HTTP if PROXY_ENABLED else None, https_proxy=PROXY_HTTPS if PROXY_ENABLED else None)
        for land_index in range(1, 7):
            api.plant_seed(this_session, seed_ID, land_index, proxy_enabled=PROXY_ENABLED, http_proxy=PROXY_HTTP if PROXY_ENABLED else None, https_proxy=PROXY_HTTPS if PROXY_ENABLED else None)
            api.remove_plant(this_session, land_index, proxy_enabled=PROXY_ENABLED, http_proxy=PROXY_HTTP if PROXY_ENABLED else None, https_proxy=PROXY_HTTPS if PROXY_ENABLED else None)
        quest_data = api.redeem_quest(this_session, proxy_enabled=PROXY_ENABLED, http_proxy=PROXY_HTTP if PROXY_ENABLED else None, https_proxy=PROXY_HTTPS if PROXY_ENABLED else None).get("jData", {})
        for reward in quest_data.get("rewards", []):
            if int(reward.get("rewardId")) == 1000001:  # Gold
                gained_gold += int(reward.get("rewardAmount", 0))
                #print(f"Gained {reward.get('rewardAmount', 0)} gold. Total: {gained_gold}/{gold_target}")
    print(f"Target of {gold_target} gold reached. Total gained gold: {gained_gold}")

def main_menu():
    print("=== Wild Rift Crystal Rose Main Menu ===")
    print("1. Farm Bot")
    print("2. Cheat Gold Bot")
    print("3. exit")
    while True:
        choice = input("[+] Select an option (1-3): ")
        if choice in ["1", "2", "3"]:
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
    return choice

if __name__ == "__main__":
    session_expiry = os.environ.get("SESSION_EXPIRY")
    this_session = prepare_session(session_expiry)
    choice = main_menu()
    if choice == "1":
        farm_bot(this_session, session_expiry)
    elif choice == "2":
        gold_target = int(os.environ.get("GOLD_TARGET", "30000"))
        cheat_loop(this_session, session_expiry, gold_target)

