import argparse
import os
import sys
import time
from threading import Thread

import lib.categorize_image as categorizer
import lib.scrape_images as scraper
import lib.training as trainer
import server.server as server

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            description=
            '''
            This program scrapes images from a given URL, and categorizes 
            each image under the following categories: forest, urban, water or others.
            It uses a perceptron to recognize the colors in an image.
            
            Running `$ python main.py` will launch a local Flask server with random images that will be scraped.
            Otherwise, use -u or --url argument to scrape images from an URL. 
            Note: Not all sites can be scraped, make sure that the images are not embedded.
            
            This comes with pre-built weights for all three categories with a training rate of 0.2 with 4000 iterations.
            This means that the perceptron is already "trained" to analyze and categorize the images.
            This is to make the program work out of the box as to avoid any time-consuming tasks of training the perceptron.
            Simply, run the program and see the categorized images under the "categorized" folder.
            If you would like to train the perceptron with your own defined values, run the script with the 
            argument -t or --trainer with two defined values: iteration and training rate, respectively.
            Example: `$ python main.py -t 10000 0.3`
            '''
        )

        parser.add_argument('-u', '--url', 
            metavar='<url>', 
            help='URL to scrape images from', 
        )
        parser.add_argument('-t', '--trainer', 
            nargs=2,
            type=float,
            metavar=('<iterations (min. 1000)>', '<training rate (0.001-0.9)>'),
            help='Initiate trainer with given values of iterations and training rate'
        )
        
        args = parser.parse_args()

        if args.trainer:
            iterations, training_rate = args.trainer

            if (iterations < 1000):
                raise ValueError('The iteration value must be higher than 1000')
            if (training_rate < 0.001 or training_rate > 0.9):
                raise ValueError('The training rate value must be between 0.001 and 0.9')
            
            print('\nInitiating the trainer...')
            trainer.find_weights(int(iterations), training_rate)
            print('Trainer finished!')

        if args.url:
            url = args.url
            print(f'\nAttempting to scrape from the URL: {url} ...')
            # scraper.scrape('https://wallpaperlayer.com/silhouette-wallpaper-1109.html') # TO BE DELETED.
            scraper.scrape(url)
            print('Scraping finished successfully!')
        else:
            print(f'\nInitiating local Flask server...\n')
            thread = Thread(target = server.run)
            thread.setDaemon(True)
            thread.start()
            
            time.sleep(1)

            print('\nScraping from the local Flask server...')
            scraper.scrape('http://127.0.0.1:5000/')
            print('Scraping finished successfully!')

        print('\nInitiating the categorization process...')
        image_list = os.listdir('./images')
        categorizer.categorize_image(image_list)
        print('Categorization finished successfully!')

        print('\nTo see the result of the categorized images, open the "categorized" folder.')  
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        print('\nShutting down...')
