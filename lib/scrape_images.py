import bs4
import os
import sys
import requests
from urllib import request as req

filenames = []

def collect_img_links(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html5lib')
    
    return [img.get('src') for img in soup.select('img') 
            if img.get('src').startswith('http')]


def download(from_url, to_file): 
    if not os.path.isfile(to_file):
        try: 
            req.urlretrieve(from_url, to_file)
            filenames.append(os.path.basename(to_file))
        except:
            pass    

def download_imgs(links, out_folder="./images/"):
    for l in links:
        file_name = os.path.join(out_folder, os.path.basename(l))
        download(l,file_name)

def scrape(url):
    links = collect_img_links(url)
    download_imgs(links)
    return filenames