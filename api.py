
def get_garden_info(session, proxy_enabled=False, http_proxy=None, https_proxy=None) -> None:
    url = "https://eu.api.h5.wildrift.leagueoflegends.com/5c/crystalrose/pub/farm?a=garden"
    if proxy_enabled and http_proxy and https_proxy:
        response = session.post(url, files={None: (None, "")}, proxies={"http": http_proxy, "https": https_proxy}, verify=False)
    else:
        response = session.post(url, files={None: (None, "")})
    info = response.json().get("jData", {}).get("gardenInfo")
    return info


def plant_seed(session, seed_type, land_index, proxy_enabled=False, http_proxy=None, https_proxy=None) -> None:
    url = "https://eu.api.h5.wildrift.leagueoflegends.com/5c/crystalrose/pub/farm?a=plant"
    payload = {"landIndex": land_index, "cropId": seed_type}
    #multipart/form-data
    if proxy_enabled and http_proxy and https_proxy:
        response = session.post(url, data=payload, proxies={"http": http_proxy, "https": https_proxy}, verify=False)
    else:
        response = session.post(url, data=payload)
    json_response = response.json()
    if json_response.get("ret") != 0:
        print(f"{json_response.get('msg')} on land {land_index} while planting")
    return response.json()

def harvest_crop(session, land_index, proxy_enabled=False, http_proxy=None, https_proxy=None) -> None:
    url = "https://eu.api.h5.wildrift.leagueoflegends.com/5c/crystalrose/pub/farm?a=harvest"
    payload = {"landIndexs": land_index}
    #multipart/form-data
    if proxy_enabled and http_proxy and https_proxy:
        response = session.post(url, data=payload, proxies={"http": http_proxy, "https": https_proxy}, verify=False)
    else:
        response = session.post(url, data=payload)
    json_response = response.json()
    if json_response.get("ret") != 0:
        print(f"{json_response.get('msg')} on land {land_index} while harvesting")
    return json_response

def water_plants(session, land_index, proxy_enabled=False, http_proxy=None, https_proxy=None) -> None:
    url = "https://eu.api.h5.wildrift.leagueoflegends.com/5c/crystalrose/pub/farm?a=water"
    payload = {"landIndex": land_index}
    #multipart/form-data
    if proxy_enabled and http_proxy and https_proxy:
        response = session.post(url, data=payload, proxies={"http": http_proxy, "https": https_proxy}, verify=False)
    else:
        response = session.post(url, data=payload)
    json_response = response.json()
    if json_response.get("ret") != 0:
        print(f"{json_response.get('msg')} on land {land_index} while watering")
    return json_response

def buy_seed(session, id, count, proxy_enabled=False, http_proxy=None, https_proxy=None) -> None:
    url = "https://eu.api.h5.wildrift.leagueoflegends.com/5c/crystalrose/pub/shop?a=buy"
    payload = {"commodityId": id, "buyCount": count}
    if proxy_enabled and http_proxy and https_proxy:
        response = session.post(url, data=payload, proxies={"http": http_proxy, "https": https_proxy}, verify=False)
    else:
        response = session.post(url, data=payload)
    return response.json()

def redeem_quest(session, proxy_enabled=False, http_proxy=None, https_proxy=None) -> None:
    url = "https://eu.api.h5.wildrift.leagueoflegends.com/5c/crystalrose/pub/mission?a=missionSubmit"
    payload = {"missionType": "1", "missionId": "7000002"}
    if proxy_enabled and http_proxy and https_proxy:
        response = session.post(url, data=payload, proxies={"http": http_proxy, "https": https_proxy}, verify=False)
    else:
        response = session.post(url, data=payload)
    return response.json()

def remove_plant(session, land_index, proxy_enabled=False, http_proxy=None, https_proxy=None) -> None:
    url = "https://eu.api.h5.wildrift.leagueoflegends.com/5c/crystalrose/pub/farm?a=eliminate"
    payload = {"landIndex": land_index}
    if proxy_enabled and http_proxy and https_proxy:
        response = session.post(url, data=payload, proxies={"http": http_proxy, "https": https_proxy}, verify=False)
    else:
        response = session.post(url, data=payload)
    return response.json()