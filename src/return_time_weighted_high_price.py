#!/usr/bin/env python
"""This module reads in .txt file data and maintains an orderbook of current oustanding
orders. It contains a function 'get_time_weighted_high_price' that acts as command line 
application. 

Compatible for python 2.7.X (not yet tested on python 3.X)

Example: $  python return_time_weighted_high_price.py example_data.txt
"""

from __future__ import division
import argparse
import os
import math

class OrderBook():
    ''' Maintains an order book of current orders
    
    Essentially a dictionary with some functions associated with it. Dictionary has keys
    defined by the order id and values defined by price. The only entries in an OrderBook
    instance are inserts (flag = I)
    
    Attributes:
        ledger (dict): dictionary that holds current insert entries
        high_price (float): current high price
        latest_time (int): current latest timestamp value
        delta_t (int): difference between ith and (i+1)th timestamps
        elapsed_time (int): cumulative total elapsed time (does not count time when no current orders are present)
        time_scaled_high_price (float): cumulative sum of high_price*delta_t 
        recalculate_max_high_flag (bool): A flag indicating whether the maximum high price needs to be recalculated 
    '''
    def __init__(self):
        self.ledger = {}
        self.high_price = None
        self.latest_time = 0
        self.delta_t = 0
        self.elapsed_time = 0
        self.time_scaled_high_price = 0
        self.recalculate_max_high_flag = True
     
    def __str__(self):
         return str(self.ledger)
        
    def insert(self,id_num,price):
        ''' insert new entry into dictionary.
        Also checks if get_high_price needs to be recalculated (if the new_price > then the current highest price)
        '''
        self.recalculate_max_high_flag = True if (price > self.high_price) or (math.isnan(self.high_price)) else False
        self.ledger[id_num] = price
    
    def erase(self,id_num):
        ''' erases old entry from dictionary. 
        Also checks if get_high_price needs to be recalculated (if the old_price == to current highest price)
        '''
        self.recalculate_max_high_flag = True if self.ledger[id_num] == self.high_price else False
        del self.ledger[id_num]

    def get_high_price(self):
        ''' Find the highest prices amongst the current orders'''
        if self.recalculate_max_high_flag:
            try:
                self.high_price = max(self.ledger.values())
            except ValueError: # catches case when orderbook is empty, sets high value to NaN (as requested)
                self.high_price = float('NaN')
        else:
            pass
    
    def update_elapsed_time(self):
        self.elapsed_time += self.delta_t

    def update_time_scaled_high_price(self):
        self.time_scaled_high_price +=  self.high_price*self.delta_t

def get_time_weighted_high_price(filepath):
    ''' Main function that gets the time-weighted high price. Creates an OrderBook 
    instance and then reads the .txt file line-by-line updating the order book. After each 
    line is read the elapsed time and highest price of the outstanding orders is found 
    and the numerator and denominator of the time-weighted high price fraction updated.
    
    Args: 
        filepath: filepath to data .txt file 
        
    Returns: printed time-weighted high price
    '''
    orderbook = OrderBook()
    with open(filepath) as f:
        for line in f:
            new_line = line.split()
            orderbook.delta_t = float(new_line[0]) - orderbook.latest_time
            orderbook.latest_time = float(new_line[0])
            orderbook.get_high_price()
            if math.isnan(orderbook.high_price):
               pass
            else:
                orderbook.update_elapsed_time()
                orderbook.update_time_scaled_high_price()
            if new_line[1] == 'I':
                orderbook.insert(int(new_line[2]),float(new_line[3]))
            else:
                orderbook.erase(int(new_line[2]))
    print orderbook.time_scaled_high_price/orderbook.elapsed_time

if __name__ == "__main__":
    def is_valid_file(parser, arg):
        ''' Simple function that checks file given exists and is nonzero'''
        if not os.path.isfile(arg):
            parser.error("The file %s does not exist!" % arg)
        elif not os.path.getsize(arg) > 0:
            parser.error("The file %s is empty!" % arg)
        else:
            return arg

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=
    '''
    Calculates and outputs the time-weighted average highest price. The function takes in
     data in the form of a standard ASCII .txt file with columns ordered:
                 [timestamp, IE-flag, id_num, price]
    
    Time periods in which there are no orders in the orderbook do not contribute to the output value.
    
    Usage: Total running time for 1 million insert/erase order pairs ~ 12.0 seconds
    ''')
    parser.add_argument("filename", help="filename of ASCII .txt files, currently code does not support relative paths", metavar="FILE",type=lambda x: is_valid_file(parser, x))

    args = parser.parse_args()
    get_time_weighted_high_price(args.filename)