import os
import sys
import subprocess
from time import time


def main():
    argvs = sys.argv
    if len(argvs) != 6:
        raise AttributeError('Example: convert_kfb2svs.py [converter_path] [src_path] [dest_path] [format_name (str)] [level (int)]')
    
    _, exe_path, src_path, dest_path, format_name, level = tuple(argvs)

    if not os.path.exists(exe_path):
        raise FileNotFoundError('Could not find converter exe file.')
    if format_name != 'tif' and format_name != 'svs':
        raise AttributeError('NOTE: format_name is either tif or svs')
    if int(level) < 2 or int(level) > 9:
        raise AttributeError('NOTE: 2 < [level] <= 9')
    if not os.path.exists(src_path):
        raise FileNotFoundError(f'could not get into dir {src_path}')
    if not os.path.exists(dest_path):
        print('NOTE: Directory for export doesnt exist. Create a new one instead.')
        os.makedirs(dest_path)

    kfb_list = os.listdir(src_path)
    kfb_list_nfile = len(kfb_list)
    kfb_list = [elem for elem in kfb_list if elem.endswith('kfb')]
    if len(kfb_list) < kfb_list_nfile:
        print('NOTE: Non-kfb files found in the source directory. Please check the suffix')

    print(f'Found {len(kfb_list)} slides, transfering to svs format ...')
    for elem in kfb_list:
        st = time()
        if ' ' in elem:
            print('NOTE: Found blankspace in filename, rename it by -')
            newname = elem.replace(' ','-')
            os.rename(os.path.join(src_path, elem), os.path.join(src_path, newname))
            kfb_elem_path = os.path.join(src_path, newname)
            elem = newname
        else:
            kfb_elem_path = os.path.join(src_path, elem)
        
        if format_name == 'svs':
            svs_dest_path = os.path.join(dest_path, elem.replace('.kfb', '.svs'))
        else:
            svs_dest_path = os.path.join(dest_path, elem.replace('.kfb', '.tif'))
        command = f'{exe_path} {kfb_elem_path} {svs_dest_path} {level}'
        print(f'Processing {elem} ...')
        p = subprocess.Popen(command)
        p.wait()
        print(f'\nFinished {elem}, time: {time() - st}s ...')
    

if __name__ == "__main__":
    main()