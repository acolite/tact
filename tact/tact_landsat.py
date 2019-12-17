## QV 2019-10-03
## updates 2019-12-10 fixed west coordinates
##         2019-12-17 renamed, and removed mpl dependency

def tact_landsat(bundle, output, limit=None, export_geotiff=False):
    import time
    import numpy as np
    from scipy import interpolate
    import tact

    ## get landsat metadata and determine date/time/extent
    metadata = tact.metadata_parse(bundle)
    if type(metadata) != dict:
        print('Bundle {} not recognised'.format(bundle))
        return(1)
    
    isodate = metadata["TIME"].strftime('%Y-%m-%d')
    c_time = metadata["TIME"].hour + metadata["TIME"].minute/60 + metadata["TIME"].second / 3600
    latrange = [metadata[k] for k in metadata if '_LAT_PRODUCT' in k]
    lonrange = [metadata[k] for k in metadata if '_LON_PRODUCT' in k]
    sc_limit = [min(latrange), min(lonrange), max(latrange), max(lonrange)]

    lat_border = []
    lon_border = []
    for c in ["UL", "UR", "LR", "LL", "UL"]:
        lat_border.append(metadata['CORNER_{}_{}_PRODUCT'.format(c, 'LAT')])
        lon_border.append(metadata['CORNER_{}_{}_PRODUCT'.format(c, 'LON')])

    ## get satellite sensor
    satsen = None
    if (metadata['SATELLITE'] == 'LANDSAT_5'): satsen = 'L5_TM'
    if (metadata['SATELLITE'] == 'LANDSAT_7'): satsen = 'L7_ETM'
    if (metadata['SATELLITE'] == 'LANDSAT_8') & ('TIRS' in metadata['SENSOR']): satsen = 'L8_TIRS'
    if satsen is None:
        print('Error with metadata: unknown satellite.')
        return(1)
    
    ## placeholder emissivity values (water)
    ## can be replaced by OLI derived em
    em = {'L8_TIRS':{'10': 0.9926494385655781, '11': 0.9877384047023862}, 
          'L5_TM':{'6': 0.9904561594813298}, 'L7_ETM':{'6': 0.9909058218284508}}
        
    ## kvalues are in metadata?
    kvalues = {'L8_TIRS':{'10':{'k1':774.8853, 'k2': 1321.0789}, '11':{'k1':480.8883, 'k2': 1201.1442}},
               'L5_TM':{'6': {'k1':607.76, 'k2': 1260.56}}, 'L7_ETM':{'6': {'k1':666.09, 'k2': 1282.71}}}
    
    ## get required parameters
    start = time.time()

    ## get ac parameters
    print('Retrieving a/c parameters')
    simst, lonc, latc = tact.tact_limit(isodate, sc_limit, c_time, verbosity=0, satsen=satsen, processes=4)
    for il, lon in enumerate(lonc):
        if lon > 180:
            lonc[il]-=360

    print('Getting a/c parameters took {:.1f} seconds'.format(time.time()-start))
        
    if limit is None:
        sub = None
        p, (xrange,yrange), proj4_string = tact.get_projection(metadata)
    else:
        scene_extent = tact.get_sub(metadata, limit)
        if type(scene_extent) is int: out_of_scene = True
        else: 
            sub, p, (xrange,yrange,grid_region), proj4_string = scene_extent
        if limit is None: sub=None

    attributes = {'sensor':satsen, 'isodate':metadata['ISODATE'], 
                  'THS':metadata['THS'],'THV':metadata['THV'], 'AZI':metadata['AZI']}

    ## track projection
    attributes['proj4_string'] = proj4_string
    attributes['xrange'] = xrange
    attributes['yrange'] = yrange
    attributes['pixel_size'] = (30,30)
    
    ##
    attributes['output_dir']=output
    attributes['output_base']=metadata['PRODUCT']

    ## get scene lat lon
    lon1, lat1 = tact.get_ll(metadata, limit=limit)

    ## create output file
    ncf = '{}/{}_ST.nc'.format(output, metadata['PRODUCT'])
    tact.nc_write(ncf, 'lat', lat1, new=True, attributes=attributes)
    tact.nc_write(ncf, 'lon', lon1)

    ## grid data
    x,y = np.meshgrid(lonc,latc)
    xr = list(x.ravel())
    yr = list(y.ravel())

    for band_name in metadata['BANDS_THERMAL']:
        band_data = {}

        ## read Lt
        band_data['Lt'] = tact.get_bt(bundle, metadata, band_name, sub=sub, return_radiance=True, etm_vcid=2)

        ## get emissivity
        band_data['em'] = em[satsen][band_name]

        ## k1 and k2
        band_data['k1'] = kvalues[satsen][band_name]['k1']
        band_data['k2'] = kvalues[satsen][band_name]['k2']

        ## interpolate simulation data
        for k in simst.keys():
            if band_name not in k: continue
            par = k.strip(band_name)
            band_data[par] = interpolate.griddata((xr,yr), list(simst[k].ravel()), 
                                                  (lon1, lat1), method='linear')

        ## compute surface radiance and temperature
        band_data['Ls'] = (((band_data['Lt']-band_data['Lu'])/band_data['tau'])-((1-band_data['em'])*band_data['Ld']))/band_data['em']
        band_data['WST'] = (band_data['k2']/np.log((band_data['k1']/band_data['Ls'])+1))-273.15

        ## write datasets to netcdf
        bdk = list(band_data.keys())
        for k in bdk:
            if type(band_data[k]) == float: continue
            if len(band_data[k].shape) != 2: continue
            print('Writing {} to {}'.format('{}{}'.format(k, band_name), ncf))
            tact.nc_write(ncf, '{}{}'.format(k, band_name), band_data[k])
            del band_data[k]
        del band_data
    del lon1, lat1

    ## output geotiff files
    if export_geotiff:
        tact.nc_to_geotiff(ncf, output=output)

    return(ncf)
