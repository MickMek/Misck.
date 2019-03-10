## SpacyPy - Satellite TLE Analysis

`spacy.py` scraps satellite information from the web, and formats all information into a comprehensive pdf report file.

Open terminal and go to the directory, then enter
`python spacy.py`

Make sure all requirements are installed.

### Requirement
```
skyfield
datetime
pytz
bs4
urlopen
pdfkit
numpy
matplotlib
```

### How to read the report

Semimajor axis (𝑎)
Eccentricity (𝑒)
Inclination (𝑖)
Right ascension of the ascending node (Ω)
Argument of pericenter (𝜔)
True anomaly (𝜈)
...

=================================================================
## Satellite RNN Analysis

`rnn_scraper.py` scraps data from n2yo.com, and formats the scrapped data into a clean dataset for Recurrent Neural Network analysis. Our aim is to be able to predict several parameters of live temporal satellite data with a trained neural network.

`rnn_satanalysis` is the preliminary RNN analysis conducted for LONGITUDE. The model is still being optimized. `rnn_data.csv` is a sample scrapped csv file using our scrapper.
