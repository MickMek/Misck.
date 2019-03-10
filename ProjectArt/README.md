# ProjectArt
Computational frameworks and machine learning algorithms applied to Art.

This repository contains codes used to conduct research on fine prints art valuation and artistic style recognition of paintings. You can find the full report in `report.pdf`

### 1. Auction Sales analysis
`scraper.py` is a script that obtains the latest data on auction houses sales. Make sure to add your username/password, and change the link/number of pages if you wish to scrap from other pages on the website.

`art_cleaning.ipynb` is a jupyter notebook that preprocesses the data obtain from the scraping scrypt. It transforms raw unstructured data into a more structured form (tables).

`artdata_xgboost` is a jupyter notebook that performs the gradient descent algorithm on the cleaned auctions sales dataset to predict future auction sales prices.

### 2. Paintings' Artistic Style Recognition
`data_processing.ipynb` renames all files in a folder, and outputs a csv file with the inventory of desired folders. This is helpful in organising your own datasets (the dataset is too large to be included here).

`artCNN.ipynb` is a jupyter notbook used to train the CNN to recognize artistic style from a painting's image. The trained model is save under `my_model.h5` and can be loaded directly into Python.
