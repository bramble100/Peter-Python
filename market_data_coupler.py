'''
Serves as interface to the market data stored persistently.

Can obtain data from CSV files for the time being.
Planned: obtain from JSON, from the web, etc.
'''
__last_change__ = '2017.08.28.'

import csv_helper
import datetime
import logging
import sys
import teletrader

_market_data_filename = 'market_data.csv'
##_test_output_market_data_filename = 'market_data_test_output.csv'
dateformat = '%Y.%m.%d'
timeformat = '%H:%M:%S'


def loaded_past_market_data(converter):
    '''
    Returns the stored market data from file.
    It may be with almost arbitrary headers.
    Not to be mistaken with the actual market data retreived from web or
    also a file (which is only test mode).
    '''

    logging.info('MarketDataCoupler: Loading market data from file.')

    loaded_market_data = {}
    missing_ttnames = set()

    for line in csv_helper.reader(_market_data_filename):

        id = line['ISIN']
        if not id and line['TeleTrader Name'] in converter:
            id = converter[line['TeleTrader Name']]

        if id:
            if id not in loaded_market_data:
                loaded_market_data[id] = {'Stock Exchange': line['Stock Exchange'],
                                          'TeleTrader Name': line['TeleTrader Name']}

            date = datetime.datetime.strptime(line['Date'],
                                              dateformat)
            time = datetime.datetime.strptime(line['Time'],
                                              timeformat)
            mydatetime = datetime.datetime(date.year,
                                           date.month,
                                           date.day,
                                           time.hour,
                                           time.minute,
                                           time.second)
            if 'Market Data' not in loaded_market_data[id]:
                loaded_market_data[id]['Market Data'] ={}
            loaded_market_data[id]['Market Data'][mydatetime] = {'Closing Price' : line['Closing Price'],
                                                                 'Volume' : line['Volume']}
        else:
            missing_ttnames.add(line['TeleTrader Name'])

    logging.info('MarketDataCoupler: %d new ID(s) loaded with market data.',
                 len(loaded_market_data))

    return loaded_market_data

def save_to_file(mylist):
    '''Saves a list of lists to CSV. The first list is the header.'''
    
    csv_helper.writer(mylist,
                      _market_data_filename,
                      True)
    
def main():
    pass

if __name__ == '__main__':
    sys.exit(main())
