'''
Library to fetch the stock exchange closing prices and volume
from tdcfinancial on a given day, sorted alphabetically by company name.
'''

__last_change__ = '2017.08.30.'


import configparser
import datetime
import logging
import marketdata_coupler as mdc
import sys
import teletrader

_datetimeformat = mdc.dateformat + ' ' + mdc.timeformat
config = configparser.ConfigParser()
config.read('config.ini')

class Registry(dict):
    '''Keeps all the basic info of all the stocks together.'''

    def __init__(self):
        '''Loads the basic data from a CSV file.'''
        logging.info('Registry: Loading basic data from CSV.')

        if len(self):
            logging.info('Registry: %d new ISIN loaded.')
        else:
            logging.warning('Registry: No ISIN loaded.')

def main():
    pass

if __name__ == '__main__':
    sys.exit(main())
