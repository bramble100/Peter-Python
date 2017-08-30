'''
Library to fetch the stock exchange closing prices and volume
from tdcfinancial on a given day, sorted alphabetically by company name.
'''

__last_change__ = '2017.08.30.'


import configparser
import csv_helper
import datetime
import logging
import marketdata_coupler as mdc
import sys
import teletrader

config = configparser.ConfigParser()
config.read('config.ini')

class Registry(dict):
    '''Keeps all the basic info of all the stocks together.'''

    def __init__(self):
        '''Loads the basic data from a CSV file.'''
        logging.info('Registry: Loading basic data from CSV.')

        self['Errors'] = {'Errors found': False,
                          'Number of missing ISINs': 0,
                          'Faulty ISINs': set(),
                          'Missing names': set(),
                          'Faulty months in report': set(),
                          'Faulty report expiry dates': set()}

        self.update( {row['ISIN'] : self._registry_row(row)
                      for row
                      in csv_helper.reader(config['Registry']['Registry filename'])
                      if self._registry_row_is_addable(row)})
        
        if len(self):
            if not self['Errors']['Errors found']:
                logging.info('Registry: %d new ISIN loaded. No errors found.', len(self))
            else:            
                logging.error('Registry: The following errors found:')
        else:
            logging.error('Registry: No ISIN loaded.')

    def _registry_row_is_addable(self, row):
        '''Checks one stock data in a dict.'''       

        if not row['ISIN']:
            self['Errors']['Errors found'] = True
            self['Errors']['Number of missing ISINs'] += 1
            return False
        elif len(row['ISIN']) != 12:
            self['Errors']['Errors found'] = True
            self['Errors']['Faulty ISINs'].add(row['ISIN'])
            return False

        if not row['Name']:
            self['Errors']['Errors found'] = True
            self['Errors']['Missing names'].add(row['ISIN'])
            return True

        # months = int(row['Months in Report']) if row['Months in Report'] != '' else 0
        
        if row['Months in Report'] not in (3, 6, 9, 12):
            self['Errors']['Errors found'] = True
            self['Errors']['Faulty months in report'].add(row['ISIN'])
            return True
        
    def _registry_row(self, row):
        '''Processes one stock data from a dict.'''
        
        return {'Name' : row['Name'],
                'EPS': row['EPS'],
                'Months in Report': row['Months in Report'],
                'Report Expiry Date': row['Report Expiry Date'],
                'Own Investor Link': row['Own Investor Link'],
                'Stock Exchange Link': row['Stock Exchange Link']}
    
def main():
    pass

if __name__ == '__main__':
    sys.exit(main())
