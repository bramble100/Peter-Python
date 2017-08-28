'''
Contains all the objects, functions and data for parsing data obtained from
TeleTrader pages.
'''

__last_change__ = '2017.08.28.'

import csv_helper
import datetime
from html.parser import HTMLParser
import logging
import sys

urls_filename = 'teletrader-links.csv'
tt2isin_filename = 'ISIN.csv'
# source string example: 07.14./17:35
_datetime_format = '%m.%d./%H:%M'

# pattern to process
pattern = ( ('start', 'tr'),
            ('start', 'td'), # col 1 (name)
            #('start', 'span'),
            ('data', 'read'), # *** NAME ***
            #('end', 'span'),
            ('end', 'td'),
            ('start', 'td'), # col 2 (closing price)
            ('data', 'read'), # *** CLOSING PRICE ***
            ('end', 'td'),
            ('start', 'td'), # col 3 (trend)
            ('end', 'td'),
            ('start', 'td'), # col 4 (diff)
            #('start', 'span'),
            #('end', 'span'),
            ('end', 'td'),
            ('start', 'td'), # col 5 (diff%)
            #('start', 'span'),
            #('end', 'span'),
            ('end', 'td'),
            ('start', 'td'), # col 6 (date/time)
            ('data', 'read'), # *** DATE/TIME ***
            ('end', 'td'),
            ('start', 'td'), # col 7 (volume)
            ('data', 'read'), # *** VOLUME ***
            ('end', 'td'),
            ('start', 'td'), # col 8 (latest closing)
            ('end', 'td'),
            ('end', 'tr')
            )

class TeletraderHTMLParser(HTMLParser):
    '''
    Parses a Teletrader html page and extracts the closing prices and the
    volume.

    Wraps the HTMLParser class, tailored for Teletrader web pages.
    '''

    def __init__(self, stock_exchange):
        HTMLParser.__init__(self)
        self.pattern_counter = 0
        self.actual_stock = []
        self.stocks = []
        self.stock_exchange = stock_exchange

    def handle_starttag(self, tag, attrs):
        '''Starts to listen when reaching a start tag.'''

        if pattern[self.pattern_counter] == ('start', tag):
            self.pattern_counter += 1

    def handle_endtag(self, tag):
        '''Stops to listen when reaching an end tag.'''

        if pattern[self.pattern_counter] == ('end', tag):
            if tag == 'tr':
                self.pattern_counter = 0
                self.actual_stock.append(str(self.stock_exchange))
                self.stocks.append(self.actual_stock)
                self.actual_stock = []
            else : self.pattern_counter += 1
        elif tag == 'tr' or tag == 'td':
            self.pattern_counter = 0
            self.actual_stock = []

    def handle_data(self, data):
        '''If appropriate reads the data.'''

        if pattern[self.pattern_counter] == ('data', 'read'):
            self.pattern_counter += 1
            self.actual_stock.append(data)

class TTConverter(dict):
    '''The dictionary to determine the ISIN by the Teletrader names.'''

    def __init__(self):
        super().__init__()
        if ' ttnames2isin' in self.__dict__:
            logging.info('TeleTrader: ISINs converter already created.')
            return self

        logging.info('TeleTrader: Loading ISINs from file.')
        self.ttnames2isin = {line['TeleTrader Name']: line['ISIN']
                             for line
                             in csv_helper.reader(tt2isin_filename)}
        logging.info(str.format('TeleTrader: {} '
                                 'new TeleTrader Name(s) loaded.',
                                 len(self.ttnames2isin)))
        missing_names = set()
        
    def __getitem__(self, key):
        '''Returns the ISIN by TeleTrader name. In case no ISIN can be returned,
        returns the TeleTrader name itself, and makes an entry in the missing
        names.'''
        
        try:
            return self.__dict__[key]
        except KeyError:
            self.missing_names.add(key)
            return key
            


def list_to_dict(raw_list):
    '''
    Returns a tuple based on a list (obtained from html).

    Contains no ISIN as the ISIN is the key by which the returned
    tuple will be stored in a dictionary.
    '''

    this_datetime = datetime.datetime.strptime(str(raw_list[2]),
                                               _datetime_format)    
    this_datetime = datetime.datetime(datetime.date.today().year,
                                      this_datetime.month,
                                      this_datetime.day,
                                      this_datetime.hour,
                                      this_datetime.minute,
                                      this_datetime.second)
    return {'TeleTrader Name':raw_list[0],
            'Stock Exchange':raw_list[4],
            'Market Data':{this_datetime: {'Closing Price':raw_list[1],
                                           'Volume':raw_list[3]}}}

def main():
    pass

if __name__ == '__main__':
    sys.exit(main())
