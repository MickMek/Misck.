from skyfield.api import load, EarthSatellite
from skyfield.timelib import Time
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pytz
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pdfkit
import os
import sys

cwd = os.getcwd()
#ENTER_NORAD_ID = 42063
ENTER_NORAD_ID = input("Enter NORAD ID: ")

my_url = f"https://www.n2yo.com/satellite/?s={ENTER_NORAD_ID}"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, 'html.parser')
page_soup = page_soup.findAll("div", {"id":"tle"})[0].text
page_soup2 = soup(page_html, 'html.parser')
sat_name = page_soup2.findAll("div", {"id":"satinfo"})[0].findAll("h1")[0].text
text = page_soup[3:143].replace("\r\n2"," \n2")

# Standard Gravitational parameter in km^3 / s^2 of Earth
GM = 398600.4418
pi = np.pi

def plot_orbital(axis, centers=None, hw=None):
    lims = ax.get_xlim(), ax.get_ylim(), ax.get_zlim()
    if centers == None:
        centers = [0.5*sum(pair) for pair in lims] 

    if hw == None:
        widths  = [pair[1] - pair[0] for pair in lims]
        hw      = 0.5*max(widths)
        ax.set_xlim(centers[0]-hw, centers[0]+hw)
        ax.set_ylim(centers[1]-hw, centers[1]+hw)
        ax.set_zlim(centers[2]-hw, centers[2]+hw)
        print("hw was None so set to:", hw)
    else:
        try:
            hwx, hwy, hwz = hw
            print("ok hw requested: ", hwx, hwy, hwz)

            ax.set_xlim(centers[0]-hwx, centers[0]+hwx)
            ax.set_ylim(centers[1]-hwy, centers[1]+hwy)
            ax.set_zlim(centers[2]-hwz, centers[2]+hwz)
        except:
            print("nope hw requested: ", hw)
            ax.set_xlim(centers[0]-hw, centers[0]+hw)
            ax.set_ylim(centers[1]-hw, centers[1]+hw)
            ax.set_zlim(centers[2]-hw, centers[2]+hw)

    return centers, hw

halfpi, pi, twopi = [f*np.pi for f in [0.5, 1, 2]]
degs, rads = 180/pi, pi/180
lines = text.strip().splitlines()
ts = load.timescale()
t = ts.now()
try:
    EarthSatellite(lines[0], lines[1])
except:
    print("TLE not found")
    sys.exit(1)

Roadster = EarthSatellite(lines[0], lines[1])
hours = np.arange(0, 3, 0.01)
time = ts.utc(2018, 2, 7, hours)
Rpos    = Roadster.at(time).position.km
re = 6378.
theta = np.linspace(0, twopi, 201)
cth, sth, zth = [f(theta) for f in [np.cos, np.sin, np.zeros_like]]
lon0 = re*np.vstack((cth, zth, sth))
lons = []
for phi in rads*np.arange(0, 180, 15):
    cph, sph = [f(phi) for f in [np.cos, np.sin]]
    lon = np.vstack((lon0[0]*cph - lon0[1]*sph,
                     lon0[1]*cph + lon0[0]*sph,
                     lon0[2]) )
    lons.append(lon)

lat0 = re*np.vstack((cth, sth, zth))
lats = []
for phi in rads*np.arange(-75, 90, 15):
    cph, sph = [f(phi) for f in [np.cos, np.sin]]
    lat = re*np.vstack((cth*cph, sth*cph, zth+sph))
    lats.append(lat)

if True:    
    fig = plt.figure(figsize=[10, 8])  # [12, 10]

    ax  = fig.add_subplot(1, 1, 1, projection='3d')

    x, y, z = Rpos
    ax.plot(x, y, z)
    for x, y, z in lons:
        ax.plot(x, y, z, '-k')
    for x, y, z in lats:
        ax.plot(x, y, z, '-k')

    centers, hw = plot_orbital(ax, )

    fig.savefig('img.png')   # save the figure to file
    plt.close(fig)
    

lines = text.strip().splitlines()
sat = EarthSatellite(lines[0], lines[1])
line1 = lines[0]
line2 = lines[1]

satellite_number = int(line1[2:7])
classification = line1[7:8]
international_designator_year = int(line1[9:11])
international_designator_launch_number = int(line1[11:14])
international_designator_piece_of_launch = line1[14:17]
epoch_year = int(line1[18:20])
epoch = float(line1[20:32])
first_time_derivative_of_the_mean_motion_divided_by_two = float(line1[33:43])
second_time_derivative_of_mean_motion_divided_by_six = (line1[44:52])
bstar_drag_term = (line1[53:61])
the_number_0 = float(line1[62:63])
element_number = float(line1[64:68])
checksum1 = float(line1[68:69])

