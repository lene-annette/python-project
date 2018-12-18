# Python Project: Image Analyzer & Categorizer using a Perceptron
This program uses a perceptron to analyze the colors in an image in order to determine which of the following categories the image belongs to: `forest`, `urban`, `water` and `others`. The program scrapes images from a given URL, and then categorizes each image under one of the above categories. To run the perceptron, see the [Usage](#usage) section below.

From out-of-the-box, it comes with a perceptron that is already trained using a precomputed module. This is to avoid any time-consuming tasks of training the perceptron. Instead of training the perceptron every time the program is run, the perceptron simply uses this module to categorize scraped images. To train the perceptron, see the [Usage](#usage) section below.

The output and results of the program are the categorized images, which can be found in a created ```categorized``` folder after the program finishes and shuts down.

## Dependencies
* Python - Anaconda Distribution  
  To make sure that all libraries are present for an error-free execution of the program, we recommend using the Anaconda distribution of Python. The program is also likely to run with other distributions, but certain libraries might need to be downloaded and installed.

## Usage
For minimalistic and quick usage, simply run:
```
$ python main.py
```
This will launch a local [Flask](http://flask.pocoo.org/) server with random images that will be scraped and categorized.

You can also scrape from a given URL:
```
$ python main.py -u <url>
```
**Note**: Not all sites can be scraped; make sure that the images are not embedded.

This project comes with a precomputed `weights.py` module (in the `modules` folder) that has been run with over **X** iterations using a training rate of **X**. This means that you do not need to train the perceptron. It has already been trained using the images in the `training_images` folder. However, if you wish to train the perceptron yourself, simply run:
```
$ python main.py -t <iterations> <training rate>
```
**Note**: The trainer takes two arguments. The higher the iteration value, the longer the computation process will take.

### Example
```
python main.py -u https://wallpaperlayer.com/silhouette-wallpaper-1109.html -t 10000 0.3
```

### Optional arguments
* `-h, --help`    -  show the help message and exit
* `-u, --url`     -  url to scrape images from
* `-t, --trainer` -  initiate trainer to compute weights with given values of iterations (min. 1000) and training rate (between 0.001-0.9)

## Output and Results
The output and results of the program are the categorized images, which can be found in a created ```categorized``` folder after the program finishes and shuts down.

## Authors
* **Devran Coskun** – *cph-dc63@cphbusiness.dk* – [GitHub: cph-dc](https://github.com/cph-dc)
* **Gert Philip Lehmann Madsen** – *cph-gm50@cphbusiness.dk* – [GitHub: GertMadsen](http://github.com/GertMadsen)
* **Lene Annette Skov** – *cph-ls283@cphbusiness.dk* – [GitHub: lene-annette](https://github.com/lene-annette)
* **Mikkel Lindstøm Hansen** – *cph-mh643@cphbusiness.dk* – [GitHub: MikkelHansen95](https://github.com/MikkelHansen95)
