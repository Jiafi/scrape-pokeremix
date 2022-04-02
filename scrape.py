import os
import requests

from bs4 import BeautifulSoup
response = requests.get("http://www.lycanroc.net/music/?g=pokeremixstudio")
html = response.content

soup = BeautifulSoup(html, features="html.parser")

def create_download_urls():
    base_url = "http://www.lycanroc.net/media" 
    result = soup.find("div", class_="music_block")
    download_urls = []
    for child in result.children:
        for item in str(child).split():
            if item.startswith("play"):
                suffix = item.split("'")[1]
                to_append = (f"{base_url}/{suffix}", suffix)
                download_urls.append(to_append)
    return download_urls

def download_files(download_urls):
    for download_url, suffix in download_urls:
        doc = requests.get(download_url)
        file_name = suffix.split("/")[-1].replace("%20", "_")
        os.makedirs("music", exist_ok=True)
        full_path = f"music/{file_name}"
        with open(full_path, 'wb') as f:
            f.write(doc.content)
        print(f"Wrote file={full_path}")

download_urls = create_download_urls()
download_files(download_urls)
