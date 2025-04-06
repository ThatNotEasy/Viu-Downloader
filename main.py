import os, time
from modules.viu import VIU, RED, YELLOW, GREEN, RESET, CYAN, WHITE
from modules.config import prompt_and_save_token
from modules.logging import setup_logging
from modules.banners import banners
from modules.downloader import download_file, find_and_merge_files, download_hls, cleanup_logs_dir, ensure_logs_directory, logs_dir, create_m3u_playlist

logging = setup_logging()
viu = VIU()


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
    resolutions = viu.get_manifest(ccs_product_id)
    create_m3u_playlist(series_name, resolutions, append=True)
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
    
    token = prompt_and_save_token()
    if not token:
        print(f"{RED}[ERROR]{RESET} No token provided. Exiting.")
        exit(1)

    print(f"{YELLOW}Choose option:{RESET}")
    print(f"{GREEN}1. VOD{RESET}")
    print(f"{CYAN}2. Series{RESET}")
    option = input(f"{YELLOW}Enter your choice (1 or 2): {WHITE}{RESET}")

    if option == "1":
        # VOD option - proceed with original flow
        url = input(f"{YELLOW}Enter VIU URL: {RESET}")
        time.sleep(1)
        banners()
        try:
            product_id, series_id, series_name = viu.get_product_series_id(url)
            print(f"{GREEN}[INFO]{RESET} Series Name: {CYAN}{series_name}{RESET}\n")
        except ValueError as e:
            print(f"{RED}[ERROR]{RESET} {str(e)}")
            exit(1)

        subtitles = viu.get_subtitle(product_id)
        if subtitles:
            choose_subtitle_and_download(subtitles)

        ccs_product_id = viu.get_ccs_product_id(series_id)
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
        else:
            print(f"{RED}[ERROR]{RESET} Video download failed.")

    elif option == "2":
        # Series option - extract product ID from URL and use get_series
        url = input(f"{YELLOW}Enter VIU Series URL: {RESET}")
        product_id = viu.extract_product_id(url)
        if not product_id:
            print(f"{RED}[ERROR]{RESET} Could not extract product ID from URL.")
            exit(1)
        
        print(f"{GREEN}[INFO]{RESET} Extracted Product ID: {CYAN}{product_id}{RESET}")
        
        # Get series information using the get_series method
        try:
            series_info = viu.get_series(product_id)
            series_id = series_info["series_id"]
            ccs_product_id = series_info["ccs_product_id"]
            series_name = series_info["series_name"] or input(f"{YELLOW}Enter series name (for filename): {RESET}").strip()
            
            print(f"{GREEN}[INFO]{RESET} Series ID: {CYAN}{series_id}{RESET}")
            print(f"{GREEN}[INFO]{RESET} CCS Product ID: {CYAN}{ccs_product_id}{RESET}")
            
            # Continue with the download process
            subtitles = viu.get_subtitle(product_id)
            if subtitles:
                choose_subtitle_and_download(subtitles)

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
            else:
                print(f"{RED}[ERROR]{RESET} Video download failed.")
                
        except Exception as e:
            print(f"{RED}[ERROR]{RESET} Failed to get series information: {str(e)}")
            exit(1)
