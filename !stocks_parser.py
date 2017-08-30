'''Fetches the stock exchange closing values from tdcfinancial on a given day,
sorted alphabetically by company name.
'''

__last_change__ = '2017.08.29.'

import configparser
import os
import logging
import marketdata
import sys

def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    logging.basicConfig(level=logging.INFO)
##    logging.basicConfig(level=logging.DEBUG)
    
    past_market_data = marketdata.MarketData()
    past_market_data.load_from_file()
    
    past_market_data.clean()

    actual_market_data = marketdata.MarketData()
    actual_market_data.load_from_html(config['DEFAULT']['Source is web'] == str(True))
    
    past_market_data.append(actual_market_data.marketdata)
    past_market_data.clean()
    
    past_market_data.save_to_file()

    # wait for key stroke
    os.system('pause')

if __name__ == '__main__':
    sys.exit(main())
