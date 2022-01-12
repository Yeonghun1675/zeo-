import subprocess
from pathlib import Path
from tqdm import tqdm


NUM_QSUB = 160 # Number of QSUB file
NUM_CORE = 1 # Number of core
CORE = 'aa'  # Core property
PROPERTIES = ['vol', 'sa'] # res : pore diameter, sa : surface area, vol: pore volume
extent = 'cif'

cssr_path = Path('/home/users/dudgns1675/pormake/primitive_cif')
save_path = Path('/home/users/dudgns1675/zeo++/ver3_primitive_result')
qsub_path = Path('/home/users/dudgns1675/zeo++/qsub/')

# ZEO++ network file
zeo_path = Path('/home/users/dudgns1675/zeo++/zeo++-0.2.2/network')


#######################################################################

assert cssr_path.exists() # cssr_path must be existed

if not save_path.exists(): # Make SAVE_PATH if not exists
    save_path.mkdir(parents=True)
if not qsub_path.exists(): # Make QSUB_PATH if not exists
    qsub_path.mkdir(parents=True)


def get_cssr_list(prop):
    global NUM_QSUB

    cssr_list = []
    for cssr in cssr_path.glob(f'*.{extent}'):
        name = cssr.stem
        prop_name = save_path/f'{name}.{prop}'
        if not prop_name.exists():
            cssr_list.append(cssr)

    interval = len(cssr_list) // NUM_QSUB

    return cssr_list, interval


def zeo_command(cssr, prop):
    global cssr_path, save_path, zeo_path
    save_file = save_path/f'{cssr.stem}.{prop}'
    if prop == 'sa':
        return f'{str(zeo_path)} -ha -sa 1.2 1.2 2000 {str(save_file)} {str(cssr)}\n'
    elif prop == 'res':
        return f'{str(zeo_path)} -ha -res {str(save_file)} {str(cssr)}\n'
    elif prop == 'vol':
        return f'{str(zeo_path)} -ha -vol 1.2 1.2 5000 {str(save_file)} {str(cssr)}\n'
    else:
        raise ValueError(prop)



def write_qsub(cssr_part, index, interval, prop):
    global qsub_path, NUM_CORE, CORE
    qsub_file = qsub_path/f"{prop}-{index}.qsub"

    with open(str(qsub_file), 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#PBS -r n\n')
        f.write('#PBS -q long\n')
        f.write(f'#PBS -l nodes=1:ppn={NUM_CORE}:{CORE}\n')
        f.write('\n')
        f.write('cd $PBS_O_WORKDIR\n')
        for cssr in cssr_part:
            f.write(zeo_command(cssr, prop))


def main():
    global PROPERTIES, NUM_QSUB

    for prop in PROPERTIES:
        print ('start : ', prop)
        cssr_list, interval = get_cssr_list(prop)

        for i in tqdm(range(NUM_QSUB), desc=prop):
            cssr_part = cssr_list[interval*i:interval*(i+1)]
            write_qsub(cssr_part, i, interval, prop)


if __name__ == '__main__':
    main()
