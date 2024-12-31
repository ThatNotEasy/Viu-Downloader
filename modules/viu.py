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

def get_product_series_id():
    url = "https://api-gateway-global.viu.com/api/audienceTargeting/recommendations"
    querystring = {
        "platform_flag_label": "web",
        "area_id": "1001",
        "language_flag_id": "7",
        "platformFlagLabel": "web",
        "areaId": "1001",
        "languageFlagId": "7",
        "countryCode": "MY",
        "ut": "0",
        "platform": "web",
        "languageId": "7",
        "deviceId": "3067c03d-d1a6-4673-8cba-4336200020c4",
        "deviceType": "COOKIE",
        "abtestId": "z",
        "pageType": "home",
        "pageId": "0"
    }
    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.KgzgnAiUSNs2pUi6rogOcnt47PJN2EA_Mq7-FqYoCUxq6QAPd5C_iw.0u6YGJU2jxOe7r1QZIZO6A.nHupAtiRXzUbE_WGoDm4liyitvJUJF9hSMRemAwfUCF3_xKHFQO5qFacF6x8YIYsuY8JGeY2iUf8EXQzxWZtyKQULZfgVngeywtWyslDJbjU-OIkrziLVViRf6epgFX8dtG1I-CgrKWNIjI4d5Zk-oclttYnwz25qh9tnLSmp3Gb4UX-R_Plps0hpnBWp1iava2uGqxQnYIMq1wzVV52U1hqi8lBNpf9CnDYCSFpqAWWHHuiFSOp18Q-Wqo-CeHG.KTfvbROerYQy7FmsZC0acg",
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
        print(f"{RED}Failed to fetch data. Status code: {response.status_code}{RESET}")
        return []

    data = json.loads(response.text)
    data_str = json.dumps(data)
    regex = r'"(?:(product_id|series_id|series_name|ccs_product_id))"\s*:\s*"([^"]*)"'
    matches = re.findall(regex, data_str)

    results = []
    grouped_data = {}

    for key, value in matches:
        value = value.encode('utf-8').decode('unicode_escape')
        if key == "product_id" and grouped_data:
            results.append({
                "product_id": grouped_data.get("product_id", "N/A"),
                "series_id": grouped_data.get("series_id", "N/A"),
                "series_name": grouped_data.get("series_name", "N/A")
            })
            print("=" * 80)
            print(f"{YELLOW}PRODUCT ID{RED} : {GREEN}{grouped_data.get('product_id', 'N/A')}{RESET}")
            print(f"{YELLOW}SERIES ID{RED}  : {GREEN}{grouped_data.get('series_id', 'N/A')}{RESET}")
            print(f"{YELLOW}TITLE{RED}      : {GREEN}{grouped_data.get('series_name', 'N/A')}{RESET}")
            grouped_data = {}
        grouped_data[key] = value

    if grouped_data:
        results.append({
            "product_id": grouped_data.get("product_id", "N/A"),
            "series_id": grouped_data.get("series_id", "N/A"),
            "series_name": grouped_data.get("series_name", "N/A")
        })
        print("=" * 80)
        print(f"{YELLOW}PRODUCT ID{RED} : {GREEN}{grouped_data.get('product_id', 'N/A')}{RESET}")
        print(f"{YELLOW}SERIES ID{RED}  : {GREEN}{grouped_data.get('series_id', 'N/A')}{RESET}")
        print(f"{YELLOW}TITLE{RED}      : {GREEN}{grouped_data.get('series_name', 'N/A')}{RESET}")
        print("=" * 80 + "\n")

    return results

        
def get_subtitle(product_id):
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
        "authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.KgzgnAiUSNs2pUi6rogOcnt47PJN2EA_Mq7-FqYoCUxq6QAPd5C_iw.0u6YGJU2jxOe7r1QZIZO6A.nHupAtiRXzUbE_WGoDm4liyitvJUJF9hSMRemAwfUCF3_xKHFQO5qFacF6x8YIYsuY8JGeY2iUf8EXQzxWZtyKQULZfgVngeywtWyslDJbjU-OIkrziLVViRf6epgFX8dtG1I-CgrKWNIjI4d5Zk-oclttYnwz25qh9tnLSmp3Gb4UX-R_Plps0hpnBWp1iava2uGqxQnYIMq1wzVV52U1hqi8lBNpf9CnDYCSFpqAWWHHuiFSOp18Q-Wqo-CeHG.KTfvbROerYQy7FmsZC0acg",
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
            
def get_ccs_product_id(series_id):
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
        "authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.KgzgnAiUSNs2pUi6rogOcnt47PJN2EA_Mq7-FqYoCUxq6QAPd5C_iw.0u6YGJU2jxOe7r1QZIZO6A.nHupAtiRXzUbE_WGoDm4liyitvJUJF9hSMRemAwfUCF3_xKHFQO5qFacF6x8YIYsuY8JGeY2iUf8EXQzxWZtyKQULZfgVngeywtWyslDJbjU-OIkrziLVViRf6epgFX8dtG1I-CgrKWNIjI4d5Zk-oclttYnwz25qh9tnLSmp3Gb4UX-R_Plps0hpnBWp1iava2uGqxQnYIMq1wzVV52U1hqi8lBNpf9CnDYCSFpqAWWHHuiFSOp18Q-Wqo-CeHG.KTfvbROerYQy7FmsZC0acg",
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

def get_manifest(ccs_product_id):
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
        "authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.KgzgnAiUSNs2pUi6rogOcnt47PJN2EA_Mq7-FqYoCUxq6QAPd5C_iw.0u6YGJU2jxOe7r1QZIZO6A.nHupAtiRXzUbE_WGoDm4liyitvJUJF9hSMRemAwfUCF3_xKHFQO5qFacF6x8YIYsuY8JGeY2iUf8EXQzxWZtyKQULZfgVngeywtWyslDJbjU-OIkrziLVViRf6epgFX8dtG1I-CgrKWNIjI4d5Zk-oclttYnwz25qh9tnLSmp3Gb4UX-R_Plps0hpnBWp1iava2uGqxQnYIMq1wzVV52U1hqi8lBNpf9CnDYCSFpqAWWHHuiFSOp18Q-Wqo-CeHG.KTfvbROerYQy7FmsZC0acg",
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
            print(f"{YELLOW}[VIU-DOWNLOADER]{RED}: {WHITE}SELECTED{RED}: {GREEN}{selected_res}{RESET}")
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