satellite = int(line2[2:7])
inclination = float(line2[8:16])
right_ascension = float(line2[17:25])
eccentricity = float(line2[26:33]) * 0.0000001
argument_perigee = float(line2[34:42])
mean_anomaly = float(line2[43:51])
mean_motion = float(line2[52:63])
revolution = float(line2[63:68])
checksum2 = float(line2[68:69])

# Inferred Epoch date
year = 2000 + epoch_year if epoch_year < 70 else 1900 + epoch_year
epoch_date = datetime(year=year, month=1, day=1, tzinfo=pytz.utc) + timedelta(days=epoch-1) # Have to subtract one day to get correct midnight

# Time difference of now from epoch, offset in radians
diff = datetime.now().replace(tzinfo=pytz.utc) + timedelta(hours=8) - epoch_date # Offset for PDT
diff_seconds = 24*60*60*diff.days + diff.seconds + 1e-6*diff.microseconds # sec
motion_per_sec = mean_motion * 2*pi / (24*60*60) # rad/sec
offset = diff_seconds * motion_per_sec #rad
mean_anomaly += offset * 180/pi % 360
epoch_date = epoch_date.strftime("%Y-%m-%d %H:%M:%S.%f %Z")

# Inferred period
day_seconds = 24*60*60
period = day_seconds * 1./mean_motion

# Inferred semi-major axis (in km)
semi_major_axis = ((period/(2*pi))**2 * GM)**(1./3)

# Other Calculations
lines = text.strip().splitlines()
#data = load('de421.bsp')
#earth   = data['earth']
ts = load.timescale()
t = ts.now()
sat = EarthSatellite(lines[0], lines[1])
days = t - sat.epoch
geocentric = sat.at(t)
subpoint = geocentric.subpoint()


html= f'''
<body>
<pre>
----------------------------------------------------------------------------------------
<h3 align="center"><B>Satellite Name: {sat_name}</B></h3>
----------------------------------------------------------------------------------------
TLE:
{line1}
{line2}
----------------------------------------------------------------------------------------
Satellite number                                          = {satellite_number}
International Designator                                  = YR: {international_designator_year}, LAUNCH #{international_designator_launch_number}, PIECE: {international_designator_piece_of_launch}
Epoch Date                                                = {epoch_date}
                                                            YR:{epoch_year} 
                                                            DAY:{epoch}
First Time Derivative of the Mean Motion divided by two   = {first_time_derivative_of_the_mean_motion_divided_by_two}
Second Time Derivative of Mean Motion divided by six      = {second_time_derivative_of_mean_motion_divided_by_six}
BSTAR drag term                                           = {bstar_drag_term}
The number 0                                              = {the_number_0}
Element number                                            = {element_number}

Inclination [Degrees]                                     = {inclination}
Right Ascension of the Ascending Node [Degrees]           = {right_ascension}
Eccentricity                                              = {eccentricity}
Argument of Perigee [Degrees]                             = {argument_perigee}
Mean Motion [Revs per day] Motion                         = {mean_motion}
Period                                                    = {timedelta(seconds=period)}
Revolution number at epoch [Revs]                         = {revolution}

semi_major_axis = {semi_major_axis}
eccentricity    = {eccentricity}
inclination     = {inclination}
arg_perigee     = {argument_perigee}
right_ascension = {right_ascension}
----------------------------------------------------------------------------------------
Time offset: {diff}
Radians per second: {motion_per_sec}
Offset to apply: {offset}
----------------------------------------------------------------------------------------
{sat}
{days} days away from epoch
Geocentric Position (km): {geocentric.position.km}
Latitude: {subpoint.latitude}
Longitude: {subpoint.longitude}
Elevation (m): {int(subpoint.elevation.m)}
----------------------------------------------------------------------------------------
Plotting
{Roadster.epoch.tt}
{Rpos.shape}
centers are: {centers}
hw is:       {hw}
<img src="{cwd}/img.png" alt="Trajectory" height="500" width="500" align="center">
----------------------------------------------------------------------------------------
</pre>
</body>

'''

pdfkit.from_string(html, f'sat_{satellite_number}.pdf')
os.remove(f"{cwd}/img.png")
