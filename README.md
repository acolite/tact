## About TACT
TACT is the Thermal Atmospheric Correction Tool for Landsat developed at RBINS. It retrieves ERA5 atmospheric profiles and uses libRadtran to compute the atmospheric transmittance, and down- and upwelling radiances. Currently TACT outputs the Water Surface Temperature (WST) in each thermal band present on the Landsat sensor, assuming a constant (water) emissivity over the scene. The method and validation using Landsat 8/TIRS data is presented in Vanhellemont, 2020 (https://doi.org/10.1016/j.rse.2019.111518).

**This repository will probably no longer be maintained, please check out TACT integration in the generic ACOLITE: https://github.com/acolite/acolite**

TACT development was funded by the Belgian Science Policy Office BRAIN-be program under contract BR/165/A1/MICROBIAN.

**TACT is provided by RBINS as an experimental tool, without explicit or implied warranty. Use of the program is at your own discretion and risk.**

## Dependencies
TACT is coded in Python 3, and requires the following Python packages to run with all functionality:`numpy scipy pyproj gdal netcdf4 python-dateutil`

TACT needs libRadtran to be installed: http://libradtran.org/doku.php

TACT needs the user to have an account at the Research Data Archive (RDA) at the University Corporation for Atmospheric Research (UCAR): https://rda.ucar.edu/

## Installation & Configuration
* cd into a suitable directory and clone the git repository: `git clone https://github.com/acolite/tact`
* cd into the new tact directory `cd tact`
* Edit the tact configuration file `nano config/config.txt` and add the full path to the libRadtran directory on your system to the libradtran_dir= setting
* Edit your .netrc file to add your RDA UCAR credentials: `nano $HOME/.netrc`, with $l and $p your login and password respectively for the RDA:

            machine rda.ucar.edu
            login $l
            password $l

* Edit your .dodsrc file to point to your .netrc file: `nano $HOME/.dodsrc`. Write the full path explicitly:
            HTTP.NETRC=/path/to/.netrc

* run `python tact.py --input $in --output $out` where $in is the full path to an extracted L1 Landsat bundle, and $out the full path to the target output directory (which will be generated).

## Options
* --limit a four coordinate bounding box (S,W,N,E) for processing of a specific region of interest
* --export_geotiff True/False for exporting datasets as GeoTIFF
