'''Library to access CSV (comma separated values) files.'''

__last_change__ = '2017.08.28.'

import csv
import logging
import sys

def reader(filename):
    '''Reads a list of lists data from a CSV file.

    The first line must be a header.

    Args:
        filename: the path (full, or relative) to the file to be written.
    Returns: 
        An OrderedDict.'''

    content = []
    
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        content.extend(line for line in reader)

    return(content)

def writer(content, filename, has_header=True):
    '''Saves a list of lists data into a CSV file.

    The first line can be a header.

    Args:
        content: a list of lists containing the data to be written.
        filename: the path (full, or relative) to the file to be written.
        has_header: optional parameter, defaults to True.
    Returns: 
        TODO: True: if everythings OK.
        TODO: False: if any of the files is missing.'''

    if content is None:
        raise ValueError("No content passed.")
    if filename is None:
        raise ValueError("No file name/path passed.")
    if len(content) == 0 or (len(content) == 1 and has_header):
        raise ValueError("Empty list passed.")
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ';')
        if has_header:
            csvwriter.writerow(content.pop(0))
        csvwriter.writerows([field for field in content])
        
        logging.info(''.join(['Number of lines written in CSV (with header if exists): ',
                              str(len(content))]))

def main():
    '''Entry point for testing purposes only'''
    
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Running modul in debugging mode.')

if __name__ == '__main__':
    sys.exit(main())
