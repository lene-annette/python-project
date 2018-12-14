import lib.scrape_images as scraper
import lib.categorize_image as categorizer
import lib.training as trainer
import server.server as server
import argparse
from threading import Thread


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='URL to scrape images from', default='localhost')
    args = parser.parse_args()

    url = args.url
    if (url is 'localhost'):
        thread = Thread(target = server.run)
        thread.setDaemon(True)
        thread.start()
        image_list = scraper.scrape('http://127.0.0.1:5000/')
    else:
        # image_list = scraper.scrape('https://commons.wikimedia.org/wiki/Main_Page')
        # image_list = scraper.scrape('https://burst.shopify.com/nature')
        image_list = scraper.scrape('https://wallpaperlayer.com/silhouette-wallpaper-1109.html')
        # image_list = scraper.scrape('https://www.elementaryos-fr.org/wallpapers/?fbclid=IwAR2gbufht5Vvv1qwT102YScAjQ2OZtepVC9hA8wKS0F7DSU65zaNNN0qzFM')

        # image_list = scraper.scrape(url)  

    trainer.find_weights(1000)
    categorizer.convert_image(image_list) 
    