## QV 2019-07-08

def landsat_thermal_rsr(satsens=['L8_TIRS', 'L5_TM', 'L7_ETM']):
    import tact
    
    rsr_data={}
    for satsen in satsens:
        if 'TIRS' in satsen:
            rsr_file = "{}/RSR/{}.txt".format(tact.config['data_dir'], satsen)
        else:
            rsr_file = "{}/RSR/{}_B6.txt".format(tact.config['data_dir'], satsen)

        r_, b_ = tact.rsr_read(rsr_file)
        rsr_data[satsen]={'rsr':r_, 'bands':b_}
    return(rsr_data)
