#!/usr/bin/env python3
__author__ = "Huan Wang"
__version__ = "version 1.0"

from glob import glob
import numpy as np
import pandas as pd
import os, sys, time



fname = 'permutations.txt'
path = sys.argv[1]
kind = sys.argv[2]


def find_permu_dir(path):
    return glob(os.path.join(path, '*/'))


def read_data(fname):
    data = []
    with open(fname, 'r') as fo:
        for line in fo:
            info = line.strip().split()[2:]
            data.append(' '.join(info))
    return np.array(data)


def main(path, filename):
    ''' The main workflow. Finding all permutations.txt files in the 
    subdirectories and then read the permutations information one file
    by another. 
        In each permutations.txt file, collecting and counting the 
    unique permutations then save them in a .csv file.
    Note: need Numpy version 0.13.0 above!
    '''
    subdirs = find_permu_dir(path)
    #print(subdirs)

    totaldf = pd.DataFrame()
    df = pd.DataFrame()
    
    for i, subdir in enumerate(subdirs):
        start_time = time.time()
        
        protein = subdir.split(os.sep)[-2][4:8].upper()
        line_fmt = ''.join(("\n", "-" * 50, "\n", "No. {:}, file {:}"))
        print(line_fmt.format(i + 1, protein))

        fullname = os.path.join(subdir, fname)
        if os.path.isfile(fullname) and os.stat(fullname).st_size != 0:
            permuts = read_data(fullname)
        
            unique, counts = np.unique(permuts, axis=0, return_counts=True)
            #print('The unique permutations:{:}\nThe number of unique permutations:{:}\n'.format(unique, counts))

            dic = {}

            for key, value in zip(unique, counts):
                dic.setdefault(key, []).append(value)
            df = pd.DataFrame(dic)
            df["PDB_ID"] = protein
            print("Data Frame\n{:}".format(df))
        
            step_time = time.time() - start_time
            time_fmt = 'Time Consumed in Step {:<8}: {:.3f} seconds.\n'
            print(time_fmt.format(i + 1, step_time))
            
        else:
            df = pd.Series({"PDB_ID":protein})
            print("Data Frame\n{:}".format(df))
            
        totaldf = totaldf.append(df, ignore_index=True)
    return totaldf


if __name__ == "__main__":
    initial_time = time.time()
    table = main(path, fname)
    fmt = ''.join(('=' * 50, '\n', 'Final Table\n{:}'))
    print(fmt.format(table))
    output = ''.join((os.path.splitext(fname)[0], "_", kind, ".csv"))
    table.to_csv(output, sep=',')
    used_time = time.time() - initial_time
    print('\nWork Complete. Used Time: {:.3f} seconds'.format(used_time))
