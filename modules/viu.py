import requests
import json
import re
from modules.banners import banners
from colorama import Fore

RED = Fore.RED
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
WHITE = Fore.WHITE
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
RESET = Fore.RESET

# def get_product_series_id():
#     url = "https://api-gateway-global.viu.com/api/audienceTargeting/recommendations"
#     querystring = {
#         "platform_flag_label": "web",
#         "area_id": "1001",
#         "language_flag_id": "7",
#         "platformFlagLabel": "web",
#         "areaId": "1001",
#         "languageFlagId": "7",
#         "countryCode": "MY",
#         "ut": "0",
#         "platform": "web",
#         "languageId": "7",
#         "deviceId": "3067c03d-d1a6-4673-8cba-4336200020c4",
#         "deviceType": "COOKIE",
#         "abtestId": "z",
#         "pageType": "home",
#         "pageId": "0"
#     }
#     headers = {
#         "sec-ch-ua-platform": "\"Windows\"",
#         "authorization": f"Bearer {TOKEN}",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
#         "accept": "application/json, text/plain, */*",
#         "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#         "sec-ch-ua-mobile": "?0",
#         "origin": "https://www.viu.com",
#         "sec-fetch-site": "same-site",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-dest": "empty",
#         "referer": "https://www.viu.com/",
#         "accept-encoding": "gzip, deflate, br, zstd",
#         "accept-language": "en-US,en;q=0.9",
#         "priority": "u=1, i"
#     }
#     response = requests.get(url, headers=headers, params=querystring)
#     if response.status_code != 200:
#         print(f"{RED}Failed to fetch data. Status code: {response.status_code}{RESET}")
#         return []

#     data = json.loads(response.text)
#     data_str = json.dumps(data)
#     regex = r'"(?:(product_id|series_id|series_name|ccs_product_id))"\s*:\s*"([^"]*)"'
#     matches = re.findall(regex, data_str)

#     results = []
#     grouped_data = {}

#     for key, value in matches:
#         value = value.encode('utf-8').decode('unicode_escape')
#         if key == "product_id" and grouped_data:
#             results.append({
#                 "product_id": grouped_data.get("product_id", "N/A"),
#                 "series_id": grouped_data.get("series_id", "N/A"),
#                 "series_name": grouped_data.get("series_name", "N/A")
#             })
#             print("=" * 80)
#             print(f"{YELLOW}PRODUCT ID{RED} : {GREEN}{grouped_data.get('product_id', 'N/A')}{RESET}")
#             print(f"{YELLOW}SERIES ID{RED}  : {GREEN}{grouped_data.get('series_id', 'N/A')}{RESET}")
#             print(f"{YELLOW}TITLE{RED}      : {GREEN}{grouped_data.get('series_name', 'N/A')}{RESET}")
#             grouped_data = {}
#         grouped_data[key] = value

#     if grouped_data:
#         results.append({
#             "product_id": grouped_data.get("product_id", "N/A"),
#             "series_id": grouped_data.get("series_id", "N/A"),
#             "series_name": grouped_data.get("series_name", "N/A")
#         })
#         print("=" * 80)
#         print(f"{YELLOW}PRODUCT ID{RED} : {GREEN}{grouped_data.get('product_id', 'N/A')}{RESET}")
#         print(f"{YELLOW}SERIES ID{RED}  : {GREEN}{grouped_data.get('series_id', 'N/A')}{RESET}")
#         print(f"{YELLOW}TITLE{RED}      : {GREEN}{grouped_data.get('series_name', 'N/A')}{RESET}")
#         print("=" * 80 + "\n")
#     return results

