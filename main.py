import os
from modules.viu import (
    get_product_series_id,
    get_subtitle,
    get_ccs_product_id,
    get_manifest,
    RED, YELLOW, GREEN, RESET, CYAN, WHITE
)
from modules.logging import setup_logging
from modules.banners import banners
from modules.downloader import download_file, find_and_merge_files, download_hls, cleanup_logs_dir, ensure_logs_directory, logs_dir

logging = setup_logging()

def choose_subtitle_and_download(subtitles):
    if not subtitles:
        print(f"{RED}[ERROR]{RESET} No subtitles available to choose from.")
        return None

    for index, subtitle in enumerate(subtitles, start=1):
        print(f"{GREEN}{index}.{RESET} {YELLOW}LANGUAGE{RESET}: {CYAN}{subtitle['name']}{RESET}")

    try:
        choice = int(input(f"\n{YELLOW}Choose a subtitle {RED}(1-{len(subtitles)}){RED}: {WHITE}{RESET}")) - 1
        if 0 <= choice < len(subtitles):
            chosen_subtitle = subtitles[choice]
            output_file = os.path.join(logs_dir, f"{chosen_subtitle['name'].replace(' ', '_')}.srt")
            download_file(chosen_subtitle["url"], output_file)
            banners()
            print(f"{GREEN}[SUCCESS]{RESET} Subtitle downloaded: {CYAN}{output_file}{RESET}\n")
            return output_file
        else:
            print(f"{RED}[ERROR]{RESET} Invalid choice. Please select a valid subtitle.")
    except ValueError:
        print(f"{RED}[ERROR]{RESET} Invalid input. Please enter a number.")
    return None


def choose_resolution_and_download(ccs_product_id, series_name):
    resolutions = get_manifest(ccs_product_id)
    if isinstance(resolutions, str):
        output_file = os.path.join(logs_dir, f"{series_name.replace(' ', '_')}.m3u8")
        download_file(resolutions, output_file)
        return output_file

    if not isinstance(resolutions, dict):
        print(f"{RED}[ERROR]{RESET} No valid resolutions found for CCS PRODUCT ID: {CYAN}{ccs_product_id}{RESET}.")
        return None

    for index, (res, url) in enumerate(resolutions.items(), start=1):
        print(f"{GREEN}{index}. {res}{RESET}{RESET}")

    try:
        choice = int(input(f"\n{YELLOW}Enter the number of the resolution to select: {WHITE}{RESET}\n")) - 1
        if 0 <= choice < len(resolutions):
            banners()
            selected_res = list(resolutions.keys())[choice]
            selected_url = resolutions[selected_res]
            print(f"{GREEN}[INFO]{RESET} You selected: {CYAN}{selected_res}{RESET}")
            output_file = os.path.join(logs_dir, f"{series_name.replace(' ', '_')}_{selected_res}.m3u8")
            download_file(selected_url, output_file)
            return output_file
        else:
            print(f"{RED}[ERROR]{RESET} Invalid choice. Please select a valid resolution.")
    except ValueError:
        print(f"{RED}[ERROR]{RESET} Invalid input. Please enter a number.")
    return None


if __name__ == '__main__':
    banners()
    ensure_logs_directory()

    product_series_data = get_product_series_id()
    product_id = input(f"{YELLOW}Enter PRODUCT ID: {RESET}")
    series_id = input(f"{YELLOW}Enter SERIES ID: {RESET}")

    product_series = next(
        (ps for ps in product_series_data if ps["product_id"] == product_id and ps["series_id"] == series_id),
        None
    )

    if not product_series:
        print(f"{RED}[ERROR]{RESET} Invalid PRODUCT ID or SERIES ID.")
        exit(1)

    series_name = product_series["series_name"].replace(' ', '_')
    banners()
    print(f"{GREEN}[INFO]{RESET} Series Name: {CYAN}{series_name}{RESET}\n")

    subtitles = get_subtitle(product_id)
    if subtitles:
        subtitle_file = choose_subtitle_and_download(subtitles)

    ccs_product_id = get_ccs_product_id(series_id)
    if not ccs_product_id:
        print(f"{RED}[ERROR]{RESET} No CCS Product ID found.")
        exit(1)

    m3u8_file = choose_resolution_and_download(ccs_product_id, series_name)
    if not m3u8_file:
        print(f"{RED}[ERROR]{RESET} No valid resolution found for download.")
        exit(1)

    downloaded_file = download_hls(m3u8_file, series_name)
    if downloaded_file:
        find_and_merge_files()
        print(f"{GREEN}[SUCCESS]{RESET} Video processing complete.")
        cleanup_logs_dir()
    else:
        print(f"{RED}[ERROR]{RESET} Video download failed.")
        cleanup_logs_dir()