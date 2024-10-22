from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import json
from dataclasses import dataclass
from typing import Optional
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@dataclass
class VideoInfo:
    video_url: str
    video_type: Optional[str] = None
    splash_image: Optional[str] = None

class VideoCrawler:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--no-sandbox")
        self.driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=firefox_options
        )
        self.xpath = "/html/body/section/article/div[1]/div[1]/div"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def get_video_info(self, url: str) -> Optional[VideoInfo]:
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.xpath))
            )
            video_element = self.driver.find_element(By.XPATH, self.xpath)
            video_data = video_element.get_attribute("data-item")
            video_info_json = json.loads(video_data)
            video_sources = video_info_json.get("sources", [])
            if not video_sources:
                raise ValueError("No video sources found in the page.")
            video_src = video_sources[0].get("src")
            video_type = video_sources[0].get("type")
            splash_image = video_info_json.get("splash")
            if not video_src:
                raise ValueError("Video URL not found in the page.")
            return VideoInfo(
                video_url=video_src,
                video_type=video_type,
                splash_image=splash_image
            )
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return None

if __name__ == "__main__":
    with VideoCrawler() as crawler:
        video_info = crawler.get_video_info(url)
        if video_info:
            print(f"Video URL: {video_info.video_url}, Video Type: {video_info.video_type}, Splash image: {video_info.splash_image}")
        else:
            print("Failed to retrieve video information.")
