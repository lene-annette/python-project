import bs4
import os
import sys
import requests


def collect_img_links(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html5lib')
    
    return [img.get('src') for img in soup.select('img') 
            if img.get('src').startswith('http')]


def download_imgs(links, out_folder="./images/"):
    for l in links:
        # You know how to do this!
        pass 