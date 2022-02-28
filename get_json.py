import sys
import re
from tqdm import tqdm
from pathlib import Path
import json


###############################################
DATA_DIR = '/home/users/dudgns1675/zeo++/omit_result'

PROPERTY = 'vol'
OUTPUT_JSON = f'/home/users/dudgns1675/zeo++/omit_{PROPERTY}.json'
##############################################

def get_property(data):
    global PROPERTY
    if PROPERTY == 'vol': # Return accessible volume fraction
        #prop = re.search(r"AV_A\^3: (?P<num>[.0-9-]+)", data)
        prop = re.search(r"AV_Volume_fraction: (?P<num>-?[.0-9]+)", data)
        return float(prop.group('num'))

    elif PROPERTY == 'sa':
        prop = re.search(r"ASA_m\^2/cm\^3: (?P<num>-?[.0-9]+)", data)
        return float(prop.group('num'))
    
    elif PROPERTY == 'res':
        #print (data)
        #print (data.split())
        prop = data.split()
        return prop[1:]

    else:
        raise NotImplementError()
    
    

def main():
    global DATA_DIR, PROPERTY

    datadir = Path(DATA_DIR)
    assert datadir.exists()

    output = {}
    for datafile in tqdm(list(datadir.glob(f'*.{PROPERTY}'))):
        with open(datafile) as f:
            data = f.read()
        try:
            prop = get_property(data)
            #print ('data', prop)
        except AttributeError:
            #print (e)
            #print (datafile.name)
            #print (data)
            continue
            #sys.exit(0)

        output[datafile.stem] = prop
        
    return output


if __name__ == '__main__':
    output = main()
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output, f)
    print (len(output))
