import requests
import json
import re
import os
from modules.banners import banners
from modules.config import setup_config
from colorama import Fore
from http.cookiejar import MozillaCookieJar

RED = Fore.RED
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
WHITE = Fore.WHITE
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
RESET = Fore.RESET

class VIU:
    def __init__(self):
        self.config = setup_config()
        self.token = self.config["VIU"]["TOKEN"]
        self.session = requests.Session()
        self.cookies_file = "cookies.txt"
        
        # Initialize headers properly
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
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
        
        # Load cookies during initialization
        self.load_cookies(self.cookies_file)
        
    def load_cookies(self, file_path):
        """Load cookies from Netscape format file into the session"""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{RED}Cookies file not found: {file_path}{RESET}")
        
        try:
            cookie_jar = MozillaCookieJar()
            cookie_jar.load(file_path, ignore_discard=True, ignore_expires=True)
            self.session.cookies = cookie_jar
            print(f"{GREEN}Successfully loaded cookies from {file_path}{RESET}")
            return True
        except Exception as e:
            print(f"{RED}Error loading cookies: {e}{RESET}")
            return False
        
    def get_product_series_id(self, url):
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                series_pattern = r'"series_id":\s*"(\d+)",\s*"series_name":\s*"(.*?)",\s*"product_id":\s*"(\d+)"'
                series_match = re.search(series_pattern, response.text)

                if not series_match:
                    print(f"{YELLOW}No match found for series information.{RESET}")
                    return None, None, None

                series_id = series_match.group(1)
                series_name = series_match.group(2)
                product_id = series_match.group(3)
                episode_pattern = r'<h2[^>]*id="type_ep"[^>]*>Episod\s+(\d+)</h2>'
                episode_match = re.search(episode_pattern, response.text)
                
                if episode_match:
                    episode_number = episode_match.group(1)
                    formatted_name = f"{series_name} Episode {episode_number}"
                else:
                    print(f"{YELLOW}No episode number found{RESET}")
                    formatted_name = series_name

                return product_id, series_id, formatted_name
            else:
                print(f"{RED}Failed to fetch URL. Status code: {response.status_code}{RESET}")
                return None, None, None
        except Exception as e:
            print(f"{RED}Error in get_product_series_id: {e}{RESET}")
            return None, None, None
    
    def get_subtitle(self, product_id):
        """Fetch available subtitles for a product"""
        url = "https://api-gateway-global.viu.com/api/mobile"
        querystring = {
            "platform_flag_label": "web",
            "area_id": "1001",
            "language_flag_id": "7",
            "countryCode": "MY",
            "ut": "0",
            "r": "/vod/detail",
            "product_id": product_id,
            "os_flag_id": "1"
        }
        
        headers = self.headers.copy()
        headers["authorization"] = f"Bearer {self.token}"
        
        try:
            response = self.session.get(url, headers=headers, params=querystring)
            if response.status_code != 200:
                print(f"{RED}Error fetching subtitles. Status code: {response.status_code}{RESET}")
                return []

            data = response.json()
            subtitles = []
            
            # More robust subtitle extraction
            if "data" in data and "product_subtitle" in data["data"]:
                for subtitle in data["data"]["product_subtitle"]:
                    subtitles.append({
                        "name": subtitle.get("name", "N/A"),
                        "url": subtitle.get("subtitle_url", "N/A"),
                        "id": subtitle.get("product_subtitle_id", "N/A")
                    })
            return subtitles
        except Exception as e:
            print(f"{RED}Error in get_subtitle: {e}{RESET}")
            return []
                
    def get_ccs_product_id(self, series_id):
        """Get CCS product IDs for a series"""
        url = "https://api-gateway-global.viu.com/api/mobile"
        querystring = {
            "platform_flag_label": "web",
            "area_id": "1001",
            "language_flag_id": "7",
            "countryCode": "MY",
            "ut": "0",
            "r": "/vod/product-list",
            "os_flag_id": "1",
            "series_id": series_id,
            "size": "-1",
            "sort": "desc"
        }
        
        headers = self.headers.copy()
        headers["authorization"] = f"Bearer {self.token}"
        
        try:
            response = self.session.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            product_list = data.get("data", {}).get("product_list", [])
            return [product["ccs_product_id"] for product in product_list if "ccs_product_id" in product]
        except Exception as e:
            print(f"{RED}Error in get_ccs_product_id: {e}{RESET}")
            return []

    def get_manifest(self, ccs_product_id):
        """Get streaming manifests for a CCS product"""
        url = "https://api-gateway-global.viu.com/api/playback/distribute"
        querystring = {
            "platform_flag_label": "web",
            "area_id": "1001",
            "language_flag_id": "7",
            "countryCode": "MY",
            "ut": "1",
            "ccs_product_id": ccs_product_id
        }
        
        headers = self.headers.copy()
        headers["authorization"] = f"Bearer {self.token}"
        
        try:
            response = self.session.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            manifests = {
                "240P": data.get("data", {}).get("stream", {}).get("url", {}).get("s240p"),
                "480P": data.get("data", {}).get("stream", {}).get("url", {}).get("s480p"),
                "720P": data.get("data", {}).get("stream", {}).get("url", {}).get("s720p"),
                "1080P": data.get("data", {}).get("stream", {}).get("url", {}).get("s1080p"),
            }
            
            # Filter out None values
            manifests = {k: v for k, v in manifests.items() if v is not None}
            
            if not manifests:
                print(f"{RED}No available resolutions found{RESET}")
                return None

            print(f"{YELLOW}[VIU-DOWNLOADER]{RED}: {GREEN}Available Resolutions{RESET}")
            print("=" * 50)
            for i, (res, url) in enumerate(manifests.items(), start=1):
                print(f"{YELLOW}[{i}]{RED}: {GREEN}{res}{RESET}")

            choice = int(input(f"\n{YELLOW}Enter the number of the resolution to select: {WHITE}"))
            selected_res = list(manifests.keys())[choice - 1]
            selected_url = manifests[selected_res]
            
            banners()
            print(f"{YELLOW}[VIU-DOWNLOADER]{RED}: {WHITE}SELECTED {GREEN}{selected_res}{RESET}")
            return selected_url
            
        except (ValueError, IndexError):
            print(f"{RED}Invalid selection. Please enter a valid number.{RESET}")
            return None
        except Exception as e:
            print(f"{RED}Error in get_manifest: {e}{RESET}")
            return None
