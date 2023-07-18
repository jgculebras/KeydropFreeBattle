import time
import re
import undetected_chromedriver as uc
import json
import requests

# Your Session ID
session_id = ""

def getBattles(token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://key-drop.com/',
        'Authorization': 'Bearer ' + str(token),
        'x-currency': 'usd',
        'Origin': 'https://key-drop.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    params = {
        'type': 'active',
        'page': '0',
        'priceFrom': '0',
        'priceTo': '0.01',
        'searchText': '',
        'sort': 'latest',
        'players': 'all',
        'roundsCount': 'all',
    }

    response = requests.get('https://kdrp2.com/CaseBattle/battle', params=params, headers=headers)

    usersjoined = []

    usersfull = []

    for battle in response.json()["data"]:
        if battle["freeBattleTicketCost"] == 1 and len(battle["cases"]) >= 2:
            response_battle = requests.get('https://kdrp2.com/CaseBattle/gameFullData/' + str(battle["id"]), headers=headers)

            for user in response_battle.json()["data"]["users"]:
                usersjoined.append(user["slot"])

            for i in range(0, response_battle.json()["data"]["maxUserCount"]):
                usersfull.append(i)

            missing_slots = [num for num in usersfull if num not in usersjoined]

            if len(missing_slots) > 0:
                slot_to_join = missing_slots[0]

                response = requests.post('https://kdrp2.com/CaseBattle/joinCaseBattle/'+ str(battle["id"]) +'/'+ str(slot_to_join), headers=headers)

                if response.json()["success"] == True:
                    return True

    return False


def bypass_cf(session_id):
    try:
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        driver = uc.Chrome(options=options)
        driver.get('https://key-drop.com/token')
        time.sleep(3)
        driver.add_cookie({"name": "session_id", "value": session_id})
        driver.refresh()

        match = re.search(r'ey\S+', driver.page_source)

        if match:
            token = match.group()
            token = token.rstrip('</body></html>')

        driver.close()
        driver.quit()
        return 'valid', token
    except Exception as err:
        return 'invalid', f'There was an error bypassing cloudflare, make sure your session_id is valid! {err}'


def get_token(session_id):
    answer = bypass_cf(session_id)
    if answer[0] == 'valid':
        joined = False
        while not joined:
            joined = getBattles(answer[1])
            time.sleep(4)
    else:
        print("Token error")

get_token(session_id)
