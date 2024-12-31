from configparser import ConfigParser
from modules.banners import banners
from modules.viu import RED, CYAN, YELLOW, GREEN, WHITE, RESET
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
        print(f"{GREEN}[INFO]{RESET} Token already exists in config.ini.")
        return config['VIU']['TOKEN']

    token = input(f"\n{YELLOW}[VIU-DOWNLOADER] {WHITE}Enter Authorization Bearer Token: {RESET}").strip()
    if not token:
        print(f"{RED}[ERROR]{RESET} No token provided. Exiting.")
        exit(1)

    config['VIU'] = {'TOKEN': token}
    with open(CONFIG, 'w') as configfile:
        config.write(configfile)

    banners()
    print(f"{YELLOW}[VIU-DOWNLOADER]{RED}: {GREEN}Token saved to {CYAN}config.ini{RESET}\n")
    return token