def get_product_series_id(url):
    cookies = {
        '_ottUID': '3067c03d-d1a6-4673-8cba-4336200020c4',
        'onboarding_date': '2024-12-31',
        'onboarding_session': 'a1f25e94-3f1c-4159-aca7-6f46d89bb35f',
        'countryCode': 'my',
        'areaId': '1001',
        'platform': 'browser',
        'account_type': '',
        'user_id': '',
        'user_level': '0',
        '_gcl_au': '1.1.1988879905.1735596325',
        'bitmovin_analytics_uuid': '735fa3b3-52a2-47e9-8cdb-1663409dfcfd',
        '_ga': 'GA1.1.1719375963.1735596327',
        '_tt_enable_cookie': '1',
        '_ttp': 'qytOGhAn64hc6wWgHKjF55y--A-.tt.1',
        'FPID': 'FPID2.2.8XWQ%2FLvXCzbsVG5Vu9ipIJMjiwoZULEqmmpWQOFxNvs%3D.1735596327',
        'FPLC': 'bldef7Smo%2BHo9y2HA%2B3bvtOKvSHcld00A%2Fid%2BcKeKDYXjOFfiWIS2Qc8YhmCoFbqmkWh7aLTyK3BntzHOSOgSWojrOmWsQgGPfeBKvmRrr2j%2FA%2BeVKy64q24buMJMw%3D%3D',
        'app_language': 'ms',
        'token': 'eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.KgzgnAiUSNs2pUi6rogOcnt47PJN2EA_Mq7-FqYoCUxq6QAPd5C_iw.0u6YGJU2jxOe7r1QZIZO6A.nHupAtiRXzUbE_WGoDm4liyitvJUJF9hSMRemAwfUCF3_xKHFQO5qFacF6x8YIYsuY8JGeY2iUf8EXQzxWZtyKQULZfgVngeywtWyslDJbjU-OIkrziLVViRf6epgFX8dtG1I-CgrKWNIjI4d5Zk-oclttYnwz25qh9tnLSmp3Gb4UX-R_Plps0hpnBWp1iava2uGqxQnYIMq1wzVV52U1hqi8lBNpf9CnDYCSFpqAWWHHuiFSOp18Q-Wqo-CeHG.KTfvbROerYQy7FmsZC0acg',
        'token_param': '{%22appVersion%22:%224.11.2%22%2C%22countryCode%22:%22MY%22%2C%22language%22:%227%22%2C%22platform%22:%22browser%22%2C%22platformFlagLabel%22:%22web%22%2C%22uuid%22:%223067c03d-d1a6-4673-8cba-4336200020c4%22%2C%22carrierId%22:%2283%22%2C%22carrierName%22:%22TELEKOM%22%2C%22env%22:%22prod_1viu%22}',
        '_clck': '1xyq8vm%7C2%7Cfs6%7C0%7C1825',
        '_ga_JWYW12WYDS': 'GS1.1.1735610997.4.0.1735612093.0.0.1637431212',
        'AWSALB': 'GMO685FRkZDdTnnvX3GmJHtHH0HAXmG9aUssMPrYmypL4ySQRVwJGGcZnEtxE9ep04I8SYhWvkTfiwqOEHVd96JIEx0R3ZWCfU52VZOAmw4FgVVr9UG9AMDbxXH1',
        'AWSALBCORS': 'GMO685FRkZDdTnnvX3GmJHtHH0HAXmG9aUssMPrYmypL4ySQRVwJGGcZnEtxE9ep04I8SYhWvkTfiwqOEHVd96JIEx0R3ZWCfU52VZOAmw4FgVVr9UG9AMDbxXH1',
        'cookie_consent_accept': 'true',
        'session_id': '3df59180-d81a-4d3f-85d6-12692b6cb431',
        '_ottAID': '9ab72032-c2ad-4b0b-829a-c73e3d9eb7ef',
        '_clsk': '186rh3e%7C1735654184943%7C1%7C0%7Cw.clarity.ms%2Fcollect',
        '_ga_VY5BCF92LV': 'GS1.1.1735654182.4.1.1735654185.0.0.0',
        '_ga_LMLQB6R0XP': 'GS1.1.1735654183.4.1.1735654187.56.0.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': '_ottUID=3067c03d-d1a6-4673-8cba-4336200020c4; onboarding_date=2024-12-31; onboarding_session=a1f25e94-3f1c-4159-aca7-6f46d89bb35f; countryCode=my; areaId=1001; platform=browser; account_type=; user_id=; user_level=0; _gcl_au=1.1.1988879905.1735596325; bitmovin_analytics_uuid=735fa3b3-52a2-47e9-8cdb-1663409dfcfd; _ga=GA1.1.1719375963.1735596327; _tt_enable_cookie=1; _ttp=qytOGhAn64hc6wWgHKjF55y--A-.tt.1; FPID=FPID2.2.8XWQ%2FLvXCzbsVG5Vu9ipIJMjiwoZULEqmmpWQOFxNvs%3D.1735596327; FPLC=bldef7Smo%2BHo9y2HA%2B3bvtOKvSHcld00A%2Fid%2BcKeKDYXjOFfiWIS2Qc8YhmCoFbqmkWh7aLTyK3BntzHOSOgSWojrOmWsQgGPfeBKvmRrr2j%2FA%2BeVKy64q24buMJMw%3D%3D; app_language=ms; token=eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.KgzgnAiUSNs2pUi6rogOcnt47PJN2EA_Mq7-FqYoCUxq6QAPd5C_iw.0u6YGJU2jxOe7r1QZIZO6A.nHupAtiRXzUbE_WGoDm4liyitvJUJF9hSMRemAwfUCF3_xKHFQO5qFacF6x8YIYsuY8JGeY2iUf8EXQzxWZtyKQULZfgVngeywtWyslDJbjU-OIkrziLVViRf6epgFX8dtG1I-CgrKWNIjI4d5Zk-oclttYnwz25qh9tnLSmp3Gb4UX-R_Plps0hpnBWp1iava2uGqxQnYIMq1wzVV52U1hqi8lBNpf9CnDYCSFpqAWWHHuiFSOp18Q-Wqo-CeHG.KTfvbROerYQy7FmsZC0acg; token_param={%22appVersion%22:%224.11.2%22%2C%22countryCode%22:%22MY%22%2C%22language%22:%227%22%2C%22platform%22:%22browser%22%2C%22platformFlagLabel%22:%22web%22%2C%22uuid%22:%223067c03d-d1a6-4673-8cba-4336200020c4%22%2C%22carrierId%22:%2283%22%2C%22carrierName%22:%22TELEKOM%22%2C%22env%22:%22prod_1viu%22}; _clck=1xyq8vm%7C2%7Cfs6%7C0%7C1825; _ga_JWYW12WYDS=GS1.1.1735610997.4.0.1735612093.0.0.1637431212; AWSALB=GMO685FRkZDdTnnvX3GmJHtHH0HAXmG9aUssMPrYmypL4ySQRVwJGGcZnEtxE9ep04I8SYhWvkTfiwqOEHVd96JIEx0R3ZWCfU52VZOAmw4FgVVr9UG9AMDbxXH1; AWSALBCORS=GMO685FRkZDdTnnvX3GmJHtHH0HAXmG9aUssMPrYmypL4ySQRVwJGGcZnEtxE9ep04I8SYhWvkTfiwqOEHVd96JIEx0R3ZWCfU52VZOAmw4FgVVr9UG9AMDbxXH1; cookie_consent_accept=true; session_id=3df59180-d81a-4d3f-85d6-12692b6cb431; _ottAID=9ab72032-c2ad-4b0b-829a-c73e3d9eb7ef; _clsk=186rh3e%7C1735654184943%7C1%7C0%7Cw.clarity.ms%2Fcollect; _ga_VY5BCF92LV=GS1.1.1735654182.4.1.1735654185.0.0.0; _ga_LMLQB6R0XP=GS1.1.1735654183.4.1.1735654187.56.0.0',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response = requests.get(url, cookies=cookies, headers=headers)
    if response.status_code == 200:
        series_pattern = r'"series_id":\s*"(\d+)",\s*"series_name":\s*"(.*?)",\s*"product_id":\s*"(\d+)"'
        series_match = re.search(series_pattern, response.text)

        if series_match:
            series_id = series_match.group(1)
            series_name = series_match.group(2)
            product_id = series_match.group(3)
            print(f"Series Name: {series_name}")
        else:
            print("No match found for series information.")
            return None, None

        episode_pattern = r'<h2[^>]*id="type_ep"[^>]*>Episod\s+(\d+)</h2>'
        episode_match = re.search(episode_pattern, response.text)
        if episode_match:
            episode_number = episode_match.group(1)
            print(f"Episode Number: {episode_number}")
        else:
            print("No match found for episode number.")
        return product_id, series_id, series_name
    else:
        print(f"Failed to fetch the URL. Status code: {response.status_code}")
        return None, None
    
def get_subtitle(product_id, token):
    url = "https://api-gateway-global.viu.com/api/mobile"
    querystring = {
        "platform_flag_label": "web",
        "area_id": "1001",
        "language_flag_id": "7",
        "platformFlagLabel": "web",
        "areaId": "1001",
        "languageFlagId": "7",
        "countryCode": "MY",
        "ut": "0",
        "r": "/vod/detail",
        "product_id": product_id,
        "os_flag_id": "1"
    }

    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "authorization": f"Bearer {token}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "origin": "https://www.viu.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.viu.com/",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        print(f"{RED}Error fetching subtitles. Status code: {response.status_code}{RESET}")
        return []

    data = response.json()
    data_str = json.dumps(data)
    subtitle_regex = r'"(?:(subtitle_url|name|product_subtitle_id))"\s*:\s*"([^"]*)"'
    subtitle_matches = re.findall(subtitle_regex, data_str)
    subtitles = []
    current_subtitle = {}
    for key, value in subtitle_matches:
        value = value.encode('utf-8').decode('unicode_escape')
        current_subtitle[key] = value
        if key == "product_subtitle_id":
            subtitles.append({
                "name": current_subtitle.get("name", "N/A"),
                "url": current_subtitle.get("subtitle_url", "N/A"),
                "id": current_subtitle.get("product_subtitle_id", "N/A")
            })
            current_subtitle = {}
    return subtitles
            
def get_ccs_product_id(series_id, token):
    url = "https://api-gateway-global.viu.com/api/mobile"
    querystring = {
        "platform_flag_label": "web",
        "area_id": "1001",
        "language_flag_id": "7",
        "platformFlagLabel": "web",
        "areaId": "1001",
        "languageFlagId": "7",
        "countryCode": "MY",
        "ut": "0",
        "r": "/vod/product-list",
        "os_flag_id": "1",
        "series_id": series_id,
        "size": "-1",
        "sort": "desc"
    }
    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "authorization": f"Bearer {token}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "origin": "https://www.viu.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.viu.com/",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    product_list = data["data"]["product_list"]
    ccs_ids = [product["ccs_product_id"] for product in product_list if "ccs_product_id" in product]
    return ccs_ids

def get_manifest(ccs_product_id, token):
    url = "https://api-gateway-global.viu.com/api/playback/distribute"
    querystring = {
        "platform_flag_label": "web",
        "area_id": "1001",
        "language_flag_id": "7",
        "platformFlagLabel": "web",
        "areaId": "1001",
        "languageFlagId": "7",
        "countryCode": "MY",
        "ut": "0",
        "ccs_product_id": ccs_product_id
    }
    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "authorization": f"Bearer {token}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "origin": "https://www.viu.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.viu.com/",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        print(f"{RED}Error fetching manifests. Status code: {response.status_code}{RESET}")
        return None

    data = response.json()
    try:
        manifests = {
            "240P": data["data"]["stream"]["url"]["s240p"],
            "480P": data["data"]["stream"]["url"]["s480p"],
            "720P": data["data"]["stream"]["url"]["s720p"],
            "1080P": data["data"]["stream"]["url"]["s1080p"],
        }

        print(f"{YELLOW}[VIU-DOWNLOADER]{RED}: {GREEN}Available Resolutions{RESET}")
        print("=" * 50)
        for i, (res, url) in enumerate(manifests.items(), start=1):
            print(f"{YELLOW}[{i}]{RED}: {GREEN}{res}{RESET}")

        choice = int(input(f"\n{YELLOW}Enter the number of the resolution to select: {WHITE}{RESET}"))
        if 1 <= choice <= len(manifests):
            selected_res = list(manifests.keys())[choice - 1]
            selected_url = manifests[selected_res]
            banners()
            print(f"{YELLOW}[VIU-DOWNLOADER]{RED}: {WHITE}SELECTED {GREEN}{selected_res}{RESET}")
            return selected_url
        else:
            print(f"{RED}Invalid choice. Please enter a number between 1 and {len(manifests)}.{RESET}")
            return None

    except KeyError as e:
        print(f"{RED}Error fetching resolutions: Missing key {e}{RESET}")
        return None
    except ValueError:
        print(f"{RED}Invalid input. Please enter a valid number.{RESET}")
        return None
