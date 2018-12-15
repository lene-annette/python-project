import lib.scrape_images as scraper
import lib.categorize_image as categorizer
import lib.training as trainer
import server.server as server
import argparse
from threading import Thread
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='URL to scrape images from', default='localhost')
    args = parser.parse_args()

    url = args.url
    if (url is 'localhost'):
        thread = Thread(target = server.run)
        thread.setDaemon(True)
        thread.start()
        scraper.scrape('http://127.0.0.1:5000/')
    else:
        scraper.scrape('https://wallpaperlayer.com/silhouette-wallpaper-1109.html')

    trainer.find_weights(4000, 0.2)
    imageList = os.listdir('./images')
    categorizer.categorize_image(imageList) 
    