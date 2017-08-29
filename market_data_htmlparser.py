'''
Serves as interface to the web to obtain latest market data.
'''

__last_change__ = '2017.08.28.'

import csv_helper
from html.parser import HTMLParser
import logging
import sys
import teletrader
import urllib.request

def loaded_market_data(converter,
                       source_is_web = True):
    '''Loads the market data from an html (the web or a file).
    It is a tuple of dictionaries with ISINs, and it is independent from
    the TeleTrader format.
    '''

    return {converter[line[0]]:teletrader.list_to_dict(line)
            for line
            in _tuples_from_html(source_is_web)}

def _tuples_from_html(source_is_web = True):
    '''
    Obtains the market data from an html (the web or a file).
    It is a tuple of tuples, and contains no ISIN.
    '''

    if source_is_web:
        logging.debug('HTMLParser: Loading market data from web.')
        return _tuples_loaded_from_urls(_urls_loaded_from_csv())

    else:
        logging.debug(
            'HTMLParser: Loading market data from html file (TEST MODE).')
        return _tuples_loaded_from_file('exp.htm')

def _tuples_loaded_from_urls(urls):
    '''
    Returns a tuple of dictionaries containing the market data combined from 
    all the given urls.
    '''

    content = []
    for stock_exchange in sorted(urls):
        content.extend(_tuples_loaded_from_url(stock_exchange,
                                               urls[stock_exchange]))
    return(tuple(content))

def _tuples_loaded_from_url(stock_exchange_name, url):
    '''
    Returns a tuple of dictionaries containing the market data parsed from 
    one url.
    '''

    return _tuples_parsed_from_html(stock_exchange_name,
                                    str(urllib.request.urlopen(url).read(),
                                        encoding='utf-8'))

def _urls_loaded_from_csv():
    '''
    Returns a dict with the URLs of the stock exchanges, loaded from a CSV file.
    '''
    
    return {line['Stock Exchange']: line['URL']
            for line
            in csv_helper.reader(teletrader.urls_filename)}

def _tuples_loaded_from_file(filename):
    '''
    Returns a list of tuples read from a file.
    '''
    
    with open(filename,
             'r',
             1,
             'UTF-8') as f:
        return (_tuples_parsed_from_html('Not specified',
                                         f.read()))

def _tuples_parsed_from_html(stock_exchange_name,
                             html_string):
    '''
    Return a list of tuples, parsed from the given string.
    '''
    
    t = teletrader.TeletraderHTMLParser(stock_exchange_name)
    t.feed(html_string)

    if t.stocks:
        logging.info('HTMLParser: Stock Exchange: %s, '
                     'Number of papers extracted: %d',
                     stock_exchange_name,
                     len(t.stocks))
    else:
        logging.warning('HTMLParser: Stock Exchange: %s, '
                        'No papers extracted',
                        stock_exchange_name)

    return t.stocks
        
def main():
    pass

if __name__ == '__main__':
    sys.exit(main())
