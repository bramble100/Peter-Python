'''Assembles a short-list of buyable stocks based on the market data and saves
it into a csv file.
'''

__last_change__ = '2017.08.30.'

import configparser
import os
import logging
import marketdata
import registry
import screener
import sys

def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

##    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    
    reg = registry.Registry()

    market_data = marketdata.MarketData()
    market_data.load_from_file()
    
### ??? ###


##    slist = screener.ShortList()
##    scr = screener.Screener()
##    slist.assemble(scr)
##
##    slist.save_to_file()

    # wait for key stroke
    os.system('pause')

if __name__ == '__main__':
    sys.exit(main())
