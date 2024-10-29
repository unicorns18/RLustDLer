from user_agent_randomizer import UserAgentRandomizer
from helpers.tqdm import tqdm
import requests, os

class RLustDownloader:
    def __init__(self):
        self.uar = UserAgentRandomizer()
    
    def download(self, url, output_filename=None):
        if output_filename is None:
            output_filename = url.split('/gen/')[-1]
            print(f"output filename: {output_filename}")
        headers = self._get_headers()
        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('Content-Length', 0))
            self._print_download_info(response.status_code, total_size)

            with open(output_filename, 'wb') as file, tqdm(
                iterable=response.iter_content(chunk_size=1024),
                desc="Downloading",
                unit="KB",
                unit_scale=True,
                total=total_size // 1024
            ) as progress_bar:
                for chunk in progress_bar:
                    file.write(chunk)
        print("ok done downloading video")
    
    def delete_file(self, filename):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    def _get_headers(self):
        return {
            'Accept': '*/*',
            'Accept-Encoding': 'identity;q=1, *;q=0',
            'Accept-Language': 'en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'rl.eros.icu',
            'Pragma': 'no-cache',
            'Range': 'bytes=0-',
            'Referer': 'https://rapelust.com/',
            'Sec-Fetch-Dest': 'video',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': self.uar.get_random_ua(),
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
    
    def _generate_filename(self, url):
        return os.path.basename(url) or "downloaded_video.mp4"
    
    def _print_download_info(self, status_code, total_size):
        print(f"Status code: {status_code}")
        print(f"Video size: {total_size / (1024 ** (i := (0, 1, 2)[(total_size >= 1024 ** 2) + (total_size >= 1024 ** 3)])):.2f} {'BKMGT'[i]}B")

if __name__ == "__main__":
    downloader = RLustDownloader()
    downloader.download("https://rl.eros.icu/gen/step_sister_takes_advantage_of_step_bro.mp4")
