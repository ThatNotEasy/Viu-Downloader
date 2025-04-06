from configparser import ConfigParser
from modules.banners import banners
from colorama import Fore
import os

CONFIG = "config.ini"

def setup_config():
    """Load the configuration from config.ini or create a new one."""
    config = ConfigParser()
    if os.path.exists(CONFIG):
        config.read(CONFIG)
    return config

def prompt_and_save_token():
    config = setup_config()
    if config.has_section('VIU') and 'TOKEN' in config['VIU']:
        print(f"{Fore.GREEN}[INFO]{Fore.RESET} Token already exists in config.ini\n")
        return config['VIU']['TOKEN']

    token = input(f"\n{Fore.YELLOW}[VIU-DOWNLOADER] {Fore.WHITE}Enter Authorization Bearer Token: {Fore.RESET}").strip()
    if not token:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} No token provided. Exiting.")
        exit(1)

    config['VIU'] = {'TOKEN': token}
    with open(CONFIG, 'w') as configfile:
        config.write(configfile)

    banners()
    print(f"{Fore.YELLOW}[VIU-DOWNLOADER]{Fore.RED}: {Fore.GREEN}Token saved to {Fore.CYAN}config.ini{Fore.RESET}\n")
    return token
