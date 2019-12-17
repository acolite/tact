from .tact_landsat import tact_landsat
from .tact_limit import tact_limit 

from .bundle_test import bundle_test
from .metadata_read import metadata_read
from .metadata_parse import metadata_parse
from .get_projection import get_projection
from .get_sub import get_sub
from .get_ll import get_ll
from .import_config import import_config

from .read_band import read_band
from .get_bt import get_bt
from .nc_write import nc_write
from .nc_read import *
from .nc_to_geotiff import *

from .landsat_thermal_rsr import landsat_thermal_rsr
from .rsr_read import rsr_read
from .rsr_convolute_dict import rsr_convolute_dict
from .lutpos import lutpos

from .run_thermal_sim import run_thermal_sim
from .cfg_create import cfg_create
from .libradtran_run_file import libradtran_run_file
from .read_out import read_out
from .read_sim import read_sim

##
import os
path = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists('{}{}config'.format(path, os.path.sep)):
    path = os.path.split(path)[0]

cfile='{}{}config{}config.txt'.format(path,os.path.sep,os.path.sep)
config = import_config(cfile)

## test whether we can find the relative paths
for t in config:
    if os.path.exists(config[t]): continue
    tmp = path + os.path.sep + config[t]
    config[t] = os.path.abspath(tmp)

