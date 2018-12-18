import argparse
import os
import shutil
import sys
import time
from threading import Thread

import lib.categorize_image as categorizer
import lib.scrape_images as scraper
import lib.training as trainer
import server.server as server

if __name__ == '__main__':

    try:
        # Using the argparse library to create arguments for the program.
        parser = argparse.ArgumentParser(
            # Maintain whitespace for all sorts of help text, including the description.
            formatter_class=argparse.RawTextHelpFormatter,
            description=
            '''
            This program uses perceptrons to analyze the colors in an image in order to 
            determine which of the following categories the image belongs to: 
            forest, urban or water. If a match is not found within one of these categories, 
            the image will be considered as others. The program scrapes images from a given URL, and then 
            categorizes each image under one of the above categories.
            
            Running `$ python main.py` will launch a local Flask server with random images that will be scraped.
            Otherwise, use the -u or --url argument to scrape images from a URL. 
            Note: Not all sites can be scraped; make sure that the images are not embedded.
            
            From out-of-the-box, it comes with perceptrons that have already been trained 
            using a precomputed weight module with a training rate of 0.01 over 1.000.000 iterations. 
            This is to avoid the time-consuming tasks of training the perceptrons. 
            Instead of training the perceptrons every time the program is executed, the perceptrons 
            simply uses the weights from this module in order to categorize scraped images. 

            If you would like to train the perceptrons with your own defined values, run the program with the 
            argument -t or --trainer with two defined values: iteration and training rate, respectively.
            Example: `$ python main.py -t 10000 0.3`

            Run the program and see the categorized images under the "categorized" folder
            after the program finishes and shuts down.
            '''
        )

        parser.add_argument('-u', '--url', 
            metavar='<url>', 
            help='a URL to scrape images from', 
        )
        parser.add_argument('-t', '--trainer', 
            # Add two parameters for this argument, converting them to float.
            nargs=2,
            type=float,
            metavar=('<iterations (min. 1000)>', '<training rate (0.001-0.9)>'),
            help='initiate trainer with given values of iterations and training rate'
        )
        
        args = parser.parse_args()

        # Clean up (before program start). ignore_errors=True = Delete read-only files as well.
        shutil.rmtree('categorized', ignore_errors=True)
        shutil.rmtree('images', ignore_errors=True)

        # If the trainer argument has been used.
        if args.trainer:
            iterations, training_rate = args.trainer

            if (iterations < 1000):
                raise ValueError('The iteration value must be higher than 1000')
            if (training_rate < 0.001 or training_rate > 0.9):
                raise ValueError('The training rate value must be between 0.001 and 0.9')
            
            print('\nInitiating the trainer with the following settings...')
            print(f'Iterations: {int(iterations)}')
            print(f'Learning rate: {training_rate}')
            # Compute weights for each category to train the perceptrons.
            trainer.compute_weights(int(iterations), training_rate)
            print('Trainer finished!')

        if args.url:
            url = args.url
            print(f'\nAttempting to scrape from the URL: {url} ...')
            # Scrape from the given URL.
            scraper.scrape(url)
            print('Scraping finished successfully!')
        else:
            print(f'\nInitiating local Flask server...\n')
            # Start the Flask server in a separate thread.
            thread = Thread(target = server.run)
            # Allows the main thread to run while the Flask server is up.
            # It will be correctly killed when the program shuts down.
            thread.setDaemon(True)
            thread.start()
            
            time.sleep(1)

            print('\nScraping from the local Flask server...')
            # Scrape from localhost.
            scraper.scrape('http://127.0.0.1:5000/')
            print('Scraping finished successfully!')

        print('\nInitiating the categorization process...')
        image_list = os.listdir('images')
        # Categorize the downloaded images.
        categorizer.categorize_image(image_list)
        print('Categorization finished successfully!')

        # Clean up (when program finishes). Only delete the "images" folder.
        shutil.rmtree('images', ignore_errors=True) # Delete read-only files as well.

        print('\nTo see the result of the categorized images, open the "categorized" folder.')  
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        print('\nShutting down...')
