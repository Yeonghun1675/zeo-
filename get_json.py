import sys
import re
from tqdm import tqdm
from pathlib import Path
import json


###############################################
DATA_DIR = '/home/users/dudgns1675/zeo++/ver3_result'
OUTPUT_JSON = '/home/users/dudgns1675/zeo++/total_PV.json'
PROPERTY = 'vol'

##############################################

def get_property(data):
    global PROPERTY
    if PROPERTY == 'vol': # Return accessible volume
        prop = re.search(r"AV_A\^3: (?P<num>[.0-9-]+)", data)
    else:
        raise NotImplementError()
    
    return float(prop.group('num'))


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
        except Exception as e:
            #print (e)
            #print (datafile.name)
            #print (data)
            continue
            #sys.exit(0)

        output[datafile.stem] = prop
        
    return output


if __name__ == '__main__':
    output = main()
    with open('OUTPUT_JSON', 'w') as f:
        json.dump(output, f)
    print (len(output))
