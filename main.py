import lib.scrape_images as scraper
import lib.convert_image as converter


if __name__ == '__main__':
    # scraper.scrape('https://commons.wikimedia.org/wiki/Main_Page')
    # imagelist = scraper.scrape('https://burst.shopify.com/nature')
    # imagelist = scraper.scrape('https://wallpaperlayer.com/silhouette-wallpaper-1109.html')
    imagelist = scraper.scrape('https://www.elementaryos-fr.org/wallpapers/?fbclid=IwAR2gbufht5Vvv1qwT102YScAjQ2OZtepVC9hA8wKS0F7DSU65zaNNN0qzFM')


 
    converter.convert_image(imagelist)
