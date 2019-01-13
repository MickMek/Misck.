# ProjectArt
Computational framework and machine learning algorithms applied to Art

This repository includes codes used to conduct research on fine prints art valuation and artistic style recognition of paintings. You can find the full report in `report.pdf`

`scraper.py` is a script that allows to obtain the latest data on auction houses sales. Make sure to add your username/password, and change the link/number of pages if you which to scrap from another page in the site.

`art_cleaning.ipynb` is a jupyter notebook that preprocesses the data obtain from the scraping. It transforms raw unstructured data into a more structured form (table).

`artdata_xgboost` is a jupyter notebook that performs the gradient descent algorithm on the dataset to predict future auction sales prices.

`data_processing.ipynb` renames all files in a folder, and outputs a csv file with the inventory of desired folders. This is really helpful when it comes to organising your dataset (did not include the dataset as it was a very large file)

`artCNN.ipynb` is the code used to train the CNN to recognize artistic style from a painting's image. The trained model is save under `model.h5` and can be loaded directly into python.
