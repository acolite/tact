## def nc_to_geotiff
## writes exports datasets from ACOLITE NetCDF to GeoTIFF
## written by Quinten Vanhellemont, RBINS for the PONDER project
## 2018-06-06
## modifications:  QV 2018-06-07 fixed S2 offset bug
##                2018-07-18 (QV) changed acolite import name
##                2018-12-17 (QV) added other output option
##                2019-12-17 (QV) integrated in tact

def nc_to_geotiff(f, datasets=None, skip_geo=True, output=None):
    import tact
    import os
    
    gatts = tact.nc_gatts(f)
    if datasets is None:
        datasets = tact.nc_datasets(f)
    tags = ['xrange', 'yrange', 'pixel_size', 'proj4_string']
    tags += ['output_dir', 'output_base', 'sensor']

    if all([t in gatts for t in tags]):
        import osgeo.osr, gdal

        xrange = gatts['xrange']
        yrange = gatts['yrange']

        pixel_size = gatts['pixel_size']

        ## make WKT
        srs = osgeo.osr.SpatialReference()
        srs.ImportFromProj4(gatts['proj4_string'])
        wkt = srs.ExportToWkt()

        ## make geotransform
        if gatts['sensor'][0] == 'L':
            trans = (xrange[0]-int(pixel_size[0]/2), pixel_size[0], 0.0, \
                     yrange[1]+int(pixel_size[1]/2), 0.0, -1*pixel_size[1])
        else:
            if yrange[1]-yrange[0] < 0: ## full scene S2
                trans = (xrange[0], pixel_size[0], 0.0, \
                         yrange[0], 0.0, -1*pixel_size[1])
            else: ## cropped
                trans = (xrange[0], pixel_size[0], 0.0, \
                         yrange[1], 0.0, -1*pixel_size[1])

        for ds in datasets:
            if (skip_geo) & (ds in ['lat', 'lon', 'x', 'y']): continue
            
            data = tact.nc_data(f, ds)
            y,x = data.shape

            driver = gdal.GetDriverByName('GTiff')
            if output is None:
                odir=gatts['output_base']
            else:
                odir='{}/{}'.format(output, os.path.basename(gatts['output_base']))

            outfile = '{}_{}{}'.format(odir, ds, '.tif')
            dataset = driver.Create(outfile,x,y,1,gdal.GDT_Float32)

            dataset.SetGeoTransform(trans)  
            dataset.SetProjection(wkt)
            dataset.GetRasterBand(1).WriteArray(data)
            dataset.FlushCache()
            print('Wrote {}'.format(outfile))
    else:
        print('File {} not  recognised. Not outputting GeoTIFF files.'.format(f))
