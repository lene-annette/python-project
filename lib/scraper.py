import bs4
import os
import requests
import sys
from tqdm import tqdm
from urllib import request as req

def scrape(url):
    '''Scrapes img (src) links from img tags and downloads the images.'''
    links = collect_img_links(url)
    download_imgs(links)

def collect_img_links(url):
    '''Collects all img (src) links in img tags from a URL (jpg files only).'''
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, 'html5lib')

        # Collect all img tags.
        img_tags = soup.find_all('img')
        # If there are any img tags, then take the src (the link) of 
        # all the images (jpg files only) and return them. 
        # Otherwise, if no img tags exist, throw a RuntimeError.
        if img_tags:
            return [img.get('src') for img in img_tags 
                if (img.get('src').startswith('http') 
                    and img.get('src').endswith('jpg'))]
        else:
            raise RuntimeError('There are no images to scrape from the provided URL! Try a different URL.')
    except Exception as e:
        # No schema supplied, e.g. http/https infront of the URL, or if no images are found.
        if e.__class__ == requests.exceptions.MissingSchema or e.__class__ == RuntimeError:
            raise Exception(e)
        else:
            raise Exception('Either the URL is malformed or does not exist!')

def download_imgs(links, output_folder='images'):
    '''Downloads a list of images to the output folder.'''
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
    for link in tqdm(links):
        filename = os.path.join(output_folder, os.path.basename(link))
        download(link, filename)

def download(from_url, to_file):
    '''Downloads from URL to file.'''
    if not os.path.isfile(to_file):
        try:
            req.urlretrieve(from_url, to_file)
        except:
            pass
