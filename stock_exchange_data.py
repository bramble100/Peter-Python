'''
Library to fetch the stock exchange closing prices and volume
from tdcfinancial on a given day, sorted alphabetically by company name.
'''

__last_change__ = '2017.08.28.'


import datetime
import logging
import market_data_coupler as mdc
import market_data_htmlparser as mdhp
import sys
import teletrader

_datetimeformat = mdc.dateformat + ' ' + mdc.timeformat

class MarketData(object):
    '''Holds all the data regarding the companies and the market data.'''

    marketdata = {}

    def __init__(self):
        self.marketdata = {}
        self.converter = teletrader.TTConverter()

    def load_from_file(self):
        '''Loads the market data from a CSV file.'''

        logging.info('MarketData: Loading market data from CSV.')
        self.marketdata = mdc.loaded_past_market_data(self.converter.ttnames2isin)

        logging.info('MarketData: %d new entry(s) loaded.',
                     len(self.marketdata))

    def load_from_html(self, source_is_web = True):
        '''Loads the market data from HTML (either web or a file).'''

        logging.info('MarketData: Loading market data from HTML.')

        self.marketdata = mdhp.loaded_market_data(self.converter.ttnames2isin,
                                                  source_is_web)

        logging.info('MarketData: %d new entry(s) loaded.',
                     len(self.marketdata))

    def clean(self):
        '''Cleans the internal market data, which means deleting entries older
        than 365 days.'''

        logging.info('MarketData: Cleaning market data from entries older '
                      'than 365 days.')

        deleted_counter = 0
        today = datetime.datetime.today()
        one_year = datetime.timedelta(days = 365)

        for isin in tuple(self.marketdata.keys()):
            for mydatetime in tuple(self.marketdata[isin]['Market Data'].keys()):
                if mydatetime < today - one_year:
                    del self.marketdata[isin]['Market Data'][mydatetime]
##                    logging.info('MarketData: Datetime (%s) from ISIN (%s) deleted.',
##                                 str(mydatetime),
##                                 isin)
                    if not self.marketdata[isin]['Market Data']:
                        del self.marketdata[isin]
##                        logging.info('MarketData: ISIN (%s) deleted.', isin)
                    deleted_counter += 1
                    
        if deleted_counter:
            logging.info('MarketData: %d old entry(s) deleted.',
                         deleted_counter)
        else:
            logging.info('MarketData: No old entry deleted.')

    def append(self, other_market_data):
        '''Appends the market data to the existing entries.'''

        logging.info('MarketData: Appending market data to this database.')
        logging.debug('MarketData: %d new ISIN might be added.', len(other_market_data))

        added_counter = 0

        for isin in other_market_data.keys():
            if isin not in self.marketdata:
                self.marketdata[isin] = {}
                self.marketdata[isin].update(other_market_data[isin])
                added_counter += len(other_market_data[isin]['Market Data'])
                logging.debug('MarketData: New ISIN (%s) appended.', isin)
                continue
            logging.debug('MarketData: ISIN (%s) is found in existing market data.', isin)
            
            for addable_datetime in other_market_data[isin]['Market Data'].keys():

                addable_date = _datetime_to_date(addable_datetime)
                logging.debug('MarketData: Date (%s) might be added.',
                              str(addable_date))

                if 'Market Data' not in self.marketdata[isin]:
                    self.marketdata[isin]['Market Data'] = {}
                    self.marketdata[isin]['Market Data'].update(
                        other_market_data[isin]['Market Data'])
                    added_counter += len(other_market_data[isin]['Market Data'])
                    logging.debug('MarketData: New market data with datetime (%s) appended.',
                                  str(addable_datetime))
                    continue
                
                for existing_datetime in sorted(
                    self.marketdata[isin]['Market Data'].keys(),
                    reverse=True):

                    # is there the same day? and if is, the new data is later?
                    logging.debug('Existing datetime: %s, addable datetime: %s',
                                  str(existing_datetime),
                                  str(addable_datetime))
                    
                    if addable_datetime > existing_datetime:
                        if addable_date == _datetime_to_date(existing_datetime):
                            del self.marketdata[isin]['Market Data'][existing_datetime]
                            logging.debug('Existing datetime (%s) deleted.',
                                          str(existing_datetime))
                        else:
                            logging.debug('Addable date (%s) not found.',
                                          str(addable_date))
                            
                        self.marketdata[isin]['Market Data'][addable_datetime] = {}
                        self.marketdata[isin]['Market Data'][
                            addable_datetime] = other_market_data[isin]['Market Data'][
                                addable_datetime]
                        logging.debug('MarketData: Datetime (%s) added.',
                                      str(addable_datetime))
                        added_counter += 1
                        break

        if added_counter:
            logging.info('MarketData: %d new entry(s) added.',
                         added_counter)
        else:
            logging.info('MarketData: No new entry added.')


    def save_to_file(self):
        '''Saves the market data into a CSV file.'''

        logging.info('MarketData: Saving market data to CSV.')

        content = list()

        # create a header
        content.append(('Name',
                        'ISIN',
                        'Date',
                        'Time',
                        'Closing Price',
                        'Volume',
                        'TeleTrader Name',
                        'Stock Exchange'))
        content.extend(_dict_to_tuple(self.marketdata))
        mdc.save_to_file(content)

def _list_contains_date(mylist, mydate):
    '''Returns True if given list contains the given date.'''

    for item in mylist:
        if _datetime_to_date(item) == _datetime_to_date(mydate):
            return True

    return False

def _datetime_to_date(dt):
    '''Returns a date obtained from the given datetime.'''

    return(datetime.date(dt.year,
                         dt.month,
                         dt.day))

def _datetime_to_time(dt):
    '''Returns a time obtained from the given datetime.'''

    return(datetime.time(dt.hour,
                         dt.minute,
                         dt.second))

def _dict_to_tuple(marketdata):
    '''Returns a tuple converted from the given dict.'''

    # TODO: needs double loop comprehension

    content = []
    for isin in sorted(marketdata):        
        for this_datetime in sorted(marketdata[isin]['Market Data']):
            content.append(['',
                            isin,
                            this_datetime.strftime(mdc.dateformat),
                            this_datetime.strftime(mdc.timeformat),
                            marketdata[isin]['Market Data'][this_datetime]['Closing Price'],
                            marketdata[isin]['Market Data'][this_datetime]['Volume'],
                            marketdata[isin]['TeleTrader Name'],
                            marketdata[isin]['Stock Exchange']])
    return(tuple(content))

def main():
    pass

if __name__ == '__main__':
    sys.exit(main())
