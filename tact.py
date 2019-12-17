## QV 2019-12-17 runs Thermal Atmospheric Correction Tool for Landsat 
##
## last modification

def run_tact():
    ## import sys to parse arguments
    import sys

    ## for evaluation of bool strings
    import distutils.core

    import tact

    ## ignore numpy errors
    import numpy as np
    olderr = np.seterr(all='ignore') 

    import argparse
    parser = argparse.ArgumentParser(description='TACT')
    parser.add_argument('--input', help='Main L1 input bundle')
    parser.add_argument('--output', help='Output directory')
    parser.add_argument('--limit', help='Limits for processing, comma separated decimal degrees S,W,N,E (default=None)', default=None)
    parser.add_argument('--export_geotiff', help='Export geotiff data (default=False)', default=False)
    args, unknown = parser.parse_known_args()

    if args.input is None:
        print('No input file given.')
        return(1)

    if args.output is None:
        print('No output directory given.')
        return(1)

    if args.limit is not None:
        limit = [float(s) for s in args.limit.split(',')]
        if len(limit) != 4: args.limit=None
        else: args.limit = limit


    ## run the processing
    tact.tact_landsat(args.input, output=args.output, limit=args.limit, export_geotiff=args.export_geotiff)

if __name__ == '__main__':
    print('Launching TACT processing.')
    run_tact()
